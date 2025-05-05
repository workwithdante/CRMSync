import httpx
import json
from urllib.parse import quote
from tqdm import tqdm

class ERPNextClient:
    """
    ERPNextClient allows interaction with ERPNext API using token authentication.
    Now uses httpx with HTTP/2 and connection pooling for high concurrency.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, endpoint_host, endpoint_port):
        if hasattr(self, 'host_api'):
            return
        self.endpoint_host = endpoint_host
        self.endpoint_port = endpoint_port
        self.api_key = None
        self.api_secret = None
        self.session = None  # will be an httpx.Client after login

    def doLogin(self, api_key, api_secret):
        """
        Sets API key and secret, and initializes httpx session with HTTP/2.
        """
        # If already authenticated, skip
        if self.session and self.session.headers.get('Authorization'):
            return True

        self.api_key = api_key
        self.api_secret = api_secret
        # Determine host_api URL
        if "localhost" in self.endpoint_host:
            self.host_api = f"http://127.0.0.1:{self.endpoint_port}"
        else:
            self.host_api = f"https://{self.endpoint_host}:{self.endpoint_port}"

        # Create httpx client with HTTP/2 and pooling
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        headers = {
            'Authorization': f'token {self.api_key}:{self.api_secret}',
            'Content-Type': 'application/json',
        }
        self.session = httpx.Client(
            headers=headers,
            http2=True,
            timeout=None,
            limits=limits
        )

        return self._check_credentials()

    def _check_credentials(self):
        """
        Verifies the credentials with frappe.auth.get_logged_user.
        """
        url = f'{self.host_api}/api/method/frappe.auth.get_logged_user'
        try:
            response = self.session.get(url)
            response.raise_for_status()
            print(f"✅ Authenticated as: {response.json().get('message')}")
            return True
        except httpx.HTTPError as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def search_by_filters(self, doctype, base_url, filters):
        # Búsqueda resumida para obtener solo el primer resultado
        params_filters = {
            "filters": json.dumps(filters),
            "fields": json.dumps(["name"]),
            "limit_page_length": 1
        }
        response = self.session.get(base_url, params=params_filters)
        data = self.extract_single_data(response.json())
        if not data:
            print(f"🔍 No {doctype} found for filters.")
            return None
        return data.get("name")

    def extract_single_data(self, response_json):
        data = response_json.get("data")
        if isinstance(data, list):
            return data[0] if data else None
        if isinstance(data, dict):
            return data
        return None

    def doQuery(self, doctype, name=None, filters=None, fields=None, include_childs=None):
        """
        Fetches a document by name or list with filters.
        Signature unchanged.
        """
        base_url = f"{self.host_api}/api/resource/{doctype}"
        params = {'fields': json.dumps(fields if fields else ["*"])}

        if not name:
            name = self.search_by_filters(doctype, base_url, filters)

        if name:
            url = f"{base_url}/{quote(name)}"
        else:
            url = base_url
            if filters:
                params['filters'] = json.dumps(filters)

        try:
            params['limit_page_length'] = 1
            if include_childs:
                params['include_child_docs'] = 'true'

            response = self.session.get(url, params=params)
            # Parse JSON before status check to catch DoesNotExistError
            if 'application/json' in response.headers.get('Content-Type', ''):
                body = response.json()
                if body.get('exc_type') == 'DoesNotExistError':
                    tqdm.write(f"🔍 {doctype} '{name}' not found (DoesNotExistError).")
                    return None

            response.raise_for_status()
            return self.extract_single_data(response.json())

        except httpx.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("🔎 Server response:", e.response.json())
                except Exception:
                    pass
            return None

    def doCreate(self, doctype, data):
        """
        Creates a new document in ERPNext.
        Signature unchanged.
        """
        url = f"{self.host_api}/api/resource/{doctype}"
        try:
            response = self.session.post(url, json=data)
            body = response.json()
            if body.get('exc_type') == 'ValidationError' and doctype == 'Contact':
                fb_url = f"{self.host_api}/api/method/mabecenter.controllers.contact.get_contact_hide"
                response = self.session.post(fb_url, json={"data": json.dumps(data)})
                name = response.json().get('message')
                if name:
                    return { 'data': { 'name': name } }

            response.raise_for_status()
            tqdm.write(f"✅ Created {doctype}: {response.json()['data']['name']}")
            return response.json()

        except httpx.HTTPError as e:
            print(f"❌ Failed to create {doctype}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("🔎 Server response:", json.dumps(e.response.json(), indent=2))
                except Exception:
                    pass
            return None

    def doUpdate(self, doctype, name, data):
        """
        Updates an existing document in ERPNext.
        Signature unchanged.
        """
        url = f"{self.host_api}/api/resource/{quote(doctype)}/{quote(name)}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            print(f"✅ Updated {doctype}: {response.json()['data']['name']}")
            return response.json()
        except httpx.HTTPError as e:
            print(f"❌ Failed to update {doctype} '{name}': {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("🔎 Server response:", json.dumps(e.response.json(), indent=2))
                except Exception:
                    pass
            return None

    def doUpdateLinks(self, doctype: str, doctype_name: str, links: list):
        """
        Adds missing links to a document.
        Signature unchanged.
        """
        url = f"{self.host_api}/api/resource/{quote(doctype)}/{quote(doctype_name)}"
        try:
            response = self.session.get(url)
            existing = response.json().get('data', {})
            existing_links = existing.get('links', []) or []
            for link in links:
                if not any(l['link_doctype']==link['link_doctype'] and l['link_name']==link['link_name'] for l in existing_links):
                    existing_links.append(link)
            response = self.session.put(url, json={'links': existing_links})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"❌ Failed to update items in {doctype}: {doctype_name}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("🔎 Server response:", e.response.json())
                except Exception:
                    pass
            return None

    def doUpdateItems(self, parent_doctype: str, parent_name: str, items: list, child_docname="items"):
        """
        Uses official endpoint to update child items in a document.
        Signature unchanged.
        """
        url = f"{self.host_api}/api/method/erpnext.controllers.accounts_controller.update_child_qty_rate"
        payload = {
            'parent_doctype': parent_doctype,
            'parent_doctype_name': parent_name,
            'child_docname': child_docname,
            'trans_items': json.dumps(items)
        }
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            print(f"✅ Updated items in {parent_doctype} '{parent_name}'")
            return response.json().get('message')
        except httpx.HTTPError as e:
            print(f"❌ Failed to update items in {parent_doctype}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print("🔎 Server response:", e.response.json())
                except Exception:
                    pass
            return None