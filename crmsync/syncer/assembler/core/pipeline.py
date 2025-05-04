from typing import List
from .step import PipelineStep

class Pipeline:
    """
    Pipeline de ejecución.

    Esta clase se encarga de ejecutar una serie de pasos en un orden específico.
    """
    def __init__(self, steps: List[PipelineStep]):
        """
        Constructor de la clase Pipeline.

        Args:
            steps (List[PipelineStep]): Lista de pasos a ejecutar.
        """
        self.steps = steps

    def run(self, context: dict):
        """
        Ejecuta el pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        for step in self.steps:
            step.execute(context)
