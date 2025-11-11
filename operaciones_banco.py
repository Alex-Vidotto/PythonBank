from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QLabel, QPushButton,
                             QLineEdit, QMessageBox, QWidget,
                             QComboBox, QVBoxLayout, QHBoxLayout,
                             QTableWidget,QTableWidgetItem ,QHeaderView)
from PyQt6.QtGui import QFont
from db import *
import qtawesome

class DepositoView(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Deposito")
        
        nro_cuenta_label = QLabel(self)
        nro_cuenta_label.setText("Nro Cuenta:")
        nro_cuenta_label.setFont(QFont("Arrial", 10))
        nro_cuenta_label.move(20, 34)
        
        self.nro_cuenta_input = QLineEdit(self)
        self.nro_cuenta_input.setPlaceholderText("Ejemplo: 1001")
        self.nro_cuenta_input.setGeometry(120, 28, 200, 24)
        
        dinero = QLabel(self)
        dinero.setText("Dinero a depositar:")
        dinero.setFont(QFont("Arial", 10))
        dinero.move(20, 69)
        
        self.dinero_input = QLineEdit(self)
        self.dinero_input.setPlaceholderText("Ejemplo: 1000")
        self.dinero_input.setGeometry(150, 65, 170, 24)
        
        btn_depositar = QPushButton(self)
        btn_depositar.setText("Depositar")
        btn_depositar.setGeometry(20, 170, 150, 30)
        btn_depositar.clicked.connect(self.realizar_deposito)
        
        
    def realizar_deposito(self):
        try:
            cuenta = self.nro_cuenta_input.text().strip()
            monto_texto = self.dinero_input.text().strip()

            if not cuenta or not monto_texto:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.", 
                                    QMessageBox.StandardButton.Ok)
                return

            try:
                monto = float(monto_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "El monto debe ser un número válido.", 
                                    QMessageBox.StandardButton.Ok)
                return

            cuenta_info = buscar_cuenta_por_id(cuenta)
            if not cuenta_info:
                QMessageBox.warning(self, "Error", "La cuenta no existe.", 
                                    QMessageBox.StandardButton.Ok)
                return

            if monto <= 0:
                QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero.",
                                    QMessageBox.StandardButton.Ok)
                return

            if depositar_dinero(cuenta, monto):
                registrar_operaciones("DEPOSITO", cuenta, None, monto)
                QMessageBox.information(self, "Éxito", "Depósito realizado con éxito",
                                        QMessageBox.StandardButton.Ok)
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Error al realizar el depósito",
                                    QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}",
                                QMessageBox.StandardButton.Ok)
            
                
class RetiroView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Retiro")
        
        nro_cuenta_label = QLabel(self)
        nro_cuenta_label.setText("Nro Cuenta:")
        nro_cuenta_label.setFont(QFont("Arrial", 10))
        nro_cuenta_label.move(20, 34)
        
        self.nro_cuenta_input = QLineEdit(self)
        self.nro_cuenta_input.setPlaceholderText("Ejemplo: 1001")
        self.nro_cuenta_input.setGeometry(120, 28, 200, 24)
        
        dinero = QLabel(self)
        dinero.setText("Dinero a retirar:")
        dinero.setFont(QFont("Arial", 10))
        dinero.move(20, 69)
        
        self.dinero_input = QLineEdit(self)
        self.dinero_input.setPlaceholderText("Ejemplo: 1000")
        self.dinero_input.setGeometry(150, 65, 170, 24)
        
        btn_retirar = QPushButton(self)
        btn_retirar.setText("Retirar")
        btn_retirar.setGeometry(20, 170, 150, 30)
        btn_retirar.clicked.connect(self.realizar_retiro)
        
        
    def realizar_retiro(self):
        try:
            cuenta = self.nro_cuenta_input.text().strip()
            monto_texto = self.dinero_input.text().strip()
            
            if not cuenta or not monto_texto:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.", 
                                    QMessageBox.StandardButton.Ok)
                return
            
            try:
                monto = float(monto_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "El monto debe ser un número válido.", 
                                    QMessageBox.StandardButton.Ok)
                return
            
            cuenta_info = buscar_cuenta_por_id(cuenta)
            if not cuenta_info:
                QMessageBox.warning(self, "Error", "La cuenta no existe.", 
                                    QMessageBox.StandardButton.Ok)
                return 
            
            saldo = saldo_actual_cuenta(cuenta)
            if saldo is None:
                QMessageBox.warning(self, "Error", "Error al consultar el saldo de la cuenta.", 
                                    QMessageBox.StandardButton.Ok)
                return
            
            if monto <= 0:
                QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero.",
                                    QMessageBox.StandardButton.Ok)
                return
            
            if monto > saldo:
                QMessageBox.warning(self, "Error", "Fondos insuficientes para realizar el retiro.",
                                    QMessageBox.StandardButton.Ok)
                return 
        
            retirar_dinero(cuenta, monto)
            registrar_operaciones("RETIRO", cuenta, None, monto)

            QMessageBox.information(self, "Éxito", "Retiro realizado con éxito",
                                    QMessageBox.StandardButton.Ok)
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}",
                                QMessageBox.StandardButton.Ok)
        
        
