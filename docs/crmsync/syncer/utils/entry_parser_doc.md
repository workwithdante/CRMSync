# entry_parser_doc
# Table of Contents

* [crmsync.syncer.utils.entry\_parser\_doc](#crmsync.syncer.utils.entry_parser_doc)
  * [create\_fuzzy\_person\_detector](#crmsync.syncer.utils.entry_parser_doc.create_fuzzy_person_detector)
  * [EntryParserDocNER](#crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER)
    * [\_\_init\_\_](#crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.__init__)
    * [normalize\_name](#crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.normalize_name)
    * [process\_text](#crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.process_text)

<a id="crmsync.syncer.utils.entry_parser_doc"></a>

# crmsync.syncer.utils.entry\_parser\_doc

<a id="crmsync.syncer.utils.entry_parser_doc.create_fuzzy_person_detector"></a>

#### create\_fuzzy\_person\_detector

```python
@Language.factory("fuzzy_person_detector",
                  default_config={
                      "valid_names": [],
                      "threshold": 75
                  })
def create_fuzzy_person_detector(nlp, name, valid_names: List[str],
                                 threshold: int)
```

Crea un detector de personas difuso.

Este componente de spaCy detecta entidades PERSON utilizando fuzzy matching.

<a id="crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER"></a>

## EntryParserDocNER Objects

```python
class EntryParserDocNER()
```

Parser de entradas de texto con NER (Named Entity Recognition).

Esta clase utiliza spaCy para realizar NER y extraer información relevante de un texto.

<a id="crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.__init__"></a>

#### \_\_init\_\_

```python
def __init__(valid_names: List[str], model_path: str = None)
```

Inicializa el parser.

**Arguments**:

- `valid_names` - lista de nombres completos válidos
- `model_path` - ruta al modelo spaCy (por defecto usa 'es_core_news_lg')

<a id="crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.normalize_name"></a>

#### normalize\_name

```python
def normalize_name(raw_name: str) -> Tuple[str, dict]
```

Normaliza un nombre.

**Arguments**:

- `raw_name` _str_ - Nombre a normalizar.
  

**Returns**:

  Tuple[str, dict]: Tupla con el nombre normalizado y los scores.

<a id="crmsync.syncer.utils.entry_parser_doc.EntryParserDocNER.process_text"></a>

#### process\_text

```python
def process_text(raw_text: str) -> List[dict]
```

Procesa un texto.

**Arguments**:

- `raw_text` _str_ - Texto a procesar.
  

**Returns**:

- `List[dict]` - Lista de diccionarios con el texto original, el nombre coincidente y los scores.

