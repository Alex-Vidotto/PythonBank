from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QMessageBox, QMainWindow
from PyQt6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()
        
    def inicializar_ui(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("Python Bank Menu")
        self.contenido()
        
    def contenido(self):
        imagen = "xd.png"
        with open(imagen):
            imagen_label = QLabel(self)
            imagen_label.setPixmap(QPixmap(imagen))