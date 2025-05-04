# customer
# Table of Contents

* [crmsync.syncer.assembler.handlers.customer](#crmsync.syncer.assembler.handlers.customer)
  * [Customer](#crmsync.syncer.assembler.handlers.customer.Customer)
    * [from\_row](#crmsync.syncer.assembler.handlers.customer.Customer.from_row)
    * [\_\_post\_init\_\_](#crmsync.syncer.assembler.handlers.customer.Customer.__post_init__)
    * [get\_filters](#crmsync.syncer.assembler.handlers.customer.Customer.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.customer.Customer.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.customer.Customer.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.customer.Customer.build_data)
    * [full\_name](#crmsync.syncer.assembler.handlers.customer.Customer.full_name)

<a id="crmsync.syncer.assembler.handlers.customer"></a>

# crmsync.syncer.assembler.handlers.customer

<a id="crmsync.syncer.assembler.handlers.customer.Customer"></a>

## Customer Objects

```python
@dataclass
class Customer(DocTypeHandler)
```

Handler para el cliente.

Esta clase se encarga de manejar la lógica para el cliente.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.from_row"></a>

#### from\_row

```python
@classmethod
def from_row(cls, row, mapping)
```

Crea una instancia de la clase desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `mapping` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__()
```

Método de inicialización posterior.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.get_filters"></a>

#### get\_filters

```python
def get_filters()
```

Obtiene los filtros para buscar el cliente.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.get_filters_child"></a>

#### get\_filters\_child

```python
def get_filters_child()
```

Obtiene los filtros para buscar los hijos del cliente.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.get_existing_name"></a>

#### get\_existing\_name

```python
def get_existing_name()
```

Obtiene el nombre existente del cliente.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.build_data"></a>

#### build\_data

```python
def build_data()
```

Construye los datos para el cliente.

<a id="crmsync.syncer.assembler.handlers.customer.Customer.full_name"></a>

#### full\_name

```python
def full_name()
```

Obtiene el nombre completo del cliente.

