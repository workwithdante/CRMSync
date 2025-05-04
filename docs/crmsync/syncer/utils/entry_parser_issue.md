# entry_parser_issue
# Table of Contents

* [crmsync.syncer.utils.entry\_parser\_issue](#crmsync.syncer.utils.entry_parser_issue)
  * [create\_fuzzy\_person\_detector](#crmsync.syncer.utils.entry_parser_issue.create_fuzzy_person_detector)
  * [EntryParserNER](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER)
    * [\_\_init\_\_](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.__init__)
    * [normalize\_date](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_date)
    * [normalize\_name](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_name)
    * [normalize\_description](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_description)
    * [process\_text](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.process_text)
    * [to\_json](#crmsync.syncer.utils.entry_parser_issue.EntryParserNER.to_json)

<a id="crmsync.syncer.utils.entry_parser_issue"></a>

# crmsync.syncer.utils.entry\_parser\_issue

<a id="crmsync.syncer.utils.entry_parser_issue.create_fuzzy_person_detector"></a>

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

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER"></a>

## EntryParserNER Objects

```python
class EntryParserNER()
```

Parser de entradas de texto con NER (Named Entity Recognition).

Esta clase utiliza spaCy para realizar NER y extraer información relevante de un texto.

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.__init__"></a>

#### \_\_init\_\_

```python
def __init__(valid_names: List[str])
```

Inicializa el parser.

**Arguments**:

- `valid_names` - lista de nombres completos válidos

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_date"></a>

#### normalize\_date

```python
def normalize_date(date_text: str) -> str
```

Normaliza una fecha.

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_name"></a>

#### normalize\_name

```python
def normalize_name(raw_name: str) -> Tuple[str, dict]
```

Normaliza un nombre.

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.normalize_description"></a>

#### normalize\_description

```python
def normalize_description(desc: str) -> str
```

Normaliza una descripción.

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.process_text"></a>

#### process\_text

```python
def process_text(text: str) -> List[dict]
```

Procesa un texto.

<a id="crmsync.syncer.utils.entry_parser_issue.EntryParserNER.to_json"></a>

#### to\_json

```python
def to_json(text: str) -> str
```

Convierte el texto procesado a JSON.

