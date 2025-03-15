-- Ángel Soto Pérez - S5A - 23270050 - 15/03/2025
-- Point of Sale: Tienda de Videojuegos "Vicioso++" - Creacion de datos de ejemplo (DML)
-- \. C:\ABDS5A\Practicas - Git\Point Of Sale - Tienda de Videojuegos\Vicioso++_DB_23270050 - DML.sql

USE ViciosoPP;

-- Tablas Padre:

INSERT INTO Proveedor (nombre, contacto, telefono, email, direccion) VALUES
('Nintendo', 'Soporte Nintendo', '555-1234', 'contacto@nintendo.com', 'Tokio, Japón'),
('Sony', 'Distribuidor Sony', '555-5678', 'ventas@sony.com', 'California, EE.UU.'),
('Microsoft', 'Microsoft Store', '555-9999', 'support@microsoft.com', 'Washington, EE.UU.');

INSERT INTO Cliente (nombre, apellido, telefono, email, direccion) VALUES
('Carlos', 'Gómez', '5512345678', 'carlosgomez@email.com', 'CDMX, México'),
('Ana', 'López', '5598765432', 'analopez@email.com', 'Guadalajara, México'),
('Miguel', 'Hernández', '5587654321', 'miguelh@email.com', 'Monterrey, México');

INSERT INTO CategoriaProducto (nombre, descripcion) VALUES
('Videojuegos', 'Juegos físicos y digitales para consolas y PC'),
('Consolas', 'Consolas de última generación y modelos retro'),
('Accesorios', 'Mandos, audífonos, cargadores y más');

INSERT INTO Sucursal (nombre, direccion, telefono) VALUES
('Sucursal Centro', 'Av. Reforma #123, CDMX', '5512345678'),
('Sucursal Norte', 'Blvd. Insurgentes #45, Monterrey', '5598765432');

-- La fecha y hora se ponen en automatico 

-- Tablas Hijas

INSERT INTO Empleado (nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal) VALUES
('Jorge', 'Martínez', '5587412589', 'jorge.martinez@email.com', 'CDMX, México', 'Cajero', 12000.00, '2024-01-15', 1),
('María', 'Sánchez', '5578963214', 'maria.sanchez@email.com', 'Monterrey, México', 'Administrador', 18000.00, '2023-11-20', 2);

INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria, id_proveedor) VALUES
('The Legend of Zelda: Breath of the Wild', 'Juego para Nintendo Switch', 1299.99, 50, 1, 1),
('PlayStation 5', 'Consola de última generación de Sony', 11999.99, 20, 2, 2),
('Xbox Series X', 'Consola de última generación de Microsoft', 11999.99, 15, 2, 3),
('Control DualSense', 'Control inalámbrico para PS5', 1799.99, 40, 3, 2);

-- Insertar Inventario
INSERT INTO Inventario (id_producto, cantidad, id_sucursal) VALUES
(1, 10, 1),
(2, 5, 1),
(3, 4, 2),
(4, 8, 2);

INSERT INTO Venta (id_cliente, id_empleado, total) VALUES
(1, 1, 1299.99), 
(2, 2, 11999.99); 
-- Ejemplo: Cliente 2 compró un PS5

INSERT INTO DetalleVenta (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 1299.99, 1299.99),
(2, 2, 1, 11999.99, 11999.99);

INSERT INTO Pago (id_venta, metodo_pago, monto) VALUES
(1, 'Efectivo', 1299.99),
(2, 'Tarjeta Crédito', 11999.99);

INSERT INTO Usuario (id_empleado, username, password_hash, rol) VALUES
(1, 'jorge123', 'contraseña1', 'Cajero'),
(2, 'maria_admin', 'contraseña2', 'Administrador');


