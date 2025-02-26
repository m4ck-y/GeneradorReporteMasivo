### 1. Crear la base de datos:

- Primero, debes crear la base de datos antes de asignarle permisos al usuario.

sql
Copiar
CREATE DATABASE report_generator;
### 2. Crear el usuario:

Luego, puedes crear el usuario con la contraseña especificada.

sql
Copiar
CREATE USER u_report WITH PASSWORD '1234567890';
### 3. Conceder permisos de conexión y creación a nivel de base de datos:

Ahora, le das permisos al usuario para conectarse a la base de datos y crear objetos dentro de ella.

sql
Copiar
GRANT CONNECT ON DATABASE report_generator TO u_report;
GRANT CREATE ON DATABASE report_generator TO u_report;
### 4. Permitir uso y permisos sobre todas las tablas del esquema `public`:

Permites que el usuario realice operaciones como `SELECT`, `INSERT`, `UPDATE`, y `DELETE` sobre todas las tablas en el esquema `public`.

sql
Copiar
GRANT USAGE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO u_report;
### 5. Permitir crear objetos dentro del esquema `public`:

También le das permisos para crear objetos (como nuevas tablas, vistas, procedimientos almacenados, etc.) en el esquema `public`.

sql
Copiar
GRANT CREATE ON SCHEMA public TO u_report;
### 6. Permitir crear procedimientos almacenados, vistas y triggers:

Si quieres que el usuario también pueda crear procedimientos almacenados, vistas y triggers, necesitarías darle los permisos apropiados. A continuación, algunos ejemplos de permisos adicionales que podrías otorgar:

sql
Copiar
GRANT CREATE ON SCHEMA public TO u_report;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO u_report;
GRANT TRIGGER ON ALL TABLES IN SCHEMA public TO u_report;
### 7. Verificar los permisos y roles del usuario:

Para comprobar qué permisos tiene un usuario o qué roles están asignados a un usuario en particular, puedes usar los siguientes comandos:

sql
Copiar
SELECT d.datname, r.rolname, r.rolsuper, r.rolcreaterole, r.rolcreatedb
FROM pg_database d
JOIN pg_roles r ON r.rolname = 'u_report'  -- Cambia esto por el nombre de tu usuario
WHERE d.datistemplate = false;

- También puedes listar las bases de datos y los roles usando estos comandos:

sql
Copiar
\l    -- Listar las bases de datos
\du   -- Listar los roles de usuarios