import yaml
import os

from TimeLog.config import app_path


class TimeManager:
    def __init__(self):
        self.projects_file = str(app_path / 'projects.yaml')
        self.time_file = str(app_path / 'times.csv')

        if os.path.exists(self.projects_file):
            with open(self.projects_file, 'rt') as f:
                self.projects = yaml.safe_load(f)
        else:
            self.projects = {}

        # Create csv column headers
        if not os.path.exists(self.time_file):
            with open(self.time_file, 'wt') as f:
                f.write('Client,Project,Start,End,Duration,Note\n')

    def get_clients(self):
        return list(self.projects.keys())

    def add_client(self, name):
        if name not in self.projects:
            self.projects[name] = []

            with open(self.projects_file, 'wt') as f:
                yaml.safe_dump(self.projects, f)

    def get_client_projects(self, client):
        if client in self.projects:
            return self.projects[client]
        else:
            return []

    def add_project(self, client, name):
        if client not in self.projects:
            self.projects[client] = [name,]
        else:
            self.projects[client].append(name)

        with open(self.projects_file, 'wt') as f:
            yaml.safe_dump(self.projects, f)

    def add_time_entry(self, client, project, start_time, end_time, duration, note):
        with open(self.time_file, 'at') as f:
            f.write(f'{client},{project},{start_time},{end_time},{duration},{note}\n')