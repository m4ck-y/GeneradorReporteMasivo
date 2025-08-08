
# Estructura de Base de Datos

Este documento describe la estructura de la base de datos necesaria para el desarrollo del sistema, incluyendo las tablas que deben existir, sus relaciones y los procedimientos almacenados necesarios para la generación de reportes.

## Tablas de la Base de Datos

### 1. **TA_SMS_MAESTRO**
Esta tabla contendrá información general sobre cada campaña.

#### Estructura de la tabla:
```sql
CREATE TABLE TA_SMS_MAESTRO (
    id SERIAL PRIMARY KEY,  -- Identificador único de la campaña
    fecha DATE NOT NULL,     -- Fecha de la campaña
    nombre_campaña VARCHAR(255) NOT NULL,  -- Nombre descriptivo de la campaña
    estado VARCHAR(50) NOT NULL,          -- Estado de la campaña (Ejemplo: Activa, Finalizada)
    descripcion TEXT         -- Descripción opcional de la campaña
);
```

#### Índices recomendados:
```sql
CREATE INDEX idx_ta_sms_maestro_fecha ON TA_SMS_MAESTRO(fecha);
```

---

### 2. **TA_SMS_DETALLE**
Esta tabla contiene los detalles de cada campaña, que pueden ser mensajes individuales o registros asociados a una campaña.

#### Estructura de la tabla:
```sql
CREATE TABLE TA_SMS_DETALLE (
    id SERIAL PRIMARY KEY,  -- Identificador único de cada detalle
    id_maestro INTEGER REFERENCES TA_SMS_MAESTRO(id) ON DELETE CASCADE, -- Relación con la campaña (TA_SMS_MAESTRO)
    telefono VARCHAR(15) NOT NULL,   -- Teléfono asociado al mensaje
    mensaje TEXT NOT NULL,           -- Contenido del mensaje
    fecha_envio TIMESTAMP NOT NULL,  -- Fecha y hora de envío
    estado VARCHAR(50) NOT NULL,     -- Estado del mensaje (Ejemplo: Enviado, Pendiente)
    error VARCHAR(255)              -- Mensaje de error en caso de fallos
);
```

#### Índices recomendados:
```sql
CREATE INDEX idx_ta_sms_detalle_id_maestro ON TA_SMS_DETALLE(id_maestro);
CREATE INDEX idx_ta_sms_detalle_fecha_envio ON TA_SMS_DETALLE(fecha_envio);
```

---

## Procedimientos Almacenados

### 1. **sp_obtener_campanas_por_fecha**
Este procedimiento almacenado consultará las campañas que se realizaron en una fecha específica.

#### SQL:
```sql
CREATE OR REPLACE PROCEDURE sp_obtener_campanas_por_fecha(
    fecha_consulta DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM TA_SMS_MAESTRO
    WHERE fecha = fecha_consulta;
END;
$$;
```

---

### 2. **sp_obtener_detalle_campana_paginado**
Este procedimiento almacenado permite obtener los detalles de una campaña específica de manera paginada. Recibe el ID de la campaña y los parámetros de paginación (página y tamaño).

#### SQL:
```sql
CREATE OR REPLACE PROCEDURE sp_obtener_detalle_campana_paginado(
    id_campana INTEGER,
    pagina INTEGER,
    tamano_pagina INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT * FROM TA_SMS_DETALLE
    WHERE id_maestro = id_campana
    ORDER BY fecha_envio
    LIMIT tamano_pagina
    OFFSET (pagina - 1) * tamano_pagina;
END;
$$;
```

---

### 3. **sp_generar_reporte_campanas**
Este procedimiento almacenado generará un reporte de las campañas para una fecha específica. Llama al procedimiento `sp_obtener_campanas_por_fecha` y obtiene los detalles de cada campaña, luego los formatea en un archivo CSV.

#### SQL:
```sql
CREATE OR REPLACE PROCEDURE sp_generar_reporte_campanas(
    fecha_consulta DATE,
    archivo_salida TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    campana RECORD;
    detalle RECORD;
    archivo_path TEXT := archivo_salida;
BEGIN
    -- Consultar campañas por fecha
    FOR campana IN SELECT * FROM sp_obtener_campanas_por_fecha(fecha_consulta) LOOP
        -- Abre el archivo para escribir el reporte de cada campaña
        PERFORM pg_catalog.pg_write_file(archivo_path || campana.id || '.csv', 'w');

        -- Consultar los detalles de la campaña de manera paginada
        FOR detalle IN SELECT * FROM sp_obtener_detalle_campana_paginado(campana.id, 1, 100) LOOP
            -- Escribir cada registro en el archivo CSV
            PERFORM pg_catalog.pg_write_file(archivo_path || campana.id || '.csv', detalle.telefono || ',' || detalle.mensaje || '
');
        END LOOP;
    END LOOP;
END;
$$;
```

---

## Estrategias de Optimización

1. **Índices**:
   - Se recomienda crear índices en las columnas que se utilizan frecuentemente para las consultas, como `fecha`, `id_maestro` y `fecha_envio`.
   - Los índices en las tablas `TA_SMS_MAESTRO` y `TA_SMS_DETALLE` mejorarán el rendimiento de las consultas y la generación de los reportes.

2. **Paginación**:
   - Utilizar la paginación en las consultas a `TA_SMS_DETALLE` para evitar cargar grandes cantidades de datos en la memoria.

3. **Manejo de Errores**:
   - En caso de errores durante la ejecución de los procedimientos almacenados (por ejemplo, en la generación de archivos), implementar manejo adecuado de excepciones y reintentos según sea necesario.

---

Este modelo de base de datos y procedimientos almacenados proporciona una estructura robusta para manejar la alta volumetría de datos de campañas y detalles de SMS, asegurando una generación de reportes eficiente.
