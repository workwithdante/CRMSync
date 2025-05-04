# pipeline
# Table of Contents

* [crmsync.syncer.assembler.core.pipeline](#crmsync.syncer.assembler.core.pipeline)
  * [Pipeline](#crmsync.syncer.assembler.core.pipeline.Pipeline)
    * [\_\_init\_\_](#crmsync.syncer.assembler.core.pipeline.Pipeline.__init__)
    * [run](#crmsync.syncer.assembler.core.pipeline.Pipeline.run)

<a id="crmsync.syncer.assembler.core.pipeline"></a>

# crmsync.syncer.assembler.core.pipeline

<a id="crmsync.syncer.assembler.core.pipeline.Pipeline"></a>

## Pipeline Objects

```python
class Pipeline()
```

Pipeline de ejecución.

Esta clase se encarga de ejecutar una serie de pasos en un orden específico.

<a id="crmsync.syncer.assembler.core.pipeline.Pipeline.__init__"></a>

#### \_\_init\_\_

```python
def __init__(steps: List[PipelineStep])
```

Constructor de la clase Pipeline.

**Arguments**:

- `steps` _List[PipelineStep]_ - Lista de pasos a ejecutar.

<a id="crmsync.syncer.assembler.core.pipeline.Pipeline.run"></a>

#### run

```python
def run(context: dict)
```

Ejecuta el pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

