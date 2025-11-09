from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton,
                             QLineEdit, QMessageBox, QWidget,
                             QComboBox, QVBoxLayout, QHBoxLayout,
                             QTableWidget,QTableWidgetItem ,QHeaderView)
from PyQt6.QtGui import QFont
from db import crear_cuenta, buscar_usuario, id_por_dni, buscar_cuenta_id_dni

class RegistrarCuentaView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Formulario de registro")
        
        
        dni_label = QLabel(self)
        dni_label.setText("DNI:")
        dni_label.setFont(QFont("Arial", 10))
        dni_label.move(20,34)
        
        self.dni_input = QLineEdit(self)
        self.dni_input.setGeometry(70, 28, 270, 24)
        
        
        eleccion_cuenta_label = QLabel(self)
        eleccion_cuenta_label.setText("Tipo de Cuenta:")
        eleccion_cuenta_label.setFont(QFont("Arial", 10))
        eleccion_cuenta_label.move(20,69)

        self.eleccion_cuenta_input = QComboBox(self)
        self.eleccion_cuenta_input.setGeometry(120, 65, 220, 24)
        self.eleccion_cuenta_input.addItems(["Cta. Corriente", "Caja de Ahorro"])
        
        divisa_label = QLabel(self)
        divisa_label.setText("Divisas:")
        divisa_label.setFont(QFont("Arial", 10))
        divisa_label.move(20, 104)
        
        self.divisa_combobox = QComboBox(self)
        self.divisa_combobox.setGeometry(70, 100, 270, 24)
        self.divisa_combobox.addItems(["ARS", "USD", "EUR", "YUAN"])
        
        create_button = QPushButton(self)
        create_button.setText("Guardar")
        create_button.setGeometry(20, 170, 150, 30)
        create_button.clicked.connect(self.crear_cuenta)
        
        cancelar_button = QPushButton(self)
        cancelar_button.setText("Cancelar")
        cancelar_button.setGeometry(170, 170, 150, 30)
        cancelar_button.clicked.connect(self.cancelar_creacion)
        
    def cancelar_creacion(self):
        self.close()
        
    def crear_cuenta(self):
        dni = self.dni_input.text()
        tipo_cuenta = self.eleccion_cuenta_input.currentText()
        divisa = self.divisa_combobox.currentText()
        
        if buscar_usuario("dni", dni) is None:
            QMessageBox.warning(self, "Error", "El usuario no esta registrado",
                                QMessageBox.StandardButton.Ok)
            return
        
        id_dni_usuario = id_por_dni(int(dni))

        if crear_cuenta(id_dni_usuario, tipo_cuenta, divisa):
            QMessageBox.information(self, "Exito", "Cuenta creada con exito",
                                    QMessageBox.StandardButton.Ok)
            self.accept()
            
class CuentasView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle("Cuentas del Usuario")
        
        layout = QVBoxLayout()
        
        busqueda_layout = QHBoxLayout()
        
        dni_label = QLabel("DNI: ")
        dni_label.setFont(QFont("Arial", 10))
        busqueda_layout.addWidget(dni_label)
        
        self.dni_input = QLineEdit()
        self.dni_input.setPlaceholderText("Ejemplo: 12345678")
        busqueda_layout.addWidget(self.dni_input)
        
        btn_ver_cuenta = QPushButton("Ver cuentas")
        btn_ver_cuenta.clicked.connect(self.mostrar_cuenta)
        busqueda_layout.addWidget(btn_ver_cuenta)
        
        layout.addLayout(busqueda_layout)
        
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID cuenta", "Tipo de cuenta", "Divisa", "Saldo"])
        
        self.tabla.resizeColumnsToContents()
        
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setAlternatingRowColors(True)
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        
    def mostrar_cuenta(self):
        dni = self.dni_input.text()
        
        if not dni:
            QMessageBox.warning(self, "Error", "Por favor ingrese un DNI",
                                QMessageBox.StandardButton.Ok)
            return
        
        usuario = buscar_usuario("dni", dni)
        if usuario is None:
            QMessageBox.warning(self, "Error", "El usuario no existe en los registros",
                                QMessageBox.StandardButton.Ok)
            return
        
        id_dni_usuario = id_por_dni(int(dni))
        cuenta = buscar_cuenta_id_dni(id_dni_usuario)
        
        if not cuenta:
            QMessageBox.information(self, "Informacion del Uusario", "El usuario no posee cuentas registradas",
                                    QMessageBox.StandardButton.Ok)
            return
        
        self.mostrar_cuentas(cuenta)
        
    def mostrar_cuentas(self, cuentas):
        self.tabla.setRowCount(len(cuentas))
        
        for fila, cuenta in enumerate(cuentas):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(cuenta[0])))  #id
            self.tabla.setItem(fila, 1, QTableWidgetItem(cuenta[2]))       #cuenta
            self.tabla.setItem(fila, 2, QTableWidgetItem(cuenta[3]))       #divisa
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(cuenta[4])))  #saldo 
            
        self.tabla.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.setWindowTitle(f"Cuentas - {len(cuentas)} encontradas")