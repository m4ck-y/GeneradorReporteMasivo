from fastapi import FastAPI
from api.reporte import ReporteService
from api.campania import CampaniaService
from fastapi.middleware.cors import CORSMiddleware

def setup_services(api_server: FastAPI):
    ReporteService(api_server)
    CampaniaService(api_server)

    # Definir las configuraciones de CORS
    api_server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todos los orígenes. Puedes poner una lista con orígenes específicos, por ejemplo: ["https://tusitio.com"]
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Permite todos los encabezados
    )