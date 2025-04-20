from sqlalchemy import MetaData

from crmsync.database.base import Base
from crmsync.database.engine import get_engine

metadata = MetaData()
metadata.reflect(bind=get_engine(), only=['vtiger_crmentity'])


class VTigerCRMEntity(Base):
    __table__ = metadata.tables['vtiger_crmentity']
