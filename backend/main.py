import datetime
from fastapi import Depends, FastAPI
from utils.fecha import convertir_fecha
from models.database import Base, engine
from models.ta_sms_detalle import TaSmsDetalle
from models.ta_sms_maestro import TaSmsMaestro

app = FastAPI()

@app.get("/reporte")
def reporte(fecha: datetime.datetime = Depends(convertir_fecha)):
    return {"obtener reporte": fecha}

Base.metadata.create_all(bind=engine)