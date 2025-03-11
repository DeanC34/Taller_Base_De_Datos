import mysql.connector
from mysql.connector import Error

#######

# Angel Soto Perez - S5A - 23270050 - 05/03/2025
# De la linea 10 a 88 son los metodos para conexion
# 90 a 98 Uso de los metodos para ejecutar los metodos

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

def crear_linea_investigacion(clave_inv, nombre_linea):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Linea_Investigacion (clave_inv, nombre_linea) VALUES (%s, %s)"
            valores = (clave_inv, nombre_linea)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Línea de investigación creada exitosamente")
        except Error as e:
            print(f"Error al crear la línea de investigación: {e}")
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
            for fila in resultados:
                print(fila)
        except Error as e:
            print(f"Error al leer las líneas de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_linea_investigacion(clave_inv, nuevo_nombre):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Linea_Investigacion SET nombre_linea = %s WHERE clave_inv = %s"
            valores = (nuevo_nombre, clave_inv)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Línea de investigación actualizada exitosamente")
        except Error as e:
            print(f"Error al actualizar la línea de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_linea_investigacion(clave_inv):
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Linea_Investigacion WHERE clave_inv = %s"
            valores = (clave_inv,)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Línea de investigación eliminada exitosamente")
        except Error as e:
            print(f"Error al eliminar la línea de investigación: {e}")
        finally:
            cursor.close()
            conexion.close()

# Ejemplos
crear_linea_investigacion('L06', 'Manukistan')
crear_linea_investigacion('L07', 'Angel - Prueba')
crear_linea_investigacion('L08', 'Robótica, Control Inteligente y Sistemas de Percepción')
leer_lineas_investigacion()
actualizar_linea_investigacion('DSIR', 'Desarrollo Sistematico Investigativo Renovable')
actualizar_linea_investigacion('TDWM', 'Tecnologías de Desarrollo Web y Móvil')
leer_lineas_investigacion()
eliminar_linea_investigacion('L08')
leer_lineas_investigacion()