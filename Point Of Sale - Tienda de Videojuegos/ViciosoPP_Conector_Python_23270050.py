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

# 📌 Menú principal
def menu_principal():
    while True:
        print("\n🎮 MENÚ PRINCIPAL - Vicioso++")
        print("1️.- Gestión de Productos")
        print("2.- Gestión de Clientes")
        print("3️.- Gestión de Empleados")
        print("4️.- Gestión de Ventas")
        print("5️.- Gestión de Detalle de Ventas")
        print("6️.- Salir")

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
