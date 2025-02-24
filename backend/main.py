import datetime
from fastapi import Depends, FastAPI
from utils.fecha import convertir_fecha
from models.database import Base, engine
from models.ta_sms_detalle import TaSmsDetalle
from models.ta_sms_maestro import TaSmsMaestro
from models.report_status import ReporteEstado
from api import setup_services

app = FastAPI()
setup_services(app)
Base.metadata.create_all(bind=engine)