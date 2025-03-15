import mysql.connector
from mysql.connector import Error

#######

# Angel Soto Perez - S5A - 23270050 - 05/03/2025
# De la linea 12 a 104 son los metodos para conexion
# 107 a 132 Uso del menu para ejecutar los metodos

#######

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='oracle',
            port=3306,
            database='Practica05_dbtaller_23270050'
        )
        if conexion.is_connected():
            print("Conexión exitosa")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_linea_investigacion():
    clave_inv = input("Ingrese la clave de la línea de investigación (Ej: L01): ").strip()
    nombre_linea = input("Ingrese el nombre de la línea de investigación: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Linea_Investigacion (clave_inv, nombre_linea) VALUES (%s, %s)"
            valores = (clave_inv, nombre_linea)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Línea de investigación creada exitosamente.")
        except Error as e:
            print(f"❌ Error al crear la línea de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

def leer_lineas_investigacion():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Linea_Investigacion")
            resultados = cursor.fetchall()
            if resultados:
                print("\n📋 Líneas de Investigación registradas:")
                for fila in resultados:
                    print(f"🔹 Clave: {fila[0]}, Nombre: {fila[1]}")
            else:
                print("⚠️ No hay líneas de investigación registradas.")
        except Error as e:
            print(f"❌ Error al leer las líneas de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_linea_investigacion():
    clave_inv = input("Ingrese la clave de la línea de investigación a actualizar: ").strip()
    nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Linea_Investigacion SET nombre_linea = %s WHERE clave_inv = %s"
            valores = (nuevo_nombre, clave_inv)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Línea de investigación actualizada exitosamente.")
            else:
                print("⚠️ No se encontró una línea de investigación con esa clave.")
        except Error as e:
            print(f"❌ Error al actualizar la línea de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_linea_investigacion():
    clave_inv = input("Ingrese la clave de la línea de investigación a eliminar: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Linea_Investigacion WHERE clave_inv = %s"
            valores = (clave_inv,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Línea de investigación eliminada exitosamente.")
            else:
                print("⚠️ No se encontró una línea de investigación con esa clave.")
        except Error as e:
            print(f"❌ Error al eliminar la línea de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

# Menú
def menu():
    while True:
        print("\n📌 MENÚ CRUD - Líneas de Investigación")
        print("C - Crear una nueva Línea de Investigación")
        print("R - Leer todas las Líneas de Investigación")
        print("U - Actualizar una Línea de Investigación")
        print("D - Eliminar una Línea de Investigación")
        print("S - Salir")

        opcion = input("Seleccione una opción: ").strip().upper()

        if opcion == 'C':
            crear_linea_investigacion()
        elif opcion == 'R':
            leer_lineas_investigacion()
        elif opcion == 'U':
            actualizar_linea_investigacion()
        elif opcion == 'D':
            eliminar_linea_investigacion()
        elif opcion == 'S':
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

menu()
