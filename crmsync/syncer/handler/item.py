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
    version_code: Optional[str] = field(init=False)
        
    @classmethod
    def from_row(cls, row, cfg):
        return cls(
            item_name=row.get(cfg["item_code"]),
            item_name_child=row.get(cfg["item_name_child"]),
            company=row.get("company"),
        )

    def __post_init__(self):
        self.doctype = "Item"
        self.normalize_fields()
        self.normalize_and_sync()
    
    def normalize_fields(self):
        self.version_code = self.item_name_child[-2:]
        if self.version_code not in ('01', '02', '03', '04', '05', '06'):
            self.version_code = '01'

    def get_filters(self):
        #return [["Item", "item_code", "=", self.variant_code()]]
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        # Aquí puedes definir cómo se extrae el nombre del resultado
        return self.variant_code()

    def build_data(self):
        # Paso 1: asegúrate de que el padre exista
        parent_code = self.item_name
        parent_fields = ["name", "item_code", "item_group", "stock_uom", "has_variants"]
        parent_result = client.doQuery("Item", name=parent_code, fields=parent_fields)
        
        if len(parent_code) != 14 and not self.company != 'Florida Blue':
            raise ValueError(f"El código del padre '{parent_code}' no tiene la longitud correcta en {self.company}.")

        if parent_result:
            parent_item = parent_result
        else:
            data_item = {
                "item_code": parent_code,
                "item_group": "Services",
                "is_stock_item": 0,
                "has_variants": 1,
                "disabled": 0,
            }
            if self.company != 'Florida Blue':
                data_item["attributes"] = [{"attribute": "Version"}]
            parent_item = client.doCreate("Item", data_item).get("data")
                    
        return {
            "item_code": self.variant_code(),
            "item_group": parent_item.get("item_group", "Services"),
            "is_stock_item": 0,
            "stock_uom": parent_item.get("stock_uom", "Unit"),
            "variant_of": self.item_name,
            "attributes": [
                {"attribute": "Version", "attribute_value": self.version_code}
            ]
        }

    def variant_code(self) -> str:
        return f"{self.item_name}-{self.version_code}"
