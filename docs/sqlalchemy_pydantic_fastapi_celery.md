
# Integración de SQLAlchemy, Pydantic, FastAPI y Celery

Este documento explica cómo integrar **SQLAlchemy**, **Pydantic**, **FastAPI** y **Celery** para desarrollar una API asíncrona que maneje grandes volúmenes de datos y genere reportes.

## Estructura del Proyecto

El proyecto tendrá la siguiente estructura:

```
/app
    /models
        __init__.py
        database.py
        ta_sms_maestro.py
        ta_sms_detalle.py
    /schemas
        __init__.py
        ta_sms_maestro.py
        ta_sms_detalle.py
    /tasks
        __init__.py
        reportes.py
    /api
        __init__.py
        reportes.py
    main.py
```

---

## 1. **SQLAlchemy con FastAPI**

### **Instalación de dependencias**
Primero, instala las dependencias necesarias para SQLAlchemy y FastAPI.

```bash
pip install sqlalchemy pydantic fastapi psycopg2
```

### **Modelo de Datos con SQLAlchemy**

Define los modelos de base de datos utilizando **SQLAlchemy**.

#### `app/models/ta_sms_maestro.py`
```python
from sqlalchemy import Column, Integer, String, Date
from app.models.database import Base

class TaSmsMaestro(Base):
    __tablename__ = 'TA_SMS_MAESTRO'
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    nombre_campaña = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
```

#### `app/models/ta_sms_detalle.py`
```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.models.database import Base

class TaSmsDetalle(Base):
    __tablename__ = 'TA_SMS_DETALLE'
    
    id = Column(Integer, primary_key=True, index=True)
    id_maestro = Column(Integer, nullable=False)
    telefono = Column(String(15), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, nullable=False)
    estado = Column(String, nullable=False)
    error = Column(Text, nullable=True)
    
    maestro = relationship("TaSmsMaestro", backref="detalles")
```

### **Base de Datos con SQLAlchemy**

Define una clase `database.py` para gestionar la conexión a la base de datos.

#### `app/models/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/database_name"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### **Interacción con la Base de Datos**

En el archivo `main.py`, crea un **CRUD** básico para interactuar con la base de datos utilizando **SQLAlchemy**.

#### `app/main.py`
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models.ta_sms_maestro import TaSmsMaestro
from app.models.ta_sms_detalle import TaSmsDetalle

app = FastAPI()

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/campanas/{fecha}")
def obtener_campanas(fecha: str, db: Session = Depends(get_db)):
    return db.query(TaSmsMaestro).filter(TaSmsMaestro.fecha == fecha).all()
```

---

## 2. **Pydantic con FastAPI**

### **Esquemas Pydantic**

Define los esquemas de Pydantic para la validación de datos.

#### `app/schemas/ta_sms_maestro.py`
```python
from pydantic import BaseModel
from datetime import date
from typing import Optional

class TaSmsMaestroBase(BaseModel):
    fecha: date
    nombre_campaña: str
    estado: str
    descripcion: Optional[str] = None

class TaSmsMaestro(TaSmsMaestroBase):
    id: int

    class Config:
        orm_mode = True
```

#### `app/schemas/ta_sms_detalle.py`
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaSmsDetalleBase(BaseModel):
    id_maestro: int
    telefono: str
    mensaje: str
    fecha_envio: datetime
    estado: str
    error: Optional[str] = None

class TaSmsDetalle(TaSmsDetalleBase):
    id: int

    class Config:
        orm_mode = True
```

---

## 3. **FastAPI - Endpoints para Consultar y Generar Reportes**

### **Endpoints para Consultar Campañas**

En `app/api/reportes.py`, crea un endpoint para obtener las campañas de una fecha determinada.

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.ta_sms_maestro import TaSmsMaestro

router = APIRouter()

@router.get("/campanas/{fecha}", response_model=list[TaSmsMaestro])
def obtener_campanas(fecha: str, db: Session = Depends(get_db)):
    return db.query(TaSmsMaestro).filter(TaSmsMaestro.fecha == fecha).all()
```

### **Endpoint para Generar Reportes (Celery)**

En `app/api/reportes.py`, puedes definir un endpoint para generar los reportes de forma asíncrona utilizando **Celery**.

```python
from fastapi import APIRouter, BackgroundTasks
from app.tasks.reportes import generar_reporte

router = APIRouter()

@router.post("/generar_reporte/{fecha}")
def generar_reporte_endpoint(fecha: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(generar_reporte, fecha)
    return {"message": "El reporte se está generando en segundo plano"}
```

---

## 4. **Celery - Tareas Asíncronas para Generación de Reportes**

### **Instalación de Celery y Redis**

Instala **Celery** y **Redis** para la gestión de tareas asíncronas.

```bash
pip install celery[redis]
```

### **Configuración de Celery**

Crea un archivo `celery_worker.py` para configurar Celery y conectar con Redis.

#### `app/celery_worker.py`
```python
from celery import Celery
from app.tasks.reportes import generar_reporte

celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(task_serializer='json', result_backend='redis://localhost:6379/0')

@celery_app.task
def generar_reporte_task(fecha: str):
    # Llama a la función de generación de reporte
    generar_reporte(fecha)
```

### **Generar Reporte en Segundo Plano**

En `app/tasks/reportes.py`, crea la función `generar_reporte` que se ejecutará en segundo plano.

#### `app/tasks/reportes.py`
```python
import csv
from datetime import datetime
from app.models.ta_sms_maestro import TaSmsMaestro
from app.models.ta_sms_detalle import TaSmsDetalle
from app.models.database import SessionLocal
from app.celery_worker import generar_reporte_task

def generar_reporte(fecha: str):
    db = SessionLocal()
    
    campanas = db.query(TaSmsMaestro).filter(TaSmsMaestro.fecha == fecha).all()
    
    for campana in campanas:
        # Crear archivo CSV
        with open(f"reporte_{campana.id}_{fecha}.csv", "w", newline="") as csvfile:
            fieldnames = ['telefono', 'mensaje', 'fecha_envio', 'estado']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            detalles = db.query(TaSmsDetalle).filter(TaSmsDetalle.id_maestro == campana.id).all()
            for detalle in detalles:
                writer.writerow({
                    'telefono': detalle.telefono,
                    'mensaje': detalle.mensaje,
                    'fecha_envio': detalle.fecha_envio,
                    'estado': detalle.estado
                })
    
    db.close()
```

---

## Conclusión

Este sistema utiliza **FastAPI** para manejar las solicitudes de la API, **SQLAlchemy** para interactuar con PostgreSQL, **Pydantic** para la validación de datos, y **Celery** para la ejecución asíncrona de tareas de generación de reportes. Con esta arquitectura, puedes manejar grandes volúmenes de datos de manera eficiente y escalable.
