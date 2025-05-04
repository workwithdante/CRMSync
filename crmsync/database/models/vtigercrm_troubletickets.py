from sqlalchemy import MetaData

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_troubletickets'])


class VTigerTroubleTickets(Base):
    """
    Modelo para la tabla vtiger_troubletickets.
    """
    __table__ = metadata.tables['vtiger_troubletickets']
