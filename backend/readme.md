# Backend - Generador de Reportes Masivos

## Requisitos del Sistema

Para el correcto funcionamiento del proyecto, es necesario contar con:

- Python 3.10 o superior
- PostgreSQL 14 o superior
- pip (gestor de paquetes de Python)

## Configuración del Entorno de Desarrollo

### 1. Entorno Virtual

Es recomendable crear y activar un entorno virtual para aislar las dependencias:

```bash
# Creación del entorno virtual
python -m venv .venv

# Activación del entorno virtual
# Para Windows:
.venv\Scripts\activate
# Para Linux/Mac:
source .venv/bin/activate
```

### 2. Dependencias del Proyecto

Para instalar las dependencias necesarias:

```bash
# Instalación de componentes principales
pip install fastapi uvicorn sqlalchemy pydantic

# Para gestionar las dependencias, se puede:
# Exportar la lista de dependencias actual
pip freeze > requirements.txt

# O instalar desde un archivo existente
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos

Es necesario crear un archivo `.env` en la raíz del proyecto con las credenciales correspondientes.

### 4. Iniciar el Servidor

Para poner en marcha el servidor de desarrollo:

```bash
# Ubicarse en el directorio backend
cd backend

# Iniciar el servidor con recarga automática
uvicorn main:app --reload
```

El servicio estará disponible en: `http://localhost:8000`

## Estructura del Proyecto

La organización del código sigue una estructura modular:

```
backend/
├── models/             # Definiciones de modelos SQLAlchemy
│   ├── database.py    # Configuración de conexión a base de datos
│   ├── ta_sms_maestro.py
│   └── ta_sms_detalle.py
├── schemas/           # Esquemas de validación Pydantic
│   ├── ta_sms_maestro.py
│   └── ta_sms_detalle.py
├── seeder/           # Generadores de datos de prueba
│   ├── generate_maestro.py
│   └── generate_details.py
├── tasks/            # Utilidades y tareas
│   └── report_generator.py  # Generador de reportes
├── main.py          # Punto de entrada de la aplicación
├── seeder.py        # Script para datos de prueba
└── requirements.txt  # Listado de dependencias
```

## Generación de Datos de Prueba

Para facilitar el desarrollo y pruebas, se incluye un generador de datos:

```bash
# Ejecutar el generador interactivo
python seeder.py

# El script solicitará:
# - Cantidad de registros maestros (predeterminado: 20)
# - Cantidad de detalles por maestro (predeterminado: 20)
# - Fecha para los registros (predeterminado: fecha actual)

# Nota: Este proceso limpiará los datos existentes antes de generar nuevos registros
```

## Sistema de Reportes

La aplicación permite generar reportes en formato CSV de dos tipos:

### Tipos de Reportes Disponibles
1. **Reporte por Campaña**: Información detallada de una campaña específica
2. **Reporte por Fecha**: Consolidado de todas las campañas en una fecha determinada

Los archivos generados se almacenan en el directorio `reports/` siguiendo la nomenclatura:
- Campaña individual: `campaign_[ID]_[TIMESTAMP].csv`
- Reporte consolidado: `summary_report_[FECHA]_[TIMESTAMP].csv`

## Documentación de la API

La documentación interactiva está disponible en:

- Interfaz Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Comandos de Referencia

```bash
# Actualización del archivo de dependencias
pip freeze > requirements.txt

# Instalación de dependencias
pip install -r requirements.txt

# Verificación de versión de Python
python --version

# Visualización de paquetes instalados
pip list
```

# Guía de instalación de psycopg2

## Consideraciones previas
Al instalar psycopg2, es posible encontrar el siguiente mensaje:
```bash
Error: pg_config executable not found.
```
Este documento proporciona los pasos para resolver esta y otras situaciones comunes.

## Requisitos del sistema

Para una instalación exitosa de `psycopg2`, es recomendable asegurarse de contar con:

1. **Sistema Operativo**: Linux (Ubuntu)
2. **Python**: Python 3.x (preferentemente la versión más reciente)
3. **PostgreSQL**: Acceso a PostgreSQL y sus bibliotecas de desarrollo
4. **Herramientas de compilación**: Componentes necesarios para compilar paquetes en C

### Preparación del entorno

Para asegurar una instalación correcta, es recomendable tener instalados los siguientes componentes:

#### 1. Paquete de desarrollo de Python
Necesario para la compilación de extensiones de Python en C:

```bash
sudo apt-get install python3-dev
```

#### 2. Herramientas de compilación (build-essential)
Facilita la compilación de código en C en el sistema:

```bash
sudo apt-get install build-essential
```

#### 3. Dependencias de PostgreSQL
Proporciona las bibliotecas de desarrollo necesarias, incluyendo pg_config:

```bash
sudo apt-get install libpq-dev
```
