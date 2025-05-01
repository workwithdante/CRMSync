from dataclasses import dataclass, field
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class Address(DocTypeHandler):
    customer_name: str
    street: str
    pobox: str
    city: str
    state: str
    code: str
    complement: Optional[str] = None
    country: str = "United States"
    
    @classmethod
    def from_row(cls, row, mapping, customer_name):
        return cls(
            customer_name=customer_name,
            street=row.get(mapping["street"]),
            pobox=row.get(mapping["pobox"]),
            city=row.get(mapping["city"]),
            state=row.get(mapping["state"]),
            code=row.get(mapping["code"]),
            complement=row.get(mapping.get("complement")),
            country=row.get(mapping.get("country"), "United States")
        )

    def __post_init__(self):
        self.doctype = "Address"
        self.normalize_and_sync()

    def get_filters(self):
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        fulladdress = self._full_address()
        return f"{fulladdress}-Shipping"

    def build_data(self):
        fulladdress = self._full_address()
        data = {
            "address_title": fulladdress,
            "address_type": "Shipping",
            "address_line1": self.street,
            "city": self.city,
            "state": self.state,
            "pincode": self.code,
            "country": self.country,
            "links": [{
                "link_doctype": "Customer",
                "link_name": self.customer_name,
            }]
        }
        if self.complement:
            data["address_line2"] = self.complement
        return data

    def _full_address(self):
        return ", ".join(filter(None, [
            self.street,
            self.city,
            self.state,
            str(int(self.code)) if str(self.code).isdigit() else None
        ]))
