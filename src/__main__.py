"""
TODO: Remember last project for each client
TODO: remember last client
TODO: alphabetically/by date last used sort client / project list?
TODO: search icon in app directory
TODO: package app in zip?
TODO: export report by month
TODO: Switch to CSV fiile
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import sys
import os

from tray import TrayProg
from time_manager import TimeManager


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

icon_path = os.path.dirname(os.path.abspath(__file__))
icon_fname = os.path.join(icon_path, "icon.png")
app.setWindowIcon(QIcon(icon_fname))

time_manager = TimeManager()
trayprog = TrayProg(time_manager)

app.exec()
