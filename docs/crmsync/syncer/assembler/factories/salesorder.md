# salesorder
# Table of Contents

* [crmsync.syncer.assembler.factories.salesorder](#crmsync.syncer.assembler.factories.salesorder)
  * [SalesOrderFactory](#crmsync.syncer.assembler.factories.salesorder.SalesOrderFactory)
    * [execute](#crmsync.syncer.assembler.factories.salesorder.SalesOrderFactory.execute)

<a id="crmsync.syncer.assembler.factories.salesorder"></a>

# crmsync.syncer.assembler.factories.salesorder

<a id="crmsync.syncer.assembler.factories.salesorder.SalesOrderFactory"></a>

## SalesOrderFactory Objects

```python
class SalesOrderFactory(PipelineStep)
```

Fábrica de órdenes de venta.

Esta clase se encarga de crear instancias de la clase SalesOrder.

<a id="crmsync.syncer.assembler.factories.salesorder.SalesOrderFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

