from dataclasses import dataclass, field
import re
from typing import Optional

from syncer.assembler.handlers.base import DocTypeHandler

@dataclass
class Address(DocTypeHandler):
    """
    Handler para la dirección.

    Esta clase se encarga de manejar la lógica para la dirección.
    """
    customer_name: str
    bank_account_name: str
    street: str
    pobox: str
    city: str
    state: str
    code: str
    complement: Optional[str] = None
    country: str = "United States"
    
    @classmethod
    def from_row(cls, row, mapping, customer_name=None, bank_account_name=None):
        """
        Crea una instancia de la clase desde una fila de datos.

        Args:
            row (dict): Fila de datos.
            mapping (dict): Mapeo de campos.
            customer_name (str): Nombre del cliente.
        """
        return cls(
            customer_name=customer_name,
            bank_account_name=bank_account_name,
            street=row.get(mapping["street"]),
            pobox=row.get(mapping["pobox"]),
            city=row.get(mapping["city"]),
            state=row.get(mapping["state"]),
            code=row.get(mapping["code"]),
            complement=row.get(mapping.get("complement")),
            country=row.get(mapping.get("country"), "United States")
        )

    def __post_init__(self):
        """
        Método de inicialización posterior.
        """
        self.doctype = "Address"
        self.normalize_fields()
        self.normalize_and_sync()
    
    def normalize_fields(self):
        """
        Normaliza los campos.
        """
        RE_NON_LETTER = re.compile(r'[^A-Za-z0-9À-ÖØ-öø-ÿ ]+')
        self.street = RE_NON_LETTER.sub("", self.street)
        self.pobox = RE_NON_LETTER.sub("", self.pobox)
        self.city = RE_NON_LETTER.sub("", self.city)
        self.state = RE_NON_LETTER.sub("", self.state)
        self.code = RE_NON_LETTER.sub("", self.code)
        self.complement = RE_NON_LETTER.sub("", self.complement) if self.complement else ""
        self.country = "United States"


    def get_filters(self):
        """
        Obtiene los filtros para buscar la dirección.
        """
        return None

    def get_filters_child(self):
        """
        Obtiene los filtros para buscar los hijos de la dirección.
        """
        return None
    
    def get_existing_name(self):
        """
        Obtiene el nombre existente de la dirección.
        """
        fulladdress = self._full_address()
        return f"{fulladdress}-Shipping"

    def build_data(self):
        """
        Construye los datos para la dirección.
        """
        fulladdress = self._full_address()
        data = {
            "address_title": fulladdress,
            "address_type": "Shipping",
            "address_line1": self.street,
            "city": self.city,
            "state": self.state,
            "pincode": self.code,
            "country": self.country,
        }

        if self.customer_name:
            data.setdefault("links", []).append({
                "link_doctype": "Customer",
                "link_name": self.customer_name,
            })

        if self.bank_account_name:
            data.setdefault("links", []).append({
                "link_doctype": "Bank Account",
                "link_name": self.bank_account_name,
            })
        if self.complement:
            data["address_line2"] = self.complement
        return data

    def _full_address(self):
        """
        Obtiene la dirección completa.
        """
        return ", ".join(filter(None, [
            self.street,
            self.city,
            self.state,
            str(int(self.code)) if str(self.code).isdigit() else None
        ]))
