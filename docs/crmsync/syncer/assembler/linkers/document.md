# document
# Table of Contents

* [crmsync.syncer.assembler.linkers.document](#crmsync.syncer.assembler.linkers.document)
  * [DocumentLinker](#crmsync.syncer.assembler.linkers.document.DocumentLinker)
    * [\_\_init\_\_](#crmsync.syncer.assembler.linkers.document.DocumentLinker.__init__)
    * [execute](#crmsync.syncer.assembler.linkers.document.DocumentLinker.execute)

<a id="crmsync.syncer.assembler.linkers.document"></a>

# crmsync.syncer.assembler.linkers.document

<a id="crmsync.syncer.assembler.linkers.document.DocumentLinker"></a>

## DocumentLinker Objects

```python
class DocumentLinker(PipelineStep)
```

Vinculador de documentos.

Resuelve documentos asociados a Contact instances.
No toca pending_links; añade tipos y deadlines directamente a los objetos.

<a id="crmsync.syncer.assembler.linkers.document.DocumentLinker.__init__"></a>

#### \_\_init\_\_

```python
def __init__(person_resolver: SimpleNameResolver)
```

Constructor de la clase DocumentLinker.

**Arguments**:

- `person_resolver` _SimpleNameResolver_ - Resolvedor de nombres de personas.

<a id="crmsync.syncer.assembler.linkers.document.DocumentLinker.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

