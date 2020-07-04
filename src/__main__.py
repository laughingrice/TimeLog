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

from tray import TrayProg
from time_manager import TimeManager
import resource


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

app.setWindowIcon(QIcon(":/icons/icon.png"))

time_manager = TimeManager()
trayprog = TrayProg(time_manager)

app.exec()
