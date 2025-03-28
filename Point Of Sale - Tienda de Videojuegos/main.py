import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from menu_principal import Ui_MainWindow
from menu_producto import MenuProducto

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar botones a funciones
        self.ui.btn_productos.clicked.connect(self.abrir_menu_productos)

    def abrir_menu_productos(self):
        self.menu_producto = MenuProducto()
        self.menu_producto.show()
        self.close()  # Cierra la ventana actual

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainApp()
    ventana.show()
    sys.exit(app.exec())
