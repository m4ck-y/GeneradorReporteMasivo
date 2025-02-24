from fastapi import FastAPI, APIRouter, Depends, HTTPException
from utils.fecha import convertir_fecha
import datetime
from models.database import get_db
from tasks.report_generator import ReportGenerator

ROUTE_NAME = 'reporte'

class ReporteService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/')(self.reporte)

    async def reporte(self,fecha: datetime.datetime = Depends(convertir_fecha)):
        "Genera un reporte CSV de todas las campañas en una fecha específica"

        try:
            report_generator = ReportGenerator(get_db())
            file_path = report_generator.generate_by_date(fecha)
            return {"reporte generado": file_path}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))