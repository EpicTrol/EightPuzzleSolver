    
from PyQt5.QtWidgets import QApplication
import puzzle.gui as gui
import sys
app = QApplication(sys.argv)
ex = gui.Example()
sys.exit(app.exec_())