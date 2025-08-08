CREATE TABLE TA_SMS_MAESTRO (
    id SERIAL PRIMARY KEY,  -- Identificador único de la campaña
    fecha DATE NOT NULL,     -- Fecha de la campaña
    nombre_campaña VARCHAR(255) NOT NULL,  -- Nombre descriptivo de la campaña
    estado VARCHAR(50) NOT NULL,          -- Estado de la campaña (Ejemplo: Activa, Finalizada)
    descripcion TEXT         -- Descripción opcional de la campaña
);

CREATE INDEX idx_ta_sms_maestro_fecha ON TA_SMS_MAESTRO(fecha);


CREATE TABLE TA_SMS_DETALLE (
    id SERIAL PRIMARY KEY,  -- Identificador único de cada detalle
    id_maestro INTEGER REFERENCES TA_SMS_MAESTRO(id) ON DELETE CASCADE, -- Relación con la campaña (TA_SMS_MAESTRO)
    telefono VARCHAR(15) NOT NULL,   -- Teléfono asociado al mensaje
    mensaje TEXT NOT NULL,           -- Contenido del mensaje
    fecha_envio TIMESTAMP NOT NULL,  -- Fecha y hora de envío
    estado VARCHAR(50) NOT NULL,     -- Estado del mensaje (Ejemplo: Enviado, Pendiente)
    error VARCHAR(255)              -- Mensaje de error en caso de fallos
);


CREATE INDEX idx_ta_sms_detalle_id_maestro ON TA_SMS_DETALLE(id_maestro);
CREATE INDEX idx_ta_sms_detalle_fecha_envio ON TA_SMS_DETALLE(fecha_envio);