import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QWidget,
                             QTabWidget, QHBoxLayout, QDockWidget, QListWidget, 
                             QLabel, QLineEdit, QVBoxLayout, QPushButton)
from PyQt6.QtGui import QAction, QKeySequence, QFont
from cuenta import RegistrarCuentaView, CuentasView
from usuario import RegistrarUsuarioView
from db import crear_tablas, buscar_cuenta_id_dni, id_por_dni

crear_tablas()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def inicializar_ui(self):
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle("Banco")
        self.generar_menu()
        self.show()
        
        
    def generar_menu(self):
        tab_bar = QTabWidget(self)
        self.sector_cuenta = QWidget()
        self.sector_operaciones = QWidget()
        self.sector_settings = QWidget()
        tab_bar.addTab(self.sector_cuenta, "Menu principal")
        tab_bar.addTab(self.sector_operaciones, "Operaciones")
        tab_bar.addTab(self.sector_settings, "Configuracion")
        
        self.sector_cuenta_ui()
        self.sector_operaciones_ui()
        
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        
        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
        
        
        
        
    def sector_cuenta_ui(self):
        layout_vertical = QVBoxLayout() #incorpora layaout principal vertical para la izquierda

        btn_crear_cuenta = QPushButton(self)
        btn_crear_cuenta.setText("Crear Cuenta")
        btn_crear_cuenta.clicked.connect(self.registrar_cuenta)
        
        btn_ver_cuenta = QPushButton(self)
        btn_ver_cuenta.setText("Ver Cuenta")
        btn_ver_cuenta.clicked.connect(self.ver_cuentas)
        
        btn_informe_cuenta = QPushButton(self)
        btn_informe_cuenta.setText("Editar Cuenta")
        
        btn_historial_cuenta = QPushButton(self)
        btn_historial_cuenta.setText("Eliminar Cuenta")
        

        btn_crear_cliente = QPushButton(self)
        btn_crear_cliente.setText("Crear Cliente")
        btn_crear_cliente.clicked.connect(self.registrar_usuario)
        
        btn_ver_cliente = QPushButton(self)
        btn_ver_cliente.setText("Ver Cliente")
        
        btn_informe_cliente = QPushButton(self)
        btn_informe_cliente.setText("Editar Cliente")
        
        btn_historial_cliente = QPushButton(self)
        btn_historial_cliente.setText("Eliminar Cliente")

        layout_vertical.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout_vertical.addWidget(btn_crear_cliente)
        layout_vertical.addWidget(btn_ver_cliente)
        layout_vertical.addWidget(btn_informe_cliente)
        layout_vertical.addWidget(btn_historial_cliente)
        
        layout_vertical.addSpacing(20)

        layout_vertical.addWidget(btn_crear_cuenta)
        layout_vertical.addWidget(btn_ver_cuenta)
        layout_vertical.addWidget(btn_informe_cuenta)
        layout_vertical.addWidget(btn_historial_cuenta)
        

        self.sector_cuenta.setLayout(layout_vertical)

    def sector_operaciones_ui(self):
        pass
    
    def registrar_cuenta(self):
        self.new_cuenta = RegistrarCuentaView()
        self.new_cuenta.show()
        
    def registrar_usuario(self):
        self.new_user = RegistrarUsuarioView()
        self.new_user.show()
        
    def ver_cuentas(self):
        self.view_cuentas = CuentasView()
        self.view_cuentas.show()
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    sys.exit(app.exec())
    
