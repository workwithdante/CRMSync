# salesorder
# Table of Contents

* [crmsync.syncer.assembler.handlers.salesorder](#crmsync.syncer.assembler.handlers.salesorder)
  * [SalesOrder](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder)
    * [from\_row](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.from_row)
    * [\_\_post\_init\_\_](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.__post_init__)
    * [normalize\_fields](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.normalize_fields)
    * [get\_filters](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.salesorder.SalesOrder.build_data)

<a id="crmsync.syncer.assembler.handlers.salesorder"></a>

# crmsync.syncer.assembler.handlers.salesorder

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder"></a>

## SalesOrder Objects

```python
@dataclass
class SalesOrder(DocTypeHandler)
```

Handler para la orden de venta.

Esta clase se encarga de manejar la lógica para la orden de venta.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.from_row"></a>

#### from\_row

```python
@classmethod
def from_row(cls, row, contacts: List[Contact], customer_name, item_name,
             address_name)
```

Crea una instancia de la clase desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `contacts` _List[Contact]_ - Lista de contactos.
- `customer_name` _str_ - Nombre del cliente.
- `item_name` _str_ - Nombre del artículo.
- `address_name` _str_ - Nombre de la dirección.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__()
```

Método de inicialización posterior.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.normalize_fields"></a>

#### normalize\_fields

```python
def normalize_fields()
```

Normaliza los campos.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_filters"></a>

#### get\_filters

```python
def get_filters()
```

Obtiene los filtros para buscar la orden de venta.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_filters_child"></a>

#### get\_filters\_child

```python
def get_filters_child()
```

Obtiene los filtros para buscar los hijos de la orden de venta.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.get_existing_name"></a>

#### get\_existing\_name

```python
def get_existing_name()
```

Obtiene el nombre existente de la orden de venta.

<a id="crmsync.syncer.assembler.handlers.salesorder.SalesOrder.build_data"></a>

#### build\_data

```python
def build_data()
```

Construye los datos para la orden de venta.

