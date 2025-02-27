from sqlalchemy import Column, Integer, String, DateTime, Date, func
from models.database import Base

class ReporteEstado(Base):
    """
    Modelo para la tabla 'reporte_estado' que almacena el estado de los reportes generados para cada campaña.
    """
    __tablename__ = 'reporte_estado'  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_campana = Column(Integer, nullable=False)

    # fecha: Fecha de ta_sms_maestro (formato YYYY-MM-DD)//pasado como parametro desde el front
    fecha = Column(Date, nullable=False)

    # estado: Estado actual del reporte. Puede ser "Pendiente", "En proceso", "Completado" o "Error"
    estado = Column(String(50), nullable=False)

    ruta_archivo = Column(String(255), nullable=True)

    timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())