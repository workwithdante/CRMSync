import json
import requests
from tqdm import tqdm

class ERPNextClient:
    """
    ERPNextClient allows interaction with ERPNext API using token authentication.
    It verifies credentials with frappe.auth.get_logged_user.
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
        self.session = requests.Session()

    def doLogin(self, api_key, api_secret):
        """
        Sets API key and secret, and initializes session headers.
        """
        if self.session.headers.get('Authorization'):
            return True

        self.api_key = api_key
        self.api_secret = api_secret
        self.session.headers.update({
            'Authorization': f'token {self.api_key}:{self.api_secret}',
            'Content-Type': 'application/json',
        })

        if "localhost" in self.endpoint_host:
            self.session.headers.update({
                'Host': f'{self.endpoint_host}'
            })
            self.host_api = f"http://127.0.0.1:{self.endpoint_port}"
        else:
            self.host_api = f"https://{self.endpoint_host}:{self.endpoint_port}"


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
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def doQuery(self, doctype, name=None, filters=None, fields=None, include_childs=None):
        """
        Fetches a document by name or list with filters.
        Args:
            doctype (str): The name of the DocType.
            name (str): The exact name of the document to fetch (primary key).
            filters (list): A list of filter conditions.
            fields (list): Optional list of fields to include in the result.
        """
        from urllib.parse import quote

        base_url = f"{self.host_api}/api/resource/{doctype}"
        params = {}
        params['fields'] = json.dumps(fields if fields else ["*"])
        
        def extract_single_data(response_json):
            data = response_json.get("data")
            if isinstance(data, list):
                return data[0] if data else None
            elif isinstance(data, dict):
                return data
            return None
        
        def search_by_filters(base_url, filters):
            # Búsqueda resumida para obtener solo el primer resultado
            filter_url = base_url
            params_filters = {
                "filters": json.dumps(filters),
                "fields": json.dumps(["name"]),
                "limit_page_length": 1
            }
            filter_response = self.session.get(filter_url, params=params_filters)
            filter_data = extract_single_data(filter_response.json())

            if not filter_data:
                print(f"🔍 No {doctype} found for filters.")
                return None

            return filter_data["name"]
        
        if not name:
            name = search_by_filters(base_url, filters)

        if name:
            url = f"{base_url}/{quote(name)}"
        else:
            url = base_url
            
            if filters:
                params['filters'] = json.dumps(filters)
            
        try:
            params["limit_page_length"] = 1
            
            if include_childs:
                params["include_child_docs"] = "true"
                
            response = self.session.get(url, params=params)

            # Intenta analizar la respuesta JSON ANTES de hacer raise_for_status
            if "application/json" in response.headers.get("Content-Type", ""):
                body = response.json()
                if body.get("exc_type") == "DoesNotExistError":
                    tqdm.write(f"🔍 {doctype} '{name}' not found (DoesNotExistError).")
                    return None
                if body.get("exc_type") == "ValidationError" and doctype == "Contact":
                    name = search_by_filters(
                        base_url,
                        filters,
                    )

                    if name:
                        return {
                            "data": [
                                {
                                    "name": name,
                                },
                            ],
                        }

            # Ahora sí, si no es DoesNotExistError, lanza error si corresponde
            response.raise_for_status()
            return extract_single_data(response.json())

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            try:
                print("🔎 Server response:", e.response.json())
            except Exception:
                pass
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Request Exception: {e}")
            return None

    
    def doCreate(self, doctype, data):
        """
        Creates a new document in ERPNext.

        Args:
            doctype (str): The name of the DocType (e.g., "SalesOrder").
            data (dict): A dictionary containing the fields and values of the document.

        Returns:
            dict or None: The created document data or None if the request failed.
        """
        url = f"{self.host_api}/api/resource/{doctype}"
        try:
            response = self.session.post(url, data=json.dumps(data))
            response.raise_for_status()
            tqdm.write(f"✅ Created {doctype}: {response.json()['data']['name']}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to create {doctype}: {e}")
            try:
                error_details = e.response.json()
                print("🔎 Server response:", json.dumps(error_details, indent=2))
            except Exception:
                print("🔎 No JSON response from server.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection or format error: {e}")
            return None

    def doUpdate(self, doctype, name, data):
        from urllib.parse import quote

        """
        Updates an existing document in ERPNext.
        """

        url = f"{self.host_api}/api/resource/{quote(doctype)}/{quote(name)}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            print(f"✅ Updated {doctype}: {response.json()['data']['name']}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to update {doctype} '{name}': {e}")
            try:
                error_details = e.response.json()
                print("🔎 Server response:", json.dumps(error_details, indent=2))
            except Exception:
                print("🔎 No JSON response from server.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection or format error: {e}")
            return None
            
    def doUpdateItems(self, parent_doctype: str, parent_name: str, items: list, child_docname="items"):
        """
        Usa el endpoint oficial para actualizar ítems en documentos enviados (como Sales Order).
        """
        url = f"{self.host_api}/api/method/erpnext.controllers.accounts_controller.update_child_qty_rate"
        payload = {
            "parent_doctype": parent_doctype,
            "parent_doctype_name": parent_name,
            "child_docname": child_docname,
            "trans_items": json.dumps(items)  # 👈 convertir lista a string JSON
        }

        try:
            response = self.session.post(url, data=json.dumps(payload))
            response.raise_for_status()
            print(f"✅ Updated items in {parent_doctype} '{parent_name}'")
            return response.json().get("message")
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to update items in {parent_doctype}: {e}")
            try:
                print("🔎 Server response:", e.response.json())
            except Exception:
                print("🔎 No JSON response from server.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection or format error: {e}")
            return None
