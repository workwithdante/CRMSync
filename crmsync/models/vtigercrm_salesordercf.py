import json
import os
import re

from sqlalchemy import MetaData, func
from sqlalchemy.ext.hybrid import hybrid_property

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_salesordercf'])


class VTigerSalesOrderCF(Base):
    __table__ = metadata.tables['vtiger_salesordercf']

    @staticmethod
    def validText(text: str | None) -> str | None:
        if text:
            return text.strip().capitalize()
        return None

    @staticmethod
    def validGender(gender: str | None) -> str | None:
        if gender:
            return gender.strip().capitalize()
        return None

    @staticmethod
    def validSSN(ssn: str | None) -> str | None:
        if ssn:
            return re.sub(r'\D', '', ssn)
        return None


# Funciones de transformación SQL para MariaDB


def sql_transform_text(column):
    """
    Simula el método capitalize: quita espacios y convierte la primera letra a mayúsculas
    y el resto a minúsculas.
    """
    return func.concat(func.upper(func.left(func.trim(column), 1)), func.lower(func.substring(func.trim(column), 2)))


def sql_transform_ssn(column):
    """
    Elimina todos los caracteres que no sean dígitos.
    En MariaDB, REGEXP_REPLACE está disponible en las últimas versiones.
    """
    return func.regexp_replace(column, '[^0-9]', '')


def create_hybrid_property(cf_column: str, prop_name: str, transform_function, sql_transform_function=None):
    @hybrid_property
    def prop(self):
        # Se aplica la transformación en Python al acceder a la propiedad en la instancia
        return transform_function(getattr(self, cf_column))

    @prop.expression  # type: ignore
    def prop(cls):
        # Se obtiene la columna correspondiente
        column = getattr(cls.__table__.c, cf_column)
        # Se aplica la transformación SQL si se provee
        if sql_transform_function is not None:
            return sql_transform_function(column).label(prop_name)
        # Valor por defecto
        return func.lower(func.trim(column)).label(prop_name)

    return prop


# Asignación dinámica para propiedades de texto (saleswoman y broker)
setattr(
    VTigerSalesOrderCF,
    'saleswoman',
    create_hybrid_property('cf_2183', 'saleswoman', VTigerSalesOrderCF.validText, sql_transform_text),
)
setattr(
    VTigerSalesOrderCF,
    'broker',
    create_hybrid_property('cf_2067', 'broker', VTigerSalesOrderCF.validText, sql_transform_text),
)

# Cargar el JSON para asignar dinámicamente los campos de género y SSN
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "mapping_salesordercf.json")
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

    # Generar listas de tuplas: (nombre_propiedad, columna) según el JSON
    gender_columns = [("gender_{}".format(i), item["gender"]) for i, item in enumerate(data)]
    ssn_columns = [("ssn_{}".format(i), item["ssn"]) for i, item in enumerate(data)]

    # Asignar dinámicamente las propiedades de género con transformación SQL para texto
    for prop_name, cf_column in gender_columns:
        setattr(
            VTigerSalesOrderCF,
            prop_name,
            create_hybrid_property(cf_column, prop_name, VTigerSalesOrderCF.validGender, sql_transform_text),
        )

    # Asignar dinámicamente las propiedades de SSN con transformación SQL para SSN
    for prop_name, cf_column in ssn_columns:
        setattr(
            VTigerSalesOrderCF,
            prop_name,
            create_hybrid_property(cf_column, prop_name, VTigerSalesOrderCF.validSSN, sql_transform_ssn),
        )
