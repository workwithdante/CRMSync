# base
# Table of Contents

* [crmsync.syncer.assembler.factories.base](#crmsync.syncer.assembler.factories.base)
  * [BaseFactory](#crmsync.syncer.assembler.factories.base.BaseFactory)
    * [execute](#crmsync.syncer.assembler.factories.base.BaseFactory.execute)

<a id="crmsync.syncer.assembler.factories.base"></a>

# crmsync.syncer.assembler.factories.base

<a id="crmsync.syncer.assembler.factories.base.BaseFactory"></a>

## BaseFactory Objects

```python
class BaseFactory(ABC)
```

Clase base para las fábricas.

Esta clase define la interfaz que deben implementar todas las fábricas.

<a id="crmsync.syncer.assembler.factories.base.BaseFactory.execute"></a>

#### execute

```python
@abstractmethod
def execute(context: dict) -> None
```

Ejecuta la fábrica.

Debe implementarse para crear o actualizar datos en context.

