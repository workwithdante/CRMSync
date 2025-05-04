# syncer
# Table of Contents

* [crmsync.syncer.syncer](#crmsync.syncer.syncer)
  * [Syncer](#crmsync.syncer.syncer.Syncer)
    * [\_\_init\_\_](#crmsync.syncer.syncer.Syncer.__init__)
    * [sync](#crmsync.syncer.syncer.Syncer.sync)
    * [recursive\_join](#crmsync.syncer.syncer.Syncer.recursive_join)

<a id="crmsync.syncer.syncer"></a>

# crmsync.syncer.syncer

<a id="crmsync.syncer.syncer.Syncer"></a>

## Syncer Objects

```python
class Syncer()
```

Sincronizador principal.

Esta clase coordina la sincronización de datos desde VTigerCRM a ERPNext.

<a id="crmsync.syncer.syncer.Syncer.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Inicializa el Syncer.

Configura el motor de base de datos, los servicios de consulta y la unidad de trabajo.

<a id="crmsync.syncer.syncer.Syncer.sync"></a>

#### sync

```python
def sync()
```

Ejecuta el proceso de sincronización.

Este método realiza la sincronización de datos en varios pasos:
1. Obtiene los registros de VTigerCRM.
2. Agrupa los registros por ID de contacto.
3. Procesa cada grupo de contactos en paralelo.

<a id="crmsync.syncer.syncer.Syncer.recursive_join"></a>

#### recursive\_join

```python
def recursive_join(query, join_list)
```

Realiza un JOIN recursivo en una consulta SQLAlchemy.

**Arguments**:

- `query` - La consulta base.
- `join_list` - Una lista de tuplas, donde cada tupla contiene un modelo y una condición de JOIN.
  

**Returns**:

  La consulta con los JOINs aplicados.