class TransferirView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Tranferencia")
        
        nro_cuenta_origen_label = QLabel(self)
        nro_cuenta_origen_label.setText("Nro Cuenta de Origen:")
        nro_cuenta_origen_label.setFont(QFont("Arial", 10))
        nro_cuenta_origen_label.move(20, 34)
        
        self.nro_cuenta_origen_input = QLineEdit(self)
        self.nro_cuenta_origen_input.setPlaceholderText("Ejemplo: 1001")
        self.nro_cuenta_origen_input.setGeometry(120, 28, 200, 24)
        
        nro_cuenta_destino_label = QLabel(self)
        nro_cuenta_destino_label.setText("Nro de Cuenta de Destino:")
        nro_cuenta_destino_label.setFont(QFont("Arial", 10))
        nro_cuenta_destino_label.move(20, 69)
        
        self.nro_cuenta_destino_input = QLineEdit(self)
        self.nro_cuenta_destino_input.setPlaceholderText("Ejemplo: 1225")
        self.nro_cuenta_destino_input.setGeometry(170, 65, 150, 24)
        
        dinero_transferir_label =QLabel(self)
        dinero_transferir_label.setText("Dienero a transferir:")
        dinero_transferir_label.setFont(QFont("Arial", 10))
        dinero_transferir_label.move(20, 104)
        
        self.dinero_transferir_input = QLineEdit(self)
        self.dinero_transferir_input.setPlaceholderText("Ejemplo: 500")
        self.dinero_transferir_input.setGeometry(150, 100, 170, 24)
        
        btn_transferir = QPushButton(self)
        btn_transferir.setText("Transferir")
        btn_transferir.setGeometry(20, 170, 150, 30)
        btn_transferir.clicked.connect(self.transferir_operacion)
        
    def transferir_operacion(self):
        try:
            cuenta_origen = self.nro_cuenta_origen_input.text().strip()
            cuenta_destino = self.nro_cuenta_destino_input.text().strip()
            monto_texto = self.dinero_transferir_input.text().strip()

            if not cuenta_origen or not cuenta_destino or not monto_texto:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.", 
                                    QMessageBox.StandardButton.Ok)
                return

            if cuenta_origen == cuenta_destino:
                QMessageBox.warning(self, "Error", "No puedes transferir a la misma cuenta.", 
                                    QMessageBox.StandardButton.Ok)
                return

            try:
                monto = float(monto_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "El monto debe ser un número válido.", 
                                    QMessageBox.StandardButton.Ok)
                return

            cuenta_origen_info = buscar_cuenta_por_id(cuenta_origen)
            cuenta_destino_info = buscar_cuenta_por_id(cuenta_destino)

            if not cuenta_origen_info:
                QMessageBox.warning(self, "Error", "La cuenta de origen no existe.", 
                                    QMessageBox.StandardButton.Ok)
                return 

            if not cuenta_destino_info:
                QMessageBox.warning(self, "Error", "La cuenta de destino no existe.", 
                                    QMessageBox.StandardButton.Ok)
                return 

            saldo_origen = saldo_actual_cuenta(cuenta_origen)
            if saldo_origen is None:
                QMessageBox.warning(self, "Error", "Error al consultar saldo de la cuenta origen.", 
                                    QMessageBox.StandardButton.Ok)
                return

            if monto <= 0:
                QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero.",
                                    QMessageBox.StandardButton.Ok)
                return

            if monto > saldo_origen:
                QMessageBox.warning(self, "Error", "Fondos insuficientes.",
                                    QMessageBox.StandardButton.Ok)
                return 

            retirar_dinero(cuenta_origen, monto)
            depositar_dinero(cuenta_destino, monto)
            registrar_operaciones("TRANSFERENCIA", cuenta_origen, cuenta_destino, monto)

            QMessageBox.information(self, "Éxito", "Transferencia realizada con éxito",
                                    QMessageBox.StandardButton.Ok)
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}",
                                QMessageBox.StandardButton.Ok)
            
