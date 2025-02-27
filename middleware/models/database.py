from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener las variables de entorno
BD_NAME = os.getenv("BD_NAME")
BD_USER = os.getenv("BD_USER")
BD_PASS = os.getenv("BD_PASS")
BD_PORT = os.getenv("BD_PORT")
BD_HOST = os.getenv("BD_HOST")

# Base para todos los modelos
Base = declarative_base()

# Conexión para PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{BD_USER}:{BD_PASS}@{BD_HOST}:{BD_PORT}/{BD_NAME}"

print("URL:", SQLALCHEMY_DATABASE_URL)

# Creando el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Creando la sesión de la base de datos
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
