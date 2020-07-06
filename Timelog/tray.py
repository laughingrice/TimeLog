from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime, QTimer

from datetime import datetime
import yaml
import os

from TimeLog.config import app_path
import TimeLog.resource

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

        self.history_file = str(app_path / "history.yaml")
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = yaml.safe_load(f)
        else:
            self.history = {'last_client': None, 'last_projects': {}}
            with open(self.history_file, 'w') as f:
                yaml.safe_dump(self.history, f)

        self.setIcon(QIcon(":/icons/icon.png"))

        self.top_menu = QMenu()
        self.top_menu_start_stop = QAction("Start")
        self.top_menu_time = QAction("Time: 00:00:00")
        self.top_menu_project = QAction("none : none")
        self.clients_menu = QMenu("Clients")
        self.clients_menu_new = QAction("New Client")
        self.projects_menu = QMenu("Projects")
        self.projects_menu_new = QAction("New Project")
        self.top_menu_quit = QAction("Quit")
        self.client_menu_clients = []
        self.project_menu_projects = []

        self.__configure_menu()

        self.setContextMenu(self.top_menu)

        self.setVisible(True)

    def __configure_menu(self):
        self.top_menu_start_stop.triggered.connect(self.start_stop)
        self.top_menu.addAction(self.top_menu_start_stop)
        self.top_menu.addAction(self.top_menu_project)
        self.top_menu.addAction(self.top_menu_time)

        self.top_menu.addSeparator()

        self.top_menu.addMenu(self.clients_menu)
        self.clients_menu.addAction(self.clients_menu_new)
        self.clients_menu_new.triggered.connect(self.new_client)
        self.clients_menu.addSeparator()

        self.top_menu.addMenu(self.projects_menu)
        self.projects_menu_new.triggered.connect(self.new_project)
        self.projects_menu.addAction(self.projects_menu_new)
        self.projects_menu.addSeparator()

        self.top_menu.addSeparator()
        self.top_menu_quit.triggered.connect(qApp.quit)
        self.top_menu.addAction(self.top_menu_quit)

        client_list = self.time_manager.get_clients()

        if len(client_list):
            if self.history['last_client'] is not None and self.history['last_client'] in client_list:
                self.active_client = self.history['last_client']
            else:
                self.active_client = client_list[0]
                self.history['last_client'] = self.active_client
                with open(self.history_file, 'w') as f:
                    yaml.safe_dump(self.history, f)

            for client in client_list:
                c = QAction(client)
                self.client_menu_clients.append(c)
                c.triggered.connect(self.set_client)
                self.clients_menu.addAction(c)

                project_list = self.time_manager.get_client_projects(client_list[0])
                if len(project_list):
                    if self.active_client in self.history['last_projects'] and self.history['last_projects'][self.active_client] in project_list:
                        self.active_project = self.history['last_projects'][self.active_client]
                    else:
                        self.active_project = project_list[0]
                        self.history['last_projects'][self.active_client] = self.active_project
                        with open(self.history_file, 'w') as f:
                            yaml.safe_dump(self.history, f)

                    for project in project_list:
                        p = QAction(project)
                        self.project_menu_projects.append(p)
                        p.triggered.connect(self.set_project)
                        self.projects_menu.addAction(p)

        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

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

        self.history['last_client'] = self.active_client
        self.history['last_projects'][self.active_client] = self.active_project
        with open(self.history_file, 'w') as f:
            yaml.safe_dump(self.history, f)

        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def set_client(self):
        client = self.sender().text()

        self.active_client = client
        self.active_project = None

        project_list = self.time_manager.get_client_projects(client)
        self.project_menu_projects = []
        if len(project_list):
            if client in self.history['last_projects']:
                self.active_project = self.history['last_projects'][client]
            else:
                self.active_project = project_list[0]

            for project in project_list:
                p = QAction(project)
                self.project_menu_projects.append(p)
                p.triggered.connect(self.set_project)
                self.projects_menu.addAction(p)

        self.history['last_client'] = self.active_client
        self.history['last_projects'][self.active_client] = self.active_project
        with open(self.history_file, 'w') as f:
            yaml.safe_dump(self.history, f)

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

        self.history['last_projects'][self.active_client] = self.active_project
        with open(self.history_file, 'w') as f:
            yaml.safe_dump(self.history, f)

        self.top_menu_project.setText(f'{self.active_client} -- {self.active_project}')

    def set_project(self, project):
        self.active_project = self.sender().text()

        self.history['last_projects'][self.active_client] = self.active_project
        with open(self.history_file, 'w') as f:
            yaml.safe_dump(self.history, f)

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