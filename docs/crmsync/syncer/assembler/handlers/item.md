# item
# Table of Contents

* [crmsync.syncer.assembler.handlers.item](#crmsync.syncer.assembler.handlers.item)
  * [Item](#crmsync.syncer.assembler.handlers.item.Item)
    * [item\_name](#crmsync.syncer.assembler.handlers.item.Item.item_name)
    * [item\_name\_child](#crmsync.syncer.assembler.handlers.item.Item.item_name_child)
    * [from\_row](#crmsync.syncer.assembler.handlers.item.Item.from_row)
    * [\_\_post\_init\_\_](#crmsync.syncer.assembler.handlers.item.Item.__post_init__)
    * [normalize\_fields](#crmsync.syncer.assembler.handlers.item.Item.normalize_fields)
    * [get\_filters](#crmsync.syncer.assembler.handlers.item.Item.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.item.Item.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.item.Item.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.item.Item.build_data)
    * [variant\_code](#crmsync.syncer.assembler.handlers.item.Item.variant_code)

<a id="crmsync.syncer.assembler.handlers.item"></a>

# crmsync.syncer.assembler.handlers.item

<a id="crmsync.syncer.assembler.handlers.item.Item"></a>

## Item Objects

```python
@dataclass
class Item(DocTypeHandler)
```

Handler para el artículo.

Esta clase se encarga de manejar la lógica para el artículo.

<a id="crmsync.syncer.assembler.handlers.item.Item.item_name"></a>

#### item\_name

Código base del plan (Item padre)

<a id="crmsync.syncer.assembler.handlers.item.Item.item_name_child"></a>

#### item\_name\_child

Código que define la versión (últimos dígitos)

<a id="crmsync.syncer.assembler.handlers.item.Item.from_row"></a>

#### from\_row

```python
@classmethod
def from_row(cls, row, cfg)
```

Crea una instancia de la clase desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `cfg` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.handlers.item.Item.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__()
```

Método de inicialización posterior.

<a id="crmsync.syncer.assembler.handlers.item.Item.normalize_fields"></a>

#### normalize\_fields

```python
def normalize_fields()
```

Normaliza los campos.

<a id="crmsync.syncer.assembler.handlers.item.Item.get_filters"></a>

#### get\_filters

```python
def get_filters()
```

Obtiene los filtros para buscar el artículo.

<a id="crmsync.syncer.assembler.handlers.item.Item.get_filters_child"></a>

#### get\_filters\_child

```python
def get_filters_child()
```

Obtiene los filtros para buscar los hijos del artículo.

<a id="crmsync.syncer.assembler.handlers.item.Item.get_existing_name"></a>

#### get\_existing\_name

```python
def get_existing_name()
```

Obtiene el nombre existente del artículo.

<a id="crmsync.syncer.assembler.handlers.item.Item.build_data"></a>

#### build\_data

```python
def build_data()
```

Construye los datos para el artículo.

<a id="crmsync.syncer.assembler.handlers.item.Item.variant_code"></a>

#### variant\_code

```python
def variant_code() -> str
```

Obtiene el código de variante.

