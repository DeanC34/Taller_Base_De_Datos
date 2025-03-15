import mysql.connector
from mysql.connector import Error
# https://github.com/DeanC34/devasc-study-team
#######

# Angel Soto Perez - S5A - 23270050 - 10/03/2025
# De la linea 12 a 98 son los metodos para conexion
# 100 a 139 Uso de los menu para ejecutar los metodos

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

def crear_profesor():
    clave_profesor = input("Clave del profesor: ").strip()
    nombre_profesor = input("Nombre del profesor: ").strip()
    rubrica_id = input("Rubrica ID: ").strip()
    rubrica_area_conocimiento_id = input("Área Conocimiento ID: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Profesor (clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id) VALUES (%s, %s, %s, %s)"
            valores = (clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Profesor creado exitosamente.")
        except Error as e:
            print(f"❌ Error al crear el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

def leer_profesores():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Profesor")
            resultados = cursor.fetchall()
            for fila in resultados:
                print(f"Clave: {fila[0]}, Nombre: {fila[1]}, Rubrica ID: {fila[2]}, Área Conocimiento ID: {fila[3]}")
        except Error as e:
            print(f"❌ Error al leer los profesores: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_profesor():
    clave_profesor = input("Clave del profesor a actualizar: ").strip()
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_rubrica_id = input("Nuevo Rubrica ID: ").strip()
    nuevo_rubrica_area_conocimiento_id = input("Nuevo Área Conocimiento ID: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Profesor SET nombre_profesor = %s, rubrica_id = %s, rubrica_area_conocimiento_id = %s WHERE clave_profesor = %s"
            valores = (nuevo_nombre, nuevo_rubrica_id, nuevo_rubrica_area_conocimiento_id, clave_profesor)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Profesor actualizado exitosamente.")
        except Error as e:
            print(f"❌ Error al actualizar el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_profesor():
    clave_profesor = input("Clave del profesor a eliminar: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Profesor WHERE clave_profesor = %s"
            valores = (clave_profesor,)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Profesor eliminado exitosamente.")
        except Error as e:
            print(f"❌ Error al eliminar el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

def menu_profesores():
    while True:
        print("\n📌 MENÚ CRUD - Profesores")
        print("C - Crear Profesor")
        print("R - Leer Profesores")
        print("U - Actualizar Profesor")
        print("D - Eliminar Profesor")
        print("S - Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip().upper()
        if opcion == 'C':
            crear_profesor()
        elif opcion == 'R':
            leer_profesores()
        elif opcion == 'U':
            actualizar_profesor()
        elif opcion == 'D':
            eliminar_profesor()
        elif opcion == 'S':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

def menu_principal():
    while True:
        print("\n📌 MENÚ PRINCIPAL")
        print("P - CRUD Profesores")
        print("T - CRUD Tipos de Proyecto")
        print("X - Salir")
        opcion = input("Seleccione una opción: ").strip().upper()
        if opcion == 'P':
            menu_profesores()
        elif opcion == 'T':
            print("(Aquí iría el menú de Tipos de Proyecto)")
        elif opcion == 'X':
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

menu_principal()

#En el adminsitrador de archivos: C:\ABDS5A\Practicas - Git Presionar directorio y poner CMD para abrir directo en el directorio la ubicacion del entorno virtual
#python -m venv bdatos
#python tipo_proyectos.py
#bdatos\Scripts\activate