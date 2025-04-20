from crmsync.config import SyncConfig
from pandas import DataFrame
from sqlalchemy import text

from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_property

import pandas as pd

from crmsync.database.models.vtigercrm_contactcf import VTigerContactsCF
from crmsync.database.models.vtigercrm_contactdetails import VTigerContactDetails
from crmsync.database.models.vtigercrm_crmentity import VTigerCRMEntity
from crmsync.database.models.vtigercrm_salesorder import VTigerSalesOrder
from crmsync.database.models.vtigercrm_salesordercf import VTigerSalesOrderCF

class QueryService:
    def __init__(self, config: SyncConfig):
        self.config = config
        
    def validate_connection(self, uow):
        result = uow.execute(text("SELECT VERSION();"))
        return result.fetchone()[0]
        
    def fetch_records(self, uow) -> DataFrame:
        joins = [
            (VTigerSalesOrder, VTigerSalesOrderCF.salesorderid == VTigerSalesOrder.salesorderid),
            (VTigerContactsCF, VTigerSalesOrder.contactid == VTigerContactsCF.contactid),
            (
                VTigerCRMEntity,
                and_(VTigerSalesOrder.salesorderid == VTigerCRMEntity.crmid, VTigerCRMEntity.deleted == 0),
            ),
            (VTigerContactDetails, VTigerSalesOrder.contactid == VTigerContactDetails.contactid),
        ]

        dynamic_columns = [
            getattr(VTigerSalesOrderCF, key)
            for key, value in VTigerSalesOrderCF.__dict__.items()
            if isinstance(value, hybrid_property)
        ]

        base_query = uow.query(
            VTigerSalesOrder.contactid, 
            *dynamic_columns,
            VTigerSalesOrderCF,
            VTigerContactsCF,
        ).select_from(VTigerSalesOrderCF)

        # Aplicar los JOINs de forma recursiva
        query = self.recursive_join(base_query, joins)

        # Aplicar los filtros según la lógica original
        query = (
            query.filter(VTigerSalesOrderCF.cf_2141.notin_(['Cancelación', 'Prospecto']))
            .filter(VTigerSalesOrderCF.cf_2059 >= '2025-01-01')
            .filter(VTigerSalesOrderCF.cf_2067 != 'Otro Broker')
            .limit(10)
        )

        # Ejecutar la consulta y mostrar los resultados
        return pd.read_sql(query.statement, uow.bind)
    
    def recursive_join(self, query, join_list):
        """
        Función recursiva que añade JOINs a la consulta.

        :param query: Consulta base.
        :param join_list: Lista de tuplas (modelo, condición de join).
        :return: Consulta con los JOINs aplicados.
        """
        if not join_list:
            return query
        model, condition = join_list[0]
        new_query = query.join(model, condition)
        return self.recursive_join(new_query, join_list[1:])
