from sqlalchemy import MetaData

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_salesorder'])


class VTigerSalesOrder(Base):
    __table__ = metadata.tables['vtiger_salesorder']
