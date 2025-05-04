# entry_parser_doc_simple
# Table of Contents

* [crmsync.syncer.utils.entry\_parser\_doc\_simple](#crmsync.syncer.utils.entry_parser_doc_simple)
  * [SimpleNameResolver](#crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver)
    * [\_\_init\_\_](#crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.__init__)
    * [normalize\_name](#crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.normalize_name)
    * [process\_text](#crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.process_text)

<a id="crmsync.syncer.utils.entry_parser_doc_simple"></a>

# crmsync.syncer.utils.entry\_parser\_doc\_simple

<a id="crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver"></a>

## SimpleNameResolver Objects

```python
class SimpleNameResolver()
```

Resolvedor de nombres simple.

Esta clase se encarga de resolver nombres a partir de una lista de nombres válidos.

<a id="crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.__init__"></a>

#### \_\_init\_\_

```python
def __init__(valid_names: List[str])
```

Inicializa el resolvedor.

**Arguments**:

- `valid_names` _List[str]_ - Lista de nombres válidos.

<a id="crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.normalize_name"></a>

#### normalize\_name

```python
def normalize_name(raw_name: str) -> Tuple[str, Dict[str, float]]
```

Normaliza un nombre.

**Arguments**:

- `raw_name` _str_ - Nombre a normalizar.
  

**Returns**:

  Tuple[str, Dict[str, float]]: Tupla con el nombre normalizado y los scores.

<a id="crmsync.syncer.utils.entry_parser_doc_simple.SimpleNameResolver.process_text"></a>

#### process\_text

```python
def process_text(raw_text: str) -> List[dict]
```

Procesa un texto.

**Arguments**:

- `raw_text` _str_ - Texto a procesar.
  

**Returns**:

- `List[dict]` - Lista de diccionarios con el texto original, el nombre coincidente y los scores.

