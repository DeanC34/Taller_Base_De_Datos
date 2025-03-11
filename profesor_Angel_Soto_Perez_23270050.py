import mysql.connector
from mysql.connector import Error
# https://github.com/DeanC34/devasc-study-team
#######

# Angel Soto Perez - S5A - 23270050 - 10/03/2025
# De la linea 11 a 96 son los metodos para conexion
# 98 a 105 Uso de los metodos para ejecutar los metodos

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

# CREATE
def crear_profesor(clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = ("INSERT INTO Profesor (clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id) "
                   "VALUES (%s, %s, %s, %s)")
            valores = (clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Profesor creado exitosamente")
        except Error as e:
            print(f"Error al crear el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

# READ
def leer_profesores():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Profesor")
            resultados = cursor.fetchall()
            for fila in resultados:
                # Imprime: (clave_profesor, nombre_profesor, rubrica_id, rubrica_area_conocimiento_id)
                print(f"Clave: {fila[0]}, Nombre: {fila[1]}, Rubrica ID: {fila[2]}, Área Conocimiento ID: {fila[3]}")
        except Error as e:
            print(f"Error al leer los profesores: {e}")
        finally:
            cursor.close()
            conexion.close()

# UPDATE
def actualizar_profesor(clave_profesor, nuevo_nombre, nuevo_rubrica_id, nuevo_rubrica_area_conocimiento_id):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = ("UPDATE Profesor SET nombre_profesor = %s, rubrica_id = %s, "
                   "rubrica_area_conocimiento_id = %s WHERE clave_profesor = %s")
            valores = (nuevo_nombre, nuevo_rubrica_id, nuevo_rubrica_area_conocimiento_id, clave_profesor)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Profesor actualizado exitosamente")
        except Error as e:
            print(f"Error al actualizar el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

# DELETE
def eliminar_profesor(clave_profesor):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Profesor WHERE clave_profesor = %s"
            valores = (clave_profesor,)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Profesor eliminado exitosamente")
        except Error as e:
            print(f"Error al eliminar el Profesor: {e}")
        finally:
            cursor.close()
            conexion.close()

# Ejemplos de uso:
crear_profesor('01', 'Néstor Antonio Morales Navarro', 1, 10)
crear_profesor('02', 'Walter Torres Robledo', 2, 20)
leer_profesores()
actualizar_profesor('01', 'Jesús Carlos Sánchez Guzmán', 1, 10)
leer_profesores()
eliminar_profesor('02')
leer_profesores()

#En el adminsitrador de archivos: C:\ABDS5A\Practicas - Git Presionar directorio y poner CMD para abrir directo en el directorio la ubicacion del entorno virtual
#python -m venv bdatos
#python tipo_proyectos.py
#bdatos\Scripts\activate