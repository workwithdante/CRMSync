from crmsync.config import SyncConfig
from database.services.query import QueryService
from tqdm import tqdm

from syncer.policy_assembler import PolicyAssembler
from crmsync.config.logging import setup_logging


from database.unit_of_work import UnitOfWork
from sqlalchemy.orm import sessionmaker
from crmsync.database.engine import get_engine



class Syncer:
    def __init__(self):
        engine = get_engine()
        
        if not engine:
            return False
        
        self.config = SyncConfig()
        self.query_service = QueryService(self.config)
        self.unit_of_work = UnitOfWork(lambda: sessionmaker(bind=engine)())

    def sync(self):
        try:
            with self.unit_of_work as uow:
                logger = setup_logging()
                version = self.query_service.validate_connection(uow)
                logger.info(f"Successfully connected to VTigerCRM. Engine version: {version}")
                
                df = self.query_service.fetch_records(uow)

                for _, row in tqdm(df.iterrows(), total=df.shape[0]):
                    row_filter = row[row != '']
                    PolicyAssembler(self.config, row_filter)
        except Exception as e:
            print(f"Error: {e}")
            return False

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
