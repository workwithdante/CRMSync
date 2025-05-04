# comparator
# Table of Contents

* [crmsync.syncer.utils.comparator](#crmsync.syncer.utils.comparator)
  * [DictComparator](#crmsync.syncer.utils.comparator.DictComparator)
    * [\_\_init\_\_](#crmsync.syncer.utils.comparator.DictComparator.__init__)
    * [register](#crmsync.syncer.utils.comparator.DictComparator.register)
    * [compare\_dicts](#crmsync.syncer.utils.comparator.DictComparator.compare_dicts)
    * [compare\_list\_of\_dicts](#crmsync.syncer.utils.comparator.DictComparator.compare_list_of_dicts)
    * [compare\_items\_with\_names](#crmsync.syncer.utils.comparator.DictComparator.compare_items_with_names)

<a id="crmsync.syncer.utils.comparator"></a>

# crmsync.syncer.utils.comparator

<a id="crmsync.syncer.utils.comparator.DictComparator"></a>

## DictComparator Objects

```python
class DictComparator()
```

Comparador de diccionarios.

Esta clase se encarga de comparar diccionarios y detectar las diferencias.

<a id="crmsync.syncer.utils.comparator.DictComparator.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Inicializa el comparador.

<a id="crmsync.syncer.utils.comparator.DictComparator.register"></a>

#### register

```python
def register(field: str, fn)
```

Registra una función de comparación especial para un campo.

**Arguments**:

- `field` _str_ - Nombre del campo.
- `fn` - Función de comparación.

<a id="crmsync.syncer.utils.comparator.DictComparator.compare_dicts"></a>

#### compare\_dicts

```python
def compare_dicts(new_data: Dict, existing_data: Dict) -> Dict
```

Compara dos diccionarios y devuelve las diferencias.

**Arguments**:

- `new_data` _Dict_ - Diccionario nuevo.
- `existing_data` _Dict_ - Diccionario existente.
  

**Returns**:

- `Dict` - Diccionario con las diferencias.

<a id="crmsync.syncer.utils.comparator.DictComparator.compare_list_of_dicts"></a>

#### compare\_list\_of\_dicts

```python
def compare_list_of_dicts(new_list: List[Dict[str, Any]],
                          existing_list: List[Dict[str, Any]],
                          keys: List[str],
                          append: bool = False) -> bool
```

Compara dos listas de diccionarios y devuelve True si hay diferencias.

**Arguments**:

- `new_list` _List[Dict[str, Any]]_ - Lista nueva.
- `existing_list` _List[Dict[str, Any]]_ - Lista existente.
- `keys` _List[str]_ - Lista de claves a comparar.
- `append` _bool_ - Indica si se deben agregar los elementos faltantes de la lista nueva a la existente.
  

**Returns**:

- `bool` - True si hay diferencias, False en caso contrario.

<a id="crmsync.syncer.utils.comparator.DictComparator.compare_items_with_names"></a>

#### compare\_items\_with\_names

```python
def compare_items_with_names(new_items, existing_items, match_by="item_code")
```

Compara dos listas de items y devuelve True si hay diferencias.

**Arguments**:

- `new_items` _List[Dict[str, Any]]_ - Lista nueva.
- `existing_items` _List[Dict[str, Any]]_ - Lista existente.
- `match_by` _str_ - Campo a usar para la comparación.
  

**Returns**:

- `bool` - True si hay diferencias, False en caso contrario.

