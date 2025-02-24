from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base para todos los modelos
Base = declarative_base()

# Aquí iría la URL de tu base de datos (por ejemplo, PostgreSQL, MySQL, SQLite, etc.)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"  # Ejemplo con SQLite

# Creando el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creando la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
