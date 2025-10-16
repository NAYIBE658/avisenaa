CREATE DATABASE AVISENA;
USE AVISENA;
CREATE TABLE modulos (
    id_modulo TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre_modulo VARCHAR(30) NOT NULL,
    PRIMARY KEY(id_modulo)
);

CREATE TABLE roles (
    id_rol TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre_rol VARCHAR(30) NOT NULL,
    descripcion TEXT(500),
    PRIMARY KEY(id_rol)
);
INSERT INTO roles (nombre_rol, descripcion) VALUES 
('supervisor', 'Encargado de supervisar las operaciones diarias'),
('admi', 'Administrador del sistema con acceso general'),
('superadmi', 'Superadministrador con acceso total'),
('operario', 'Usuario operativo con permisos limitados');


CREATE TABLE permisos (
    id_modulo TINYINT UNSIGNED NOT NULL,
    id_rol TINYINT UNSIGNED NOT NULL,
    insertar BOOLEAN NOT NULL,
    actualizar BOOLEAN NOT NULL,
    seleccionar BOOLEAN NOT NULL,
    borrar BOOLEAN NOT NULL,
    PRIMARY KEY(id_modulo, id_rol)
);

CREATE TABLE usuarios (
    id_usuario INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(70) NOT NULL,
    id_rol TINYINT UNSIGNED NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono CHAR(15) NOT NULL,
    documento VARCHAR(20) NOT NULL,
    pass_hash VARCHAR(140) NOT NULL,
    PRIMARY KEY(id_usuario)
);

CREATE TABLE tareas (
    id_tarea SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_usuario INTEGER UNSIGNED NOT NULL,
    descripcion VARCHAR(180) NOT NULL,
    fecha_hora_init DATETIME NOT NULL,
    estado ENUM('Asignada', 'Pendiente', 'En proceso', 'Completada', 'Cancelada') NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    PRIMARY KEY(id_tarea)
);

CREATE TABLE metodo_pago (
    id_tipo TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    estado BOOLEAN NOT NULL,
    PRIMARY KEY(id_tipo)
);

CREATE TABLE ventas (
    id_venta INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    fecha_hora DATETIME NOT NULL,
    id_usuario INTEGER UNSIGNED NOT NULL,
    tipo_pago TINYINT UNSIGNED NOT NULL,
    total DECIMAL NOT NULL,
    PRIMARY KEY(id_venta)
);

CREATE TABLE tipo_huevos (
    id_tipo_huevo TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    Color VARCHAR(30) NOT NULL,
    Tamaño VARCHAR(30) NOT NULL,
    PRIMARY KEY(id_tipo_huevo)
);

INSERT INTO tipo_huevos (Color, Tamaño) VALUES 
('Blanco', 'AA'),
('Marrón', 'AA'),
('Blanco', 'A'),
('Marrón', 'A');

CREATE TABLE fincas (
    id_finca INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    longitud FLOAT NOT NULL,
    latitud FLOAT NOT NULL,
    estado BOOLEAN NOT NULL,
    PRIMARY KEY(id_finca)
);
INSERT INTO fincas (nombre, longitud, latitud, estado) VALUES 
('Finca El Roble', -75.1234, 6.2518, 1),
('Finca La Esperanza', -74.4567, 5.9876, 1),
('Finca Los Pinos', -73.8765, 6.7890, 0),
('Finca Santa Marta', -75.2345, 6.1234, 1);


CREATE TABLE galpones (
    id_galpon TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_finca INTEGER UNSIGNED NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    capacidad SMALLINT NOT NULL,
    cant_actual SMALLINT NOT NULL,
    PRIMARY KEY(id_galpon)
);

CREATE TABLE tipo_gallinas (
    id_tipo_gallinas TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    raza VARCHAR(30) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_tipo_gallinas)
);

CREATE TABLE ingreso_gallinas (
    id_ingreso SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_galpon TINYINT UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    id_tipo_gallina TINYINT UNSIGNED NOT NULL,
    cantidad_gallinas SMALLINT NOT NULL,
    PRIMARY KEY(id_ingreso)
);

CREATE TABLE produccion_huevos (
    id_produccion INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_galpon TINYINT UNSIGNED NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    id_tipo_huevo TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY(id_produccion)
);

CREATE TABLE stock (
    id_producto SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    unidad_medida ENUM('unidad', 'panal', 'docena', 'medio_panal') NOT NULL,
    id_produccion INTEGER UNSIGNED NOT NULL,
    cantidad_disponible INTEGER NOT NULL,
    PRIMARY KEY(id_producto)
);

CREATE TABLE detalle_huevos (
    id_detalle INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_producto SMALLINT UNSIGNED NOT NULL,
    cantidad SMALLINT NOT NULL,
    id_venta INTEGER UNSIGNED NOT NULL,
    valor_descuento DECIMAL NOT NULL,
    precio_venta DECIMAL NOT NULL,
    PRIMARY KEY(id_detalle)
);

CREATE TABLE salvamento (
    id_salvamento INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_galpon TINYINT UNSIGNED,
    fecha DATE NOT NULL,
    id_tipo_gallina TINYINT UNSIGNED NOT NULL,
    cantidad_gallinas SMALLINT NOT NULL,
    PRIMARY KEY(id_salvamento)
);

