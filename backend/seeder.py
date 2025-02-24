from seeder.generate_maestro import seed_database
from models.database import Base, engine, Session
from models.ta_sms_maestro import TaSmsMaestro
from models.ta_sms_detalle import TaSmsDetalle
from sqlalchemy import text

def get_input_with_default(prompt: str, default_value: str) -> str:
    """Solicita input al usuario con un valor por defecto"""
    user_input = input(f"{prompt} [{default_value}]: ").strip()
    return user_input if user_input else default_value

def limpiar_tablas():
    """Elimina todos los registros de las tablas"""
    db = Session()
    try:
        # Eliminar registros de detalles primero debido a la restricción de clave foránea
        db.query(TaSmsDetalle).delete()
        db.query(TaSmsMaestro).delete()
        
        # Reiniciar las secuencias de ID en PostgreSQL
        #db.execute(text("ALTER SEQUENCE ta_sms_detalle_id_seq RESTART WITH 1"))
        #db.execute(text("ALTER SEQUENCE ta_sms_maestro_id_seq RESTART WITH 1"))
        
        db.commit()
        print("✓ Registros anteriores eliminados exitosamente")
    except Exception as e:
        db.rollback()
        print(f"✗ Error al limpiar las tablas: {str(e)}")
        raise
    finally:
        db.close()

def run_seeder():
    print("\n=== Generador de Datos de Prueba para SMS ===\n")
    
    try:
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)
        
        # Limpiar registros existentes
        limpiar_tablas()
        
        # Solicitar parámetros con valores por defecto
        print("\nPor favor, ingrese los siguientes valores (o presione Enter para usar el valor por defecto):\n")
        
        num_maestros = int(get_input_with_default(
            "Número de registros maestros a generar",
            "20"
        ))
        
        num_detalles = int(get_input_with_default(
            "Número de detalles por cada maestro",
            "20"
        ))
        
        year = int(get_input_with_default(
            "Año para los registros",
            "2025"
        ))
        
        print("\nGenerando registros...")
        print(f"- {num_maestros} registros maestros")
        print(f"- {num_detalles} detalles por cada maestro")
        print(f"- Año: {year}\n")
        
        # Ejecutar el seeder
        seed_database(num_maestros, num_detalles, year)
        
        print("\n¡Proceso completado exitosamente!")
        
    except ValueError as e:
        print("\nError: Por favor ingrese números válidos")
    except Exception as e:
        print(f"\nError durante la ejecución: {str(e)}")

if __name__ == "__main__":
    run_seeder()