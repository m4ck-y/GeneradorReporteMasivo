from sqlalchemy import Column, Integer, String, DateTime, Date, func
from models.database import Base

class ReporteEstado(Base):
    """
    Modelo para la tabla 'reporte_estado' que almacena el estado de los reportes generados para cada campaña.
    """
    __tablename__ = 'reporte_estado'  # Nombre de la tabla en la base de datos

    # Identificador único de la fila (clave primaria)
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Identificador único de la fila del reporte")

    # id_campaña: Identificador único de la campaña para la cual se genera el reporte.
    # Este campo puede ser una clave foránea si deseas relacionarlo con otra tabla (por ejemplo, TA_SMS_MAESTRO)
    id_campana = Column(Integer, nullable=False, comment="Identificador único de la campaña asociada al reporte")

    # fecha: Fecha en la que se solicitó el reporte (formato YYYY-MM-DD)
    fecha = Column(Date, nullable=False, comment="Fecha en la que se solicitó el reporte")

    # estado: Estado actual del reporte. Puede ser "Pendiente", "En proceso", "Completado" o "Error"
    estado = Column(String(50), nullable=False, comment="Estado del reporte (Pendiente, En proceso, Completado, Error)")

    # ruta_archivo: Ruta (o URL) donde se encuentra almacenado el archivo CSV generado.
    # Este campo es opcional y se llenará cuando el reporte esté completado.
    ruta_archivo = Column(String(255), nullable=True, comment="Ruta del archivo CSV generado (si está disponible)")

    # intentos: Número de reintentos en caso de fallo durante la generación del reporte.
    intentos = Column(Integer, default=0, nullable=False, comment="Número de reintentos en caso de fallo en la generación del reporte")

    # timestamp: Fecha y hora de la última actualización de este registro.
    # Se actualiza automáticamente cada vez que se modifica la fila.
    timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(),
                       comment="Fecha y hora de la última actualización del estado del reporte")