# contact
# Table of Contents

* [crmsync.syncer.assembler.linkers.contact](#crmsync.syncer.assembler.linkers.contact)
  * [ContactLinker](#crmsync.syncer.assembler.linkers.contact.ContactLinker)
    * [\_\_init\_\_](#crmsync.syncer.assembler.linkers.contact.ContactLinker.__init__)
    * [execute](#crmsync.syncer.assembler.linkers.contact.ContactLinker.execute)

<a id="crmsync.syncer.assembler.linkers.contact"></a>

# crmsync.syncer.assembler.linkers.contact

<a id="crmsync.syncer.assembler.linkers.contact.ContactLinker"></a>

## ContactLinker Objects

```python
class ContactLinker(PipelineStep)
```

Vinculador de contactos.

Toma las tuplas pending_links con doctype=="Contact" y vincula
la cuenta bancaria al Contact correspondiente.

<a id="crmsync.syncer.assembler.linkers.contact.ContactLinker.__init__"></a>

#### \_\_init\_\_

```python
def __init__(person_resolver: SimpleNameResolver)
```

Constructor de la clase ContactLinker.

**Arguments**:

- `person_resolver` _SimpleNameResolver_ - Resolvedor de nombres de personas.

<a id="crmsync.syncer.assembler.linkers.contact.ContactLinker.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

