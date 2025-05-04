# address
# Table of Contents

* [crmsync.syncer.assembler.linkers.address](#crmsync.syncer.assembler.linkers.address)
  * [AddressLinker](#crmsync.syncer.assembler.linkers.address.AddressLinker)
    * [execute](#crmsync.syncer.assembler.linkers.address.AddressLinker.execute)

<a id="crmsync.syncer.assembler.linkers.address"></a>

# crmsync.syncer.assembler.linkers.address

<a id="crmsync.syncer.assembler.linkers.address.AddressLinker"></a>

## AddressLinker Objects

```python
class AddressLinker(PipelineStep)
```

Vinculador de direcciones.

Toma las tuplas pending_links con doctype=="Address" y vincula
la cuenta bancaria a la Address cuyo `code` coincide con el pincode.

<a id="crmsync.syncer.assembler.linkers.address.AddressLinker.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

