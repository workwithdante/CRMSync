from syncer.assembler.core.step import PipelineStep

class BaseLinker(PipelineStep):
    """
    Interfaz base para linkers que disparan client.doUpdateLinks().
    """
    def execute(self, context: dict) -> None:
        """
        Ejecuta el linker.

        Este método debe ser implementado por las clases hijas.
        """
        raise NotImplementedError
