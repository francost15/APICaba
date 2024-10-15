import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Actualiza la URL de la base de datos con tus credenciales
DATABASE_URL = "mysql+mysqlconnector://uvp:Francost15@20.169.80.178:3306/shop_limpieza"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funciones para conectar y desconectar la base de datos con mensajes de registro
async def connect_db():
    try:
        await database.connect()
        logger.info("Conexión a la base de datos exitosa.")
        return True
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return False

async def disconnect_db():
    try:
        await database.disconnect()
        logger.info("Desconexión de la base de datos exitosa.")
    except Exception as e:
        logger.error(f"Error al desconectar de la base de datos: {e}")