from fastapi import FastAPI
from api.reporte import ReporteService

def setup_services(api_server: FastAPI):
    ReporteService(api_server)