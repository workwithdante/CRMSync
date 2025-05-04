# contact
# Table of Contents

* [crmsync.syncer.assembler.factories.contact](#crmsync.syncer.assembler.factories.contact)
  * [ContactFactory](#crmsync.syncer.assembler.factories.contact.ContactFactory)
    * [\_\_init\_\_](#crmsync.syncer.assembler.factories.contact.ContactFactory.__init__)
    * [execute](#crmsync.syncer.assembler.factories.contact.ContactFactory.execute)

<a id="crmsync.syncer.assembler.factories.contact"></a>

# crmsync.syncer.assembler.factories.contact

<a id="crmsync.syncer.assembler.factories.contact.ContactFactory"></a>

## ContactFactory Objects

```python
class ContactFactory(PipelineStep)
```

PipelineStep que crea y cachea instancias de Contact a partir de cada fila (row).
No contiene ninguna lógica de normalización ni mapeo: eso lo hace Contact.

<a id="crmsync.syncer.assembler.factories.contact.ContactFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mappings)
```

Constructor de la clase ContactFactory.

**Arguments**:

- `mappings` _dict_ - Mapeo de campos.

<a id="crmsync.syncer.assembler.factories.contact.ContactFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

