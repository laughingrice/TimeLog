from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import sys

from tray import TrayProg
from time_manager import TimeManager
import resource

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

app.setWindowIcon(QIcon(":/icons/icon.png"))

time_manager = TimeManager()
trayprog = TrayProg(time_manager)

app.exec()
