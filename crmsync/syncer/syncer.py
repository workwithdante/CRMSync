from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from syncer.assembler.policy import PolicyAssembler
from syncer.assembler.resolvers.simple_name import SimpleNameResolver
from tqdm import tqdm

from crmsync.config import SyncConfig
from database.services.query import QueryService
from crmsync.config.logging import setup_logging
from database.unit_of_work import UnitOfWork
from sqlalchemy.orm import sessionmaker
from crmsync.database.engine import get_engine

class Syncer:
    """
    Sincronizador principal.

    Esta clase coordina la sincronización de datos desde VTigerCRM a ERPNext.
    """
    def __init__(self):
        """
        Inicializa el Syncer.

        Configura el motor de base de datos, los servicios de consulta y la unidad de trabajo.
        """
        engine = get_engine()
        if not engine:
            raise RuntimeError("Could not create engine")
        self.config = SyncConfig()
        self.query_service = QueryService(self.config)
        self.unit_of_work = UnitOfWork(lambda: sessionmaker(bind=engine)())
        self.max_workers = 13 #self.config.max_workers
 
    def sync(self):
        """
        Ejecuta el proceso de sincronización.

        Este método realiza la sincronización de datos en varios pasos:
        1. Obtiene los registros de VTigerCRM.
        2. Agrupa los registros por ID de contacto.
        3. Procesa cada grupo de contactos en paralelo.
        """
        logger = setup_logging()
        try:
            # 1) Fetch records una vez y agrupa
            df = None
            with self.unit_of_work as uow:
                version = self.query_service.validate_connection(uow)
                logger.info(f"Conectado a VTigerCRM (versión {version})")
                df = self.query_service.fetch_records(uow)

            groups = [
                (contact_id, group.copy())
                for contact_id, group in df.groupby("contact_id")
            ]
            
            valid_names = [
                "American Express Company",
                "Discover Financial Services",
                "Mastercard Incorporated",
                "Visa Inc",
                "FirstBank",
                "Citibank",
                "Citizens Bank",
                "M&T Bank",
                "Fifth Third Bank",
                "TD Bank",
                "Regions Bank",
                "Truist Bank",
                "PNC Bank",
                "U.S. Bank",
                "Bank of America",
                "Wells Fargo Bank",
                "Chase Bank",
            ]

            parser_bank = SimpleNameResolver(valid_names=valid_names)

            # 2) Ejecuta en paralelo
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_cid = {
                    executor.submit(self._process_contact, cid, grp, parser_bank): cid
                    for cid, grp in groups
                }
                for future in tqdm(as_completed(future_to_cid),
                                   total=len(future_to_cid),
                                   desc="Procesando contactos"):
                    cid = future_to_cid[future]
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Fallo en contacto {cid}: {e}")

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
        return True

    def _process_contact(self, contact_id, rows, parser_bank):
        """
        Procesa un único contacto.

        Este método ensambla los datos del contacto utilizando PolicyAssembler.

        Args:
            contact_id: ID del contacto.
            rows: Filas de datos para el contacto.
            parser_bank: Resolvedor de nombres de bancos.
        """
        # 1) Obtén el nombre de hilo
        thread_name = threading.current_thread().name

        # 2) Imprime con tqdm.write
        tqdm.write(f"[{thread_name}] ⏱ Emsablando customer {contact_id}")

        # 3) Tu lógica
        assembler = PolicyAssembler(self.config, parser_bank)
        assembler.assemble(contact_id, rows)

    def recursive_join(self, query, join_list):
        """
        Realiza un JOIN recursivo en una consulta SQLAlchemy.

        Args:
            query: La consulta base.
            join_list: Una lista de tuplas, donde cada tupla contiene un modelo y una condición de JOIN.

        Returns:
            La consulta con los JOINs aplicados.
        """
        if not join_list:
            return query
        model, condition = join_list[0]
        new_query = query.join(model, condition)
        return self.recursive_join(new_query, join_list[1:])