CREATE TABLE detalle_salvamento (
    id_detalle INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_producto INTEGER UNSIGNED NOT NULL,
    cantidad SMALLINT NOT NULL,
    id_venta INTEGER UNSIGNED NOT NULL,
    valor_descuento DECIMAL NOT NULL,
    precio_venta DECIMAL NOT NULL,
    PRIMARY KEY(id_detalle)
);

CREATE TABLE tipo_sensores (
    id_tipo TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(70) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    modelo VARCHAR(70) NOT NULL,
    PRIMARY KEY(id_tipo)
);

CREATE TABLE sensores (
    id_sensor TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    id_tipo_sensor TINYINT UNSIGNED NOT NULL,
    id_galpon TINYINT UNSIGNED NOT NULL,
    descripcion VARCHAR(140) NOT NULL,
    PRIMARY KEY(id_sensor)
);

CREATE TABLE registro_sensores (
    id_registro INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_sensor TINYINT UNSIGNED NOT NULL,
    dato_sensor FLOAT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    u_medida ENUM('°C', 'lm', '%') NOT NULL,
    PRIMARY KEY(id_registro)
);

CREATE TABLE categoria_inventario (
    id_categoria TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(255),
    PRIMARY KEY(id_categoria)
);

CREATE TABLE inventario_finca (
    id_inventario INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    cantidad SMALLINT NOT NULL,
    unidad_medida ENUM('Lb', 'Kg') NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    id_categoria TINYINT UNSIGNED NOT NULL,
    id_finca INTEGER UNSIGNED NOT NULL,
    PRIMARY KEY(id_inventario)
);

CREATE TABLE incidentes_gallina (
    id_inc_gallina INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    galpon_origen TINYINT UNSIGNED NOT NULL,
    tipo_incidente ENUM('Enfermedad', 'Herida', 'Muerte', 'Fuga', 'Ataque Depredador', 'Produccion', 'Alimentacion', 'Plaga', 'Estres termico', 'Otro') NOT NULL,
    cantidad SMALLINT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    esta_resuelto BOOLEAN NOT NULL,
    PRIMARY KEY(id_inc_gallina)
);

CREATE TABLE aislamiento (
    id_aislamiento INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_incidente_gallina INTEGER UNSIGNED NOT NULL,
    fecha_hora DATETIME NOT NULL,
    id_galpon TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY(id_aislamiento)
);

CREATE TABLE incidentes_generales (
    id_incidente INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    descripcion VARCHAR(255) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    id_finca INTEGER UNSIGNED NOT NULL,
    esta_resuelta BOOLEAN NOT NULL,
    PRIMARY KEY(id_incidente)
);

-- Ahora agregar todas las FOREIGN KEYS en el orden correcto
ALTER TABLE permisos
ADD FOREIGN KEY (id_modulo) REFERENCES modulos(id_modulo)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE permisos
ADD FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE usuarios
ADD FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE tareas
ADD FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ventas
ADD FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ventas
ADD FOREIGN KEY (tipo_pago) REFERENCES metodo_pago(id_tipo)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE galpones
ADD FOREIGN KEY (id_finca) REFERENCES fincas(id_finca)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ingreso_gallinas
ADD FOREIGN KEY (id_galpon) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE ingreso_gallinas
ADD FOREIGN KEY (id_tipo_gallina) REFERENCES tipo_gallinas(id_tipo_gallinas)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE produccion_huevos
ADD FOREIGN KEY (id_galpon) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE produccion_huevos
ADD FOREIGN KEY (id_tipo_huevo) REFERENCES tipo_huevos(id_tipo_huevo)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE stock
ADD FOREIGN KEY (id_produccion) REFERENCES produccion_huevos(id_produccion)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE detalle_huevos
ADD FOREIGN KEY (id_producto) REFERENCES stock(id_producto)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE detalle_huevos
ADD FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE salvamento
ADD FOREIGN KEY (id_galpon) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE salvamento
ADD FOREIGN KEY (id_tipo_gallina) REFERENCES tipo_gallinas(id_tipo_gallinas)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE detalle_salvamento
ADD FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE sensores
ADD FOREIGN KEY (id_tipo_sensor) REFERENCES tipo_sensores(id_tipo)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE sensores
ADD FOREIGN KEY (id_galpon) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE registro_sensores
ADD FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE inventario_finca
ADD FOREIGN KEY (id_categoria) REFERENCES categoria_inventario(id_categoria)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE inventario_finca
ADD FOREIGN KEY (id_finca) REFERENCES fincas(id_finca)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE incidentes_gallina
ADD FOREIGN KEY (galpon_origen) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE aislamiento
ADD FOREIGN KEY (id_incidente_gallina) REFERENCES incidentes_gallina(id_inc_gallina)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE aislamiento
ADD FOREIGN KEY (id_galpon) REFERENCES galpones(id_galpon)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE incidentes_generales
ADD FOREIGN KEY (id_finca) REFERENCES fincas(id_finca)
ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE usuarios ADD COLUMN estado BOOL DEFAULT TRUE;