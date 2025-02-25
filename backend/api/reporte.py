from fastapi import FastAPI, APIRouter, Depends, HTTPException, BackgroundTasks
from utils.fecha import convertir_fecha
import datetime
from models.database import get_db
from sqlalchemy.orm import Session
from tasks.report_generator import ReportGenerator
from models.report_status import ReporteEstado
from models.ta_sms_maestro import TaSmsMaestro
from sqlalchemy import and_

ROUTE_NAME = 'reporte'

class ReporteService:

    def __init__(self, api_server: FastAPI):
        self.api_router = APIRouter(prefix=f'/{ROUTE_NAME}')
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.get('/')(self.reporte)
        self.api_router.get('/status/{id_campana}')(self.get_report_status)

    async def process_campaign_report(self, db: Session, campana_id: int, fecha: datetime.date):
        """Procesa el reporte de una campaña específica en segundo plano"""
        try:
            # Actualizar estado a EN PROCESO
            reporte_estado = db.query(ReporteEstado).filter(
                and_(
                    ReporteEstado.id_campana == campana_id,
                    ReporteEstado.fecha == fecha
                )
            ).first()

            if not reporte_estado:
                return

            reporte_estado.estado = "EN PROCESO"
            db.commit()

            # Generar reporte
            report_generator = ReportGenerator(db)
            file_path = report_generator.generate_by_campaign(campana_id)

            # Actualizar estado a COMPLETADO
            reporte_estado.estado = "COMPLETADO"
            reporte_estado.ruta_archivo = file_path
            db.commit()

        except Exception as e:
            # En caso de error, actualizar estado
            if reporte_estado:
                reporte_estado.estado = "ERROR"
                db.commit()
            print(f"Error procesando reporte para campaña {campana_id}: {str(e)}")

    async def reporte(
        self,
        fecha: datetime.datetime = Depends(convertir_fecha),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        db: Session = Depends(get_db)
    ):
        """Genera reportes CSV para todas las campañas en una fecha específica"""
        try:
            # Buscar campañas de la fecha
            campanias = db.query(TaSmsMaestro).filter(
                TaSmsMaestro.fecha == fecha.date()
            ).all()


            print("generando reportes para:", len(campanias))

            if not campanias:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontraron campañas para la fecha {fecha.date()}"
                )

            # Crear registros de estado para cada campaña
            reportes_estado = []
            for campana in campanias:
                reporte_estado = ReporteEstado(
                    id_campana=campana.id,
                    fecha=fecha.date(),
                    estado="PENDIENTE"
                )
                reportes_estado.append(reporte_estado)

            print("for done")

            db.add_all(reportes_estado)
            db.commit()

            print("commited all")

            # Agregar tareas en segundo plano para cada campaña
            for campana in campanias:
                print("agregando tarea para:", campana.id)
                background_tasks.add_task(
                    self.process_campaign_report,
                    db,
                    campana.id,
                    fecha.date()
                )

            return {
                "mensaje": f"Generación de reportes iniciada para {len(campanias)} campañas",
                "campanias": [
                    {
                        "id": c.id,
                        "nombre": c.nombre,
                        "estado": "PENDIENTE"
                    } for c in campanias
                ]
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_report_status(self, id_campana: int, db: Session = Depends(get_db)):
        """Obtiene el estado actual del reporte de una campaña"""
        reporte = db.query(ReporteEstado).filter(
            ReporteEstado.id_campana == id_campana
        ).order_by(ReporteEstado.timestamp.desc()).first()

        if not reporte:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró reporte para la campaña {id_campana}"
            )

        return {
            "id_campana": reporte.id_campana,
            "estado": reporte.estado,
            "fecha": reporte.fecha,
            "ruta_archivo": reporte.ruta_archivo if reporte.estado == "COMPLETADO" else None
        }