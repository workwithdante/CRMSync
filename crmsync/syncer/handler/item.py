from dataclasses import dataclass, field
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler
from api import client

@dataclass
class Item(DocTypeHandler):
    item_name: str                  # Código base del plan (Item padre)
    item_name_child: str               # Código que define la versión (últimos dígitos)
    plan_name: Optional[str] = None
    company: Optional[str] = None
    
    @classmethod
    def from_row(cls, row, cfg):
        return cls(
            item_name=row.get(cfg["item_code"]),
            item_name_child=row.get(cfg["item_name_child"]),
        )

    def __post_init__(self):
        self.doctype = "Item"
        self.normalize_and_sync()

    def get_filters(self):
        #return [["Item", "item_code", "=", self.variant_code()]]
        return None
    
    def get_existing_name(self):
        # Aquí puedes definir cómo se extrae el nombre del resultado
        return self.variant_code()

    def build_data(self):
        # Paso 1: asegúrate de que el padre exista
        parent_code = self.item_name
        parent_fields = ["name", "item_code", "item_group", "stock_uom", "has_variants"]
        parent_result = client.doQuery("Item", name=parent_code, fields=parent_fields)

        if parent_result:
            parent_item = parent_result
        else:
            parent_item = client.doCreate("Item", {
                "item_code": parent_code,
                "item_group": "Services",
                "is_stock_item": 0,
                "has_variants": 1,
                "disabled": 0,
                "attributes": [{"attribute": "Version"}]
            }).get("data")

        # Paso 2: construir data de la variante
        version_code = self.item_name_child[-2:]
        return {
            "item_code": self.variant_code(),
            "item_group": parent_item.get("item_group", "Services"),
            "is_stock_item": 0,
            "stock_uom": parent_item.get("stock_uom", "Unit"),
            "variant_of": self.item_name,
            "attributes": [
                {"attribute": "Version", "attribute_value": version_code}
            ]
        }

    def variant_code(self):
        return f"{self.item_name}-{self.item_name_child[-2:]}"
