# query
# Table of Contents

* [crmsync.database.services.query](#crmsync.database.services.query)
  * [QueryService](#crmsync.database.services.query.QueryService)
    * [\_\_init\_\_](#crmsync.database.services.query.QueryService.__init__)
    * [validate\_connection](#crmsync.database.services.query.QueryService.validate_connection)
    * [fetch\_records](#crmsync.database.services.query.QueryService.fetch_records)
    * [recursive\_join](#crmsync.database.services.query.QueryService.recursive_join)
    * [fetch\_issues](#crmsync.database.services.query.QueryService.fetch_issues)
    * [clean\_for\_polars](#crmsync.database.services.query.QueryService.clean_for_polars)

<a id="crmsync.database.services.query"></a>

# crmsync.database.services.query

<a id="crmsync.database.services.query.QueryService"></a>

## QueryService Objects

```python
class QueryService()
```

Servicio de consultas a la base de datos.

<a id="crmsync.database.services.query.QueryService.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config: SyncConfig)
```

Inicializa una nueva instancia de QueryService.

**Arguments**:

- `config` _SyncConfig_ - Configuración de sincronización.

<a id="crmsync.database.services.query.QueryService.validate_connection"></a>

#### validate\_connection

```python
def validate_connection(uow)
```

Valida la conexión a la base de datos.

<a id="crmsync.database.services.query.QueryService.fetch_records"></a>

#### fetch\_records

```python
def fetch_records(uow,
                  offset_contacts: int = 1,
                  limit_contacts: int = 1) -> DataFrame
```

Obtiene los registros de la base de datos.

**Arguments**:

- `uow` - Unidad de trabajo.
- `offset_contacts` _int_ - Offset de los contactos.
- `limit_contacts` _int_ - Límite de los contactos.
  

**Returns**:

- `DataFrame` - DataFrame con los registros.

<a id="crmsync.database.services.query.QueryService.recursive_join"></a>

#### recursive\_join

```python
def recursive_join(query, join_list)
```

Función recursiva que añade JOINs a la consulta.

**Arguments**:

- `query` - Consulta base.
- `join_list` - Lista de tuplas (modelo, condición de join).
  

**Returns**:

  Consulta con los JOINs aplicados.

<a id="crmsync.database.services.query.QueryService.fetch_issues"></a>

#### fetch\_issues

```python
def fetch_issues(uow, contact_id) -> DataFrame
```

Obtiene todos los tickets de problemas (issues) para un contact_id dado.

**Arguments**:

- `uow` - Unidad de trabajo.
- `contact_id` - ID del contacto.
  

**Returns**:

- `DataFrame` - DataFrame con ticket_id, status, title, created_time, description, solution.

<a id="crmsync.database.services.query.QueryService.clean_for_polars"></a>

#### clean\_for\_polars

```python
def clean_for_polars(df: pd.DataFrame) -> pd.DataFrame
```

Limpia el DataFrame para usar con Polars.

