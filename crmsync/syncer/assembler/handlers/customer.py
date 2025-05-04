from dataclasses import dataclass, field
from typing import Optional
from syncer.assembler.handlers.base import DocTypeHandler

@dataclass
class Customer(DocTypeHandler):
    """
    Handler para el cliente.

    Esta clase se encarga de manejar la lógica para el cliente.
    """
    first_name: str
    last_name: str
    second_name: str
    customer_name: str
    
    @classmethod
    def from_row(cls, row, mapping):
        """
        Crea una instancia de la clase desde una fila de datos.

        Args:
            row (dict): Fila de datos.
            mapping (dict): Mapeo de campos.
        """
        return cls(
            first_name=row.get(mapping["first_name"]),
            last_name=row.get(mapping["last_name"]),
            second_name=row.get(mapping.get("second_name")),
            customer_name=row.get("customer_name"),
        )

    def __post_init__(self):
        """
        Método de inicialización posterior.
        """
        self.doctype = "Customer"
        self.normalize_and_sync()

    def get_filters(self):
        """
        Obtiene los filtros para buscar el cliente.
        """
        return None

    def get_filters_child(self):
        """
        Obtiene los filtros para buscar los hijos del cliente.
        """
        return None
    
    def get_existing_name(self):
        """
        Obtiene el nombre existente del cliente.
        """
        return self.full_name()

    def build_data(self):
        """
        Construye los datos para el cliente.
        """
        return {
            "customer_name": self.full_name(),
            "customer_group": "Individual",
            "territory": "United States",
            "default_currency": "USD",
            "default_price_list": "Standard Selling",
        }

    def full_name(self):
        """
        Obtiene el nombre completo del cliente.
        """
        if self.first_name and self.last_name:
            return " ".join(filter(None, [self.first_name, self.second_name, self.last_name]))
        else:
            return self.customer_name
