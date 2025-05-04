# item
# Table of Contents

* [crmsync.syncer.assembler.factories.item](#crmsync.syncer.assembler.factories.item)
  * [ItemFactory](#crmsync.syncer.assembler.factories.item.ItemFactory)
    * [\_\_init\_\_](#crmsync.syncer.assembler.factories.item.ItemFactory.__init__)
    * [execute](#crmsync.syncer.assembler.factories.item.ItemFactory.execute)

<a id="crmsync.syncer.assembler.factories.item"></a>

# crmsync.syncer.assembler.factories.item

<a id="crmsync.syncer.assembler.factories.item.ItemFactory"></a>

## ItemFactory Objects

```python
class ItemFactory(PipelineStep)
```

Fábrica de artículos.

Esta clase se encarga de crear instancias de la clase Item.

<a id="crmsync.syncer.assembler.factories.item.ItemFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mapping)
```

Constructor de la clase ItemFactory.

**Arguments**:

- `mapping` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.factories.item.ItemFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