class PlazoFijoView(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()
        
    def generar_formulario(self):
        self.setFixedSize(350, 250)
        self.setWindowTitle("Plazo Fijo")
        
        
        dni_icon = qtawesome.icon('fa5s.id-card', color='#3498db')
        dni_label = QLabel(self)
        dni_label.setPixmap(dni_icon.pixmap(16, 16))
        dni_label.move(20, 34)

        dni_text = QLabel(self)
        dni_text.setText("DNI:")
        dni_text.setFont(QFont("Arial", 10))
        dni_text.move(40, 34)

        self.dni_input = QLineEdit(self)
        self.dni_input.setGeometry(80, 28, 250, 24)
        
        dias_icon = qtawesome.icon('fa5s.university', color='#e74c3c')
        dias_label = QLabel(self)
        dias_label.setPixmap(dias_icon.pixmap(16, 16))
        dias_label.move(20, 69)

        eleccion_dias_label = QLabel(self)
        eleccion_dias_label.setText("Tiempo del Plazo Fijo:")
        eleccion_dias_label.setFont(QFont("Arial", 10))
        eleccion_dias_label.move(40, 69)

        self.eleccion_dias_input = QComboBox(self)
        self.eleccion_dias_input.setGeometry(140, 65, 190, 24)
        self.eleccion_dias_input.addItems(["30", "60", "90", "180", "365"])
        
        monto_icon = qtawesome.icon('fa5s.money-bill-wave', color='#27ae60')
        monto_label = QLabel(self)
        monto_label.setPixmap(monto_icon.pixmap(16, 16))
        monto_label.move(20, 104)
        
        monto_label_text = QLabel(self)
        monto_label_text.setText("Monto a depositar en Plazo Fijo:")
        monto_label_text.setFont(QFont("Arial", 10))
        monto_label_text.move(40, 104)
        
        self.monto_input = QLineEdit(self)
        self.monto_input.setGeometry(220, 100, 110, 24)
        
        btn_crear_plazo_fijo = QPushButton(self)
        btn_crear_plazo_fijo.setText("Crear Plazo Fijo")
        btn_crear_plazo_fijo.setGeometry(20, 170, 150, 30)
        btn_crear_plazo_fijo.clicked.connect(self.crear_plazo_fijo)
        
    def crear_plazo_fijo(self):
        try:
            dni = self.dni_input.text().strip()
            tiempo_texto = self.eleccion_dias_input.currentText().strip()
            monto_texto = self.monto_input.text().strip()

            # Validar campos vacíos
            if not dni or not tiempo_texto or not monto_texto:
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios",
                                    QMessageBox.StandardButton.Ok)
                return

            # Validar usuario
            usuario = buscar_usuario("dni", dni)
            if usuario is None:
                QMessageBox.warning(self, "Error", "El usuario no existe",  # Corregido "Erro"
                                    QMessageBox.StandardButton.Ok)
                return

            # Validar monto
            try:
                monto = float(monto_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "El monto debe ser un número válido.", 
                                    QMessageBox.StandardButton.Ok)
                return

            if monto <= 0:
                QMessageBox.warning(self, "Error", "El monto debe ser mayor a cero.",
                                    QMessageBox.StandardButton.Ok)
                return      

            # Obtener id_dni y extraer días del texto
            id_dni_usuario = id_por_dni(dni)  # Sin int() si dni es texto

            # Extraer solo los números del texto de tiempo (ej: "30 días" -> 30)
            try:
                if not tiempo_texto.isdigit():
                    QMessageBox.warning(self, "Error", "El tiempo debe contener solo números",
                                        QMessageBox.StandardButton.Ok)
                    return
                tiempo_dias = int(tiempo_texto)
            except ValueError:
                QMessageBox.warning(self, "Error", "El tiempo debe ser un número válido",
                                    QMessageBox.StandardButton.Ok)
                return

            # Crear la cuenta de plazo fijo
            if crear_cuenta_plazo_fijo(id_dni_usuario, 'Plazo Fijo', 'ARS', tiempo_dias, monto):
                QMessageBox.information(self, "Éxito", "Plazo fijo creado correctamente",
                                        QMessageBox.StandardButton.Ok)
                self.close()
            else:
                QMessageBox.warning(self, "Error", "No se pudo crear el plazo fijo",
                                    QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error crítico: {str(e)}",
                                 QMessageBox.StandardButton.Ok)