# Import Frappe framework for configuration access
# Import SQLAlchemy engine creation function
from sqlalchemy import create_engine

from crmsync.config import SyncConfig
from crmsync.config.logging import setup_logging

# Import Frappe framework for configuration access
# Import SQLAlchemy engine creation function
from sqlalchemy import create_engine

from crmsync.config import SyncConfig
from crmsync.config.logging import setup_logging

conf = SyncConfig()
engine = None

def get_engine():
    """
    Obtiene el motor de SQLAlchemy.

    Crea y devuelve un motor de SQLAlchemy basado en la configuración.
    """
    global engine
    if engine:
        return engine
    """
    Crea y devuelve un motor de SQLAlchemy basado en la configuración de Frappe.
    """
    # Obtener detalles de conexión a la base de datos desde la configuración de Frappe

    db_user = conf.user
    db_password = conf.password
    db_host = conf.host
    db_port = conf.port
    db_name = conf.name_db
    db_type = conf.type
    db_conn = conf.connector
    logger = setup_logging()

    # Construir la cadena de conexión MySQL
    if all([db_user, db_password, db_host, db_port, db_name]):
        connection_string = f"{db_type}+{db_conn}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"  # noqa: E231
    else:
        logger.error("Faltan detalles de conexión para VTigerCRM.")
        connection_string = None

    # Crear el motor de SQLAlchemy con configuraciones de pooling
    if connection_string:
        try:
            engine = create_engine(
                connection_string,
                pool_pre_ping=True,  # Verificar la conexión antes de usarla
                pool_timeout=30,  # Tiempo de espera de la conexión en segundos
                pool_recycle=3600,  # Reciclar conexiones después de 1 hora
                connect_args={"connect_timeout": 10},  # Tiempo de espera de conexión MySQL
            )
            logger.info(f"Se crea el motor de SQLAlchemy con la cadena de conexión: {connection_string}")
            return engine
        except Exception as e:
            logger.error(f"Error al crear el motor de SQLAlchemy: {e}")
            return None
    else:
        logger.error("No se pudo construir la cadena de conexión. El motor no se creó.")
        return None
