import os
import re
import os
import re
from sqlalchemy import Float, MetaData, func
from sqlalchemy.ext.hybrid import hybrid_property

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_salesordercf'])


class VTigerSalesOrderCF(Base):
    """
    Modelo para la tabla vtiger_salesordercf.
    """
    __table__ = metadata.tables['vtiger_salesordercf']

    @staticmethod
    def validText(text: str | None) -> str | None:
        """
        Valida un texto.
        """
        if text is None:
            return None

        cleaned = text.strip()
        if len(cleaned) <= 1:
            return None

        return cleaned.capitalize()

    @staticmethod
    def validSSN(ssn: str | None) -> str | None:
        """
        Valida un SSN.
        """
        if not ssn:
            return None
        cleaned = re.sub(r'\D', '', ssn)
        # Si queda vacío o un solo dígito, devolvemos None
        if len(cleaned) <= 1:
            return None
        return cleaned

    @staticmethod
    def validItemCode(code: str | None) -> str | None:
        """
        Valida un código de artículo.
        """
        if not code:
            return None
        cleaned = code.strip().upper()
        # Si queda vacío o un solo carácter, devolvemos None
        if len(cleaned) <= 1:
            return None
        return cleaned

    @staticmethod
    def validDate(value) -> str | None:
        """
        Valida una fecha.
        """
        # Asegurarnos de que tenga método strftime (por ejemplo un datetime.date)
        if not value or not hasattr(value, 'strftime'):
            return None
        formatted = value.strftime('%Y-%m-%d')
        # Aunque casi siempre tendrá varios caracteres,
        # seguimos la misma regla por consistencia
        if len(formatted) <= 1:
            return None
        return formatted

    @staticmethod
    def validFloat(val) -> float | None:
        """
        Valida un número de punto flotante.
        """
        if val is None:
            return None
        s = str(val).strip()
        # Si, tras limpiar, no queda nada o sólo un carácter,
        # devolvemos None en lugar de intentar parsear
        if len(s) <= 1:
            return None
        try:
            return float(s)
        except (ValueError, TypeError):
            return None


# Funciones de transformación SQL

def sql_transform_text(column):
    """
    Transforma un texto en SQL.
    """
    # 1) Trim y colapsar múltiples espacios en uno
    no_double_spaces = func.regexp_replace(
        func.trim(column),
        r'\\s+',   # expresión regular: uno o más espacios
        ' '        # reemplázalo por un único espacio
    )
    # 2) Primera letra en mayúscula
    first_letter = func.upper(func.left(no_double_spaces, 1))
    # 3) Resto en minúscula
    rest        = func.lower(func.substring(no_double_spaces, 2))
    # 4) Concatenar
    return func.concat(first_letter, rest)

def sql_transform_ssn(column):
    """
    Transforma un SSN en SQL.
    """
    return func.regexp_replace(column, '[^0-9]', '')

def sql_transform_date(column):
    """
    Transforma una fecha en SQL.
    """
    return func.date_format(column, '%Y-%m-%d')

def sql_transform_float(column):
    """
    Transforma un número de punto flotante en SQL.
    """
    return func.cast(column, Float)

def sql_transform_title_case(column):
    """
    Transforma un texto a formato Title Case en SQL.
    """
    # Reemplaza "_" por " "
    base = func.replace(column, '_', ' ')

    # Capitaliza la primera letra de cada palabra (hasta 2 palabras por simplicidad)
    return func.concat_ws(
        ' ',
        func.concat(
            func.upper(func.left(func.substring_index(base, ' ', 1), 1)),
            func.lower(func.substring(func.substring_index(base, ' ', 1), 2))
        ),
        func.if_(
            func.instr(base, ' '),
            func.concat(
                func.upper(func.left(func.substring_index(base, ' ', -1), 1)),
                func.lower(func.substring(func.substring_index(base, ' ', -1), 2))
            ),
            ''
        )
    )

def sql_transform_pass(column):
    """
    Transforma una contraseña en SQL.
    """
    return column

