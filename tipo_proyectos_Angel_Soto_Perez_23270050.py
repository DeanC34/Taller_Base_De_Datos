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

def crear_tipo_proyecto():
    tipo = input("Ingrese el código del tipo de proyecto (Ej: DT): ").strip()
    nombre_tipo = input("Ingrese el nombre del tipo de proyecto: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO tipo_proyecto (tipo, nombre_tipo) VALUES (%s, %s)"
            valores = (tipo, nombre_tipo)
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Tipo de proyecto creado exitosamente.")
        except Error as e:
            print(f"❌ Error al crear el Tipo de proyecto: {e}")
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
            if resultados:
                print("\n📋 Lista de Tipos de Proyecto:")
                for fila in resultados:
                    print(f"🔹 Código: {fila[0]}, Nombre: {fila[1]}")
            else:
                print("⚠️ No hay tipos de proyecto registrados.")
        except Error as e:
            print(f"❌ Error al leer los Tipos de Proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

def actualizar_tipo_proyecto():
    tipo = input("Ingrese el código del tipo de proyecto a actualizar: ").strip()
    nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "UPDATE tipo_proyecto SET nombre_tipo = %s WHERE tipo = %s"
            valores = (nuevo_nombre, tipo)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Tipo de proyecto actualizado exitosamente.")
            else:
                print("⚠️ No se encontró un tipo de proyecto con ese código.")
        except Error as e:
            print(f"❌ Error al actualizar el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_tipo_proyecto():
    tipo = input("Ingrese el código del tipo de proyecto a eliminar: ").strip()
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM tipo_proyecto WHERE tipo = %s"
            valores = (tipo,)
            cursor.execute(sql, valores)
            conexion.commit()
            if cursor.rowcount > 0:
                print("✅ Tipo de proyecto eliminado exitosamente.")
            else:
                print("⚠️ No se encontró un tipo de proyecto con ese código.")
        except Error as e:
            print(f"❌ Error al eliminar el Tipo de proyecto: {e}")
        finally:
            cursor.close()
            conexion.close()

# Menú 
def menu():
    while True:
        print("\n📌 MENÚ CRUD - Tipos de Proyecto")
        print("C - Crear un nuevo Tipo de Proyecto")
        print("R - Leer todos los Tipos de Proyecto")
        print("U - Actualizar un Tipo de Proyecto")
        print("D - Eliminar un Tipo de Proyecto")
        print("S - Salir")

        opcion = input("Seleccione una opción: ").strip().upper()

        if opcion == 'C':
            crear_tipo_proyecto()
        elif opcion == 'R':
            leer_tipos_proyecto()
        elif opcion == 'U':
            actualizar_tipo_proyecto()
        elif opcion == 'D':
            eliminar_tipo_proyecto()
        elif opcion == 'S':
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

menu()
