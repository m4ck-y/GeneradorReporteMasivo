from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import distinct
from models.database import get_db
from sqlalchemy.orm import Session
from models.ta_sms_maestro import TaSmsMaestro
from utils.fecha import convertir_fecha
import datetime

ROUTE_NAME = 'campania'

class CampaniaService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/list')(self.list_capanias)
        self.api_router.get('/fechas')(self.obtener_fechas)

    async def list_capanias(self, db: Session = Depends(get_db)):
        return db.query(TaSmsMaestro).all()
    
    async def obtener_fechas(self, db: Session = Depends(get_db)):
        """Obtiene todas las fechas distintas donde existen campañas"""
        fechas = db.query(distinct(TaSmsMaestro.fecha))\
                  .order_by(TaSmsMaestro.fecha.desc())\
                  .all()
        
        # Convertir las fechas a formato ISO para JSON
        fechas_formateadas = [
            fecha[0].strftime("%Y-%m-%d") 
            for fecha in fechas
        ]
        
        return {
            "fechas": fechas_formateadas,
            "total": len(fechas_formateadas)
        }