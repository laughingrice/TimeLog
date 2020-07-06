from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from TimeLog.tray import TrayProg
from TimeLog.time_manager import TimeManager
import TimeLog.resource


def TimeLog(argv):
    app = QApplication(argv)
    app.setQuitOnLastWindowClosed(False)

    app.setWindowIcon(QIcon(":/icons/icon.png"))

    time_manager = TimeManager()
    trayprog = TrayProg(time_manager)

    app.exec()