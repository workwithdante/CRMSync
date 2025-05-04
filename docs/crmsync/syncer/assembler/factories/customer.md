# customer
# Table of Contents

* [crmsync.syncer.assembler.factories.customer](#crmsync.syncer.assembler.factories.customer)
  * [CustomerFactory](#crmsync.syncer.assembler.factories.customer.CustomerFactory)
    * [\_\_init\_\_](#crmsync.syncer.assembler.factories.customer.CustomerFactory.__init__)
    * [execute](#crmsync.syncer.assembler.factories.customer.CustomerFactory.execute)

<a id="crmsync.syncer.assembler.factories.customer"></a>

# crmsync.syncer.assembler.factories.customer

<a id="crmsync.syncer.assembler.factories.customer.CustomerFactory"></a>

## CustomerFactory Objects

```python
class CustomerFactory(PipelineStep)
```

Fábrica de clientes.

Esta clase se encarga de crear instancias de la clase Customer.

<a id="crmsync.syncer.assembler.factories.customer.CustomerFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mapping)
```

Constructor de la clase CustomerFactory.

**Arguments**:

- `mapping` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.factories.customer.CustomerFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

