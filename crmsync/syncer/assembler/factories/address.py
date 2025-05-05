

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.address import Address # Importa la clase Address del módulo syncer.assembler.handlers.address


class AddressFactory(PipelineStep):
    """
    Fábrica de direcciones.

    Esta clase se encarga de crear instancias de la clase Address.
    """
    def __init__(self, mapping):
        """
        Constructor de la clase AddressFactory.

        Args:
            mapping (dict): Mapeo de campos.
        """
        # Mapeo de campos
        self.mapping = mapping
        # Cache de direcciones
        self.cache: dict = {}

    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene la fila de datos del contexto
        row = context["row"]
        # Obtiene el cliente del contexto
        customer = context["customer"]

        # Obtiene la cuenta bancaria del contexto
        bank_account = context["bank_account"]

        # Define la clave para el cache
        key = (
            row.get(self.mapping["street"]),
            row.get(self.mapping["city"]),
            row.get(self.mapping["state"]),
            row.get(self.mapping["code"]),
        )
        # Inicializa la variable address
        address = None
        # Si todos los campos de la clave existen y al menos uno no está vacío
        if all(key) and any(isinstance(s, str) and s.strip() for s in key):
            # Si la clave está en el cache
            if key in self.cache:
                # Obtiene la dirección del cache
                address = self.cache[key]
            else:
                optional = {
                    "customer_name": customer.name if customer is not None else None,
                    "bank_account_name": bank_account.name if bank_account is not None else None,
                }
                filtered_kwargs = {k: v for k, v in optional.items() if v is not None}

                # Crea una nueva instancia de Address
                address = Address.from_row(row, self.mapping, **filtered_kwargs)
                # Agrega la dirección al cache
                self.cache[key] = address
        # Agrega la dirección al contexto
        context["address"] = address
        # Expone el cache al contexto para linkers
        context["address_cache"] = self.cache
