from sqlalchemy import ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from models.database import Base
from typing import Optional

class TaSmsDetalle(Base):
    __tablename__ = 'TA_SMS_DETALLE'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    id_maestro: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('TA_SMS_MAESTRO.id', ondelete="CASCADE"), #ondelete="CASCADE" para que si se elimina una campaña, se eliminen sus detalles
        nullable=False,
        index=True)

    mensaje: Mapped[str] = mapped_column(Text, nullable=False)

    estado: Mapped[str] = mapped_column(String, nullable=False)