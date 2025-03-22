import mysql.connector
from mysql.connector import Error
from crud_producto import menu_producto
from crud_cliente import menu_cliente
from crud_empleado import menu_empleado
from crud_venta import menu_venta
from crud_detalleventa import menu_detalle_venta

#######
# Ángel Soto Pérez - S5A - 23270050 - 15/03/2025
# CRUD para el POS "Vicioso++" con conexión a MySQL
#######

# 🔗 Función para conectar a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # host principal
            user="root",             # root de mysql commandline
            password="oracle",       # Contraseña MySQL
            database="viciosopp"     # La base de datos del POS
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conexion
    except Error as error:
        print(f"❌ Error al conectar con MySQL: {error}")
        return None

# 📌 Menú principal
def menu_principal():
    while True:
        print("\n🎮 MENÚ PRINCIPAL - Vicioso++")
        print("1️⃣ - Gestión de Productos")
        print("2️⃣ - Gestión de Clientes")
        print("3️⃣ - Gestión de Empleados")
        print("4️⃣ - Gestión de Ventas")
        print("5️⃣ - Gestión de Detalle de Ventas")
        print("6️⃣ - Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            menu_producto()
        elif opcion == '2':
            menu_cliente()
        elif opcion == '3':
            menu_empleado()
        elif opcion == '4':
            menu_venta()
        elif opcion == '5':
            menu_detalle_venta()
        elif opcion == '6':
            print("👋 Saliendo del programa... ¡Hasta pronto!")
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

# 🏁 Ejecutar el menú principal
if __name__ == "__main__":
    menu_principal()
