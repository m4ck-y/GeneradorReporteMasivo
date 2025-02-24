# Backend - Generador de Reportes Masivos

## Requisitos Previos

- Python 3.10 o superior
- PostgreSQL 14 o superior
- pip (gestor de paquetes de Python)

## Configuración del Entorno de Desarrollo

### 1. Crear y Activar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias principales
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install pydantic

# Exportar dependencias a requirements.txt
pip freeze > requirements.txt

# O instalar todas las dependencias desde requirements.txt
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos

Crear archivo `.env` en la raíz del proyecto:

### 4. Ejecutar el Proyecto

```bash
# Ubicarse en la carpeta backend
cd backend

# Ejecutar el servidor de desarrollo
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

## Estructura del Proyecto

```
backend/
├── models/             # Modelos SQLAlchemy
│   ├── database.py    # Configuración de base de datos
│   ├── ta_sms_maestro.py
│   └── ta_sms_detalle.py
├── schemas/           # Esquemas Pydantic
│   ├── ta_sms_maestro.py
│   └── ta_sms_detalle.py
├── seeder/           # Generadores de datos de prueba
│   ├── generate_maestro.py
│   └── generate_details.py
├── tasks/            # Tareas y utilidades
│   └── report_generator.py  # Generador de reportes
├── main.py          # Punto de entrada de la aplicación
├── seeder.py        # Script para generar datos de prueba
└── requirements.txt  # Dependencias del proyecto
```

## Generar Datos de Prueba

```bash
# Ejecutar el seeder interactivo
python seeder.py

# El seeder solicitará:
# - Número de registros maestros (default: 20)
# - Número de detalles por maestro (default: 20)
# - Año para los registros (default: 2025)

# Nota: El seeder limpiará todos los registros existentes antes de generar nuevos datos
```

## Generación de Reportes

El sistema permite generar diferentes tipos de reportes en formato CSV:

### Tipos de Reportes
1. **Reporte por Campaña**: Detalle completo de una campaña específica
2. **Reporte por Fecha**: Genera reportes para todas las campañas de una fecha

Los reportes se guardan en el directorio `reports/` con la siguiente nomenclatura:
- Campaña: `campaign_[ID]_[TIMESTAMP].csv`
- Resumen: `summary_report_[FECHA]_[TIMESTAMP].csv`

## Documentación API

Una vez ejecutado el servidor, puedes acceder a:

- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Comandos Útiles

```bash
# Actualizar requirements.txt
pip freeze > requirements.txt

# Instalar nuevas dependencias desde requirements.txt
pip install -r requirements.txt

# Verificar versión de Python
python --version

# Listar paquetes instalados
pip list
```