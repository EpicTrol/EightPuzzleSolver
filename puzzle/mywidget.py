from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QFont

class Btn(QPushButton):
    def __init__(self, QIcon, str, parent=None):
        super().__init__(QIcon, str, parent=parent)
        
        