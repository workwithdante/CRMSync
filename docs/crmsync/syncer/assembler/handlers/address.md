# address
# Table of Contents

* [crmsync.syncer.assembler.handlers.address](#crmsync.syncer.assembler.handlers.address)
  * [Address](#crmsync.syncer.assembler.handlers.address.Address)
    * [from\_row](#crmsync.syncer.assembler.handlers.address.Address.from_row)
    * [\_\_post\_init\_\_](#crmsync.syncer.assembler.handlers.address.Address.__post_init__)
    * [normalize\_fields](#crmsync.syncer.assembler.handlers.address.Address.normalize_fields)
    * [get\_filters](#crmsync.syncer.assembler.handlers.address.Address.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.address.Address.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.address.Address.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.address.Address.build_data)

<a id="crmsync.syncer.assembler.handlers.address"></a>

# crmsync.syncer.assembler.handlers.address

<a id="crmsync.syncer.assembler.handlers.address.Address"></a>

## Address Objects

```python
@dataclass
class Address(DocTypeHandler)
```

Handler para la dirección.

Esta clase se encarga de manejar la lógica para la dirección.

<a id="crmsync.syncer.assembler.handlers.address.Address.from_row"></a>

#### from\_row

```python
@classmethod
def from_row(cls, row, mapping, customer_name)
```

Crea una instancia de la clase desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `mapping` _dict_ - Mapeo de campos.
- `customer_name` _str_ - Nombre del cliente.

<a id="crmsync.syncer.assembler.handlers.address.Address.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__()
```

Método de inicialización posterior.

<a id="crmsync.syncer.assembler.handlers.address.Address.normalize_fields"></a>

#### normalize\_fields

```python
def normalize_fields()
```

Normaliza los campos.

<a id="crmsync.syncer.assembler.handlers.address.Address.get_filters"></a>

#### get\_filters

```python
def get_filters()
```

Obtiene los filtros para buscar la dirección.

<a id="crmsync.syncer.assembler.handlers.address.Address.get_filters_child"></a>

#### get\_filters\_child

```python
def get_filters_child()
```

Obtiene los filtros para buscar los hijos de la dirección.

<a id="crmsync.syncer.assembler.handlers.address.Address.get_existing_name"></a>

#### get\_existing\_name

```python
def get_existing_name()
```

Obtiene el nombre existente de la dirección.

<a id="crmsync.syncer.assembler.handlers.address.Address.build_data"></a>

#### build\_data

```python
def build_data()
```

Construye los datos para la dirección.

