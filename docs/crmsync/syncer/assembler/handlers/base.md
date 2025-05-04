# base
# Table of Contents

* [crmsync.syncer.assembler.handlers.base](#crmsync.syncer.assembler.handlers.base)
  * [DocTypeHandler](#crmsync.syncer.assembler.handlers.base.DocTypeHandler)
    * [from\_row](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.from_row)
    * [get\_filters](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_filters)
    * [get\_filters\_child](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_filters_child)
    * [get\_existing\_name](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_existing_name)
    * [build\_data](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.build_data)
    * [extract\_name](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.extract_name)
    * [normalize\_and\_sync](#crmsync.syncer.assembler.handlers.base.DocTypeHandler.normalize_and_sync)

<a id="crmsync.syncer.assembler.handlers.base"></a>

# crmsync.syncer.assembler.handlers.base

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler"></a>

## DocTypeHandler Objects

```python
@dataclass(kw_only=True)
class DocTypeHandler(ABC)
```

Clase base para los handlers de DocType.

Esta clase define la estructura base para los handlers de DocType,
que se encargan de la lógica de mapeo, normalización y sincronización
de los datos.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.from_row"></a>

#### from\_row

```python
@classmethod
@abstractmethod
def from_row(cls, row, mapping: dict)
```

Crea una instancia de la clase desde una fila de datos.

**Arguments**:

- `row` _dict_ - Fila de datos.
- `mapping` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_filters"></a>

#### get\_filters

```python
@abstractmethod
def get_filters() -> list
```

Obtiene los filtros para buscar si el documento ya existe.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_filters_child"></a>

#### get\_filters\_child

```python
@abstractmethod
def get_filters_child() -> list
```

Obtiene los filtros para buscar si el documento ya existe en los hijos.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.get_existing_name"></a>

#### get\_existing\_name

```python
@abstractmethod
def get_existing_name() -> str
```

Obtiene el nombre estimado del documento (para uso en la búsqueda).

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.build_data"></a>

#### build\_data

```python
@abstractmethod
def build_data() -> dict
```

Construye la estructura de datos nueva a crear o comparar.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.extract_name"></a>

#### extract\_name

```python
def extract_name(result: dict)
```

Extrae el nombre del resultado.

**Arguments**:

- `result` _dict_ - Resultado de la API.

<a id="crmsync.syncer.assembler.handlers.base.DocTypeHandler.normalize_and_sync"></a>

#### normalize\_and\_sync

```python
def normalize_and_sync()
```

Normaliza y sincroniza los datos.

Este método se encarga de normalizar los datos y sincronizarlos
con la API de ERPNext.

