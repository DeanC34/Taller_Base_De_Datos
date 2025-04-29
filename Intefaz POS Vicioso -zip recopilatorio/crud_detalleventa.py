from db_connector import conectar_bd
from mysql.connector import Error

#######
# CRUD para la tabla DetalleVenta
#######

# En crud_detalleventa.py - Funciones para la interfaz Flet

def obtener_detalles_venta(id_venta=None):
    """Obtiene todos los detalles de venta para mostrar en la tabla"""
    conexion = conectar_bd()
    detalles = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            if id_venta:
                cursor.execute("""
                    SELECT d.id_detalle as id, p.nombre as producto, d.cantidad, 
                           d.precio_unitario, d.subtotal, v.id_venta
                    FROM DetalleVenta d
                    JOIN Producto p ON d.id_producto = p.id_producto
                    JOIN Venta v ON d.id_venta = v.id_venta
                    WHERE d.id_venta = %s
                """, (id_venta,))
            else:
                cursor.execute("""
                    SELECT d.id_detalle as id, p.nombre as producto, d.cantidad, 
                           d.precio_unitario, d.subtotal, v.id_venta
                    FROM DetalleVenta d
                    JOIN Producto p ON d.id_producto = p.id_producto
                    JOIN Venta v ON d.id_venta = v.id_venta
                """)
            detalles = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener detalles de venta: {error}")
        finally:
            cursor.close()
            conexion.close()
    return detalles

def crear_detalle_venta_backend(id_venta, id_producto, cantidad, precio_unitario):
    """Crea un nuevo detalle de venta en la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar que venta y producto existan
            cursor.execute("SELECT id_venta FROM Venta WHERE id_venta = %s", (id_venta,))
            if not cursor.fetchone():
                print("❌ Venta no encontrada")
                return False
                
            cursor.execute("SELECT id_producto FROM Producto WHERE id_producto = %s", (id_producto,))
            if not cursor.fetchone():
                print("❌ Producto no encontrado")
                return False

            subtotal = cantidad * precio_unitario
            sql = """
            INSERT INTO DetalleVenta 
            (id_venta, id_producto, cantidad, precio_unitario, subtotal) 
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (id_venta, id_producto, cantidad, precio_unitario, subtotal)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Detalle de venta creado correctamente.")
            return cursor.lastrowid  # Retornar el ID del detalle creado
        except Error as error:
            print(f"❌ Error al crear detalle de venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_detalle_por_id(id_detalle):
    """Obtiene un detalle de venta específico por su ID"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT d.id_detalle, d.id_venta, d.id_producto, d.cantidad, 
                       d.precio_unitario, d.subtotal, p.nombre as producto
                FROM DetalleVenta d
                JOIN Producto p ON d.id_producto = p.id_producto
                WHERE d.id_detalle = %s
            """, (id_detalle,))
            detalle = cursor.fetchone()
            return detalle
        except Error as error:
            print(f"❌ Error al obtener detalle de venta: {error}")
            return None
        finally:
            cursor.close()
            conexion.close()
    return None

def actualizar_detalle_venta_backend(id_detalle, id_venta, id_producto, cantidad, precio_unitario):
    """Actualiza los datos de un detalle de venta existente"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar que venta y producto existan
            cursor.execute("SELECT id_venta FROM Venta WHERE id_venta = %s", (id_venta,))
            if not cursor.fetchone():
                print("❌ Venta no encontrada")
                return False
                
            cursor.execute("SELECT id_producto FROM Producto WHERE id_producto = %s", (id_producto,))
            if not cursor.fetchone():
                print("❌ Producto no encontrado")
                return False

            subtotal = cantidad * precio_unitario
            sql = """
            UPDATE DetalleVenta 
            SET id_venta = %s, id_producto = %s, cantidad = %s, 
                precio_unitario = %s, subtotal = %s 
            WHERE id_detalle = %s
            """
            valores = (id_venta, id_producto, cantidad, precio_unitario, subtotal, id_detalle)
            cursor.execute(sql, valores)
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al actualizar detalle de venta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def eliminar_detalle_venta_backend(id_detalle):
    """Elimina un detalle de venta de la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Verificar si el detalle existe
            cursor.execute("SELECT id_detalle FROM DetalleVenta WHERE id_detalle = %s", (id_detalle,))
            if not cursor.fetchone():
                return False
            
            # Eliminar el detalle
            cursor.execute("DELETE FROM DetalleVenta WHERE id_detalle = %s", (id_detalle,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al eliminar detalle de venta: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_ventas_para_dropdown():
    """Obtiene ventas para dropdown"""
    conexion = conectar_bd()
    ventas = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_venta as id, CONCAT('Venta #', id_venta) as nombre 
                FROM Venta
                ORDER BY id_venta DESC
            """)
            ventas = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener ventas: {error}")
        finally:
            cursor.close()
            conexion.close()
    return ventas

def obtener_productos_para_dropdown():
    """Obtiene productos para dropdown"""
    conexion = conectar_bd()
    productos = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_producto as id, nombre 
                FROM Producto
                ORDER BY nombre
            """)
            productos = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener productos: {error}")
        finally:
            cursor.close()
            conexion.close()
    return productos

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
        print("1.- Registrar nuevo detalle de venta")
        print("2️.- Ver detalles de una venta")
        print("3️.- Actualizar un detalle de venta")
        print("4️.- Eliminar un detalle de venta")
        print("5️.- Volver al menú principal")

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
