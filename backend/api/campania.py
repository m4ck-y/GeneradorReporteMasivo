from fastapi import FastAPI, APIRouter, Depends
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

    async def list_capanias(self, db: Session = Depends(get_db)):
        return db.query(TaSmsMaestro).all()