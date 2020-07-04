"""
TODO: Remember last project for each client
TODO: remember last client
TODO: alphabetically/by date last used sort client / project list?
TODO: export report by month
TODO: Switch to CSV fiile
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import sys
import pathlib

from tray import TrayProg
from time_manager import TimeManager
import resource


# Create the app director
appPath = (pathlib.Path().home() / pathlib.Path(".local/share/TimeLog"))
appPath.mkdir(parents=True, exist_ok=True)

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

app.setWindowIcon(QIcon(":/icons/icon.png"))

time_manager = TimeManager(appPath)
trayprog = TrayProg(appPath, time_manager)

app.exec()
