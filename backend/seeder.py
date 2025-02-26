import os
from seeder.generate_maestro import seed_database
from models.database import Base, engine, Session
from models.ta_sms_maestro import TaSmsMaestro
from models.ta_sms_detalle import TaSmsDetalle
from models.report_status import ReporteEstado
import shutil
from datetime import datetime
from sqlalchemy import text

def get_input_with_default(prompt: str, default_value: str, is_date: bool = False) -> str:
    """Solicita input al usuario con un valor por defecto"""
    user_input = input(f"{prompt} [{default_value}]: ").strip()
    
    if is_date and user_input:
        try:
            # Validar formato de fecha
            datetime.strptime(user_input, '%y/%m/%d')
        except ValueError:
            print("Formato de fecha inválido. Usando valor por defecto.")
            return default_value
            
    return user_input if user_input else default_value

def limpiar_tablas():
    """Elimina todos los registros de las tablas"""
    db = Session()
    try:
        # Eliminar registros de detalles primero debido a la restricción de clave foránea
        db.query(TaSmsDetalle).delete()
        db.query(TaSmsMaestro).delete()
        db.query(ReporteEstado).delete()

        # Reiniciar las secuencias de ID en PostgreSQL
        # Verificar si la secuencia existe antes de reiniciarla
        # Para evitar el error cuando la secuencia no existe
        db.execute(text(""" 
            DO $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'TA_SMS_DETALLE_id_seq' AND relkind = 'S') THEN
                    ALTER SEQUENCE "TA_SMS_DETALLE_id_seq" RESTART WITH 1;
                END IF;
            END $$;
        """))

        db.execute(text(""" 
            DO $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'TA_SMS_MAESTRO_id_seq' AND relkind = 'S') THEN
                    ALTER SEQUENCE "TA_SMS_MAESTRO_id_seq" RESTART WITH 1;
                END IF;
            END $$;
        """))

        db.execute(text(""" 
            DO $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'reporte_estado_id_seq' AND relkind = 'S') THEN
                    ALTER SEQUENCE "reporte_estado_id_seq" RESTART WITH 1;
                END IF;
            END $$;
        """))
        
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

        # Eliminar la carpeta y su contenido
        if os.path.exists("./reports"):
            shutil.rmtree("./reports")
        
        # Fecha actual en formato yy/mm/dd
        fecha_actual = datetime.now().strftime('%y/%m/%d')
        
        print("\nPor favor, ingrese los siguientes valores (o presione Enter para usar el valor por defecto):\n")
        
        fecha_str = get_input_with_default(
            "Fecha para los registros (formato: yy/mm/dd)",
            fecha_actual,
            is_date=True
        )
        
        num_maestros = int(get_input_with_default(
            "Número de registros maestros a generar",
            "20"
        ))
        
        num_detalles = int(get_input_with_default(
            "Número de detalles por cada maestro",
            "20"
        ))
        
        # Convertir string de fecha a objeto datetime
        fecha = datetime.strptime(fecha_str, '%y/%m/%d').date()
        
        print("\nGenerando registros...")
        print(f"- Fecha: {fecha.strftime('%Y-%m-%d')}")
        print(f"- {num_maestros} registros maestros")
        print(f"- {num_detalles} detalles por cada maestro\n")
        
        # Ejecutar el seeder
        seed_database(num_maestros, num_detalles, fecha)
        
        print("\n¡Proceso completado exitosamente!")
        
    except ValueError as e:
        print("\nError: Por favor ingrese valores válidos")
    except Exception as e:
        print(f"\nError durante la ejecución: {str(e)}")

if __name__ == "__main__":
    run_seeder()