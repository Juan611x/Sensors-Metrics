CREATE TABLE IF NOT EXISTS sensores (
    idSensor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lectura_sensor (
    idLecturaSensor SERIAL PRIMARY KEY,
    idSensor INT NOT NULL,
    unidad VARCHAR(20),
    valor FLOAT,
    fecha_registro TIMESTAMP,
    nombre VARCHAR(50),
    CONSTRAINT fk_sensor FOREIGN KEY (idSensor) REFERENCES sensores(idSensor)
);
