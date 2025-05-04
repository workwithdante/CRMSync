# bank_account
# Table of Contents

* [crmsync.syncer.assembler.factories.bank\_account](#crmsync.syncer.assembler.factories.bank_account)
  * [BankAccountFactory](#crmsync.syncer.assembler.factories.bank_account.BankAccountFactory)
    * [\_\_init\_\_](#crmsync.syncer.assembler.factories.bank_account.BankAccountFactory.__init__)
    * [execute](#crmsync.syncer.assembler.factories.bank_account.BankAccountFactory.execute)

<a id="crmsync.syncer.assembler.factories.bank_account"></a>

# crmsync.syncer.assembler.factories.bank\_account

<a id="crmsync.syncer.assembler.factories.bank_account.BankAccountFactory"></a>

## BankAccountFactory Objects

```python
class BankAccountFactory(PipelineStep)
```

Fábrica de cuentas bancarias.

Esta clase se encarga de crear instancias de la clase BankAccount.

<a id="crmsync.syncer.assembler.factories.bank_account.BankAccountFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__(mappings, parser_bank)
```

Constructor de la clase BankAccountFactory.

**Arguments**:

- `mappings` _dict_ - Mapeo de campos.
- `parser_bank` _ParserBank_ - Parser para bancos.

<a id="crmsync.syncer.assembler.factories.bank_account.BankAccountFactory.execute"></a>

#### execute

```python
def execute(context: dict) -> None
```

Ejecuta el paso del pipeline.

**Arguments**:

- `context` _dict_ - Contexto del pipeline.

