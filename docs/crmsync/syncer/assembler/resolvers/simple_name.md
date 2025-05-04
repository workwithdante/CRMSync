# simple_name
# Table of Contents

* [crmsync.syncer.assembler.resolvers.simple\_name](#crmsync.syncer.assembler.resolvers.simple_name)
  * [SimpleNameResolver](#crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver)
    * [\_\_init\_\_](#crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.__init__)
    * [normalize\_name](#crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.normalize_name)
    * [process\_text](#crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.process_text)

<a id="crmsync.syncer.assembler.resolvers.simple_name"></a>

# crmsync.syncer.assembler.resolvers.simple\_name

<a id="crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver"></a>

## SimpleNameResolver Objects

```python
class SimpleNameResolver()
```

Resolvedor de nombres simple.

Esta clase se encarga de resolver nombres a partir de una lista de nombres válidos.

<a id="crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.__init__"></a>

#### \_\_init\_\_

```python
def __init__(valid_names: List[str])
```

Constructor de la clase SimpleNameResolver.

**Arguments**:

- `valid_names` _List[str]_ - Lista de nombres válidos.

<a id="crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.normalize_name"></a>

#### normalize\_name

```python
def normalize_name(raw_name: str) -> Tuple[str, Dict[str, float]]
```

Normaliza un nombre.

**Arguments**:

- `raw_name` _str_ - Nombre a normalizar.
  

**Returns**:

  Tuple[str, Dict[str, float]]: Tupla con el nombre normalizado y los scores.

<a id="crmsync.syncer.assembler.resolvers.simple_name.SimpleNameResolver.process_text"></a>

#### process\_text

```python
def process_text(raw_text: str) -> List[dict]
```

Procesa un texto.

**Arguments**:

- `raw_text` _str_ - Texto a procesar.
  

**Returns**:

- `List[dict]` - Lista de diccionarios con el texto original, el nombre coincidente y los scores.

