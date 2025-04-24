from dataclasses import dataclass, field
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class Customer(DocTypeHandler):
    first_name: str
    last_name: str
    second_name: str
    customer_name: str
    
    @classmethod
    def from_row(cls, row, mapping):
        return cls(
            first_name=row.get(mapping["first_name"]),
            last_name=row.get(mapping["last_name"]),
            second_name=row.get(mapping.get("second_name")),
            customer_name=row.get("customer_name"),
        )

    def __post_init__(self):
        self.doctype = "Customer"
        self.normalize_and_sync()

    def get_filters(self):
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        return self.full_name()

    def build_data(self):
        return {
            "customer_name": self.full_name()
        }

    def full_name(self):
        if self.first_name and self.last_name:
            return " ".join(filter(None, [self.first_name, self.second_name, self.last_name]))
        else:
            return self.customer_name
