-- Ángel Soto Pérez - S5A - 23270050 - 15/03/2025
-- Point of Sale: Tienda de Videojuegos "Vicioso++" - Creacion de la Base de datos (DDL)
-- \. C:\ABDS5A\Practicas - Git\Point Of Sale - Tienda de Videojuegos\Vicioso++_DB_23270050 - DDL.sql

DROP DATABASE IF EXISTS ViciosoPP;
CREATE DATABASE ViciosoPP;
USE ViciosoPP;

-- Tablas Padre:

CREATE TABLE Proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CategoriaProducto (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE Sucursal (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20)
);

-- Tabla para Roles: Administrador, Cajero, Cliente
CREATE TABLE Rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE, 
    descripcion TEXT
);

-- Tablas Hijas

CREATE TABLE Empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccion TEXT,
    puesto VARCHAR(50),
    salario DECIMAL(10,2),
    fecha_contratacion DATE,
    id_sucursal INT,
    CONSTRAINT Pertenece_a_una FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id_sucursal)
);

CREATE TABLE Producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    id_categoria INT,
    id_proveedor INT,
    CONSTRAINT Pertenece FOREIGN KEY (id_categoria) REFERENCES CategoriaProducto(id_categoria),
    CONSTRAINT Es_Suministrado FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor)
);

CREATE TABLE Inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    cantidad INT DEFAULT 0,
    id_sucursal INT,
    CONSTRAINT Almacena FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT Esta_Ubicado FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id_sucursal)
);

CREATE TABLE Venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_empleado INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    CONSTRAINT Adquiere FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    CONSTRAINT Realiza FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado)
);

CREATE TABLE DetalleVenta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    id_producto INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    CONSTRAINT Detalla_una FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
    CONSTRAINT Contiene FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

CREATE TABLE Pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    metodo_pago ENUM('Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia') NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    CONSTRAINT Realiza_Transaccion FOREIGN KEY (id_venta) REFERENCES Venta(id_venta)
);

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT,  
    CONSTRAINT Define_a FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado),
    CONSTRAINT Tiene_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE MatrizDerechos (
    id_derecho INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT,
    modulo VARCHAR(50) NOT NULL, -- Módulo o funcionalidad
    permiso ENUM('Lectura', 'Escritura', 'Modificación', 'Eliminación') NOT NULL,
    CONSTRAINT Asigna_derecho FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

-- Inserción 
INSERT INTO Rol (nombre_rol, descripcion) VALUES
('Administrador', 'Acceso completo al sistema'),
('Cajero', 'Gestiona ventas e inventario'),
('Cliente', 'Visualización de sus compras');

INSERT INTO MatrizDerechos (id_rol, modulo, permiso) VALUES
(1, 'Ventas', 'Escritura'),
(1, 'Inventario', 'Modificación'),
(1, 'Usuarios', 'Escritura'),
(2, 'Ventas', 'Escritura'),
(2, 'Inventario', 'Lectura'),
(3, 'Compras', 'Lectura');

-- Creación de Usuarios

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
GRANT ALL PRIVILEGES ON ViciosoPP.* TO 'admin'@'localhost' WITH GRANT OPTION;

CREATE USER 'cajero'@'localhost' IDENTIFIED BY 'cajero_pass';
GRANT SELECT, INSERT, UPDATE ON ViciosoPP.* TO 'cajero'@'localhost';

CREATE USER 'cliente'@'localhost' IDENTIFIED BY 'cliente_pass';
GRANT SELECT ON ViciosoPP.* TO 'cliente'@'localhost';

-- Aplicar
FLUSH PRIVILEGES;
