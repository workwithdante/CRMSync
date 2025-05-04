

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.customer import Customer # Importa la clase Customer del módulo syncer.assembler.handlers.customer


class CustomerFactory(PipelineStep):
    """
    Fábrica de clientes.

    Esta clase se encarga de crear instancias de la clase Customer.
    """
    def __init__(self, mapping):
        """
        Constructor de la clase CustomerFactory.

        Args:
            mapping (dict): Mapeo de campos.
        """
        # Mapeo de campos
        self.mapping = mapping

    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene las filas de datos del contexto
        rows = context["rows"]
        # Obtiene la primera fila de datos
        first_row = rows.iloc[0]
        # Crea una instancia de Customer
        customer = Customer.from_row(first_row, *self.mapping)
        # Agrega el cliente al contexto
        context["customer"] = customer
        # Inicializa contenedores
        context.setdefault("contacts", [])
        context.setdefault("pending_links", [])
