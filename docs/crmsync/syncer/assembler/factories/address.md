# address
# Table of Contents

* [crmsync.syncer.assembler.factories.address](#crmsync.syncer.assembler.factories.address)
  * [AddressFactory](#crmsync.syncer.assembler.factories.address.AddressFactory)
    * [\_\_init\_\_](#crmsync.syncer.assembler.factories.address.AddressFactory.__init__)
    * [execute](#crmsync.syncer.assembler.factories.address.AddressFactory.execute)

<a id="crmsync.syncer.assembler.factories.address"></a>

# crmsync.syncer.assembler.factories.address

<a id="crmsync.syncer.assembler.factories.address.AddressFactory"></a>

## AddressFactory Objects

```python
class AddressFactory(PipelineStep)
```

Fábrica de direcciones.

Esta clase se encarga de crear instancias de la clase Address.

<a id="crmsync.syncer.assembler.factories.address.AddressFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mapping)
```

Constructor de la clase AddressFactory.

**Arguments**:

- `mapping` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.factories.address.AddressFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

