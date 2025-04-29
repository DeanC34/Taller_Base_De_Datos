from db_connector import conectar_bd
from mysql.connector import Error
import re
#######
# CRUD para la tabla Venta
#######

# En crud_venta.py - Funciones para la interfaz Flet

def obtener_ventas():
    """Obtiene todas las ventas para mostrar en la tabla"""
    conexion = conectar_bd()
    ventas = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id_venta as id, 
                       CONCAT(c.nombre, ' ', c.apellido) as cliente,
                       CONCAT(e.nombre, ' ', e.apellido) as empleado,
                       v.fecha, 
                       v.total
                FROM Venta v
                JOIN Cliente c ON v.id_cliente = c.id_cliente
                JOIN Empleado e ON v.id_empleado = e.id_empleado
                ORDER BY v.fecha DESC
            """)
            ventas = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener ventas: {error}")
        finally:
            cursor.close()
            conexion.close()
    return ventas

def crear_venta_backend(id_cliente, id_empleado, total):
    """Crea una nueva venta en la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar que cliente y empleado existan
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = %s", (id_cliente,))
            if not cursor.fetchone():
                print("❌ Cliente no encontrado")
                return False
                
            cursor.execute("SELECT id_empleado FROM Empleado WHERE id_empleado = %s", (id_empleado,))
            if not cursor.fetchone():
                print("❌ Empleado no encontrado")
                return False

            sql = "INSERT INTO Venta (id_cliente, id_empleado, total) VALUES (%s, %s, %s)"
            valores = (id_cliente, id_empleado, total)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Venta creada correctamente.")
            return True
        except Error as error:
            print(f"❌ Error al crear venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_venta_por_id(id_venta):
    """Obtiene una venta específica por su ID"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.id_venta, v.id_cliente, v.id_empleado, v.total, v.fecha,
                       CONCAT(c.nombre, ' ', c.apellido) as cliente,
                       CONCAT(e.nombre, ' ', e.apellido) as empleado
                FROM Venta v
                JOIN Cliente c ON v.id_cliente = c.id_cliente
                JOIN Empleado e ON v.id_empleado = e.id_empleado
                WHERE v.id_venta = %s
            """, (id_venta,))
            venta = cursor.fetchone()
            return venta
        except Error as error:
            print(f"❌ Error al obtener venta: {error}")
            return None
        finally:
            cursor.close()
            conexion.close()
    return None

def actualizar_venta_backend(id_venta, id_cliente, id_empleado, total):
    """Actualiza los datos de una venta existente"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar que cliente y empleado existan
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = %s", (id_cliente,))
            if not cursor.fetchone():
                print("❌ Cliente no encontrado")
                return False
                
            cursor.execute("SELECT id_empleado FROM Empleado WHERE id_empleado = %s", (id_empleado,))
            if not cursor.fetchone():
                print("❌ Empleado no encontrado")
                return False

            sql = """
            UPDATE Venta 
            SET id_cliente = %s, id_empleado = %s, total = %s 
            WHERE id_venta = %s
            """
            valores = (id_cliente, id_empleado, total, id_venta)
            cursor.execute(sql, valores)
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al actualizar venta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_clientes_para_dropdown():
    """Obtiene clientes para dropdown"""
    conexion = conectar_bd()
    clientes = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_cliente as id, CONCAT(nombre, ' ', apellido) as nombre 
                FROM Cliente
                ORDER BY nombre
            """)
            clientes = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener clientes: {error}")
        finally:
            cursor.close()
            conexion.close()
    return clientes

def obtener_empleados_para_dropdown():
    """Obtiene empleados para dropdown"""
    conexion = conectar_bd()
    empleados = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_empleado as id, CONCAT(nombre, ' ', apellido) as nombre 
                FROM Empleado
                ORDER BY nombre
            """)
            empleados = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener empleados: {error}")
        finally:
            cursor.close()
            conexion.close()
    return empleados

def eliminar_venta_backend(id_venta):
    """Elimina una venta de la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Verificar si la venta existe
            cursor.execute("SELECT id_venta FROM Venta WHERE id_venta = %s", (id_venta,))
            if not cursor.fetchone():
                return False
            
            # Eliminar la venta
            cursor.execute("DELETE FROM Venta WHERE id_venta = %s", (id_venta,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al eliminar venta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

# ➕ Crear una nueva venta
def crear_venta():
    id_cliente = int(input("Ingrese el ID del cliente: "))
    id_empleado = int(input("Ingrese el ID del empleado: "))
    total = float(input("Ingrese el total de la venta: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Venta (id_cliente, id_empleado, total) VALUES (%s, %s, %s)"
            valores = (id_cliente, id_empleado, total)
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"✅ Venta registrada correctamente con ID {cursor.lastrowid}.")
        except Error as error:
            print(f"❌ Error al registrar la venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📚 Leer todas las ventas
def leer_ventas():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT v.id_venta, c.nombre, c.apellido, e.nombre, e.apellido, v.fecha, v.total
                FROM Venta v
                JOIN Cliente c ON v.id_cliente = c.id_cliente
                JOIN Empleado e ON v.id_empleado = e.id_empleado
            """)
            ventas = cursor.fetchall()

            print("\n🧾 Lista de ventas registradas:")
            for v in ventas:
                print(f"🆔 Venta {v[0]} | Cliente: {v[1]} {v[2]} | Empleado: {v[3]} {v[4]} | 📅 Fecha: {v[5]} | 💲 Total: {v[6]}")
        except Error as error:
            print(f"❌ Error al leer las ventas: {error}")
        finally:
            cursor.close()
            conexion.close()

# ✏️ Actualizar una venta
def actualizar_venta():
    id_venta = int(input("Ingrese el ID de la venta a actualizar: "))
    nuevo_total = float(input("Ingrese el nuevo total: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Venta SET total = %s WHERE id_venta = %s"
            valores = (nuevo_total, id_venta)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Venta actualizada exitosamente.")
            else:
                print("⚠️ No se encontró una venta con ese ID.")
        except Error as error:
            print(f"❌ Error al actualizar la venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 🗑️ Eliminar una venta
def eliminar_venta():
    id_venta = int(input("Ingrese el ID de la venta a eliminar: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Venta WHERE id_venta = %s"
            valores = (id_venta,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Venta eliminada exitosamente.")
            else:
                print("⚠️ No se encontró una venta con ese ID.")
        except Error as error:
            print(f"❌ Error al eliminar la venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📌 Menú para gestión de ventas
def menu_venta():
    while True:
        print("\n🧾 MENÚ CRUD - Ventas en Vicioso++")
        print("1️.- Registrar nueva venta")
        print("2️.- Ver todas las ventas")
        print("3️.- Actualizar una venta")
        print("4️.- Eliminar una venta")
        print("5️.- Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_venta()
        elif opcion == '2':
            leer_ventas()
        elif opcion == '3':
            actualizar_venta()
        elif opcion == '4':
            eliminar_venta()
        elif opcion == '5':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")
