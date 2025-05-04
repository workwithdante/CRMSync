from sqlalchemy import MetaData

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_ticketcf'])


class VTigerTicketCF(Base):
    """
    Modelo para la tabla vtiger_ticketcf.
    """
    __table__ = metadata.tables['vtiger_ticketcf']
