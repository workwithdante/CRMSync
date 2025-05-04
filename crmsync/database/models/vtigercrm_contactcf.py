import re

import re

from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_contactscf'])


class VTigerContactsCF(Base):
    """
    Modelo para la tabla vtiger_contactscf.
    """
    __table__ = metadata.tables['vtiger_contactscf']

    @hybrid_property
    def phone(self):
        """
        Obtiene el número de teléfono.
        """
        if self.cf_819:
            return self.cf_819 if self.clean_us_phone(self.cf_819) else None
        return None

    @hybrid_property
    def otherphone(self):
        """
        Obtiene el número de teléfono alternativo.
        """
        if self.cf_827:
            return self.cf_827 if self.clean_us_phone(self.cf_827) else None
        return None

    @hybrid_property
    def emergencyphone(self):
        """
        Obtiene el número de teléfono de emergencia.
        """
        if self.cf_1983:
            return self.cf_827 if self.clean_us_phone(self.cf_1983) else None
        return None

    @hybrid_property
    def email1(self):
        """
        Obtiene el correo electrónico principal.
        """
        if self.cf_815:
            return self.cf_815 if self.clean_email(self.cf_815) else None
        return None

    @hybrid_property
    def email2(self):
        """
        Obtiene el correo electrónico alternativo.
        """
        if self.cf_1589:
            return self.cf_1589 if self.clean_email(self.cf_1589) else None
        return None

    @staticmethod
    def clean_us_phone(number: str) -> str:
        """
        Limpia un número de teléfono de EE. UU.

        Elimina cualquier carácter que no sea dígito.
        Si el número tiene 11 dígitos y comienza con '1', eliminar el primer dígito.
        Retornar el número limpio si tiene 10 dígitos, o None en caso contrario.
        """
        # Eliminar cualquier carácter que no sea dígito.
        cleaned = re.sub(r'\D', '', number)

        # Si el número tiene 11 dígitos y comienza con '1', eliminar el primer dígito.
        if len(cleaned) == 11 and cleaned.startswith('1'):
            cleaned = cleaned[1:]

        # Retornar el número limpio si tiene 10 dígitos, o None en caso contrario.
        return cleaned if len(cleaned) == 10 else ''

    @staticmethod
    def clean_email(email: str) -> str:
        """
        Limpia una dirección de correo electrónico.

        Elimina espacios en blanco al principio y al final, y si hay espacios en el
        interior, toma solo la primera parte (antes del primer espacio).
        """
        email = email.strip()
        # Si existen espacios en el email, tomar solo la primera parte.
        if ' ' in email:
            email = email.split()[0]

        return email if VTigerContactsCF.is_valid_email(email) else ''

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Valida si el correo electrónico tiene un formato adecuado.

        La expresión regular permite letras, dígitos, puntos, guiones y subrayados en el nombre
        de usuario y en el dominio, seguido de una extensión.
        """
        # Patrón que cubre la mayoría de los casos comunes para emails.
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
