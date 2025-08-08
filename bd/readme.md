# Configuración de Base de Datos

## 1. Crear la base de datos

```sql
CREATE DATABASE report_generator;
```

## 2. Crear el usuario

```sql
CREATE USER u_report WITH PASSWORD '1234567890';
```

## 3. Conceder permisos básicos

```sql
GRANT CONNECT ON DATABASE report_generator TO u_report;
GRANT CREATE ON DATABASE report_generator TO u_report;
GRANT USAGE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO u_report;
GRANT CREATE ON SCHEMA public TO u_report;
```

## 4. Procedimientos Almacenados

### Procedimiento para listar campañas con paginación

```sql
CREATE OR REPLACE FUNCTION get_campanias_by_fecha(
    p_fecha_in DATE,  -- Parámetro de entrada
    p_page INTEGER DEFAULT 1,  -- Número de página
    p_page_size INTEGER DEFAULT 10  -- Tamaño de página
)
RETURNS TABLE(
    id INTEGER, 
    nombre TEXT, 
    fecha DATE, 
    estado TEXT, 
    descripcion TEXT,
    total_registros BIGINT,
    total_paginas INTEGER
) 
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_registros BIGINT;
    v_total_paginas INTEGER;
    v_offset INTEGER;
BEGIN
    -- Calcular el total de registros
    SELECT COUNT(*) INTO v_total_registros
    FROM "TA_SMS_MAESTRO" m
    WHERE m.fecha = p_fecha_in;  -- Aquí usamos "m.fecha" para referirnos a la columna

    -- Calcular el total de páginas
    v_total_paginas := CEIL(v_total_registros::float / p_page_size);

    -- Calcular el offset para la paginación
    v_offset := (p_page - 1) * p_page_size;

    -- Retornar los resultados con la paginación
    RETURN QUERY
    SELECT
        m.id,
        m.nombre::TEXT,
        m.fecha,
        m.estado::TEXT,
        m.descripcion::TEXT,
        v_total_registros AS total_registros,
        v_total_paginas AS total_paginas
    FROM "TA_SMS_MAESTRO" m
    WHERE m.fecha = p_fecha_in  -- Nuevamente, usando "m.fecha"
    ORDER BY m.id
    LIMIT p_page_size
    OFFSET v_offset;

END;
$$;
```


## Funcion

Consulta los registros de TA_SMS_MAESTRO que no tienen un reporte en reporte_estado
CREATE OR REPLACE FUNCTION obtener_maestros_sin_reporte(fecha_param DATE)
RETURNS TABLE (
    maestro_id INT,
    maestro_nombre TEXT,
    maestro_fecha DATE,
    estado_reporte TEXT,
    ruta_archivo TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT maestro.id, maestro.nombre, maestro.fecha, estado.estado, estado.ruta_archivo
    FROM TA_SMS_MAESTRO maestro
    LEFT JOIN reporte_estado estado 
        ON maestro.id = estado.id_campana AND maestro.fecha = estado.fecha
    WHERE maestro.fecha = fecha_param
    AND estado.id IS NULL;  -- Solo los maestros sin reporte
END;
$$ LANGUAGE plpgsql;



### Uso del procedimiento

```sql
-- Ejemplo 1: Obtener primera página (10 registros)
BEGIN;
CALL get_campanias_by_fecha('2024-03-20', 1, 10, 'resultados');
FETCH ALL IN "resultados";
COMMIT;

-- Ejemplo 2: Obtener segunda página con 20 registros por página
BEGIN;
CALL get_campanias_by_fecha('2024-03-20', 2, 20, 'resultados');
FETCH ALL IN "resultados";
COMMIT;

-- Ejemplo 3: Usar valores por defecto
BEGIN;
CALL get_campanias_by_fecha('2024-03-20', p_result := 'resultados');
FETCH ALL IN "resultados";
COMMIT;
```

## 5. Verificar permisos

```sql
-- Verificar permisos del usuario
SELECT d.datname, r.rolname, r.rolsuper, r.rolcreaterole, r.rolcreatedb
FROM pg_database d
JOIN pg_roles r ON r.rolname = 'u_report'
WHERE d.datistemplate = false;

-- Listar bases de datos y roles
\l    -- Listar bases de datos
\du   -- Listar roles de usuarios
```

## 6. Permisos adicionales para procedimientos

```sql
-- Permisos para ejecutar procedimientos
GRANT EXECUTE ON PROCEDURE get_campanias_by_fecha(date, integer, integer, refcursor) TO u_report;
```

### Notas:
- El procedimiento almacenado maneja la paginación de forma eficiente en la base de datos
- Retorna información adicional como total de registros y páginas
- Incluye parámetros opcionales para página y tamaño de página
- Los resultados se ordenan por ID de campaña