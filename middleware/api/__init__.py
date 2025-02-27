from fastapi import FastAPI
from api.report import ReportService
from fastapi.middleware.cors import CORSMiddleware

def setup_services(api_server: FastAPI):
    ReportService(api_server)

    # Configuraciones de CORS
    api_server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )