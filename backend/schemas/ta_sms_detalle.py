from pydantic import BaseModel

class TaSmsDetalleBase(BaseModel):
    id_maestro: int
    mensaje: str
    estado: str

class TaSmsDetalleCreate(TaSmsDetalleBase):
    pass

class TaSmsDetalle(TaSmsDetalleBase):
    id: int

    class Config:
        from_attributes = True 