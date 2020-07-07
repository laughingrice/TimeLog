from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import sys

from TimeLog.tray import TrayProg
from TimeLog.time_manager import TimeManager
import TimeLog.resource


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    app.setWindowIcon(QIcon(":/icons/icon.png"))

    time_manager = TimeManager()
    trayprog = TrayProg(time_manager)
    trayprog.setToolTip('TimeLog')
    trayprog.show()

    app.exec()