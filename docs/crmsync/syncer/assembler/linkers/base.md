# base
# Table of Contents

* [crmsync.syncer.assembler.linkers.base](#crmsync.syncer.assembler.linkers.base)
  * [BaseLinker](#crmsync.syncer.assembler.linkers.base.BaseLinker)
    * [execute](#crmsync.syncer.assembler.linkers.base.BaseLinker.execute)

<a id="crmsync.syncer.assembler.linkers.base"></a>

# crmsync.syncer.assembler.linkers.base

<a id="crmsync.syncer.assembler.linkers.base.BaseLinker"></a>

## BaseLinker Objects

```python
class BaseLinker(PipelineStep)
```

Interfaz base para linkers que disparan client.doUpdateLinks().

<a id="crmsync.syncer.assembler.linkers.base.BaseLinker.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el linker.

Este método debe ser implementado por las clases hijas.

