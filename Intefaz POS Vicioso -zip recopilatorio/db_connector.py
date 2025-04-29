# db_connector.py
import mysql.connector
from mysql.connector import Error

# 🔗 Función para conectar a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # Cambia si usas otro host
            user="root",             # Usuario de MySQL
            password="oracle",       # Tu contraseña de MySQL
            database="viciosopp"     # La base de datos del POS
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conexion
    except Error as error:
        print(f"❌ Error al conectar con MySQL: {error}")
        return None
