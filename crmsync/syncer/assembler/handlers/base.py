from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from tqdm import tqdm

from crmsync.syncer.utils.comparator import DictComparator


@dataclass(kw_only=True)
class DocTypeHandler(ABC):
    """
    Clase base para los handlers de DocType.

    Esta clase define la estructura base para los handlers de DocType,
    que se encargan de la lógica de mapeo, normalización y sincronización
    de los datos.
    """
    name: Optional[str] = None
    doctype: Optional[str] = None
    
    @classmethod
    @abstractmethod
    def from_row(cls, row, mapping: dict):
        """
        Crea una instancia de la clase desde una fila de datos.

        Args:
            row (dict): Fila de datos.
            mapping (dict): Mapeo de campos.
        """
        pass

    @abstractmethod
    def get_filters(self) -> list:
        """
        Obtiene los filtros para buscar si el documento ya existe.
        """
        pass

    @abstractmethod
    def get_filters_child(self) -> list:
        """
        Obtiene los filtros para buscar si el documento ya existe en los hijos.
        """
        pass

    @abstractmethod
    def get_existing_name(self) -> str:
        """
        Obtiene el nombre estimado del documento (para uso en la búsqueda).
        """
        pass

    @abstractmethod
    def build_data(self) -> dict:
        """
        Construye la estructura de datos nueva a crear o comparar.
        """
        pass

    def extract_name(self, result: dict):
        """
        Extrae el nombre del resultado.

        Args:
            result (dict): Resultado de la API.
        """
        return result.get("name")

    def normalize_and_sync(self):
        """
        Normaliza y sincroniza los datos.

        Este método se encarga de normalizar los datos y sincronizarlos
        con la API de ERPNext.
        """
        from api import client

        filters = self.get_filters()
        name = self.get_existing_name()
        new_data = self.build_data()
        filters_child = self.get_filters_child()

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

        if self.doctype == "Contact":
            fields_list.remove("email_ids") if "email_ids" in fields_list else None
            fields_list.remove("phone_nos") if "phone_nos" in fields_list else None
        
        existing = client.doQuery(
            self.doctype,
            name=name,
            filters=filters,
            fields=fields_list
        )

        if existing and filters_child:
            def match_child_filter_strict_exact(dependents, filters_child):
                if not filters_child or not dependents:
                    return False

                for filter_group in filters_child:
                    childtable = filter_group.get("childtable")
                    conditions = filter_group.get("conditions", {})

                    expected_contacts = conditions.get("contact", [])
                    expected_relationships = conditions.get("relationship", [])

                    if not expected_contacts or not expected_relationships:
                        return False

                    # Si hay más dependents que expected, cortamos los dependents solo a los que queremos comparar
                    subset_dependents = dependents[:len(expected_contacts)]

                    # Primero, validar tamaños
                    if len(subset_dependents) != len(expected_contacts):
                        return False

                    dep = subset_dependents[0]
                    exp_contact = expected_contacts[0]
                    exp_relationship = expected_relationships[0] 
                    
                    if dep.get("contact") != exp_contact or dep.get("relationship") != exp_relationship:
                        return False

                return True

            dependents = existing.get("custom_dependents", [])
            if not match_child_filter_strict_exact(dependents, filters_child):
                existing = None

        if existing:
            existing = existing if isinstance(existing, dict) else existing.get("data")

            comparator = DictComparator()
            comparator.register("links", lambda n, e: comparator.compare_list_of_dicts(n, e, ["link_name", "link_doctype"], True if self.doctype == "Address" else False))
            comparator.register("email_ids", lambda n, e: comparator.compare_list_of_dicts(n, e, ["email_id", "is_primary"]))
            comparator.register("phone_nos", lambda n, e: comparator.compare_list_of_dicts(n, e, ["phone", "is_primary_phone", "is_primary_mobile_no"]))
            comparator.register("attributes", lambda n, e: comparator.compare_list_of_dicts(n, e, ["attribute", "attribute_value"]))
            comparator.register("items", lambda n, e: comparator.compare_items_with_names(n, e, match_by="item_code"))
            comparator.register("custom_dependents", lambda n, e: comparator.compare_list_of_dicts(n, e, ["contact", "first_name", "middle_name", "last_name", "gender", "day_of_birth", "relationship", "social_security_number", "job_type", "income", "migratory_status", "smoke", "been_in_jail", "coverage", "language"]))
            comparator.register("custom_company_info", lambda n, e: comparator.compare_list_of_dicts(n, e, ["contact", "member_id", "user", "password"]))
            comparator.register("custom_broker_info", lambda n, e: comparator.compare_list_of_dicts(n, e, ["broker_name", "national_producer_number", "initial_date", "end_date"]))
            comparator.register("custom_documents", lambda n, e: comparator.compare_list_of_dicts(n, e, ["contact", "ssn", "income", "migratory", "coverage", "citizenship", "dateline"]))

            changes = comparator.compare_dicts(new_data, existing)

            if changes != {}:
                if list(changes.keys()) == ["items"] and existing["status"] != 'Draft':
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
            tqdm.write(f"Creating {self.doctype}: {self.name}")
