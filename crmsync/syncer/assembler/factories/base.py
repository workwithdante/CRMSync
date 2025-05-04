from abc import ABC, abstractmethod

class BaseFactory(ABC):
    """
    Clase base para las fábricas.

    Esta clase define la interfaz que deben implementar todas las fábricas.
    """
    @abstractmethod
    def execute(self, context: dict) -> None:
        """
        Ejecuta la fábrica.

        Debe implementarse para crear o actualizar datos en context.
        """
        pass
