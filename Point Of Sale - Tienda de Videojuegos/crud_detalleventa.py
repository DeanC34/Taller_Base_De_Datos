from ViciosoPP_Conector_Python_23270050 import conectar_bd
from mysql.connector import Error

#######
# CRUD para la tabla DetalleVenta
#######

# ➕ Crear un nuevo detalle de venta
def crear_detalle_venta():
    id_venta = int(input("Ingrese el ID de la venta: "))
    id_producto = int(input("Ingrese el ID del producto: "))
    cantidad = int(input("Ingrese la cantidad: "))
    precio_unitario = float(input("Ingrese el precio unitario del producto: "))

    subtotal = cantidad * precio_unitario

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO DetalleVenta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (id_venta, id_producto, cantidad, precio_unitario, subtotal)
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"✅ Detalle de venta registrado correctamente con ID {cursor.lastrowid}.")
        except Error as error:
            print(f"❌ Error al registrar el detalle de venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📚 Leer todos los detalles de una venta
def leer_detalles_venta():
    id_venta = int(input("Ingrese el ID de la venta para ver los detalles: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT d.id_detalle, p.nombre, d.cantidad, d.precio_unitario, d.subtotal
                FROM DetalleVenta d
                JOIN Producto p ON d.id_producto = p.id_producto
                WHERE d.id_venta = %s
            """, (id_venta,))
            detalles = cursor.fetchall()

            if detalles:
                print(f"\n🧾 Detalles de la venta {id_venta}:")
                for d in detalles:
                    print(f"🆔 Detalle {d[0]} | Producto: {d[1]} | 📦 Cantidad: {d[2]} | 💲 Precio Unitario: {d[3]} | 🧮 Subtotal: {d[4]}")
            else:
                print("⚠️ No hay detalles para esta venta.")
        except Error as error:
            print(f"❌ Error al leer los detalles de la venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# ✏️ Actualizar un detalle de venta
def actualizar_detalle_venta():
    id_detalle = int(input("Ingrese el ID del detalle de venta a actualizar: "))
    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
    nuevo_precio_unitario = float(input("Ingrese el nuevo precio unitario: "))

    nuevo_subtotal = nueva_cantidad * nuevo_precio_unitario

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE DetalleVenta
                SET cantidad = %s, precio_unitario = %s, subtotal = %s
                WHERE id_detalle = %s
            """
            valores = (nueva_cantidad, nuevo_precio_unitario, nuevo_subtotal, id_detalle)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Detalle de venta actualizado exitosamente.")
            else:
                print("⚠️ No se encontró un detalle de venta con ese ID.")
        except Error as error:
            print(f"❌ Error al actualizar el detalle de venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 🗑️ Eliminar un detalle de venta
def eliminar_detalle_venta():
    id_detalle = int(input("Ingrese el ID del detalle de venta a eliminar: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM DetalleVenta WHERE id_detalle = %s"
            valores = (id_detalle,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Detalle de venta eliminado exitosamente.")
            else:
                print("⚠️ No se encontró un detalle de venta con ese ID.")
        except Error as error:
            print(f"❌ Error al eliminar el detalle de venta: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📌 Menú para gestión de detalles de venta
def menu_detalle_venta():
    while True:
        print("\n📦 MENÚ CRUD - Detalles de Venta en Vicioso++")
        print("1️⃣ - Registrar nuevo detalle de venta")
        print("2️⃣ - Ver detalles de una venta")
        print("3️⃣ - Actualizar un detalle de venta")
        print("4️⃣ - Eliminar un detalle de venta")
        print("5️⃣ - Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_detalle_venta()
        elif opcion == '2':
            leer_detalles_venta()
        elif opcion == '3':
            actualizar_detalle_venta()
        elif opcion == '4':
            eliminar_detalle_venta()
        elif opcion == '5':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")
