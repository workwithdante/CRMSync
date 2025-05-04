

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.item import Item # Importa la clase Item del módulo syncer.assembler.handlers.item


class ItemFactory(PipelineStep):
    """
    Fábrica de artículos.

    Esta clase se encarga de crear instancias de la clase Item.
    """
    def __init__(self, mapping):
        """
        Constructor de la clase ItemFactory.

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
        # Obtiene la fila de datos del contexto
        row = context["row"]
        # Crea una instancia de Item
        item = Item.from_row(row, *self.mapping)
        # Agrega el artículo al contexto
        context["item"] = item
