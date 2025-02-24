# Backend - Generador de Reportes Masivos

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

# Instalar desde requirements.txt
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
├── main.py          # Punto de entrada de la aplicación
├── seeder.py        # Script para generar datos de prueba
└── requirements.txt  # Dependencias del proyecto
```

## Generar Datos de Prueba

```bash
# Ejecutar el seeder interactivo
python seeder.py

# Se solicitará:
# - Número de registros maestros
# - Número de detalles por maestro
# - Año para los registros
```

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