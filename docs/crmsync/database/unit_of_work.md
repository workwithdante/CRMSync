# unit_of_work
# Table of Contents

* [crmsync.database.unit\_of\_work](#crmsync.database.unit_of_work)
  * [UnitOfWork](#crmsync.database.unit_of_work.UnitOfWork)
    * [\_\_init\_\_](#crmsync.database.unit_of_work.UnitOfWork.__init__)
    * [\_\_enter\_\_](#crmsync.database.unit_of_work.UnitOfWork.__enter__)
    * [\_\_exit\_\_](#crmsync.database.unit_of_work.UnitOfWork.__exit__)

<a id="crmsync.database.unit_of_work"></a>

# crmsync.database.unit\_of\_work

<a id="crmsync.database.unit_of_work.UnitOfWork"></a>

## UnitOfWork Objects

```python
class UnitOfWork()
```

Implementación del patrón Unit of Work para las transacciones de la base de datos.

<a id="crmsync.database.unit_of_work.UnitOfWork.__init__"></a>

#### \_\_init\_\_

```python
def __init__(session_factory)
```

Inicializa una nueva instancia de UnitOfWork.

**Arguments**:

- `session_factory` - Función de fábrica para crear nuevas sesiones.

<a id="crmsync.database.unit_of_work.UnitOfWork.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

Crea una nueva sesión al entrar en el contexto.

<a id="crmsync.database.unit_of_work.UnitOfWork.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb)
```

Maneja la finalización de la transacción.

