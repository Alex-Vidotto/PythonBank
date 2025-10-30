from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton,
                             QLineEdit, QMessageBox, QWidget)
from PyQt6.QtGui import QFont
from db import registrar_user

class RegistrarUsuarioView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle("Formulario de registro")
        
        user_label = QLabel(self)
        user_label.setText("Usuario:")
        user_label.setFont(QFont("Arial", 10))
        user_label.move(20,44)
        
        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(90, 40, 250, 24)
        
        dni_label = QLabel(self)
        dni_label.setText("DNI:")
        dni_label.setFont(QFont("Arial", 10))
        dni_label.move(20,74)
        
        self.dni_input = QLineEdit(self)
        self.dni_input.setGeometry(90, 70, 250, 24)
        
        
        password_1_label = QLabel(self)
        password_1_label.setText("Contraseña:")
        password_1_label.setFont(QFont("Arial", 10))
        password_1_label.move(20,104)

        self.password_1_input = QLineEdit(self)
        self.password_1_input.setGeometry(90, 100, 250, 24)
        self.password_1_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        
        password_2_label = QLabel(self)
        password_2_label.setText("Contraseña:")
        password_2_label.setFont(QFont("Arial", 10))
        password_2_label.move(20,134)

        self.password_2_input = QLineEdit(self)
        self.password_2_input.setGeometry(90, 130, 250, 24)
        self.password_2_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        
        create_button = QPushButton(self)
        create_button.setText("Guardar")
        create_button.setGeometry(20, 170, 150, 30)
        create_button.clicked.connect(self.crear_usuario)
        
        cancelar_button = QPushButton(self)
        cancelar_button.setText("Cancelar")
        cancelar_button.setGeometry(170, 170, 150, 30)
        cancelar_button.clicked.connect(self.cancelar_creacion)
        
    def cancelar_creacion(self):
        self.close()
        
    def crear_usuario(self):
        dni = self.dni_input.text()
        nombre = self.user_input.text()
        password1 = self.password_1_input.text()
        password2 = self.password_2_input.text()
        lista = [dni, nombre, password1, password2]
        
        if not all([dni, nombre, password1, password2]):
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.",
                                    QMessageBox.StandardButton.Close)
                return
        if password1 != password2:
             QMessageBox.warning(self, "Erro", "Contraseña no son identicas",
                                 QMessageBox.StandardButton.Close)
             return
        
        try:
            registrar_user(dni, nombre, password1)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e), QMessageBox.StandardButton.Close)
            return
        QMessageBox.information(self, "Creacion exitosa", f"Usuario {nombre}, creado exitosamente",
                                QMessageBox.StandardButton.Ok)
        self.accept()