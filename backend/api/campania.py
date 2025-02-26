from fastapi import FastAPI, APIRouter, Depends, Query
from sqlalchemy import distinct, func, text
from models.database import get_db
from sqlalchemy.orm import Session
from models.ta_sms_maestro import TaSmsMaestro
from schemas.ta_sms_maestro import TaSmsMaestro as TaSmsMaestroSchema
from schemas.pagination import PaginatedResponse, PaginationParams
from utils.fecha import convertir_fecha
import datetime
from typing import Optional
from fastapi import HTTPException

ROUTE_NAME = 'campania'
"Campaña"

class CampaniaService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/list/')(self.list_campanias_fecha)#listar las campañas por fecha y paginacion
        self.api_router.get('/fechas')(self.obtener_fechas)#obtener todas las fechas distintas donde existen campañas
    
    async def list_campanias_fecha(
        self,
        fecha: datetime.datetime = Depends(convertir_fecha),
        page: int = Query(1, ge=1, description="Número de página"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
        db: Session = Depends(get_db)) -> PaginatedResponse[TaSmsMaestroSchema]:

        try:
            # Ejecutar la función get_campanias_by_fecha
            results = db.execute(
                text("""
                    SELECT * FROM get_campanias_by_fecha(:fecha, :page, :page_size);
                """),
                {
                    "fecha": fecha.date(),
                    "page": page,
                    "page_size": page_size
                }
            ).fetchall()

            # Verificar si hay resultados, si no hay, retornar lista vacía
            if not results:
                return PaginatedResponse(
                    items=[],
                    total=0,
                    page=page,
                    page_size=page_size,
                    total_pages=0
                )

            # Convertir los resultados a objetos TaSmsMaestro (en caso de que haya más registros)
            campanias = [
                TaSmsMaestro(
                    id=row[0],
                    nombre=row[1],
                    fecha=row[2],
                    estado=row[3],
                    descripcion=row[4]
                )
                for row in results
            ]

            # Asumimos que la primera fila contiene los datos de 'total_registros' y 'total_paginas'
            total_registros = results[0][5]  # total_registros
            total_paginas = results[0][6]    # total_paginas

            return PaginatedResponse(
                items=campanias,
                total=total_registros,
                page=page,
                page_size=page_size,
                total_pages=total_paginas
            )

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener campañas: {str(e)}"
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