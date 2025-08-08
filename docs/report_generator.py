import csv
import os
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.ta_sms_maestro import TaSmsMaestro
from models.ta_sms_detalle import TaSmsDetalle
import threading
from pathlib import Path

# Número máximo de reintentos permitidos
MAX_RETRIES = 3

# Lock para evitar que dos hilos procesen la misma tarea simultáneamente
task_lock = threading.Lock()

class ReportGenerator:
    def __init__(self, db: Session):
        self.db = db
        # Crear directorio para reportes si no existe
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def generate_campaign_report(self, campaign_id: int) -> str:
        """
        Genera un reporte CSV para una campaña específica
        Retorna: Path del archivo generado
        """
        # Obtener información de la campaña
        campaign = self.db.query(TaSmsMaestro).filter(TaSmsMaestro.id == campaign_id).first()
        if not campaign:
            raise ValueError(f"No se encontró la campaña con ID {campaign_id}")

        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"campaign_{campaign_id}_{timestamp}.csv"
        filepath = self.reports_dir / filename

        # Obtener detalles de la campaña
        details = self.db.query(TaSmsDetalle).filter(
            TaSmsDetalle.id_maestro == campaign_id
        ).yield_per(1000)  # Procesar en lotes de 1000

        # Escribir el archivo CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezado del reporte
            writer.writerow([
                "ID Campaña", "Nombre Campaña", "Fecha Campaña", 
                "Estado Campaña", "Teléfono", "Mensaje", 
                "Fecha Envío", "Estado Mensaje", "Error"
            ])
            
            # Escribir detalles
            for detail in details:
                writer.writerow([
                    campaign.id,
                    campaign.nombre,
                    campaign.fecha.strftime("%Y-%m-%d"),
                    campaign.estado,
                    detail.mensaje,
                    detail.estado,
                ])

        return str(filepath)

    def generate_date_report(self, date: datetime.date) -> list[str]:
        """
        Genera reportes CSV para todas las campañas de una fecha específica
        Retorna: Lista de paths de los archivos generados
        """
        # Obtener todas las campañas de la fecha
        campaigns = self.db.query(TaSmsMaestro).filter(
            TaSmsMaestro.fecha == date
        ).all()

        generated_files = []
        for campaign in campaigns:
            try:
                filepath = self.generate_campaign_report(campaign.id)
                generated_files.append(filepath)
            except Exception as e:
                print(f"Error generando reporte para campaña {campaign.id}: {str(e)}")

        return generated_files

    def generate_summary_report(self, date: datetime.date) -> str:
        """
        Genera un reporte resumen de todas las campañas de una fecha
        Retorna: Path del archivo generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{date.strftime('%Y%m%d')}_{timestamp}.csv"
        filepath = self.reports_dir / filename

        # Obtener estadísticas de las campañas
        campaigns = self.db.query(TaSmsMaestro).filter(
            TaSmsMaestro.fecha == date
        ).all()

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir encabezado
            writer.writerow([
                "ID Campaña", "Nombre", "Estado",
                "Total Mensajes", "Enviados", "Pendientes", "Fallidos"
            ])
            
            # Escribir estadísticas de cada campaña
            for campaign in campaigns:
                details = self.db.query(TaSmsDetalle).filter(
                    TaSmsDetalle.id_maestro == campaign.id
                )
                
                total = details.count()
                enviados = details.filter(TaSmsDetalle.estado == 'ENVIADO').count()
                pendientes = details.filter(TaSmsDetalle.estado == 'PENDIENTE').count()
                fallidos = details.filter(TaSmsDetalle.estado == 'FALLIDO').count()

                writer.writerow([
                    campaign.id,
                    campaign.nombre,
                    campaign.estado,
                    total,
                    enviados,
                    pendientes,
                    fallidos
                ])

        return str(filepath)