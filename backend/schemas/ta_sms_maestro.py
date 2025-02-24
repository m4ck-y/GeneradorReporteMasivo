from pydantic import BaseModel
from datetime import date
from typing import Optional

class TaSmsMaestroBase(BaseModel):
    fecha: date
    nombre: str
    estado: str
    descripcion: Optional[str] = None

class TaSmsMaestroCreate(TaSmsMaestroBase):
    pass

class TaSmsMaestro(TaSmsMaestroBase):
    id: int

    class Config:
        from_attributes = True