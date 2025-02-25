import random
from datetime import datetime, timedelta
import argparse
from models.database import Session
from models.ta_sms_maestro import TaSmsMaestro
from schemas.ta_sms_maestro import TaSmsMaestroCreate
from sqlalchemy.exc import SQLAlchemyError
from seeder.generate_details import seed_detalles_database
from models.ta_sms_detalle import TaSmsDetalle
from models.ta_sms_maestro import TaSmsMaestro
from models.database import Base, engine

# Tipos de campañas y sus descripciones base
tipos_campanas = {
    "Promoción": [
        "Campaña {estacion} {año}",
        "Ofertas Flash {mes}",
        "Promoción Especial {festividad}",
        "Descuentos {categoria}"
    ],
    "Notificación": [
        "Actualización Sistema {mes}",
        "Mantenimiento Programado {area}",
        "Aviso Importante {servicio}",
        "Notificación {tipo_servicio}"
    ],
    "Recordatorio": [
        "Recordatorio Pagos {mes}",
        "Recordatorio Citas {especialidad}",
        "Recordatorio Eventos {tipo_evento}",
        "Vencimiento {servicio}"
    ],
    "Marketing": [
        "Campaña Fidelización {trimestre}",
        "Newsletter {mes}",
        "Encuesta Satisfacción {periodo}",
        "Programa Referidos {mes}"
    ]
}

# Variables para personalizar mensajes
variables = {
    "estacion": ["Verano", "Otoño", "Invierno", "Primavera"],
    "mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "festividad": ["Navidad", "Año Nuevo", "Pascua", "Día de la Madre", "Día del Padre", "Black Friday", "Cyber Monday"],
    "categoria": ["Tecnología", "Hogar", "Deportes", "Moda", "Electrónica"],
    "area": ["Servidores", "Base de Datos", "Aplicación", "Red", "Sistemas"],
    "servicio": ["Facturación", "Soporte", "Plataforma", "Cuenta", "Suscripción"],
    "tipo_servicio": ["Seguridad", "Actualización", "Cambios", "Mejoras"],
    "especialidad": ["Médicas", "Técnicas", "Asesoría", "Consultoría"],
    "tipo_evento": ["Webinar", "Conferencia", "Taller", "Seminario"],
    "trimestre": ["Q1", "Q2", "Q3", "Q4"],
    "periodo": ["Mensual", "Trimestral", "Semestral", "Anual"]
}

estados = ["ACTIVO", "PAUSADO", "COMPLETADO"]

def generar_nombre_campana(year):
    tipo = random.choice(list(tipos_campanas.keys()))
    plantilla = random.choice(tipos_campanas[tipo])
    
    # Reemplazar variables en la plantilla
    for var in variables.keys():
        if "{" + var + "}" in plantilla:
            plantilla = plantilla.replace("{" + var + "}", random.choice(variables[var]))
    
    # Reemplazar año si existe en la plantilla
    if "{año}" in plantilla:
        plantilla = plantilla.replace("{año}", str(year))
    
    return plantilla

def generar_descripcion(nombre):
    descripciones = {
        "Promoción": ["Ofertas especiales para clientes", "Descuentos exclusivos en productos seleccionados", "Promociones por tiempo limitado"],
        "Notificación": ["Información importante sobre servicios", "Avisos sobre cambios en el sistema", "Actualizaciones programadas"],
        "Recordatorio": ["Recordatorios importantes para usuarios", "Avisos de vencimiento", "Notificaciones de seguimiento"],
        "Marketing": ["Campañas de fidelización", "Información sobre nuevos servicios", "Encuestas de satisfacción"]
    }
    
    tipo = next((k for k in tipos_campanas.keys() if k in nombre), "Promoción")
    return random.choice(descripciones[tipo])

def generar_registros(num_registros: int, fecha: datetime.date) -> list[TaSmsMaestro]:
    """
    Genera registros utilizando el modelo SQLAlchemy y validando con Pydantic
    """
    registros = []

    for _ in range(num_registros):
        nombre = generar_nombre_campana(fecha.year)
        
        # Crear datos usando el schema Pydantic para validación
        registro_data = {
            'fecha': fecha,
            'nombre': nombre,
            'estado': random.choice(estados),
            'descripcion': generar_descripcion(nombre)
        }
        
        # Validar datos con Pydantic
        registro_validado = TaSmsMaestroCreate(**registro_data)
        
        # Crear instancia del modelo SQLAlchemy
        registro = TaSmsMaestro(
            fecha=registro_validado.fecha,
            nombre=registro_validado.nombre,
            estado=registro_validado.estado,
            descripcion=registro_validado.descripcion
        )
        registros.append(registro)

    return registros

def seed_database(num_registros: int, detalles_por_maestro: int, fecha: datetime.date):
    """
    Inserta los registros maestros y sus detalles en la base de datos
    """
    db = Session()
    try:
        # Generar y guardar registros maestros
        registros = generar_registros(num_registros, fecha)
        db.add_all(registros)
        db.commit()
        print(f"✓ Se generaron {num_registros} registros maestros exitosamente")

        # Generar detalles para cada maestro
        total_detalles = 0
        for i, registro in enumerate(registros, 1):
            try:
                seed_detalles_database(registro.id, detalles_por_maestro)
                total_detalles += detalles_por_maestro
                print(f"  → Maestro {i}/{num_registros}: {detalles_por_maestro} detalles generados")
            except Exception as e:
                print(f"  ✗ Error en maestro {i}/{num_registros}: {str(e)}")
                continue
        
        print(f"\n✓ Total de detalles generados: {total_detalles}")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"✗ Error al insertar en la base de datos: {str(e)}")
        raise
    finally:
        db.close()