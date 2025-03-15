import mysql.connector
from mysql.connector import Error

#######
# Ángel Soto Pérez - S5A - 23270050 - 15/03/2025
# CRUD para el POS "Vicioso++" con conexión a MySQL
#######

# 🔗 Función para conectar a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # Cambia si usas otro host
            user="root",             # Tu usuario de MySQL
            password="tu_contraseña", # Tu contraseña de MySQL
            database="ViciosoPP"     # La base de datos del POS
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conexion
    except Error as error:
        print(f"❌ Error al conectar con MySQL: {error}")
        return None

# 📌 CRUD para la tabla Producto
def crear_producto():
    nombre = input("Ingrese el nombre del producto: ").strip()
    descripcion = input("Ingrese la descripción del producto: ").strip()
    precio = float(input("Ingrese el precio del producto: "))
    stock = int(input("Ingrese el stock inicial: "))
    id_categoria = int(input("Ingrese el ID de la categoría: "))
    id_proveedor = int(input("Ingrese el ID del proveedor: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
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

# 📌 Menú principal
def menu():
    while True:
        print("\n🎮 MENÚ CRUD - Productos en Vicioso++")
        print("1️⃣ - Crear un nuevo producto")
        print("2️⃣ - Leer todos los productos")
        print("3️⃣ - Actualizar un producto")
        print("4️⃣ - Eliminar un producto")
        print("5️⃣ - Salir")

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
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

# 🏁 Ejecutar el menú
menu()
