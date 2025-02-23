import datetime
from fastapi import Depends, FastAPI, Query
from utils.fecha import convertir_fecha


app = FastAPI()

@app.get("/reporte")
def reporte(fecha: datetime.datetime = Depends(convertir_fecha)):
    return {"obtener reporte": fecha}