from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime, QTimer

from datetime import datetime


class TrayProg(QSystemTrayIcon):
    def __init__(self, time_manager):
        super().__init__()

        self.time_manager = time_manager
        self.running = False
        self.active_client = None
        self.active_project = None
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.TimerTick)

        self.setIcon(QIcon("icon.png"))

        self.top_menu = QMenu()
        self.create_menu()

        self.setVisible(True)

    def create_menu(self):
        self.top_menu_start_stop = QAction("Start")
        self.top_menu_start_stop.triggered.connect(self.start_stop)
        self.top_menu.addAction(self.top_menu_start_stop)

        self.top_menu_project = QAction("none : none")
        self.top_menu.addAction(self.top_menu_project)

        self.top_menu_time = QAction("Time: 00:00:00")
        self.top_menu.addAction(self.top_menu_time)

        self.top_menu.addSeparator()

        self.clients_menu = QMenu("Clients")

        self.clients_menu_new = QAction("New Client")
        self.clients_menu_new.triggered.connect(self.new_client)
        self.clients_menu.addAction(self.clients_menu_new)
        self.clients_menu.addSeparator()

        client_list = self.time_manager.get_clients()
        self.client_menu_clients = []

        if len(client_list):
            self.active_client = client_list[0]

            for client in client_list:
                c = QAction(client)
                self.client_menu_clients.append(c)
                c.triggered.connect(self.set_client)
                self.clients_menu.addAction(c)

        self.top_menu.addMenu(self.clients_menu)

        self.projects_menu = QMenu("Projects")

        self.projects_menu_new = QAction("New Project")
        self.projects_menu_new.triggered.connect(self.new_project)
        self.projects_menu.addAction(self.projects_menu_new)
        self.projects_menu.addSeparator()

        if len(client_list):
            project_list = self.time_manager.get_client_projects(client_list[0])
            self.project_menu_projects = []
            if len(project_list):
                self.active_project = project_list[0]

                for project in project_list:
                    p = QAction(project)
                    self.project_menu_projects.append(p)
                    p.triggered.connect(self.set_project)
                    self.projects_menu.addAction(p)

        self.top_menu.addMenu(self.projects_menu)

        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

        # Add a Quit option to the menu.
        self.top_menu.addSeparator()
        self.top_menu_quit = QAction("Quit")
        self.top_menu_quit.triggered.connect(qApp.quit)
        self.top_menu.addAction(self.top_menu_quit)

        # Add the menu to the tray
        self.setContextMenu(self.top_menu)

    def new_client(self):
        client, res = QInputDialog.getText(None, 'Add Client', 'Client Name')
        if not res:
            return

        self.time_manager.add_client(client)

        c = QAction(client)
        self.client_menu_clients.append(c)
        c.triggered.connect(self.set_client)
        self.clients_menu.addAction(c)

        self.active_client = client
        self.active_project = None
        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def set_client(self):
        client = self.sender().text()

        self.active_client = client
        self.active_project = None

        project_list = self.time_manager.get_client_projects(client)
        self.project_menu_projects = []
        if len(project_list):
            self.active_project = project_list[0]

            for project in project_list:
                p = QAction(project)
                self.project_menu_projects.append(p)
                p.triggered.connect(self.set_project)
                self.projects_menu.addAction(p)

        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def new_project(self):
        project, res = QInputDialog.getText(None, 'Add Project', 'Project Name')
        if not res:
            return

        self.time_manager.add_project(self.active_client, project)

        p = QAction(project)
        self.project_menu_projects.append(p)
        p.triggered.connect(self.set_project)
        self.projects_menu.addAction(p)

        self.active_project = project
        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def set_project(self, project):
        self.active_project = self.sender().text()
        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def start_stop(self):
        self.running = not self.running
        self.top_menu_start_stop.setText("Stop" if self.running else "Start")

        if self.running:
            self.start_time = datetime.now()
            self.timer.start(1000.0)
        else:
            end_time = datetime.now()
            self.timer.stop()
            duration = end_time - self.start_time

            self.time_manager.add_time_entry(self.active_client, self.active_project, self.start_time, end_time, duration.total_seconds())

            self.start_time = None

    def TimerTick(self):
        duration = datetime.now() - self.start_time
        self.top_menu_time.setText(f"Time: {str(duration).split('.')[0]}")