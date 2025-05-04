# vtigercrm_contactcf
# Table of Contents

* [crmsync.database.models.vtigercrm\_contactcf](#crmsync.database.models.vtigercrm_contactcf)
  * [VTigerContactsCF](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF)
    * [phone](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.phone)
    * [otherphone](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.otherphone)
    * [emergencyphone](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.emergencyphone)
    * [email1](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.email1)
    * [email2](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.email2)
    * [clean\_us\_phone](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.clean_us_phone)
    * [clean\_email](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.clean_email)
    * [is\_valid\_email](#crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.is_valid_email)

<a id="crmsync.database.models.vtigercrm_contactcf"></a>

# crmsync.database.models.vtigercrm\_contactcf

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF"></a>

## VTigerContactsCF Objects

```python
class VTigerContactsCF(Base)
```

Modelo para la tabla vtiger_contactscf.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.phone"></a>

#### phone

```python
@hybrid_property
def phone()
```

Obtiene el número de teléfono.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.otherphone"></a>

#### otherphone

```python
@hybrid_property
def otherphone()
```

Obtiene el número de teléfono alternativo.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.emergencyphone"></a>

#### emergencyphone

```python
@hybrid_property
def emergencyphone()
```

Obtiene el número de teléfono de emergencia.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.email1"></a>

#### email1

```python
@hybrid_property
def email1()
```

Obtiene el correo electrónico principal.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.email2"></a>

#### email2

```python
@hybrid_property
def email2()
```

Obtiene el correo electrónico alternativo.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.clean_us_phone"></a>

#### clean\_us\_phone

```python
@staticmethod
def clean_us_phone(number: str) -> str
```

Limpia un número de teléfono de EE. UU.

Elimina cualquier carácter que no sea dígito.
Si el número tiene 11 dígitos y comienza con '1', eliminar el primer dígito.
Retornar el número limpio si tiene 10 dígitos, o None en caso contrario.

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.clean_email"></a>

#### clean\_email

```python
@staticmethod
def clean_email(email: str) -> str
```

Limpia una dirección de correo electrónico.

Elimina espacios en blanco al principio y al final, y si hay espacios en el
interior, toma solo la primera parte (antes del primer espacio).

<a id="crmsync.database.models.vtigercrm_contactcf.VTigerContactsCF.is_valid_email"></a>

#### is\_valid\_email

```python
@staticmethod
def is_valid_email(email: str) -> bool
```

Valida si el correo electrónico tiene un formato adecuado.

La expresión regular permite letras, dígitos, puntos, guiones y subrayados en el nombre
de usuario y en el dominio, seguido de una extensión.

