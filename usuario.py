from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton,
                             QLineEdit, QMessageBox, QWidget, QComboBox)
from PyQt6.QtGui import QFont
from db import registrar_user, buscar_usuario

class RegistrarUsuarioView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Formulario de registro")
        
        user_label = QLabel(self)
        user_label.setText("Usuario:")
        user_label.setFont(QFont("Arial", 10))
        user_label.move(20,44)
        
        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(70, 40, 260, 24)
        
        dni_label = QLabel(self)
        dni_label.setText("DNI:")
        dni_label.setFont(QFont("Arial", 10))
        dni_label.move(20,84)
        
        self.dni_input = QLineEdit(self)
        self.dni_input.setGeometry(60, 74, 270, 24)
        
        
        user_label = QLabel(self)
        user_label.setText("Tipo de Cliente:")
        user_label.setFont(QFont("Arial", 10))
        user_label.move(20,118)
        
        self.eleccion_persona = QComboBox(self)
        self.eleccion_persona.setGeometry(120, 114, 210, 24)
        self.eleccion_persona.addItems(["Persona", "Empresa"])
        
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
        eleccion_persona = self.eleccion_persona.currentText()
        
        if not all([dni, nombre, eleccion_persona]):
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.",
                                    QMessageBox.StandardButton.Close)
                return
        if buscar_usuario("dni", dni) != None:
             QMessageBox.warning(self, "Erro", "Ya existe el usuario",
                                 QMessageBox.StandardButton.Close)
             return
        
        try:
            registrar_user(dni, nombre, eleccion_persona)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e), QMessageBox.StandardButton.Close)
            return
        QMessageBox.information(self, "Creacion exitosa", f"Usuario {nombre}, creado exitosamente",
                                QMessageBox.StandardButton.Ok)
        self.accept()