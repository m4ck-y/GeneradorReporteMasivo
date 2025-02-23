import datetime
from fastapi import HTTPException

def convertir_fecha(fecha_str: str) -> datetime.datetime:
    """Convierte una cadena de fecha en formato 'YYYY/MM/DD' a un objeto datetime."""

    try:
        return datetime.datetime.strptime(fecha_str, "%Y/%m/%d")

    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use 'YYYY/MM/DD'.")