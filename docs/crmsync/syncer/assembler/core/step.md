# step
# Table of Contents

* [crmsync.syncer.assembler.core.step](#crmsync.syncer.assembler.core.step)
  * [PipelineStep](#crmsync.syncer.assembler.core.step.PipelineStep)
    * [execute](#crmsync.syncer.assembler.core.step.PipelineStep.execute)

<a id="crmsync.syncer.assembler.core.step"></a>

# crmsync.syncer.assembler.core.step

<a id="crmsync.syncer.assembler.core.step.PipelineStep"></a>

## PipelineStep Objects

```python
class PipelineStep(ABC)
```

Clase base para los pasos del pipeline.

Esta clase define la interfaz que deben implementar todos los pasos del pipeline.

<a id="crmsync.syncer.assembler.core.step.PipelineStep.execute"></a>

#### execute

```python
@abstractmethod
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

Modifica el context en sitio (agrega o vincula objetos).

