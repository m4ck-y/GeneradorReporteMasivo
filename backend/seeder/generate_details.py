import random
from models.database import Session
from models.ta_sms_detalle import TaSmsDetalle
from schemas.ta_sms_detalle import TaSmsDetalleCreate
from sqlalchemy.exc import SQLAlchemyError

# Estados posibles para los mensajes
estados = ['ENVIADO', 'PENDIENTE', 'FALLIDO']

# Tipos de mensajes base para variar
tipos_mensajes = [
    "¡Oferta especial! {descuento}% de descuento en {producto}",
    "Última oportunidad: {producto} con {descuento}% off",
    "No te pierdas esta oferta en {producto}",
    "¡{producto} en promoción! Solo por hoy",
    "Descuento exclusivo: {descuento}% en {producto}"
]

productos = [
    "smartphones", "laptops", "tablets", "auriculares", "smartwatches",
    "cámaras", "televisores", "consolas", "videojuegos", "accesorios",
    "ropa deportiva", "calzado", "muebles", "electrodomésticos", "libros"
]

def generar_detalles(id_maestro: int, num_detalles: int) -> list[TaSmsDetalle]:
    """
    Genera registros de detalle para un maestro específico
    """
    detalles = []
    
    for _ in range(num_detalles):
        mensaje = random.choice(tipos_mensajes).format(
            descuento=random.randint(10, 70),
            producto=random.choice(productos)
        )
        
        # Crear datos usando el schema Pydantic para validación
        detalle_data = {
            'id_maestro': id_maestro,
            'mensaje': mensaje,
            'estado': random.choice(estados)
        }
        
        # Validar datos con Pydantic
        detalle_validado = TaSmsDetalleCreate(**detalle_data)
        
        # Crear instancia del modelo SQLAlchemy
        detalle = TaSmsDetalle(
            id_maestro=detalle_validado.id_maestro,
            mensaje=detalle_validado.mensaje,
            estado=detalle_validado.estado
        )
        detalles.append(detalle)
    
    return detalles

def seed_detalles_database(id_maestro: int, num_detalles: int):
    """
    Inserta los detalles generados en la base de datos
    """
    db = Session()
    try:
        detalles = generar_detalles(id_maestro, num_detalles)
        db.add_all(detalles)
        db.commit()
        return detalles
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()