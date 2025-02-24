from fastapi import FastAPI
from api.reporte import ReporteService
from api.campania import CampaniaService

def setup_services(api_server: FastAPI):
    ReporteService(api_server)
    CampaniaService(api_server)