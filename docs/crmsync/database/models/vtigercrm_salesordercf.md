# vtigercrm_salesordercf
# Table of Contents

* [crmsync.database.models.vtigercrm\_salesordercf](#crmsync.database.models.vtigercrm_salesordercf)
  * [VTigerSalesOrderCF](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF)
    * [validText](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validText)
    * [validSSN](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validSSN)
    * [validItemCode](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validItemCode)
    * [validDate](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validDate)
    * [validFloat](#crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validFloat)
  * [sql\_transform\_text](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_text)
  * [sql\_transform\_ssn](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_ssn)
  * [sql\_transform\_date](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_date)
  * [sql\_transform\_float](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_float)
  * [sql\_transform\_title\_case](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_title_case)
  * [sql\_transform\_pass](#crmsync.database.models.vtigercrm_salesordercf.sql_transform_pass)
  * [create\_hybrid\_property](#crmsync.database.models.vtigercrm_salesordercf.create_hybrid_property)

<a id="crmsync.database.models.vtigercrm_salesordercf"></a>

# crmsync.database.models.vtigercrm\_salesordercf

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF"></a>

## VTigerSalesOrderCF Objects

```python
class VTigerSalesOrderCF(Base)
```

Modelo para la tabla vtiger_salesordercf.

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validText"></a>

#### validText

```python
@staticmethod
def validText(text: str | None) -> str | None
```

Valida un texto.

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validSSN"></a>

#### validSSN

```python
@staticmethod
def validSSN(ssn: str | None) -> str | None
```

Valida un SSN.

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validItemCode"></a>

#### validItemCode

```python
@staticmethod
def validItemCode(code: str | None) -> str | None
```

Valida un código de artículo.

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validDate"></a>

#### validDate

```python
@staticmethod
def validDate(value) -> str | None
```

Valida una fecha.

<a id="crmsync.database.models.vtigercrm_salesordercf.VTigerSalesOrderCF.validFloat"></a>

#### validFloat

```python
@staticmethod
def validFloat(val) -> float | None
```

Valida un número de punto flotante.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_text"></a>

#### sql\_transform\_text

```python
def sql_transform_text(column)
```

Transforma un texto en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_ssn"></a>

#### sql\_transform\_ssn

```python
def sql_transform_ssn(column)
```

Transforma un SSN en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_date"></a>

#### sql\_transform\_date

```python
def sql_transform_date(column)
```

Transforma una fecha en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_float"></a>

#### sql\_transform\_float

```python
def sql_transform_float(column)
```

Transforma un número de punto flotante en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_title_case"></a>

#### sql\_transform\_title\_case

```python
def sql_transform_title_case(column)
```

Transforma un texto a formato Title Case en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.sql_transform_pass"></a>

#### sql\_transform\_pass

```python
def sql_transform_pass(column)
```

Transforma una contraseña en SQL.

<a id="crmsync.database.models.vtigercrm_salesordercf.create_hybrid_property"></a>

#### create\_hybrid\_property

```python
def create_hybrid_property(cf_column: str,
                           prop_name: str,
                           transform_function,
                           sql_transform_function=None)
```

Crea una propiedad híbrida.

