from db_connector import conectar_bd
from mysql.connector import Error
import re

# Inicio: Para interfaz flet

def obtener_empleados():
    """Obtiene todos los empleados para mostrar en la tabla"""
    conexion = conectar_bd()
    empleados = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT e.id_empleado as id, e.nombre, e.apellido, e.telefono, e.email, 
                       e.puesto, e.salario, e.fecha_contratacion, s.nombre as sucursal
                FROM Empleado e
                JOIN Sucursal s ON e.id_sucursal = s.id_sucursal
            """)
            empleados = cursor.fetchall()
        except Error as error:
            print(f"❌ Error al obtener empleados: {error}")
        finally:
            cursor.close()
            conexion.close()
    return empleados

def crear_empleado_backend(nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal):
    """Crea un nuevo empleado en la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar email único
            cursor.execute("SELECT id_empleado FROM Empleado WHERE email = %s", (email,))
            if cursor.fetchone():
                print("❌ Ya existe un empleado con este email")
                return False
                
            # Validar formato email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                print("❌ Formato de email inválido")
                return False

            sql = """
            INSERT INTO Empleado 
            (nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Empleado creado correctamente.")
            return True
        except Error as error:
            print(f"❌ Error al crear empleado: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def obtener_empleado_por_id(id_empleado):
    """Obtiene un empleado específico por su ID"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_empleado, nombre, apellido, telefono, email, direccion, 
                       puesto, salario, fecha_contratacion, id_sucursal 
                FROM Empleado WHERE id_empleado = %s
            """, (id_empleado,))
            empleado = cursor.fetchone()
            return empleado
        except Error as error:
            print(f"❌ Error al obtener empleado: {error}")
            return None
        finally:
            cursor.close()
            conexion.close()
    return None

def actualizar_empleado_backend(id_empleado, nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal):
    """Actualiza los datos de un empleado existente"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar email único (excluyendo al empleado actual)
            cursor.execute(
                "SELECT id_empleado FROM Empleado WHERE email = %s AND id_empleado != %s", 
                (email, id_empleado)
            )
            if cursor.fetchone():
                print("❌ Ya existe otro empleado con este email")
                return False
                
            # Validar formato email
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                print("❌ Formato de email inválido")
                return False

            sql = """
            UPDATE Empleado 
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, 
                direccion = %s, puesto = %s, salario = %s, 
                fecha_contratacion = %s, id_sucursal = %s 
            WHERE id_empleado = %s
            """
            valores = (
                nombre, apellido, telefono, email, direccion, 
                puesto, salario, fecha_contratacion, id_sucursal, 
                id_empleado
            )
            cursor.execute(sql, valores)
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al actualizar empleado: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

def eliminar_empleado_backend(id_empleado):
    """Elimina un empleado de la base de datos"""
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Verificar si el empleado existe
            cursor.execute("SELECT id_empleado FROM Empleado WHERE id_empleado = %s", (id_empleado,))
            if not cursor.fetchone():
                return False
            
            # Eliminar al empleado
            cursor.execute("DELETE FROM Empleado WHERE id_empleado = %s", (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"❌ Error al eliminar empleado: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
    return False

# Fin: Para interfaz flet

# ➕ Crear un nuevo empleado
def crear_empleado():
    nombre = input("Ingrese el nombre del empleado: ").strip()
    apellido = input("Ingrese el apellido del empleado: ").strip()
    telefono = input("Ingrese el teléfono: ").strip()
    email = input("Ingrese el correo electrónico: ").strip()
    direccion = input("Ingrese la dirección: ").strip()
    puesto = input("Ingrese el puesto: ").strip()
    salario = float(input("Ingrese el salario: "))
    fecha_contratacion = input("Ingrese la fecha de contratación (YYYY-MM-DD): ").strip()
    id_sucursal = int(input("Ingrese el ID de la sucursal: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Empleado (nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal)
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"✅ Empleado '{nombre} {apellido}' agregado correctamente.")
        except Error as error:
            print(f"❌ Error al insertar el empleado: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📚 Leer todos los empleados
def leer_empleados():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Empleado")
            empleados = cursor.fetchall()

            print("\n👥 Lista de empleados:")
            for emp in empleados:
                print(f"🆔 {emp[0]} | {emp[1]} {emp[2]} | 📧 {emp[4]} | 📞 {emp[3]} | {emp[5]} | 💼 {emp[6]} | 💲 {emp[7]}")
        except Error as error:
            print(f"❌ Error al leer los empleados: {error}")
        finally:
            cursor.close()
            conexion.close()

# ✏️ Actualizar un empleado
def actualizar_empleado():
    id_empleado = int(input("Ingrese el ID del empleado a actualizar: "))
    nuevo_telefono = input("Ingrese el nuevo teléfono: ").strip()
    nuevo_email = input("Ingrese el nuevo correo electrónico: ").strip()
    nuevo_puesto = input("Ingrese el nuevo puesto: ").strip()
    nuevo_salario = float(input("Ingrese el nuevo salario: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Empleado SET telefono = %s, email = %s, puesto = %s, salario = %s WHERE id_empleado = %s"
            valores = (nuevo_telefono, nuevo_email, nuevo_puesto, nuevo_salario, id_empleado)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Empleado actualizado exitosamente.")
            else:
                print("⚠️ No se encontró un empleado con ese ID.")
        except Error as error:
            print(f"❌ Error al actualizar el empleado: {error}")
        finally:
            cursor.close()
            conexion.close()

# 🗑️ Eliminar un empleado
def eliminar_empleado():
    id_empleado = int(input("Ingrese el ID del empleado a eliminar: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Empleado WHERE id_empleado = %s"
            valores = (id_empleado,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Empleado eliminado exitosamente.")
            else:
                print("⚠️ No se encontró un empleado con ese ID.")
        except Error as error:
            print(f"❌ Error al eliminar el empleado: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📌 Menú para gestión de empleados
def menu_empleado():
    while True:
        print("\n📦 MENÚ CRUD - Empleados en Vicioso++")
        print("1.- Contratar empleado")
        print("2.- Ver todos los empleados")
        print("3.- Modificar datos de un empleado")
        print("4.- Destituir empleado")
        print("5.- Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_empleado()
        elif opcion == '2':
            leer_empleados()
        elif opcion == '3':
            actualizar_empleado()
        elif opcion == '4':
            eliminar_empleado()
        elif opcion == '5':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")