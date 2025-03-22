from ViciosoPP_Conector_Python_23270050 import conectar_bd
from mysql.connector import Error

# 📌 CRUD para la tabla Cliente
def crear_cliente():
    nombre = input("Ingrese el nombre del cliente: ").strip()
    apellido = input("Ingrese el apellido del cliente: ").strip()
    telefono = input("Ingrese el teléfono: ").strip()
    email = input("Ingrese el email: ").strip()
    direccion = input("Ingrese la dirección: ").strip()

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Cliente (nombre, apellido, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s)"
            valores = (nombre, apellido, telefono, email, direccion)
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"✅ Cliente '{nombre} {apellido}' agregado correctamente.")
        except Error as error:
            print(f"❌ Error al insertar el cliente: {error}")
        finally:
            cursor.close()
            conexion.close()

def leer_clientes():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()

            print("\n👥 Lista de clientes:")
            for cliente in clientes:
                print(f"🆔 {cliente[0]} | {cliente[1]} {cliente[2]} | 📞 {cliente[3]} | 📧 {cliente[4]}")
        except Error as error:
            print(f"❌ Error al leer los clientes: {error}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_cliente():
    id_cliente = int(input("Ingrese el ID del cliente a actualizar: "))
    nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
    nuevo_apellido = input("Ingrese el nuevo apellido: ").strip()
    nuevo_telefono = input("Ingrese el nuevo teléfono: ").strip()
    nuevo_email = input("Ingrese el nuevo email: ").strip()

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Cliente SET nombre = %s, apellido = %s, telefono = %s, email = %s WHERE id_cliente = %s"
            valores = (nuevo_nombre, nuevo_apellido, nuevo_telefono, nuevo_email, id_cliente)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Cliente actualizado exitosamente.")
            else:
                print("⚠️ No se encontró un cliente con ese ID.")
        except Error as error:
            print(f"❌ Error al actualizar el cliente: {error}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_cliente():
    id_cliente = int(input("Ingrese el ID del cliente a eliminar: "))

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Cliente WHERE id_cliente = %s"
            valores = (id_cliente,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Cliente eliminado exitosamente.")
            else:
                print("⚠️ No se encontró un cliente con ese ID.")
        except Error as error:
            print(f"❌ Error al eliminar el cliente: {error}")
        finally:
            cursor.close()
            conexion.close()

# 📌 Menú para gestión de clientes
def menu_cliente():
    while True:
        print("\n👥 MENÚ CRUD - Clientes en Vicioso++")
        print("1️⃣ - Crear un nuevo cliente")
        print("2️⃣ - Leer todos los clientes")
        print("3️⃣ - Actualizar un cliente")
        print("4️⃣ - Eliminar un cliente")
        print("5️⃣ - Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            crear_cliente()
        elif opcion == '2':
            leer_clientes()
        elif opcion == '3':
            actualizar_cliente()
        elif opcion == '4':
            eliminar_cliente()
        elif opcion == '5':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")
