from ViciosoPP_Conector_Python_23270050 import conectar_bd
from mysql.connector import Error

#######
# CRUD para la tabla Venta
#######

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
        print("1️⃣ - Registrar nueva venta")
        print("2️⃣ - Ver todas las ventas")
        print("3️⃣ - Actualizar una venta")
        print("4️⃣ - Eliminar una venta")
        print("5️⃣ - Volver al menú principal")

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
