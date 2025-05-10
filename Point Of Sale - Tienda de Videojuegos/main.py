# C:\Users\nepex>pip show flet
# Name: flet
# Version: 0.27.6
# Location: c:\users\nepex\appdata\local\programs\python\python39\lib\site-packages

# Flet esta sujeto a cambios por ello dejo especificado la version ya que siguiendo tutoriales quedaron obsoletos algunas palabras reservadas
# UserControl -> Container
# NavigationDestination -> NavigationRailDestination

import mysql.connector
from mysql.connector import Error
from db_connector import conectar_bd
from crud_producto import obtener_productos, crear_producto_backend, actualizar_producto_backend, obtener_producto_por_id, eliminar_producto_backend
from crud_cliente import obtener_clientes, obtener_cliente_por_id, crear_cliente_backend, actualizar_cliente_backend, eliminar_cliente_backend
from crud_empleado import obtener_empleados, obtener_empleado_por_id, crear_empleado_backend, actualizar_empleado_backend, eliminar_empleado_backend
from crud_venta import obtener_ventas, obtener_venta_por_id, crear_venta_backend, actualizar_venta_backend, eliminar_venta_backend, obtener_clientes_para_dropdown, obtener_empleados_para_dropdown
from crud_detalleventa import obtener_detalles_venta, obtener_detalle_por_id, crear_detalle_venta_backend, actualizar_detalle_venta_backend, eliminar_detalle_venta_backend, obtener_productos_para_dropdown, obtener_ventas_para_dropdown
import random

import flet as ft

