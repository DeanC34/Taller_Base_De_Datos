from db_connector import conectar_bd
from mysql.connector import Error

# 📌 CRUD para la tabla Producto
def crear_producto():
    nombre = input("Ingrese el nombre del producto: ").strip()
    descripcion = input("Ingrese la descripción del producto: ").strip()
    precio = float(input("Ingrese el precio del producto: "))
    stock = int(input("Ingrese el stock inicial: "))
    id_categoria = int(input("(1.- Videojuegos, 2.-Consolas, 3.- Accesorios) \n Ingrese el ID de la categoría: "))
    id_proveedor = int(input("Ingrese el ID del proveedor: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar existencia de id_categoria e id_proveedor
            cursor.execute("SELECT id_categoria FROM CategoriaProducto WHERE id_categoria = %s", (id_categoria,))
            if cursor.fetchone() is None:
                print("⚠️ La categoría no existe. Verifique el ID.")
                return

            cursor.execute("SELECT id_proveedor FROM Proveedor WHERE id_proveedor = %s", (id_proveedor,))
            if cursor.fetchone() is None:
                print("⚠️ El proveedor no existe. Verifique el ID.")
                return

            sql = "INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria, id_proveedor) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (nombre, descripcion, precio, stock, id_categoria, id_proveedor)
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"✅ Producto '{nombre}' agregado correctamente.")
        except Error as error:
            print(f"❌ Error al insertar el producto: {error}")
        finally:
            cursor.close()
            conexion.close()

def leer_productos():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Producto")
            productos = cursor.fetchall()

            print("\n📦 Lista de productos:")
            for producto in productos:
                print(f"🆔 {producto[0]} | {producto[1]} | 💲 {producto[3]} | 🏷️ Stock: {producto[4]}")
        except Error as error:
            print(f"❌ Error al leer los productos: {error}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_producto_backend(id_producto, nombre, precio, stock, id_categoria, id_proveedor):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Validar existencia de categoría y proveedor
            cursor.execute("SELECT id_categoria FROM CategoriaProducto WHERE id_categoria = %s", (id_categoria,))
            if cursor.fetchone() is None:
                print("⚠️ La categoría no existe.")
                return

            cursor.execute("SELECT id_proveedor FROM Proveedor WHERE id_proveedor = %s", (id_proveedor,))
            if cursor.fetchone() is None:
                print("⚠️ El proveedor no existe.")
                return

            sql = """
            UPDATE Producto 
            SET nombre = %s, precio = %s, stock = %s, id_categoria = %s, id_proveedor = %s 
            WHERE id_producto = %s
            """
            valores = (nombre, precio, stock, id_categoria, id_proveedor, id_producto)
            cursor.execute(sql, valores)
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"✅ Producto con ID {id_producto} actualizado correctamente.")
            else:
                print("⚠️ No se encontró un producto con ese ID.")
        except Error as e:
            print(f"❌ Error al actualizar el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

# Inicio: Para flet

def obtener_productos():
    conexion = conectar_bd()
    productos = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, descripcion, precio, stock FROM Producto")
            resultado = cursor.fetchall()
            for fila in resultado:
                productos.append({
                    "id": fila[0],
                    "nombre": fila[1],
                    "descripcion": fila[2],
                    "precio": fila[3],
                    "stock": fila[4]
                })
        except Error as error:
            print(f"❌ Error al obtener los productos: {error}")
        finally:
            cursor.close()
            conexion.close()
    return productos

def crear_producto_backend(nombre, precio, stock, id_categoria, id_proveedor):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Validar existencia de categoría y proveedor
            cursor.execute("SELECT id_categoria FROM CategoriaProducto WHERE id_categoria = %s", (id_categoria,))
            if cursor.fetchone() is None:
                print("⚠️ La categoría no existe.")
                return

            cursor.execute("SELECT id_proveedor FROM Proveedor WHERE id_proveedor = %s", (id_proveedor,))
            if cursor.fetchone() is None:
                print("⚠️ El proveedor no existe.")
                return

            sql = "INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria, id_proveedor) VALUES (%s, '', %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, precio, stock, id_categoria, id_proveedor))
            conexion.commit()
            print("✅ Producto creado correctamente")
        except Error as e:
            print(f"❌ Error al crear el producto: {e}")
        finally:
            cursor.close()
            conexion.close()

def obtener_producto_por_id(id_producto):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    consulta = "SELECT id_producto, nombre, precio, stock, id_categoria, id_proveedor FROM Producto WHERE id_producto = %s"
    cursor.execute(consulta, (id_producto,))
    producto = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    return producto

def eliminar_producto_backend(id_producto):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Verificar si el producto existe
            cursor.execute("SELECT id_producto FROM Producto WHERE id_producto = %s", (id_producto,))
            if not cursor.fetchone():
                return False
            
            # Eliminar el producto
            cursor.execute("DELETE FROM Producto WHERE id_producto = %s", (id_producto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

# Fin de: Para flet

def actualizar_producto():
    id_producto = int(input("Ingrese el ID del producto a actualizar: "))
    nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
    nuevo_precio = float(input("Ingrese el nuevo precio: "))
    nuevo_stock = int(input("Ingrese el nuevo stock: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Producto SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
            valores = (nuevo_nombre, nuevo_precio, nuevo_stock, id_producto)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Producto actualizado exitosamente.")
            else:
                print("⚠️ No se encontró un producto con ese ID.")
        except Error as error:
            print(f"❌ Error al actualizar el producto: {error}")
        finally:
            cursor.close()
            conexion.close()


def eliminar_producto():
    id_producto = int(input("Ingrese el ID del producto a eliminar: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Producto WHERE id_producto = %s"
            valores = (id_producto,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Producto eliminado exitosamente.")
            else:
                print("⚠️ No se encontró un producto con ese ID.")
        except Error as error:
            print(f"❌ Error al eliminar el producto: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📌 Menú para gestión de productos
def menu_producto():
    while True:
        print("\n📦 MENÚ CRUD - Productos en Vicioso++")
        print("1️.- Crear un nuevo producto")
        print("2️.- Leer todos los productos")
        print("3️.- Actualizar un producto")
        print("4️.- Eliminar un producto")
        print("5️.- Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_producto()
        elif opcion == '2':
            leer_productos()
        elif opcion == '3':
            actualizar_producto()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")