def create_hybrid_property(cf_column: str, prop_name: str, transform_function, sql_transform_function=None):
    """
    Crea una propiedad híbrida.
    """
    @hybrid_property
    def prop(self):
        return transform_function(getattr(self, cf_column))

    @prop.expression  # type: ignore
    def prop(cls):
        column = getattr(cls, cf_column)
        if sql_transform_function:
            return sql_transform_function(column).label(prop_name)
        else:
            return func.lower(func.trim(column)).label(prop_name)

    return prop

# Asignaciones directas con validaciones y transformaciones:
setattr(VTigerSalesOrderCF, 'saleswoman', create_hybrid_property('cf_2183', 'saleswoman', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'broker', create_hybrid_property('cf_2067', 'broker', VTigerSalesOrderCF.validText, sql_transform_pass))
setattr(VTigerSalesOrderCF, 'item_code', create_hybrid_property('cf_2035', 'item_code', VTigerSalesOrderCF.validItemCode, sql_transform_text))
setattr(VTigerSalesOrderCF, 'custom_ffm_app_id', create_hybrid_property('cf_2115', 'custom_ffm_app_id', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'custom_subscriber_id', create_hybrid_property('cf_2803', 'custom_subscriber_id', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'custom_app_review', create_hybrid_property('cf_2827', 'custom_app_review', VTigerSalesOrderCF.validText, sql_transform_title_case))
setattr(VTigerSalesOrderCF, 'custom_consent', create_hybrid_property('cf_2825', 'custom_consent', VTigerSalesOrderCF.validText, sql_transform_title_case))
setattr(VTigerSalesOrderCF, 'custom_renew', create_hybrid_property('cf_2829', 'custom_renew', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'custom_sales_person', create_hybrid_property('saleswoman', 'custom_sales_person', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'custom_sales_date', create_hybrid_property('cf_2179', 'custom_sales_date', VTigerSalesOrderCF.validDate, sql_transform_date))
setattr(VTigerSalesOrderCF, 'custom_digitizer', create_hybrid_property('cf_2257', 'custom_digitizer', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'transaction_date', create_hybrid_property('cf_2255', 'transaction_date', VTigerSalesOrderCF.validDate, sql_transform_date))
setattr(VTigerSalesOrderCF, 'delivery_date', create_hybrid_property('cf_2059', 'delivery_date', VTigerSalesOrderCF.validDate, sql_transform_date))
setattr(VTigerSalesOrderCF, 'custom_expiry_date', create_hybrid_property('cf_2193', 'custom_expiry_date', VTigerSalesOrderCF.validDate, sql_transform_date))
setattr(VTigerSalesOrderCF, 'rate', create_hybrid_property('cf_2033', 'rate', VTigerSalesOrderCF.validFloat, sql_transform_float))
setattr(VTigerSalesOrderCF, 'company', create_hybrid_property('cf_2069', 'company', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_person_1', create_hybrid_property('cf_1501', 'document_person_1', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_name_1', create_hybrid_property('cf_1515', 'document_name_1', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_person_2', create_hybrid_property('cf_1503', 'document_person_2', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_name_2', create_hybrid_property('cf_1517', 'document_name_2', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_person_3', create_hybrid_property('cf_1505', 'document_person_3', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_name_3', create_hybrid_property('cf_1519', 'document_name_3', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_person_4', create_hybrid_property('cf_1507', 'document_person_4', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_name_4', create_hybrid_property('cf_1521', 'document_name_4', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_person_5', create_hybrid_property('cf_1509', 'document_person_5', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_name_5', create_hybrid_property('cf_1523', 'document_name_5', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_status', create_hybrid_property('cf_1527', 'document_status', VTigerSalesOrderCF.validText, sql_transform_text))
setattr(VTigerSalesOrderCF, 'document_deadline', create_hybrid_property('cf_1513', 'document_deadline', VTigerSalesOrderCF.validDate, sql_transform_text))
