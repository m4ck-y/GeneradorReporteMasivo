import csv
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from models.ta_sms_maestro import TaSmsMaestro
from models.ta_sms_detalle import TaSmsDetalle
from fastapi import HTTPException

class ReportGenerator:
    def __init__(self, db: Session):
        self.db = db
        # Crear directorio para reportes si no existe
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def generate_by_date(self, date: datetime.date) -> str:
        """
        Genera un reporte CSV con todas las campañas de una fecha específica
        """
        try:
            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_date_{date.strftime('%Y%m%d')}_{timestamp}.csv"
            filepath = self.reports_dir / filename

            print("Buscando campañas para la fecha", date)

            # Obtener campañas de la fecha
            campaigns = self.db.query(TaSmsMaestro).filter(
                TaSmsMaestro.fecha == date
            ).all()

            if not campaigns:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontraron campañas para la fecha {date.strftime('%Y-%m-%d')}"
                )

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir encabezado
                writer.writerow([
                    "ID Campaña", "Nombre Campaña", "Estado Campaña",
                    "Total Mensajes", "Enviados", "Pendientes", "Fallidos"
                ])
                
                # Escribir datos de cada campaña
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

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generando reporte por fecha: {str(e)}"
            )

    def generate_by_campaign(self, campaign_id: int) -> str:
        """
        Genera un reporte CSV con los detalles de una campaña específica
        """
        try:
            # Obtener información de la campaña
            campaign = self.db.query(TaSmsMaestro).filter(
                TaSmsMaestro.id == campaign_id
            ).first()

            if not campaign:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró la campaña con ID {campaign_id}"
                )

            # Crear nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_campaign_{campaign_id}_{timestamp}.csv"
            filepath = self.reports_dir / filename

            # Obtener detalles de la campaña
            details = self.db.query(TaSmsDetalle).filter(
                TaSmsDetalle.id_maestro == campaign_id
            ).all()

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir encabezado
                writer.writerow([
                    "ID Campaña", "Nombre Campaña", "Fecha Campaña",
                    "Mensaje", "Estado Mensaje"
                ])
                
                # Escribir detalles
                for detail in details:
                    writer.writerow([
                        campaign.id,
                        campaign.nombre,
                        campaign.fecha.strftime("%Y-%m-%d"),
                        detail.mensaje,
                        detail.estado
                    ])

            return str(filepath)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generando reporte de campaña: {str(e)}"
            )