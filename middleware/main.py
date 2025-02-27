import datetime
from fastapi import Depends, FastAPI
from models.database import Base, engine
from models.ta_sms_detalle import TaSmsDetalle
from models.ta_sms_maestro import TaSmsMaestro
from models.report_status import ReporteEstado
from api import setup_services
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()
setup_services(app)
Base.metadata.create_all(bind=engine)