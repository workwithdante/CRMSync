from database.models.vtigercrm_troubletickets import VTigerTroubleTickets
from database.models.vtigercrm_ticketcf import VTigerTicketCF
from crmsync.config import SyncConfig

from sqlalchemy import func, text

from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_property

from pandas import DataFrame
import pandas as pd

from crmsync.database.models.vtigercrm_contactcf import VTigerContactsCF
from crmsync.database.models.vtigercrm_contactdetails import VTigerContactDetails
from crmsync.database.models.vtigercrm_crmentity import VTigerCRMEntity
from crmsync.database.models.vtigercrm_salesorder import VTigerSalesOrder
from crmsync.database.models.vtigercrm_salesordercf import VTigerSalesOrderCF

class QueryService:
    """
    Servicio de consultas a la base de datos.
    """
    def __init__(self, config: SyncConfig):
        """
        Inicializa una nueva instancia de QueryService.

        Args:
            config (SyncConfig): Configuración de sincronización.
        """
        self.config = config
        
    def validate_connection(self, uow):
        """
        Valida la conexión a la base de datos.
        """
        result = uow.execute(text("SELECT VERSION();"))
        return result.fetchone()[0]

    def fetch_records(self, uow, offset_contacts: int = 0, limit_contacts: int = 1000) -> DataFrame:
        """
        Obtiene los registros de la base de datos.

        Args:
            uow: Unidad de trabajo.
            offset_contacts (int): Offset de los contactos.
            limit_contacts (int): Límite de los contactos.

        Returns:
            DataFrame: DataFrame con los registros.
        """
        # ----------- 0) JOIN definitions -----------
        joins = [
            (VTigerSalesOrder, VTigerSalesOrderCF.salesorderid == VTigerSalesOrder.salesorderid),
            (VTigerContactsCF, VTigerSalesOrder.contactid == VTigerContactsCF.contactid),
            (VTigerCRMEntity, and_(
                VTigerSalesOrder.salesorderid == VTigerCRMEntity.crmid,
                VTigerCRMEntity.deleted == 0
            )),
            (VTigerContactDetails, VTigerSalesOrder.contactid == VTigerContactDetails.contactid),
        ]

        # ----------- 1) Get valid contact IDs in Python -----------
        subquery = (
            uow.query(VTigerSalesOrder.contactid)
            .join(VTigerSalesOrderCF, VTigerSalesOrderCF.salesorderid == VTigerSalesOrder.salesorderid)
            .join(VTigerCRMEntity, and_(
                VTigerSalesOrder.salesorderid == VTigerCRMEntity.crmid,
                VTigerCRMEntity.deleted == 0
            ))
            .filter(VTigerSalesOrderCF.cf_2141.notin_(['Cancelación', 'Prospecto']))
            .filter(VTigerSalesOrderCF.cf_2059 >= '2025-01-01')
            .filter(VTigerSalesOrderCF.cf_2067 != 'Otro Broker')
            .filter(VTigerSalesOrder.contactid.isnot(None))  # muy importante
            .distinct()
            .subquery()
        )

        contact_query = (
            uow.query(subquery.c.contactid)
            .offset(offset_contacts)
            .limit(limit_contacts)
        )

        contact_ids = [row[0] for row in contact_query.all()]
        if not contact_ids:
            print("❌ No contact_ids encontrados.")
            return pd.DataFrame()

        # ----------- 2) Campos y columnas dinámicas -----------
        customer_name_col = func.concat_ws(
            ' ',
            VTigerContactDetails.firstname,
            func.nullif(func.trim(VTigerContactsCF.cf_1895), ''),
            VTigerContactDetails.lastname
        ).label('customer_name')

        dynamic_columns = [
            getattr(VTigerSalesOrderCF, k)
            for k, v in VTigerSalesOrderCF.__dict__.items()
            if isinstance(v, hybrid_property)
        ]

        # ----------- 3) Consulta principal -----------
        base_q = uow.query(
            customer_name_col,
            VTigerSalesOrder.salesorderid,
            VTigerSalesOrder.subject,
            VTigerSalesOrder.contactid.label("contact_id"),
            *dynamic_columns,
            VTigerSalesOrderCF,
            VTigerContactsCF,
        ).select_from(VTigerSalesOrderCF)

        q = self.recursive_join(base_q, joins)

        # ----------- 4) Filtrar por contactos válidos -----------
        q = q.filter(
            VTigerSalesOrder.contactid.in_(contact_ids),
            VTigerSalesOrderCF.cf_2141.notin_(['Cancelación','Prospecto']),
            VTigerSalesOrderCF.cf_2059.isnot(None),
        )

        # ----------- 5) Orden final -----------
        q = q.order_by(
            VTigerSalesOrderCF.cf_2059.desc(),
            VTigerCRMEntity.createdtime.asc()
        )

        # ----------- 6) Ejecutar y retornar -----------
        df = pd.read_sql(q.statement, uow.bind)
        #dfpd = self.clean_for_polars(dfpd)
        #df =pl.from_pandas(dfpd)
        print(f"✅ {len(df)} registros encontrados para {len(contact_ids)} contactos.")
        return df
        
    def recursive_join(self, query, join_list):
        """
        Función recursiva que añade JOINs a la consulta.

        Args:
            query: Consulta base.
            join_list: Lista de tuplas (modelo, condición de join).

        Returns:
            Consulta con los JOINs aplicados.
        """
        if not join_list:
            return query
        model, condition = join_list[0]
        new_query = query.join(model, condition)
        return self.recursive_join(new_query, join_list[1:])
    
    def fetch_issues(self, uow, contact_id) -> DataFrame:
        """
        Obtiene todos los tickets de problemas (issues) para un contact_id dado.

        Args:
            uow: Unidad de trabajo.
            contact_id: ID del contacto.

        Returns:
            DataFrame: DataFrame con ticket_id, status, title, created_time, description, solution.
        """
        # Build query directly from troubletickets and crmentity
        q = (
            uow.query(
                VTigerTroubleTickets.ticketid.label("ticket_id"),
                VTigerTroubleTickets.status,
                VTigerTroubleTickets.title,
                VTigerCRMEntity.createdtime.label("created_time"),
                VTigerCRMEntity.description,
                VTigerTroubleTickets.solution,
                VTigerTicketCF.cf_1987.label("custom_field_1987")
            )
            .select_from(VTigerTroubleTickets)
            .join(
                VTigerTicketCF,
                VTigerTicketCF.ticketid == VTigerTroubleTickets.ticketid
            )
            .join(
                VTigerCRMEntity,
                (VTigerCRMEntity.crmid == VTigerTroubleTickets.ticketid) &
                (VTigerCRMEntity.deleted == 0)
            )
            .filter(VTigerTroubleTickets.contact_id == contact_id)
            .order_by(VTigerCRMEntity.createdtime.asc())
        )

        df = pd.read_sql(q.statement, uow.bind)
        #dfpd = self.clean_for_polars(dfpd)
        #df =pl.from_pandas(dfpd)
        print(f"✅ {len(df)} issues found for contact {contact_id}.")
        return df

    def clean_for_polars(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia el DataFrame para usar con Polars.
        """
        return df.astype(str)
