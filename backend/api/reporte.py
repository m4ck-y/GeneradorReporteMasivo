from fastapi import FastAPI, APIRouter, Depends
from utils.fecha import convertir_fecha
import datetime

ROUTE_NAME = 'reporte'

class ReporteService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/')(self.reporte)

    async def reporte(self,fecha: datetime.datetime = Depends(convertir_fecha)):
        return {"obtener reporte": fecha}