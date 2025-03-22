from ViciosoPP_Conector_Python_23270050 import conectar_bd
from mysql.connector import Error

#######
# CRUD para la tabla Empleado
#######

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
        print("1️⃣ - Contratar empleado")
        print("2️⃣ - Ver todos los empleados")
        print("3️⃣ - Actualizar un empleado")
        print("4️⃣ - Destituir empleado")
        print("5️⃣ - Volver al menú principal")

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