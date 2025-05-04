# contact
# Table of Contents

* [crmsync.syncer.assembler.handlers.contact](#crmsync.syncer.assembler.handlers.contact)
  * [Contact](#crmsync.syncer.assembler.handlers.contact.Contact)
    * [\_\_post\_init\_\_](#crmsync.syncer.assembler.handlers.contact.Contact.__post_init__)
    * [from\_row](#crmsync.syncer.assembler.handlers.contact.Contact.from_row)
    * [get\_filters](#crmsync.syncer.assembler.handlers.contact.Contact.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.contact.Contact.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.contact.Contact.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.contact.Contact.build_data)
    * [full\_name](#crmsync.syncer.assembler.handlers.contact.Contact.full_name)

<a id="crmsync.syncer.assembler.handlers.contact"></a>

# crmsync.syncer.assembler.handlers.contact

<a id="crmsync.syncer.assembler.handlers.contact.Contact"></a>

## Contact Objects

```python
@dataclass
class Contact(DocTypeHandler)
```

DocTypeHandler para Contact: contiene toda la lógica de mapeo, normalización
y construcción de payload para la API de ERPNext.

**Arguments**:

- `customer_name` _str_ - Nombre del cliente.
- `relationship` _str_ - Relación con el cliente.
- `first_name` _str_ - Nombre.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__()
```

Método de inicialización posterior.

Este método se llama después de que se crea una instancia de la clase.
Se encarga de normalizar los datos y sincronizarlos.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.from_row"></a>

#### from\_row

```python
@classmethod
def from_row(cls, row, cfg: dict, customer_name: str)
```

Método de clase para crear una instancia de Contact desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `cfg` _dict_ - Configuración.
- `customer_name` _str_ - Nombre del cliente.
  

**Returns**:

- `Contact` - Una instancia de la clase Contact.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.get_filters"></a>

#### get\_filters

```python
def get_filters()
```

Obtiene los filtros para buscar el contacto.

Este método se encarga de obtener los filtros para buscar el contacto
en la base de datos.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.get_filters_child"></a>

#### get\_filters\_child

```python
def get_filters_child()
```

Obtiene los filtros para buscar los hijos del contacto.

Este método se encarga de obtener los filtros para buscar los hijos del contacto
en la base de datos.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.get_existing_name"></a>

#### get\_existing\_name

```python
def get_existing_name()
```

Obtiene el nombre existente del contacto.

Este método se encarga de obtener el nombre existente del contacto.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.build_data"></a>

#### build\_data

```python
def build_data()
```

Construye los datos para el contacto.

Este método se encarga de construir los datos para el contacto
que se enviarán a la API de ERPNext.

<a id="crmsync.syncer.assembler.handlers.contact.Contact.full_name"></a>

#### full\_name

```python
def full_name()
```

Obtiene el nombre completo del contacto.

Este método se encarga de obtener el nombre completo del contacto,
concatenando el nombre, el apellido y el nombre del cliente.

