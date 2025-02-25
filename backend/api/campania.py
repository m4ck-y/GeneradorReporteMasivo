from fastapi import FastAPI, APIRouter, Depends, Query
from sqlalchemy import distinct, func
from models.database import get_db
from sqlalchemy.orm import Session
from models.ta_sms_maestro import TaSmsMaestro
from schemas.ta_sms_maestro import TaSmsMaestro as TaSmsMaestroSchema
from schemas.pagination import PaginatedResponse, PaginationParams
from utils.fecha import convertir_fecha
import datetime
from typing import Optional

ROUTE_NAME = 'campania'
"Campaña"

class CampaniaService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/list')(self.list_campanias)
        self.api_router.get('/list/')(self.list_campanias_fecha)
        self.api_router.get('/fechas')(self.obtener_fechas)

    async def list_campanias(self, db: Session = Depends(get_db)):
        return db.query(TaSmsMaestro).all()
    
    async def list_campanias_fecha(
        self,
        fecha: datetime.datetime = Depends(convertir_fecha),
        page: int = Query(1, ge=1, description="Número de página"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
        db: Session = Depends(get_db)
    ) -> PaginatedResponse[TaSmsMaestroSchema]:
        # Calcular offset para paginación
        offset = (page - 1) * page_size

        # Query base filtrada por fecha
        base_query = db.query(TaSmsMaestro).filter(
            TaSmsMaestro.fecha == fecha.date()
        )

        # Obtener total de registros para esta fecha
        total = base_query.count()

        # Obtener registros paginados
        campanias = base_query\
            .order_by(TaSmsMaestro.id)\
            .offset(offset)\
            .limit(page_size)\
            .all()

        # Calcular total de páginas
        total_pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=campanias,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def obtener_fechas(self, db: Session = Depends(get_db)):
        """Obtiene todas las fechas distintas donde existen campañas"""
        fechas = db.query(distinct(TaSmsMaestro.fecha))\
                  .order_by(TaSmsMaestro.fecha.desc())\
                  .all()
        
        # Convertir las fechas a formato ISO para JSON
        fechas_formateadas = [
            fecha[0].strftime("%Y/%m/%d") 
            for fecha in fechas
        ]
        
        return {
            "fechas": fechas_formateadas,
            "total": len(fechas_formateadas)
        }