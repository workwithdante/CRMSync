from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from crmsync.syncer.utils.comparator import DictComparator


@dataclass(kw_only=True)
class DocTypeHandler(ABC):
    name: Optional[str] = None
    doctype: Optional[str] = None
    
    @classmethod
    @abstractmethod
    def from_row(cls, row, mapping: dict):
        pass

    @abstractmethod
    def get_filters(self) -> list:
        """Filtros para buscar si el documento ya existe."""
        pass

    @abstractmethod
    def get_existing_name(self) -> str:
        """Nombre estimado del documento (para uso en la búsqueda)."""
        pass

    @abstractmethod
    def build_data(self) -> dict:
        """Estructura de datos nueva a crear o comparar."""
        pass

    def extract_name(self, result: dict):
        return result.get("name")

    def normalize_and_sync(self):
        from api import client

        filters = self.get_filters()
        name = self.get_existing_name()
        new_data = self.build_data()

        special_fields = {"links", "email_ids", "phone_nos", "attributes"}  # ← ya se comparan aparte

        def expand_child_fields(key: str, child: list) -> list:
            """Convierte 'items': [{...}] en ['items.field1', 'items.field2', ...]"""
            if key in special_fields:
                return [key]  # no expandas si ya se compara por lógica especial
            if not isinstance(child, list) or not child or not isinstance(child[0], dict):
                return [key]
            return [f"{key}.{k}" for k in child[0].keys()]

        fields_list = ["name"]
        for key, value in new_data.items():
            if key == "name":
                continue
            if isinstance(value, list):
                fields_list += expand_child_fields(key, value)
            else:
                fields_list.append(key)
        
        existing = client.doQuery(
            self.doctype,
            name=name,
            filters=filters,
            fields=fields_list
        )

        if existing:
            existing = existing if isinstance(existing, dict) else existing.get("data")

            comparator = DictComparator()
            comparator.register("links", lambda n, e: comparator.compare_list_of_dicts(n, e, ["link_name", "link_doctype"]))
            comparator.register("email_ids", lambda n, e: comparator.compare_list_of_dicts(n, e, ["email_id", "is_primary"]))
            comparator.register("phone_nos", lambda n, e: comparator.compare_list_of_dicts(n, e, ["phone", "is_primary_phone", "is_primary_mobile_no"]))
            comparator.register("attributes", lambda n, e: comparator.compare_list_of_dicts(n, e, ["attribute", "attribute_value"]))
            comparator.register("items", lambda n, e: comparator.compare_items_with_names(n, e, match_by="item_code"))
            comparator.register("custom_dependents", lambda n, e: comparator.compare_list_of_dicts(n, e, ["contact", "first_name", "middle_name", "last_name", "gender", "day_of_birth", "relationship", "social_security_number", "job_type", "income", "migratory_status", "smoke", "been_in_jail", "coverage", "language"]))
            comparator.register("custom_company_info", lambda n, e: comparator.compare_list_of_dicts(n, e, ["contact", "member_id", "user", "password"]))
            comparator.register("custom_broker_info", lambda n, e: comparator.compare_list_of_dicts(n, e, ["broker_name", "national_producer_number", "initial_date", "end_date"]))

            changes = comparator.compare_dicts(new_data, existing)

            if changes:
                if list(changes.keys()) == ["items"]:
                    client.doUpdateItems(
                        parent_doctype=self.doctype,
                        parent_name=existing["name"],
                        items=changes["items"]
                    )
                    changes.pop("items")
                updated = client.doUpdate(self.doctype, existing["name"], changes)
                self.name = self.extract_name(updated.get("data"))
            else:
                self.name = self.extract_name(existing)

        else:
            created = client.doCreate(self.doctype, new_data)
            self.name = self.extract_name(created.get("data"))
