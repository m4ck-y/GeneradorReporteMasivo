from fastapi import FastAPI
from api.reporte import ReporteService
from api.campania import CampaniaService
from fastapi.middleware.cors import CORSMiddleware

def setup_services(api_server: FastAPI):
    ReporteService(api_server)
    CampaniaService(api_server)

    # Configuraciones de CORS
    api_server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )