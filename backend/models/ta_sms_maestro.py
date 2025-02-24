from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from models.database import Base
from typing import Optional


class TaSmsMaestro(Base):
    __tablename__ = 'TA_SMS_MAESTRO'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fecha: Mapped[str] = mapped_column(Date, nullable=False)

    nombre: Mapped[str] = mapped_column(String, nullable=False)
    "nombre_campaña"

    estado: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
