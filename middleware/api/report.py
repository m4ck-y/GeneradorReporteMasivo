from pathlib import Path
import csv

from sqlalchemy import text
from models.database import get_db
from datetime import datetime
from models.report_status import ReporteEstado
from models.ta_sms_detalle import TaSmsDetalle
from models.ta_sms_maestro import TaSmsMaestro
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query

ROUTE_NAME = "reporte"

class ReportService:
    def __init__(self, api_server: FastAPI):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

        self.api_router = APIRouter(prefix="/report")
        self.setup_routes()
        api_server.include_router(self.api_router)

    def setup_routes(self):
        self.api_router.post("/")(self.procesar_reportes)

    def obtener_maestros_sin_reporte(self,fecha:datetime, db:Session = Depends(get_db)):

        try:
            results = db.execute(
                text("""
            SELECT * FROM obtener_maestros_sin_reporte(:fecha);
            """), {'fecha': fecha}
            ).fetchall()

            return results

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener campañas: {str(e)}"
            )
        
    def obtener_detalles_maestro(self, id_maestro, db:Session = Depends(get_db)):
        detalles = db.query(TaSmsDetalle.id, TaSmsDetalle.mensaje, TaSmsDetalle.estado) \
            .filter(TaSmsDetalle.id_maestro == id_maestro) \
            .all()
        
        return detalles
    def generar_csv(self, maestro, detalles, db:Session = Depends(get_db)):
        archivo = f"{maestro.nombre}_{maestro.fecha}.csv"  # Usamos el nombre y la fecha para el archivo
        with open(archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID Detalle', 'Mensaje', 'Estado'])  # Encabezados del CSV
            for detalle in detalles:
                writer.writerow([detalle[0], detalle[1], detalle[2]])  # Escribir detalles
        return archivo
    
    def procesar_reportes(self, fecha):
        # Obtener los maestros sin reporte generado
        maestros = self.obtener_maestros_sin_reporte(fecha)

        for maestro in maestros:
            # Obtener los detalles de cada maestro
            detalles = self.obtener_detalles_maestro(maestro.id)  # maestro.id es el ID del maestro
            # Generar el archivo CSV para este maestro
            archivo_csv = self.generar_csv(maestro, detalles)
            
            
            # Registrar o actualizar el estado del reporte en la base de datos
            self.registrar_reporte(maestro.id, maestro.fecha, archivo_csv)
        
            print(f"Reporte CSV generado y registrado en reporte_estado: {archivo_csv}")


    def registrar_reporte(self, id_campana: int, fecha: str, ruta_archivo: str, session: Session = Depends(get_db)):
        # Verificar si ya existe un reporte para esta campaña y fecha
        reporte = session.query(ReporteEstado).filter_by(id_campana=id_campana, fecha=fecha).first()

        if reporte:
            # Si el reporte ya existe, actualizamos el estado y la ruta del archivo
            reporte.estado = 'Completado'  # O el estado que corresponda
            reporte.ruta_archivo = ruta_archivo
        else:
            # Si no existe, creamos un nuevo registro en la tabla reporte_estado
            reporte = ReporteEstado(
                id_campana=id_campana,
                fecha=fecha,
                estado='Completado',
                ruta_archivo=ruta_archivo
            )
            session.add(reporte)

        # Guardar los cambios en la base de datos
        session.commit()