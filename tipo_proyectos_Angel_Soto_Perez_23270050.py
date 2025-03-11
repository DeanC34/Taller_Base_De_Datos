import mysql.connector
from mysql.connector import Error

#######

# Angel Soto Perez - S5A - 23270050 - 05/03/2025
# Nuevamente
# De la linea 10 a 88 son los metodos para conexion
# 90 a 98 Uso de los metodos para ejecutar los metodos

#En el adminsitrador de archivos: C:\ABDS5A\Practicas - Git Presionar directorio y poner CMD para abrir directo en el directorio la ubicacion del entorno virtual
#python -m venv bdatos
#python tipo_proyectos.py

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


def crear_tipo_proyecto(tipo, nombre_tipo):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO tipo_proyecto (tipo, nombre_tipo) VALUES (%s, %s)"
            valores = (tipo, nombre_tipo)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Tipo de proyecto creado exitosamente")
        except Error as e:
            print(f"Error al crear el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

def leer_tipos_proyecto():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM tipo_proyecto")
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)
        except Error as e:
            print(f"Error al leer el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_tipo_proyecto(tipo, nuevo_nombre):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE tipo_proyecto SET nombre_tipo = %s WHERE tipo = %s"
            valores = (nuevo_nombre, tipo)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Tipo de proyecto actualizado exitosamente")
        except Error as e:
            print(f"Error al actualizar el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_tipo_proyecto(tipo):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM tipo_proyecto WHERE tipo = %s"
            valores = (tipo,)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Tipo de proyecto eliminado exitosamente")
        except Error as e:
            print(f"Error al eliminar el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

# Ejemplos
crear_tipo_proyecto('DT', 'Manukistan')
crear_tipo_proyecto('I', 'Angel - Prueba')
crear_tipo_proyecto('DT', 'Desarrollo Tecnológico')
leer_tipos_proyecto()
actualizar_tipo_proyecto('DT', 'Desarrollo Tecnológico')
actualizar_tipo_proyecto('I', 'Investigación')
leer_tipos_proyecto()
eliminar_tipo_proyecto('DT')
leer_tipos_proyecto()