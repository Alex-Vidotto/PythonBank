"""from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from db import buscar_usuario, id_por_dni, buscar_cuenta_id_dni

class CuentasView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(500, 300)
        self.setWindowTitle("Buscar Cuentas")
        
        layout = QVBoxLayout()
        
        # Búsqueda rápida
        search_layout = QHBoxLayout()
        self.dni_input = QLineEdit(placeholderText="DNI del usuario")
        self.dni_input.returnPressed.connect(self.buscar)
        search_layout.addWidget(QLabel("DNI:"))
        search_layout.addWidget(self.dni_input)
        search_layout.addWidget(QPushButton("Buscar", clicked=self.buscar))
        
        # Tabla simple
        self.tabla = QTableWidget(0, 4)
        self.tabla.setHorizontalHeaderLabels(["Cuenta", "DNI", "Tipo", "Divisa"])
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Limpiar", clicked=self.limpiar))
        btn_layout.addStretch()
        btn_layout.addWidget(QPushButton("Cerrar", clicked=self.close))
        
        layout.addLayout(search_layout)
        layout.addWidget(self.tabla)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def buscar(self):
        dni = self.dni_input.text().strip()
        if not dni: return
        
        usuario = buscar_usuario("dni", dni)
        if not usuario: 
            QMessageBox.warning(self, "Error", "Usuario no existe")
            return
            
        id_dni = id_por_dni(int(dni))
        cuentas = buscar_cuenta_id_dni(id_dni) if id_dni else []
        
        self.tabla.setRowCount(len(cuentas))
        for i, cuenta in enumerate(cuentas):
            for j, valor in enumerate(cuenta):
                self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))
        
    def limpiar(self):
        self.dni_input.clear()
        self.tabla.setRowCount(0)"""