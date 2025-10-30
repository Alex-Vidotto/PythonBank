import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit,
                             QPushButton, QMessageBox, QCheckBox)
from PyQt6.QtGui import QFont, QPixmap

from vista.registrar_usuario import RegistrarUsuarioView
from db import crear_tablas, buscar_usuario
from vista.menu_principal import MainWindow

crear_tablas()
class Login(QWidget):
    
    def __init__(self):
        super().__init__()
        self.inicializar_interfaz()
        
    def inicializar_interfaz(self):
        self.setGeometry(100,100,350,250)
        self.setWindowTitle("Python Bank")
        self.inicio_sesion()
        self.show()
        
    def inicio_sesion(self):
        self.is_logged = False
        
        dni_label = QLabel(self)
        dni_label.setText("DNI:")
        dni_label.setFont(QFont('Arial',10))
        dni_label.move(20,54)
        
        self.dni_input = QLineEdit(self)
        self.dni_input.setGeometry(90, 50, 250, 24)
        
        password_label = QLabel(self)
        password_label.setText("Contraseña: ")
        password_label.setFont(QFont('Arial',10))
        password_label.move(20,86)
        
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(90, 82, 250, 24)
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.check_view_password = QCheckBox(self)
        self.check_view_password.setText("Ver contraseña")
        self.check_view_password.move(90,110)
        self.check_view_password.clicked.connect(self.mostrar_password)
        
        
        login_button = QPushButton(self)
        login_button.setText("Iniciar sesion")
        login_button.setGeometry(20, 140, 320, 34)
        login_button.clicked.connect(self.iniciar_user)
        
        register_button = QPushButton(self)
        register_button.setText("Registrarse")
        register_button.setGeometry(20, 180, 320, 34)
        register_button.clicked.connect(self.registrar_user)
        
        
    def mostrar_password(self, click):
        if click:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def iniciar_user(self):
        dni = self.dni_input.text()
        password = self.password_input.text()
        usuario = buscar_usuario("dni", dni)

        if not usuario:
            QMessageBox.warning(self, "Error", "DNI no registrado.",
                                QMessageBox.StandardButton.Ok)
            return
    
        if usuario[2] != password:
            QMessageBox.warning(self, "Error", "Contraseña incorrecta.",
                                QMessageBox.StandardButton.Ok)
            return
    
        QMessageBox.information(self, "Bienvenido", f"Usuario {usuario[1]} inició sesión.",
                                QMessageBox.StandardButton.Ok)
        self.close()
        self.open_main_window()
    
    def registrar_user(self):
        self.new_user = RegistrarUsuarioView()
        self.new_user.show()
        
    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())
    