#Constructor
class UI(ft.Container):         #UserControl -> Container
    def __init__(self, page):
        super().__init__(expand=True)       
        self.page = page  # Guarda la referencia a la página

        self.color_teal = "#00BFFF"
        self.mode_switch = ft.Switch(
            value=True,
            on_change=lambda e: self.toggle_theme(page)
        )

        # Panel de la izquiera "Panel de navegación"
        self.navigation_rail = ft.NavigationRail(
            bgcolor=self.color_teal,
            expand=True,
            selected_index=0,
            on_change=self.cambiar_contenido,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.HOME, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.HOME_FILLED, color="white"),
                    label="Inicio"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.SHOPPING_CART, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.SHOPPING_CART_CHECKOUT, color="white"),
                    label="Productos",
                    
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.SUPERVISED_USER_CIRCLE, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.VERIFIED_USER, color="white"),
                    label="Clientes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.WORK, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.WORK_HISTORY, color="white"),
                    label="Empleados"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.ATTACH_MONEY, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.MONEY_OFF, color="white"),
                    label="Ventas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.BOOK, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.MENU_BOOK, color="white"),
                    label="Detalle de Ventas"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(name=ft.Icons.SETTINGS, color="white"),
                    selected_icon=ft.Icon(name=ft.Icons.SETTINGS_SUGGEST, color="white"), # icons -> Icons para la 0.28
                    label="Configuración"
                )
            ]
        )


        # Columna lateral fija con el NavigationRail
        self.navigation_container = ft.Container(
            width=150,
            border_radius=5,
            bgcolor=self.color_teal,
            padding=10,
            content=ft.Column([
                ft.Container(expand=True, content=self.navigation_rail),
                ft.Container(
                    alignment=ft.alignment.bottom_center,
                    padding=10,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Oscuro / Claro", color="white"),
                            self.mode_switch
                        ]
                    )
                )
            ])
        )

        # Area de texto - Area inicial
        self.frame_2_text = ft.Text(
            "🎮 ¡Bienvenido a *Vicioso++*! 🎉\n\n"
            "Explora y gestiona todo lo relacionado con tu tienda de videojuegos favorita:\n\n"
            "🛒 Productos en inventario\n"
            "👥 Empleados activos\n"
            "📈 Ventas realizadas\n"
            "⭐ Clientes frecuentes\n"
            "📦 Detalles de cada venta\n\n"
            "¡Todo a tu alcance desde un solo lugar! 💻",
            color="black",
            size=16,
            weight=ft.FontWeight.NORMAL
        )

        self.contador = 0
        self.click_text = ft.Text("Haz clic en el botón y mira cómo sube el contador! 🎯", size=14)

        self.boton_clicker = ft.ElevatedButton(
            text="Haz clic! 🎮",
            on_click=self.incrementar_contador,
            bgcolor="#00BFFF",
            color="white"
        )

        self.resultado_clicks = ft.Text(f"Clicks: {self.contador}", size=18, weight=ft.FontWeight.BOLD)

        self.frame_3_text = ft.Text("Aqui estara las funciones acerca de Contratar empleados o añadir productos!", color="black")

        self.extra_panel_1_text = ft.Text("Aqui podras buscar entre los datos!", color="black")
        self.extra_panel_2_text = ft.Text("Aqui podras Actualizar (Update)", color="black")
        self.extra_panel_3_text = ft.Text("Y... Aqui podras Despedir o Eliminar", color="black")

        # Area de Paneles (Contenido)

        self.frame_2 = ft.Container(
            expand= True,  # Se expande para ocupar altura no olvidar que intentaran ocupar la misma altura lo cual puede provocar espacios grandes vacios
            width=700,
            border_radius=5,
            padding=10,
            bgcolor="white",
            content=ft.Column([
                    self.frame_2_text,
                    self.click_text,
                    self.boton_clicker,
                    self.resultado_clicks
            ], expand=True)
        )
        
        self.frame_3 = ft.Container(                    
            expand=True,
            width=370,
            border_radius=5,
            padding=10,
            bgcolor="white",
            content=ft.Column([
                self.frame_3_text
            ])
        )                                           

        self.buscador_input = ft.TextField(hint_text="Buscar...", width=300)
        
        self.boton_refrescar = ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Refrescar tabla", on_click=lambda _: self.cambiar_contenido(None))

        self.boton_buscar = ft.IconButton(icon=ft.Icons.SEARCH, tooltip="Buscar", on_click=self.buscar_producto)

        # Mas paneles y su contenido relacionado
        self.extra_panel_1 = ft.Container(
            height=120,
            width=700,
            bgcolor="white",
            border_radius=5,
            padding=10,
            content=ft.Column([
                self.extra_panel_1_text,
                ft.Row([
                    self.buscador_input,
                    self.boton_buscar,
                    self.boton_refrescar
                ], spacing=10)
            ])
        )

        self.actualizar_id_input = ft.TextField(label="ID", width=120)
        self.boton_proceder_actualizar = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            tooltip="Cargar formulario de actualización",
            on_click=self.cargar_formulario_actualizar
        )

        self.extra_panel_2 = ft.Container(
            height=120,
            width=185,
            bgcolor="white",
            border_radius=5,
            padding=10,
            content=ft.Column([
                self.extra_panel_2_text,
                ft.Row([
                    self.actualizar_id_input,
                    self.boton_proceder_actualizar
                ], spacing=5)
            ])
        )

        self.eliminar_id_input = ft.TextField(label="ID", width=120)
        self.boton_proceder_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Eliminar producto",
            on_click=self.confirmar_eliminar_producto,
            icon_color="red"
        )

        self.extra_panel_3 = ft.Container(
            height=120,
            width=175,
            bgcolor="white",
            border_radius=5,
            padding=10,
            content=ft.Column([
                self.extra_panel_3_text,
                ft.Row([
                    self.eliminar_id_input,
                    self.boton_proceder_eliminar
                ], spacing=5)
            ])
        )

        # Agrupar frame_2 y extra_panel_1 en una sola columna
        self.columna_principal = ft.Column(
            controls=[
                self.frame_2,
                self.extra_panel_1
            ],

            spacing=10  
        )


        # Nueva columna para panel secundario + paneles extra (Agrupación 2)
        self.panel_secundario_y_extra = ft.Column(
            controls=[
                self.frame_3,
                ft.Row(
                    controls=[self.extra_panel_2, self.extra_panel_3],
                    spacing=10
                )
            ],
            spacing=10,   
        )

        # Organizar contenido a la derecha del NavigationRail
        self.right_side = ft.Row([
            self.columna_principal,
            self.panel_secundario_y_extra
        ], expand=True, spacing=10)

        # Contenedor principal: NavigationRail a la izquierda, y columnas a la derecha
        self.container = ft.Row(
            expand=True,
            controls=[
                self.navigation_container,
                self.right_side
            ]
        )

        self.content = self.container
        
    #Metodos:

    def toggle_theme(self, page):
        is_light = self.mode_switch.value
        page.theme_mode = ft.ThemeMode.LIGHT if is_light else ft.ThemeMode.DARK

        frame_bgcolor = "white" if is_light else "#3E3E3E"
        text_color = "black" if is_light else "white"

        # Cambiar colores de todos los paneles
        paneles = [self.frame_2, self.frame_3, self.extra_panel_1, self.extra_panel_2, self.extra_panel_3]
        for panel in paneles:
            panel.bgcolor = frame_bgcolor
            if isinstance(panel.content, ft.Text):
                panel.content.color = text_color

        # Cambiar textos principales
        self.frame_2_text.value = "Bienvenido a Vicioso++! \nAquí Revisaras todo lo que gustes" \
        "\n Entre ellos están:" \
        "\n1.- Los productos en existencia (inventario)" \
        "\n2.- Los Empleados en activo \n3.- Las ventas realizadas \n4.- Clientes frecuentes que se registraron voluntariamente " \
        "\n5.- Y si hace falta algunos detalles de venta"
        self.frame_3_text.value = "Aqui estara las funciones acerca de Crear o Contratar!"

        self.extra_panel_1_text.value = "Aqui podras buscar entre los datos!"
        self.extra_panel_2_text.value = "Aqui podras Actualizar (Update)"
        self.extra_panel_3_text.value = "Y... Aqui podras Despedir o Eliminar"

        self.frame_2_text.color = text_color
        self.frame_3_text.color = text_color
        self.extra_panel_1_text.color = text_color
        self.extra_panel_2_text.color = text_color
        self.extra_panel_3_text.color = text_color 

        page.update()

    def incrementar_contador(self, e):
            self.contador += 1
            self.resultado_clicks.value = f"Clicks: {self.contador}"
            self.page.update()

    def cambiar_contenido(self, e):
        indice = self.navigation_rail.selected_index

        # Si está seleccionada la sección Productos (índice 1)

        if indice == 1:  # Productos
            self.frame_2.content = ft.Column([
                ft.Text("Inventario: Tabla de productos disponibles:", size=18, weight=ft.FontWeight.BOLD),
                self.construir_tabla_productos()
            ])
            self.frame_3.content = self.construir_formulario_productos()
            self.boton_buscar.on_click = self.buscar_producto
            self.boton_proceder_actualizar.on_click = self.cargar_formulario_actualizar
            self.boton_proceder_eliminar.on_click = self.confirmar_eliminar_producto

        elif indice == 2:  # Clientes
            self.boton_buscar.on_click = self.buscar_cliente
            self.boton_proceder_actualizar.on_click = self.cargar_formulario_actualizar_cliente
            self.boton_proceder_eliminar.on_click = self.confirmar_eliminar_cliente
            self.frame_2.content = ft.Column([
                ft.Text("Clientes registrados:", size=18, weight=ft.FontWeight.BOLD),
                self.construir_tabla_clientes()
            ])
            self.frame_3.content = self.construir_formulario_clientes()

        elif indice == 3:  # Empleados
            self.boton_buscar.on_click = self.buscar_empleado
            self.boton_proceder_actualizar.on_click = self.cargar_formulario_actualizar_empleado
            self.boton_proceder_eliminar.on_click = self.confirmar_eliminar_empleado
            self.frame_2.content = ft.Column([
                ft.Text("Empleados registrados:", size=18, weight=ft.FontWeight.BOLD),
                self.construir_tabla_empleados()
            ])
            self.frame_3.content = self.construir_formulario_empleados()

        elif indice == 4:  # Ventas
            self.boton_buscar.on_click = self.buscar_venta
            self.boton_proceder_actualizar.on_click = self.cargar_formulario_actualizar_venta
            self.boton_proceder_eliminar.on_click = self.confirmar_eliminar_venta
            self.frame_2.content = ft.Column([
                ft.Text("Historial de Ventas:", size=18, weight=ft.FontWeight.BOLD),
                self.construir_tabla_ventas()
            ])
            self.frame_3.content = self.construir_formulario_ventas()
        
        elif indice == 5:  # Detalles de Venta
            self.boton_buscar.on_click = self.buscar_detalle_venta
            self.boton_proceder_actualizar.on_click = self.cargar_formulario_actualizar_detalle_venta
            self.boton_proceder_eliminar.on_click = self.confirmar_eliminar_detalle_venta
            self.frame_2.content = ft.Column([
                ft.Text("Detalles de Ventas:", size=18, weight=ft.FontWeight.BOLD),
                self.construir_tabla_detalles_venta()
            ])
            self.frame_3.content = self.construir_formulario_detalles_venta()

        elif indice == 6:  # Configuración
            self.color_picker = ft.Dropdown(
                label="Color principal",
                options=[
                    ft.dropdown.Option("#00BFFF", "Azul Claro (Default)"),
                    ft.dropdown.Option("#4CAF50", "Verde"),
                    ft.dropdown.Option("#FF5722", "Naranja"),
                    ft.dropdown.Option("#9C27B0", "Púrpura"),
                    ft.dropdown.Option("#EDE721", "Amarrillo")
                ],
                value=self.color_teal,
                on_change=self.cambiar_color_principal
            )

            self.frame_2.content = ft.Column([
                ft.Text("Configuración de la App", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Personaliza la apariencia:", size=16),
                self.color_picker,
            ], spacing=15)

            # Juego sencillo: Adivina el número
            self.numero_secreto = random.randint(1, 10)
            self.intentos = 3
            self.juego_adivina = ft.Column([
                ft.Text("Juego: Adivina el número (1-10)", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Tienes {self.intentos} intentos", color="blue"),
                ft.TextField(label="Tu número", width=100),
                ft.ElevatedButton("Adivinar", on_click=self.juego_adivinar_numero),
                ft.Text("", color="red", size=14)  # Para mensajes
            ])

            self.frame_3.content = ft.Column([
                ft.Text("Mini Juego", size=18, weight=ft.FontWeight.BOLD),
                self.juego_adivina,
                ft.Divider(),
                ft.Text("Versión: 0.2.3\n© Vicioso++ 2023", size=12, color="grey")
            ], spacing=15)
        
        else:
            self.frame_2.content = ft.Column([
                self.frame_2_text,
                self.click_text,
                self.boton_clicker,
                self.resultado_clicks
            ])

            self.frame_3.content = ft.Column([
                ft.Text("¡Volviste! :D")
            ])

        self.frame_2.update()
        self.frame_3.update()
        self.extra_panel_1.update()
        self.extra_panel_2.update()
        self.extra_panel_3.update()

    def cambiar_color_principal(self, e):
        self.color_teal = self.color_picker.value
        self.navigation_container.bgcolor = self.color_teal
        self.navigation_rail.bgcolor = self.color_teal
        self.page.update()

    def juego_adivinar_numero(self, e):
        try:
            numero_usuario = int(self.juego_adivina.controls[2].value)
            mensaje = self.juego_adivina.controls[4]
            
            if numero_usuario == self.numero_secreto:
                mensaje.value = "¡Correcto! Has ganado."
                mensaje.color = "green"
                self.juego_adivina.controls[1].value = "¡Ganaste!"
                self.juego_adivina.controls[3].disabled = True
            else:
                self.intentos -= 1
                if self.intentos > 0:
                    mensaje.value = f"Incorrecto. Te quedan {self.intentos} intentos."
                    mensaje.color = "orange"
                    self.juego_adivina.controls[1].value = f"Tienes {self.intentos} intentos"
                else:
                    mensaje.value = f"¡Perdiste! El número era {self.numero_secreto}"
                    mensaje.color = "red"
                    self.juego_adivina.controls[1].value = "¡Fin del juego!"
                    self.juego_adivina.controls[3].disabled = True
            
            self.page.update()
        except ValueError:
            self.juego_adivina.controls[4].value = "Ingresa un número válido"
            self.juego_adivina.controls[4].color = "red"
            self.page.update()

    # Inicio CRUD's Productos

    # Tabla (Read)

    def construir_tabla_productos(self):
        productos = obtener_productos()
        columnas = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Precio")),
            ft.DataColumn(label=ft.Text("Stock")),
        ]

        filas = []
        for p in productos:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p["id"]))),
                    ft.DataCell(ft.Text(p["nombre"])),
                    ft.DataCell(ft.Text(str(p["precio"]))),
                    ft.DataCell(ft.Text(str(p["stock"]))),
                ]
            )
            filas.append(fila)

        tabla = ft.DataTable(columns=columnas, rows=filas)

        # El cambio está aquí: usamos Column con scroll y luego Container para fijar la altura
        return ft.Column([
            ft.Container(
                ft.Column([tabla], scroll="auto"),
                height=500
            ),
        ])


    
    # Create 
    def construir_formulario_productos(self):
        self.nombre_input = ft.TextField(label="Nombre del Producto", width=300)
        self.precio_input = ft.TextField(label="Precio", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        self.stock_input = ft.TextField(label="Stock", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        self.categoria_input = ft.TextField(label="ID Categoría", width=300, keyboard_type=ft.KeyboardType.NUMBER)
        self.proveedor_input = ft.TextField(label="ID Proveedor", width=300, keyboard_type=ft.KeyboardType.NUMBER)

        boton_crear = ft.ElevatedButton(
            text="Crear Producto",
            on_click=self.crear_producto
        )

        texto_categorias = ft.Text(
            "\nEjemplo " \
            "\nID de Categoría: 1.- Videojuego, 2.- Consolas y Hardware, 3.- Accesorios",
            size=12,
            color="gray"
        )

        return ft.Column([
            ft.Text("Formulario de Creación de Producto", size=20, weight=ft.FontWeight.BOLD),
            self.nombre_input,
            self.precio_input,
            self.stock_input,
            self.categoria_input,
            self.proveedor_input,
            boton_crear,
            texto_categorias
        ])
    
        # Al presionar el boton "Crear"
    def crear_producto(self, e):
        nombre = self.nombre_input.value
        try:
            precio = float(self.precio_input.value)
            stock = int(self.stock_input.value)
            id_categoria = int(self.categoria_input.value)
            id_proveedor = int(self.proveedor_input.value)
        except ValueError:
            print("❌ Error: Algún valor es inválido")
            return

        # Ahora puedes llamar a la función de backend pasando los 5 valores
        crear_producto_backend(nombre, precio, stock, id_categoria, id_proveedor)
    
    # Logica del buscador
    def buscar_producto(self, e):
        termino = self.buscador_input.value.strip().lower()
        if not termino:
            return  # Si no hay término, no hace nada

        productos = obtener_productos()
        filtrados = [p for p in productos if termino in p["nombre"].lower()]

        columnas = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Precio")),
            ft.DataColumn(label=ft.Text("Stock")),
        ]

        filas = []
        for p in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p["id"]))),
                    ft.DataCell(ft.Text(p["nombre"])),
                    ft.DataCell(ft.Text(str(p["precio"]))),
                    ft.DataCell(ft.Text(str(p["stock"]))),
                ]
            )
            filas.append(fila)

        tabla_filtrada = ft.DataTable(columns=columnas, rows=filas)

        self.frame_2.content = ft.Column([
            ft.Text(f"Resultados para '{termino}':", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([tabla_filtrada], scroll="auto"),
                height=300
            ),
            ft.Row([self.boton_refrescar], alignment=ft.MainAxisAlignment.END)
        ])

        self.frame_2.update()

    def cargar_formulario_actualizar(self, e):
        try:
            id_producto = int(self.actualizar_id_input.value)
        except ValueError:
            print("❌ ID inválido")
            return

        producto = obtener_producto_por_id(id_producto)
        if not producto:
            print("❌ Producto no encontrado")
            return

        self.nombre_actualizar = ft.TextField(label="Nombre del Producto", value=producto[1], width=300)
        self.precio_actualizar = ft.TextField(label="Precio", value=str(producto[2]), width=300)
        self.stock_actualizar = ft.TextField(label="Stock", value=str(producto[3]), width=300)
        self.categoria_actualizar = ft.TextField(label="ID Categoría", value=str(producto[4]), width=300)
        self.proveedor_actualizar = ft.TextField(label="ID Proveedor", value=str(producto[5]), width=300)

        boton_actualizar = ft.ElevatedButton(
            text="Actualizar Producto",
            on_click=lambda e: self.actualizar_producto(id_producto)
        )

        boton_volver = ft.TextButton (
            text="← Volver a Crear",
            on_click=self.cambiar_a_formulario_producto
        )

        self.frame_3.content = ft.Column([
            ft.Text("Formulario de Actualización", size=20, weight=ft.FontWeight.BOLD),
            self.nombre_actualizar,
            self.precio_actualizar,
            self.stock_actualizar,
            self.categoria_actualizar,
            self.proveedor_actualizar,
            boton_actualizar,
            boton_volver
        ])

        self.frame_3.update()

    def actualizar_producto(self, id_producto):
        try:
            nombre = self.nombre_actualizar.value
            precio = float(self.precio_actualizar.value)
            stock = int(self.stock_actualizar.value)
            id_categoria = int(self.categoria_actualizar.value)
            id_proveedor = int(self.proveedor_actualizar.value)
        except ValueError:
            print("❌ Error en los campos")
            return

        actualizar_producto_backend(id_producto, nombre, precio, stock, id_categoria, id_proveedor)
        print("✔ Producto actualizado")    

    def cambiar_a_formulario_producto(self, e):
        self.frame_3.content = self.construir_formulario_productos()
        self.frame_3.update()

    def eliminar_producto(self, id_producto):
        try:
            if eliminar_producto_backend(id_producto):
                self.mostrar_mensaje(f"✅ Producto {id_producto} eliminado correctamente")
                self.eliminar_id_input.value = ""
                # Refrescar la tabla
                self.cambiar_contenido(None)
            else:
                self.mostrar_mensaje("❌ No se pudo eliminar el producto", color="red")
        except Exception as e:
            self.mostrar_mensaje(f"❌ Error al eliminar: {str(e)}", color="red")

    def confirmar_eliminar_producto(self, e):
        try:
            id_producto = int(self.eliminar_id_input.value)
        except ValueError:
            self.mostrar_mensaje("❌ ID inválido", color="red")
            return
        
        # Eliminar directamente sin diálogo de confirmación
        self.eliminar_producto(id_producto)

    def mostrar_mensaje(self, mensaje, color=None):
        if hasattr(self, 'page') and self.page is not None:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            print(mensaje)  # Fallback en caso de que page no esté disponible

    # Fin CRUD's Productos

    # Inicio CRUD's Clientes
    def construir_tabla_clientes(self):
        clientes = obtener_clientes()
        columnas = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Apellido")),
            ft.DataColumn(label=ft.Text("Teléfono")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Dirección")),
        ]

        filas = []
        for c in clientes:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(c.get("id", "")))),
                    ft.DataCell(ft.Text(c.get("nombre", ""))),
                    ft.DataCell(ft.Text(c.get("apellido", ""))),
                    ft.DataCell(ft.Text(c.get("telefono", ""))),
                    ft.DataCell(ft.Text(c.get("email", ""))), 
                    ft.DataCell(ft.Text(c.get("direccion", "")))
                ]
            )
            filas.append(fila)

        return ft.Column([
            ft.Container(
                content=ft.ListView(
                    [ft.DataTable(
                        columns=columnas,
                        rows=filas,
                        column_spacing=20,
                        horizontal_margin=10,
                        heading_row_height=40,
                        data_row_min_height=40,
                        data_row_max_height=60
                    )],
                    expand=True
                ),
                height=500,
                padding=10
            )
        ])

    def construir_formulario_clientes(self):
        self.cliente_nombre_input = ft.TextField(label="Nombre", width=300)
        self.cliente_apellido_input = ft.TextField(label="Apellido", width=300)
        self.cliente_telefono_input = ft.TextField(label="Teléfono", width=300)
        self.cliente_email_input = ft.TextField(label="Email", width=300)
        self.cliente_direccion_input = ft.TextField(label="Dirección", width=300)

        boton_crear = ft.ElevatedButton(
            text="Registrar Cliente",
            on_click=self.crear_cliente
        )

        return ft.Column([
            ft.Text("Registro de Cliente", size=20, weight=ft.FontWeight.BOLD),
            self.cliente_nombre_input,
            self.cliente_apellido_input,
            self.cliente_telefono_input,
            self.cliente_email_input,
            self.cliente_direccion_input,
            boton_crear
        ])

    def crear_cliente(self, e):
        nombre = self.cliente_nombre_input.value.strip()
        apellido = self.cliente_apellido_input.value.strip()
        telefono = self.cliente_telefono_input.value.strip()
        email = self.cliente_email_input.value.strip()
        direccion = self.cliente_direccion_input.value.strip()

        # Validación de campos obligatorios
        if not all([nombre, apellido, telefono, email, direccion]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        # Validación básica de email
        if "@" not in email or "." not in email:
            self.mostrar_mensaje("❌ Ingrese un email válido", color="red")
            return

        if crear_cliente_backend(nombre, apellido, telefono, email, direccion):
            self.mostrar_mensaje("✅ Cliente registrado correctamente")
            # Limpiar campos después de registro exitoso
            self.cliente_nombre_input.value = ""
            self.cliente_apellido_input.value = ""
            self.cliente_telefono_input.value = ""
            self.cliente_email_input.value = ""
            self.cliente_direccion_input.value = ""
            self.cambiar_contenido(None)  # Refrescar la tabla
        else:
            self.mostrar_mensaje("❌ Error al registrar cliente", color="red")

    def buscar_cliente(self, e):
        termino = self.buscador_input.value.strip().lower()
        if not termino:
            return

        clientes = obtener_clientes()
        filtrados = [c for c in clientes if termino in c["nombre"].lower()]

        columnas = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Teléfono")),
        ]

        filas = []
        for c in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(c["id"]))),
                    ft.DataCell(ft.Text(c["nombre"])),
                    ft.DataCell(ft.Text(c["email"])),
                    ft.DataCell(ft.Text(c["telefono"])),
                ]
            )
            filas.append(fila)

        tabla_filtrada = ft.DataTable(columns=columnas, rows=filas)

        self.frame_2.content = ft.Column([
            ft.Text(f"Resultados para '{termino}':", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([tabla_filtrada], scroll="auto"),
                height=300
            ),
            ft.Row([self.boton_refrescar], alignment=ft.MainAxisAlignment.END)
        ])

        self.frame_2.update()

    def cargar_formulario_actualizar_cliente(self, e):
        try:
            id_cliente = int(self.actualizar_id_input.value)
        except ValueError:
            self.mostrar_mensaje("❌ ID inválido", color="red")
            return

        cliente = obtener_cliente_por_id(id_cliente)
        if not cliente:
            self.mostrar_mensaje("❌ Cliente no encontrado", color="red")
            return

        # Crear campos para todos los datos del cliente
        self.cliente_nombre_actualizar = ft.TextField(label="Nombre", value=cliente[1], width=300)
        self.cliente_apellido_actualizar = ft.TextField(label="Apellido", value=cliente[2], width=300)
        self.cliente_telefono_actualizar = ft.TextField(label="Teléfono", value=cliente[3], width=300)
        self.cliente_email_actualizar = ft.TextField(label="Email", value=cliente[4], width=300)
        self.cliente_direccion_actualizar = ft.TextField(label="Dirección", value=cliente[5], width=300)

        boton_actualizar = ft.ElevatedButton(
            text="Actualizar Cliente",
            on_click=lambda e: self.actualizar_cliente(id_cliente)
        )

        boton_volver = ft.TextButton(
            text="← Volver a Crear",
            on_click=self.cambiar_a_formulario_clientes
        )

        self.frame_3.content = ft.Column([
            ft.Text("Formulario de Actualización", size=20, weight=ft.FontWeight.BOLD),
            self.cliente_nombre_actualizar,
            self.cliente_apellido_actualizar,
            self.cliente_telefono_actualizar,
            self.cliente_email_actualizar,
            self.cliente_direccion_actualizar,
            boton_actualizar,
            boton_volver
        ])

        self.frame_3.update()

    def actualizar_cliente(self, id_cliente):
        nombre = self.cliente_nombre_actualizar.value.strip()
        apellido = self.cliente_apellido_actualizar.value.strip()
        telefono = self.cliente_telefono_actualizar.value.strip()
        email = self.cliente_email_actualizar.value.strip()
        direccion = self.cliente_direccion_actualizar.value.strip()

        # Validación de campos obligatorios
        if not all([nombre, apellido, telefono, email, direccion]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        # Validación básica de email (frontend)
        if "@" not in email or "." not in email:
            self.mostrar_mensaje("❌ Ingrese un email válido", color="red")
            return

        if actualizar_cliente_backend(id_cliente, nombre, apellido, telefono, email, direccion):
            self.mostrar_mensaje("✅ Cliente actualizado correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al actualizar cliente", color="red")

    def confirmar_eliminar_cliente(self, e):
        try:
            id_cliente = int(self.eliminar_id_input.value)
        except ValueError:
            print("❌ ID inválido")
            return

        eliminar_cliente_backend(id_cliente)
        self.cambiar_contenido(None)

    def cambiar_a_formulario_clientes(self, e):
        """Vuelve al formulario de creación de clientes"""
        self.frame_3.content = self.construir_formulario_clientes()
        self.frame_3.update()
    # Fin CRUD's Clientes

    # Inicio CRUD's Empleados
    def construir_tabla_empleados(self):
        empleados = obtener_empleados()
        
        columnas = [
            ft.DataColumn(ft.Text("ID", size=10)),
            ft.DataColumn(ft.Text("Nombre", size=10)),
            ft.DataColumn(ft.Text("Apellido", size=10)),
            ft.DataColumn(ft.Text("Teléfono", size=10)),
            ft.DataColumn(ft.Text("Email", size=10)),
            ft.DataColumn(ft.Text("Puesto", size=10)),
            ft.DataColumn(ft.Text("Salario", size=10)),
            ft.DataColumn(ft.Text("Sucursal", size=10)),
        ]

        filas = []

        def limitar_texto(valor, max_len):
            if valor is None:
                return ""
            texto = str(valor)
            return texto[:max_len] + "..." if len(texto) > max_len else texto

        for e in empleados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(e.get("id", "")), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("nombre"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("apellido"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("telefono"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("email"), 15), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("puesto"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("salario"), 8), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(e.get("sucursal"), 10), size=10)),
                ]
            )
            filas.append(fila)

        data_table = ft.DataTable(
            columns=columnas,
            rows=filas,
            column_spacing=2,  # Menor separación entre columnas
            horizontal_margin=2,
            heading_row_height=25,
            data_row_min_height=25,
            data_row_max_height=30,
        )

        return ft.Container(
            content=data_table,
            width=700,
            height=300,
            padding=5,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def obtener_sucursales(self):
        """Obtiene las sucursales para el dropdown"""
        conexion = conectar_bd()
        sucursales = []
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT id_sucursal as id, nombre FROM Sucursal")
                sucursales = cursor.fetchall()
            except Error as error:
                print(f"❌ Error al obtener sucursales: {error}")
            finally:
                cursor.close()
                conexion.close()
        return sucursales

    def construir_formulario_empleados(self):
        # Obtener sucursales para el dropdown
        sucursales = self.obtener_sucursales()
        
        # Campos del formulario con ancho reducido
        field_width = 250
        text_size = 12
        
        self.empleado_nombre_input = ft.TextField(label="Nombre", width=field_width, text_size=text_size)
        self.empleado_apellido_input = ft.TextField(label="Apellido", width=field_width, text_size=text_size)
        self.empleado_telefono_input = ft.TextField(label="Teléfono", width=field_width, text_size=text_size)
        self.empleado_email_input = ft.TextField(label="Email", width=field_width, text_size=text_size)
        self.empleado_direccion_input = ft.TextField(label="Dirección", width=field_width, text_size=text_size)
        self.empleado_puesto_input = ft.TextField(label="Puesto", width=field_width, text_size=text_size)
        self.empleado_salario_input = ft.TextField(
            label="Salario", 
            width=field_width, 
            input_filter=ft.NumbersOnlyInputFilter(), 
            text_size=text_size
        )
        self.empleado_fecha_input = ft.TextField(
            label="Fecha Contratación", 
            width=field_width,
            hint_text="YYYY-MM-DD",
            text_size=text_size
        )
        self.empleado_sucursal_dropdown = ft.Dropdown(
            label="Sucursal",
            width=field_width,
            options=[ft.dropdown.Option(s["id"], s["nombre"]) for s in sucursales],
            text_size=text_size
        )

        boton_crear = ft.ElevatedButton(
            text="Registrar Empleado",
            on_click=self.crear_empleado,
            width=field_width
        )

        # Contenedor con scroll vertical automático
        form_content = ft.Column(
            controls=[
                ft.Text("Registro de Empleado", size=16, weight=ft.FontWeight.BOLD),
                self.empleado_nombre_input,
                self.empleado_apellido_input,
                self.empleado_telefono_input,
                self.empleado_email_input,
                self.empleado_direccion_input,
                self.empleado_puesto_input,
                self.empleado_salario_input,
                self.empleado_fecha_input,
                self.empleado_sucursal_dropdown,
                boton_crear
            ],
            spacing=8
        )

        return ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,  # Altura fija con scroll interno si se necesita
            width=300,   # Ancho más compacto
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def crear_empleado(self, e):
        nombre = self.empleado_nombre_input.value.strip()
        apellido = self.empleado_apellido_input.value.strip()
        telefono = self.empleado_telefono_input.value.strip()
        email = self.empleado_email_input.value.strip()
        direccion = self.empleado_direccion_input.value.strip()
        puesto = self.empleado_puesto_input.value.strip()
        salario = self.empleado_salario_input.value.strip()
        fecha_contratacion = self.empleado_fecha_input.value.strip()
        id_sucursal = self.empleado_sucursal_dropdown.value

        # Validación de campos obligatorios
        if not all([nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        # Validación básica de email
        if "@" not in email or "." not in email:
            self.mostrar_mensaje("❌ Ingrese un email válido", color="red")
            return

        try:
            salario = float(salario)
        except ValueError:
            self.mostrar_mensaje("❌ Salario debe ser un número válido", color="red")
            return

        if crear_empleado_backend(nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal):
            self.mostrar_mensaje("✅ Empleado registrado correctamente")
            # Limpiar campos después de registro exitoso
            self.empleado_nombre_input.value = ""
            self.empleado_apellido_input.value = ""
            self.empleado_telefono_input.value = ""
            self.empleado_email_input.value = ""
            self.empleado_direccion_input.value = ""
            self.empleado_puesto_input.value = ""
            self.empleado_salario_input.value = ""
            self.empleado_fecha_input.value = ""
            self.empleado_sucursal_dropdown.value = None
            self.cambiar_contenido(None)  # Refrescar la tabla
        else:
            self.mostrar_mensaje("❌ Error al registrar empleado", color="red")

    def buscar_empleado(self, e):
        termino = self.buscador_input.value.strip().lower()
        if not termino:
            return

        empleados = obtener_empleados()
        filtrados = [e for e in empleados if 
                    termino in e["nombre"].lower() or 
                    termino in e["apellido"].lower() or
                    termino in e["puesto"].lower()]

        columnas = [
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Nombre")),
            ft.DataColumn(label=ft.Text("Apellido")),
            ft.DataColumn(label=ft.Text("Puesto")),
            ft.DataColumn(label=ft.Text("Sucursal")),
        ]

        filas = []
        for e in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(e["id"]))),
                    ft.DataCell(ft.Text(e["nombre"])),
                    ft.DataCell(ft.Text(e["apellido"])),
                    ft.DataCell(ft.Text(e["puesto"])),
                    ft.DataCell(ft.Text(e["sucursal"])),
                ]
            )
            filas.append(fila)

        tabla_filtrada = ft.DataTable(columns=columnas, rows=filas)

        self.frame_2.content = ft.Column([
            ft.Text(f"Resultados para '{termino}':", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([tabla_filtrada], scroll="auto"),
                height=300
            ),
            ft.Row([self.boton_refrescar], alignment=ft.MainAxisAlignment.END)
        ])

        self.frame_2.update()

    def cargar_formulario_actualizar_empleado(self, e):
        try:
            id_empleado = int(self.actualizar_id_input.value)
        except ValueError:
            self.mostrar_mensaje("❌ ID inválido", color="red")
            return

        empleado = obtener_empleado_por_id(id_empleado)
        if not empleado:
            self.mostrar_mensaje("❌ Empleado no encontrado", color="red")
            return

        sucursales = self.obtener_sucursales()
        field_width = 250
        text_size = 12

        self.empleado_nombre_actualizar = ft.TextField(label="Nombre", value=empleado["nombre"], width=field_width, text_size=text_size)
        self.empleado_apellido_actualizar = ft.TextField(label="Apellido", value=empleado["apellido"], width=field_width, text_size=text_size)
        self.empleado_telefono_actualizar = ft.TextField(label="Teléfono", value=empleado["telefono"], width=field_width, text_size=text_size)
        self.empleado_email_actualizar = ft.TextField(label="Email", value=empleado["email"], width=field_width, text_size=text_size)
        self.empleado_direccion_actualizar = ft.TextField(label="Dirección", value=empleado["direccion"], width=field_width, text_size=text_size)
        self.empleado_puesto_actualizar = ft.TextField(label="Puesto", value=empleado["puesto"], width=field_width, text_size=text_size)
        self.empleado_salario_actualizar = ft.TextField(
            label="Salario", 
            value=str(empleado["salario"]), 
            width=field_width, 
            input_filter=ft.NumbersOnlyInputFilter(), 
            text_size=text_size
        )
        self.empleado_fecha_actualizar = ft.TextField(
            label="Fecha Contratación", 
            value=empleado["fecha_contratacion"].strftime("%Y-%m-%d") if empleado["fecha_contratacion"] else "",
            width=field_width,
            hint_text="YYYY-MM-DD",
            text_size=text_size
        )
        self.empleado_sucursal_actualizar = ft.Dropdown(
            label="Sucursal",
            width=field_width,
            options=[ft.dropdown.Option(s["id"], s["nombre"]) for s in sucursales],
            value=empleado["id_sucursal"],
            text_size=text_size
        )

        boton_actualizar = ft.ElevatedButton(
            text="Actualizar Empleado",
            on_click=lambda e: self.actualizar_empleado(id_empleado),
            width=field_width
        )

        boton_volver = ft.TextButton(
            text="← Volver a Crear",
            on_click=self.cambiar_a_formulario_empleados
        )

        form_content = ft.Column(
            controls=[
                ft.Text("Formulario de Actualización", size=16, weight=ft.FontWeight.BOLD),
                self.empleado_nombre_actualizar,
                self.empleado_apellido_actualizar,
                self.empleado_telefono_actualizar,
                self.empleado_email_actualizar,
                self.empleado_direccion_actualizar,
                self.empleado_puesto_actualizar,
                self.empleado_salario_actualizar,
                self.empleado_fecha_actualizar,
                self.empleado_sucursal_actualizar,
                boton_actualizar,
                boton_volver
            ],
            spacing=8
        )

        self.frame_3.content = ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,
            width=300,
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

        self.frame_3.update()

    def actualizar_empleado(self, id_empleado):
        nombre = self.empleado_nombre_actualizar.value.strip()
        apellido = self.empleado_apellido_actualizar.value.strip()
        telefono = self.empleado_telefono_actualizar.value.strip()
        email = self.empleado_email_actualizar.value.strip()
        direccion = self.empleado_direccion_actualizar.value.strip()
        puesto = self.empleado_puesto_actualizar.value.strip()
        salario = self.empleado_salario_actualizar.value.strip()
        fecha_contratacion = self.empleado_fecha_actualizar.value.strip()
        id_sucursal = self.empleado_sucursal_actualizar.value

        # Validación de campos obligatorios
        if not all([nombre, apellido, telefono, email, direccion, puesto, salario, fecha_contratacion, id_sucursal]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        # Validación básica de email
        if "@" not in email or "." not in email:
            self.mostrar_mensaje("❌ Ingrese un email válido", color="red")
            return

        try:
            salario = float(salario)
        except ValueError:
            self.mostrar_mensaje("❌ Salario debe ser un número válido", color="red")
            return

        if actualizar_empleado_backend(
            id_empleado, nombre, apellido, telefono, email, 
            direccion, puesto, salario, fecha_contratacion, id_sucursal
        ):
            self.mostrar_mensaje("✅ Empleado actualizado correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al actualizar empleado", color="red")

    def confirmar_eliminar_empleado(self, e):
        try:
            id_empleado = int(self.eliminar_id_input.value)
        except ValueError:
            print("❌ ID inválido")
            return

        if eliminar_empleado_backend(id_empleado):
            self.mostrar_mensaje("✅ Empleado eliminado correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al eliminar empleado", color="red")

    def cambiar_a_formulario_empleados(self, e):
        """Vuelve al formulario de creación de empleados"""
        self.frame_3.content = self.construir_formulario_empleados()
        self.frame_3.update()
    # Fin CRUD's Empleados

    # Inicio CRUD's Ventas
    def construir_tabla_ventas(self):
        ventas = obtener_ventas()
        
        columnas = [
            ft.DataColumn(ft.Text("ID", size=10)),
            ft.DataColumn(ft.Text("Cliente", size=10)),
            ft.DataColumn(ft.Text("Empleado", size=10)),
            ft.DataColumn(ft.Text("Fecha", size=10)),
            ft.DataColumn(ft.Text("Total", size=10)),
        ]

        filas = []

        def limitar_texto(valor, max_len):
            if valor is None:
                return ""
            texto = str(valor)
            return texto[:max_len] + "..." if len(texto) > max_len else texto

        for v in ventas:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(v.get("id", "")), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(v.get("cliente"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(v.get("empleado"), 10), size=10)),
                    ft.DataCell(ft.Text(limitar_texto(v.get("fecha"), 10), size=10)),
                    ft.DataCell(ft.Text(f"${float(v.get('total', 0)):.2f}", size=10)),
                ]
            )
            filas.append(fila)

        data_table = ft.DataTable(
            columns=columnas,
            rows=filas,
            column_spacing=2,
            horizontal_margin=2,
            heading_row_height=25,
            data_row_min_height=25,
            data_row_max_height=30,
        )

        return ft.Container(
            content=data_table,
            width=700,
            height=300,
            padding=5,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def construir_formulario_ventas(self):
        # Obtener clientes y empleados para dropdowns
        clientes = obtener_clientes_para_dropdown()
        empleados = obtener_empleados_para_dropdown()
        
        # Campos del formulario
        field_width = 250
        text_size = 12
        
        self.venta_cliente_dropdown = ft.Dropdown(
            label="Cliente",
            width=field_width,
            options=[ft.dropdown.Option(c["id"], c["nombre"]) for c in clientes],
            text_size=text_size
        )
        self.venta_empleado_dropdown = ft.Dropdown(
            label="Empleado",
            width=field_width,
            options=[ft.dropdown.Option(e["id"], e["nombre"]) for e in empleados],
            text_size=text_size
        )
        self.venta_total_input = ft.TextField(
            label="Total",
            width=field_width,
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_text="$",
            text_size=text_size
        )

        boton_crear = ft.ElevatedButton(
            text="Registrar Venta",
            on_click=self.crear_venta,
            width=field_width
        )

        # Contenedor con scroll vertical automático
        form_content = ft.Column(
            controls=[
                ft.Text("Registro de Venta", size=16, weight=ft.FontWeight.BOLD),
                self.venta_cliente_dropdown,
                self.venta_empleado_dropdown,
                self.venta_total_input,
                boton_crear
            ],
            spacing=8
        )

        return ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,
            width=300,
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def crear_venta(self, e):
        id_cliente = self.venta_cliente_dropdown.value
        id_empleado = self.venta_empleado_dropdown.value
        total = self.venta_total_input.value.strip()

        # Validación de campos obligatorios
        if not all([id_cliente, id_empleado, total]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        try:
            total = float(total)
        except ValueError:
            self.mostrar_mensaje("❌ Total debe ser un número válido", color="red")
            return

        if crear_venta_backend(id_cliente, id_empleado, total):
            self.mostrar_mensaje("✅ Venta registrada correctamente")
            # Limpiar campos después de registro exitoso
            self.venta_total_input.value = ""
            self.cambiar_contenido(None)  # Refrescar la tabla
        else:
            self.mostrar_mensaje("❌ Error al registrar venta", color="red")

    def cargar_formulario_actualizar_venta(self, e):
        try:
            id_venta = int(self.actualizar_id_input.value)
        except ValueError:
            self.mostrar_mensaje("❌ ID inválido", color="red")
            return

        venta = obtener_venta_por_id(id_venta)
        if not venta:
            self.mostrar_mensaje("❌ Venta no encontrada", color="red")
            return

        # Obtener clientes y empleados para dropdowns
        clientes = obtener_clientes_para_dropdown()
        empleados = obtener_empleados_para_dropdown()
        
        field_width = 250
        text_size = 12

        self.venta_cliente_actualizar = ft.Dropdown(
            label="Cliente",
            width=field_width,
            options=[ft.dropdown.Option(c["id"], c["nombre"]) for c in clientes],
            value=venta["id_cliente"],
            text_size=text_size
        )
        self.venta_empleado_actualizar = ft.Dropdown(
            label="Empleado",
            width=field_width,
            options=[ft.dropdown.Option(e["id"], e["nombre"]) for e in empleados],
            value=venta["id_empleado"],
            text_size=text_size
        )
        self.venta_total_actualizar = ft.TextField(
            label="Total",
            width=field_width,
            value=str(venta["total"]),
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_text="$",
            text_size=text_size
        )

        boton_actualizar = ft.ElevatedButton(
            text="Actualizar Venta",
            on_click=lambda e: self.actualizar_venta(id_venta),
            width=field_width
        )

        boton_volver = ft.TextButton(
            text="← Volver a Crear",
            on_click=self.cambiar_a_formulario_ventas
        )

        form_content = ft.Column(
            controls=[
                ft.Text("Formulario de Actualización", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Venta ID: {id_venta}", size=14),
                ft.Text(f"Fecha: {venta['fecha']}", size=14),
                self.venta_cliente_actualizar,
                self.venta_empleado_actualizar,
                self.venta_total_actualizar,
                boton_actualizar,
                boton_volver
            ],
            spacing=8
        )

        self.frame_3.content = ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,
            width=300,
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

        self.frame_3.update()

    def actualizar_venta(self, id_venta):
        id_cliente = self.venta_cliente_actualizar.value
        id_empleado = self.venta_empleado_actualizar.value
        total = self.venta_total_actualizar.value.strip()

        # Validación de campos obligatorios
        if not all([id_cliente, id_empleado, total]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        try:
            total = float(total)
        except ValueError:
            self.mostrar_mensaje("❌ Total debe ser un número válido", color="red")
            return

        if actualizar_venta_backend(id_venta, id_cliente, id_empleado, total):
            self.mostrar_mensaje("✅ Venta actualizada correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al actualizar venta", color="red")

    def confirmar_eliminar_venta(self, e):
        try:
            id_venta = int(self.eliminar_id_input.value)
        except ValueError:
            print("❌ ID inválido")
            return

        if eliminar_venta_backend(id_venta):
            self.mostrar_mensaje("✅ Venta eliminada correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al eliminar venta", color="red")

    def cambiar_a_formulario_ventas(self, e):
        """Vuelve al formulario de creación de ventas"""
        self.frame_3.content = self.construir_formulario_ventas()
        self.frame_3.update()

    def buscar_venta(self, e):
        termino = self.buscador_input.value.strip().lower()
        if not termino:
            return

        ventas = obtener_ventas()
        filtrados = [v for v in ventas if 
                    termino in str(v["id"]).lower() or 
                    termino in v["cliente"].lower() or
                    termino in v["empleado"].lower()]

        columnas = [
            ft.DataColumn(ft.Text("ID", size=10)),
            ft.DataColumn(ft.Text("Cliente", size=10)),
            ft.DataColumn(ft.Text("Empleado", size=10)),
            ft.DataColumn(ft.Text("Total", size=10)),
            ft.DataColumn(ft.Text("Fecha", size=10)),
        ]

        filas = []
        for v in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(v["id"]), size=10)),
                    ft.DataCell(ft.Text(v["cliente"][:10] + "..." if len(v["cliente"]) > 10 else v["cliente"], size=10)),
                    ft.DataCell(ft.Text(v["empleado"][:10] + "..." if len(v["empleado"]) > 10 else v["empleado"], size=10)),
                    ft.DataCell(ft.Text(f"${float(v['total']):.2f}", size=10)),
                    ft.DataCell(ft.Text(str(v["fecha"])[:10], size=10)),
                ]
            )
            filas.append(fila)

        tabla_filtrada = ft.DataTable(
            columns=columnas,
            rows=filas,
            column_spacing=2,
            horizontal_margin=2,
            heading_row_height=25,
            data_row_min_height=25,
            data_row_max_height=30,
        )

        self.frame_2.content = ft.Column([
            ft.Text(f"Resultados para '{termino}':", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=tabla_filtrada,
                width=700,
                height=300,
                padding=5,
                border=ft.border.all(1, "#e0e0e0"),
                border_radius=ft.border_radius.all(8),
            ),
            ft.Row([self.boton_refrescar], alignment=ft.MainAxisAlignment.END)
        ])

        self.frame_2.update()

    # Fin CRUD's Ventas
    
    # Inicio CRUD's DetalleVenta

    def construir_tabla_detalles_venta(self, id_venta=None):
        detalles = obtener_detalles_venta(id_venta)
        columnas = [
            ft.DataColumn(ft.Text("ID", size=10)),
            ft.DataColumn(ft.Text("Venta", size=10)),
            ft.DataColumn(ft.Text("Producto", size=10)),
            ft.DataColumn(ft.Text("Cantidad", size=10)),
            ft.DataColumn(ft.Text("P. Unitario", size=10)),
            ft.DataColumn(ft.Text("Subtotal", size=10)),
        ]

        filas = []

        def limitar_texto(valor, max_len):
            if valor is None:
                return ""
            texto = str(valor)
            return texto[:max_len] + "..." if len(texto) > max_len else texto

        for d in detalles:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(d.get("id", "")), size=10)),
                    ft.DataCell(ft.Text(f"#{d.get('id_venta', '')}", size=10)),
                    ft.DataCell(ft.Text(limitar_texto(d.get("producto"), 10), size=10)),
                    ft.DataCell(ft.Text(str(d.get("cantidad", "")), size=10)),
                    ft.DataCell(ft.Text(f"${float(d.get('precio_unitario', 0)):.2f}", size=10)),
                    ft.DataCell(ft.Text(f"${float(d.get('subtotal', 0)):.2f}", size=10)),
                ]
            )
            filas.append(fila)

        data_table = ft.DataTable(
            columns=columnas,
            rows=filas,
            column_spacing=2,
            horizontal_margin=2,
            heading_row_height=25,
            data_row_min_height=25,
            data_row_max_height=30,
        )

        return ft.Container(
            content=data_table,
            width=700,
            height=300,
            padding=5,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def construir_formulario_detalles_venta(self):
        # Obtener ventas y productos para dropdowns
        ventas = obtener_ventas_para_dropdown()
        productos = obtener_productos_para_dropdown()
        
        # Campos del formulario
        field_width = 250
        text_size = 12
        
        self.detalle_venta_dropdown = ft.Dropdown(
            label="Venta",
            width=field_width,
            options=[ft.dropdown.Option(v["id"], v["nombre"]) for v in ventas],
            text_size=text_size
        )
        self.detalle_producto_dropdown = ft.Dropdown(
            label="Producto",
            width=field_width,
            options=[ft.dropdown.Option(p["id"], p["nombre"]) for p in productos],
            text_size=text_size
        )
        self.detalle_cantidad_input = ft.TextField(
            label="Cantidad",
            width=field_width,
            input_filter=ft.NumbersOnlyInputFilter(),
            text_size=text_size
        )
        self.detalle_precio_input = ft.TextField(
            label="Precio Unitario",
            width=field_width,
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_text="$",
            text_size=text_size
        )

        boton_crear = ft.ElevatedButton(
            text="Agregar Detalle",
            on_click=self.crear_detalle_venta,
            width=field_width
        )

        # Contenedor con scroll vertical automático
        form_content = ft.Column(
            controls=[
                ft.Text("Registro de Detalle", size=16, weight=ft.FontWeight.BOLD),
                self.detalle_venta_dropdown,
                self.detalle_producto_dropdown,
                self.detalle_cantidad_input,
                self.detalle_precio_input,
                boton_crear
            ],
            spacing=8
        )

        return ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,
            width=300,
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

    def crear_detalle_venta(self, e):
        id_venta = self.detalle_venta_dropdown.value
        id_producto = self.detalle_producto_dropdown.value
        cantidad = self.detalle_cantidad_input.value.strip()
        precio_unitario = self.detalle_precio_input.value.strip()

        # Validación de campos obligatorios
        if not all([id_venta, id_producto, cantidad, precio_unitario]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        try:
            cantidad = int(cantidad)
            precio_unitario = float(precio_unitario)
        except ValueError:
            self.mostrar_mensaje("❌ Cantidad y precio deben ser números válidos", color="red")
            return

        if crear_detalle_venta_backend(id_venta, id_producto, cantidad, precio_unitario):
            self.mostrar_mensaje("✅ Detalle de venta registrado correctamente")
            # Limpiar campos después de registro exitoso
            self.detalle_cantidad_input.value = ""
            self.detalle_precio_input.value = ""
            self.cambiar_contenido(None)  # Refrescar la tabla
        else:
            self.mostrar_mensaje("❌ Error al registrar detalle de venta", color="red")

    def buscar_detalle_venta(self, e):
        termino = self.buscador_input.value.strip().lower()
        if not termino:
            return

        detalles = obtener_detalles_venta()
        filtrados = [d for d in detalles if 
                    termino in str(d["id"]).lower() or 
                    termino in d["producto"].lower() or
                    termino in str(d["id_venta"]).lower()]

        columnas = [
            ft.DataColumn(ft.Text("ID", size=10)),
            ft.DataColumn(ft.Text("Venta", size=10)),
            ft.DataColumn(ft.Text("Producto", size=10)),
            ft.DataColumn(ft.Text("Subtotal", size=10)),
        ]

        filas = []
        for d in filtrados:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(d["id"]), size=10)),
                    ft.DataCell(ft.Text(f"#{d['id_venta']}", size=10)),
                    ft.DataCell(ft.Text(d["producto"][:10] + "..." if len(d["producto"]) > 10 else d["producto"], size=10)),
                    ft.DataCell(ft.Text(f"${float(d['subtotal']):.2f}", size=10)),
                ]
            )
            filas.append(fila)

        tabla_filtrada = ft.DataTable(
            columns=columnas,
            rows=filas,
            column_spacing=2,
            horizontal_margin=2,
            heading_row_height=25,
            data_row_min_height=25,
            data_row_max_height=30,
        )

        self.frame_2.content = ft.Column([
            ft.Text(f"Resultados para '{termino}':", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=tabla_filtrada,
                width=700,
                height=300,
                padding=5,
                border=ft.border.all(1, "#e0e0e0"),
                border_radius=ft.border_radius.all(8),
            ),
            ft.Row([self.boton_refrescar], alignment=ft.MainAxisAlignment.END)
        ])

        self.frame_2.update()

    def cargar_formulario_actualizar_detalle_venta(self, e):
        try:
            id_detalle = int(self.actualizar_id_input.value)
        except ValueError:
            self.mostrar_mensaje("❌ ID inválido", color="red")
            return

        detalle = obtener_detalle_por_id(id_detalle)
        if not detalle:
            self.mostrar_mensaje("❌ Detalle de venta no encontrado", color="red")
            return

        # Obtener ventas y productos para dropdowns
        ventas = obtener_ventas_para_dropdown()
        productos = obtener_productos_para_dropdown()
        
        field_width = 250
        text_size = 12

        self.detalle_venta_actualizar = ft.Dropdown(
            label="Venta",
            width=field_width,
            options=[ft.dropdown.Option(v["id"], v["nombre"]) for v in ventas],
            value=detalle["id_venta"],
            text_size=text_size
        )
        self.detalle_producto_actualizar = ft.Dropdown(
            label="Producto",
            width=field_width,
            options=[ft.dropdown.Option(p["id"], p["nombre"]) for p in productos],
            value=detalle["id_producto"],
            text_size=text_size
        )
        self.detalle_cantidad_actualizar = ft.TextField(
            label="Cantidad",
            width=field_width,
            value=str(detalle["cantidad"]),
            input_filter=ft.NumbersOnlyInputFilter(),
            text_size=text_size
        )
        self.detalle_precio_actualizar = ft.TextField(
            label="Precio Unitario",
            width=field_width,
            value=str(detalle["precio_unitario"]),
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_text="$",
            text_size=text_size
        )

        boton_actualizar = ft.ElevatedButton(
            text="Actualizar Detalle",
            on_click=lambda e: self.actualizar_detalle_venta(id_detalle),
            width=field_width
        )

        boton_volver = ft.TextButton(
            text="← Volver a Crear",
            on_click=self.cambiar_a_formulario_detalles_venta
        )

        form_content = ft.Column(
            controls=[
                ft.Text("Formulario de Actualización", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Detalle ID: {id_detalle}", size=14),
                ft.Text(f"Subtotal actual: ${float(detalle['subtotal']):.2f}", size=14),
                self.detalle_venta_actualizar,
                self.detalle_producto_actualizar,
                self.detalle_cantidad_actualizar,
                self.detalle_precio_actualizar,
                boton_actualizar,
                boton_volver
            ],
            spacing=8
        )

        self.frame_3.content = ft.Container(
            content=ft.ListView(
                controls=[form_content],
                expand=True
            ),
            height=400,
            width=300,
            padding=10,
            border=ft.border.all(1, "#e0e0e0"),
            border_radius=ft.border_radius.all(8),
        )

        self.frame_3.update()

    def actualizar_detalle_venta(self, id_detalle):
        id_venta = self.detalle_venta_actualizar.value
        id_producto = self.detalle_producto_actualizar.value
        cantidad = self.detalle_cantidad_actualizar.value.strip()
        precio_unitario = self.detalle_precio_actualizar.value.strip()

        # Validación de campos obligatorios
        if not all([id_venta, id_producto, cantidad, precio_unitario]):
            self.mostrar_mensaje("❌ Todos los campos son obligatorios", color="red")
            return

        try:
            cantidad = int(cantidad)
            precio_unitario = float(precio_unitario)
        except ValueError:
            self.mostrar_mensaje("❌ Cantidad y precio deben ser números válidos", color="red")
            return

        if actualizar_detalle_venta_backend(id_detalle, id_venta, id_producto, cantidad, precio_unitario):
            self.mostrar_mensaje("✅ Detalle de venta actualizado correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al actualizar detalle de venta", color="red")

    def confirmar_eliminar_detalle_venta(self, e):
        try:
            id_detalle = int(self.eliminar_id_input.value)
        except ValueError:
            print("❌ ID inválido")
            return

        if eliminar_detalle_venta_backend(id_detalle):
            self.mostrar_mensaje("✅ Detalle de venta eliminado correctamente")
            self.cambiar_contenido(None)
        else:
            self.mostrar_mensaje("❌ Error al eliminar detalle de venta", color="red")

    def cambiar_a_formulario_detalles_venta(self, e):
        """Vuelve al formulario de creación de detalles de venta"""
        self.frame_3.content = self.construir_formulario_detalles_venta()
        self.frame_3.update()

# Fin CRUD's DetalleVenta

    def build(self):
        return self.container
    
# Metodo main

def main(page: ft.Page):
    # Tamaño inicial
    page.window_width = 1280
    page.window_height = 720
    
    # Tamaño mínimo permitido
    page.window_min_height = 400
    page.window_min_width = 800
    
    # Tamaño maximo
    page.window_max_width = 1280
    page.window_max_height = 720

    page.theme_mode = ft.ThemeMode.SYSTEM
    
    page.title = "Tienda de Videojuegos - Vicioso++"
    page.window_icon = "C:\ABDS5A\Practicas - Git\Point Of Sale - Tienda de Videojuegos\imagenes\icons8-videojuego-64.ico"

    page.window.center() #En java es SetLocationRelativeTo(null)
    page.window.maximizable = False
    page.window.shadow

    ui = UI(page)
    page.add(ui.build())

ft.app(target=main, view=ft.AppView.FLET_APP)