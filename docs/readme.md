
**GeneradorReporteMasivo**
Diseñado para generar reportes detallados de campañas SMS utilizando FastAPI, SQLAlchemy, Celery y PostgreSQL. La solución está orientada a manejar grandes volúmenes de datos de manera eficiente y generar reportes en formato CSV de manera asíncrona.

## Descripción
Este proyecto expone una API REST que recibe una fecha como parámetro y genera reportes de todas las campañas SMS registradas en la base de datos. Los reportes incluyen detalles de cada campaña y se generan en archivos CSV o TXT. El procesamiento de las campañas se realiza de manera asíncrona utilizando Celery y Redis como broker de mensajes.

### Funcionalidades principales:
- **Generación de reportes**: Se generan reportes de campañas por fecha.
- **Alta volumetría**: El sistema está diseñado para manejar grandes volúmenes de datos, con más de 1,000 campañas diarias y hasta 400,000 registros por campaña.
- **Asincronía**: Utiliza Celery para procesar las tareas de generación de reportes en segundo plano.
- **Paginación**: Utiliza paginación para manejar eficientemente los datos de las campañas y sus detalles.

## Tecnologías

- **FastAPI**: Framework web moderno para crear APIs REST rápidas.
- **SQLAlchemy**: ORM para interactuar con la base de datos PostgreSQL.
- **Pydantic**: Validación de datos de entrada y salida en la API.
- **Celery**: Sistema de tareas asíncronas para procesamiento en segundo plano.
- **Redis**: Broker de mensajes utilizado por Celery.
- **PostgreSQL**: Base de datos relacional para almacenar los detalles de las campañas.
- **Docker**: Contenerización del proyecto para facilitar su despliegue.

## Requisitos

- Python 3.8 o superior
- Docker (opcional, para desplegar el proyecto de manera fácil)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/CampaignReportGenerator.git
cd CampaignReportGenerator

2. Crear un entorno virtual

python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate

3. Instalar dependencias

pip install -r requirements.txt

4. Configurar la base de datos

    Asegúrate de tener PostgreSQL instalado y funcionando.
    Crea una base de datos y actualiza las credenciales en el archivo app/models/database.py.

5. Ejecutar las migraciones (si usas alembic o similar)

# Si tienes Alembic configurado
alembic upgrade head

6. Iniciar el proyecto

Para iniciar la API con FastAPI:

uvicorn app.main:app --reload

Para iniciar Celery con Redis como broker:

celery -A app.celery_worker.celery_app worker --loglevel=info

7. Docker (opcional)

Si prefieres usar Docker, el proyecto ya está configurado para ser ejecutado en contenedores. Solo necesitas ejecutar:

docker-compose up --build

Esto levantará los contenedores para la API, PostgreSQL y Redis automáticamente.
Uso de la API
Endpoint para consultar campañas

GET /campanas/{fecha}

Parámetros:

    fecha: Fecha en formato YYYY-MM-DD para filtrar las campañas.

Respuesta: Devuelve una lista de campañas para la fecha indicada.
Endpoint para generar el reporte de campañas

POST /generar_reporte/{fecha}

Parámetros:

    fecha: Fecha en formato YYYY-MM-DD para generar los reportes.

Descripción: Este endpoint generará el reporte de las campañas para la fecha proporcionada. El procesamiento se realiza en segundo plano utilizando Celery, y el reporte se guarda en archivos CSV.
Estructura de la Base de Datos

La base de datos está compuesta por dos tablas principales:

    TA_SMS_MAESTRO: Almacena información general sobre las campañas.
    TA_SMS_DETALLE: Almacena los detalles de cada mensaje enviado, relacionado con la campaña.
