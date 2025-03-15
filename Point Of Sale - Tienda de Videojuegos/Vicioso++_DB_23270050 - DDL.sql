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

-- Automaticamente se pondra la fecha y hora de mi dispositivo cuando se añada un campo en la tabla

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
    rol ENUM('Administrador', 'Cajero') NOT NULL,
    CONSTRAINT Define_a FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado)
);

