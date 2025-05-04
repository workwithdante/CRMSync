# policy_assembler
# Table of Contents

* [crmsync.syncer.assembler.policy\_assembler](#crmsync.syncer.assembler.policy_assembler)
  * [PolicyAssembler](#crmsync.syncer.assembler.policy_assembler.PolicyAssembler)
    * [\_\_init\_\_](#crmsync.syncer.assembler.policy_assembler.PolicyAssembler.__init__)
    * [assemble](#crmsync.syncer.assembler.policy_assembler.PolicyAssembler.assemble)

<a id="crmsync.syncer.assembler.policy_assembler"></a>

# crmsync.syncer.assembler.policy\_assembler

<a id="crmsync.syncer.assembler.policy_assembler.PolicyAssembler"></a>

## PolicyAssembler Objects

```python
class PolicyAssembler()
```

Ensamblador de políticas.

Esta clase se encarga de ensamblar las políticas para un contacto,
coordinando la creación de objetos y el establecimiento de relaciones
entre ellos.

<a id="crmsync.syncer.assembler.policy_assembler.PolicyAssembler.__init__"></a>

#### \_\_init\_\_

```python
def __init__(config, parser_bank)
```

Constructor de la clase PolicyAssembler.

Inicializa el ensamblador con la configuración y los resolvedores necesarios.

**Arguments**:

- `config` _dict_ - Configuración de la aplicación.
- `parser_bank` _ParserBank_ - Parser para nombres de bancos.

<a id="crmsync.syncer.assembler.policy_assembler.PolicyAssembler.assemble"></a>

#### assemble

```python
def assemble(contact_id: str, rows)
```

Ensambla las políticas para un contacto.

Este método toma un ID de contacto y una lista de filas de datos,
y ejecuta el pipeline para crear y relacionar los objetos correspondientes.

**Arguments**:

- `contact_id` _str_ - ID del contacto.
- `rows` _list_ - Lista de filas de datos.

