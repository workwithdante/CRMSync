from abc import ABC, abstractmethod

class PipelineStep(ABC):
    """
    Clase base para los pasos del pipeline.

    Esta clase define la interfaz que deben implementar todos los pasos del pipeline.
    """
    @abstractmethod
    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Modifica el context en sitio (agrega o vincula objetos).
        """
