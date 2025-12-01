DROP DATABASE IF EXISTS ceramica_db;
CREATE DATABASE ceramica_db;
USE ceramica_db;

-- =========================
--  TABLE: usuarios
-- =========================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150),
    rol ENUM('cliente','artesano','administrador') NOT NULL,
    password VARCHAR(255)
);

-- =========================
--  TABLE: material
-- =========================
CREATE TABLE material (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('arcilla','pigmento','esmalte') NOT NULL
);

-- =========================
--  TABLE: inventario
-- =========================
CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    cantidad DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (material_id) REFERENCES material(id)
);

-- =========================
--  TABLE: pieza_ceramica
-- =========================
CREATE TABLE pieza_ceramica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    color VARCHAR(50),
    tipo VARCHAR(50),
    precio DECIMAL(10,2)
);

-- =========================
--  TABLE: pieza_personalizada
-- =========================
CREATE TABLE pieza_personalizada (
    id INT PRIMARY KEY,
    diseno_cliente TEXT,
    material_extra VARCHAR(100),
    FOREIGN KEY (id) REFERENCES pieza_ceramica(id)
);

-- =========================
--  TABLE: pedido
-- =========================
CREATE TABLE pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    artesano_id INT,
    estado VARCHAR(50) DEFAULT 'registrado',
    fecha DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (artesano_id) REFERENCES usuarios(id)
);

-- =========================
--  TABLE: pedido_pieza
-- =========================
CREATE TABLE pedido_pieza (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    pieza_id INT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (pieza_id) REFERENCES pieza_ceramica(id)
);

-- =========================
--  TABLE: historial_estado_pedido
-- =========================
CREATE TABLE historial_estado_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    estado VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedido(id)
);
