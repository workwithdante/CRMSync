
from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.salesorder import SalesOrder # Importa la clase SalesOrder del módulo syncer.assembler.handlers.salesorder


class SalesOrderFactory(PipelineStep):
    """
    Fábrica de órdenes de venta.

    Esta clase se encarga de crear instancias de la clase SalesOrder.
    """
    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene la fila de datos del contexto
        row = context["row"]
        # Crea una instancia de SalesOrder
        so = SalesOrder.from_row(
            row,
            contacts=context.get("contacts", []),
            customer_name=context["customer"].name,
            item_name=context.get("item").name if context.get("item") else None,
            address_name=context.get("address").name if context.get("address") else None,
        )
