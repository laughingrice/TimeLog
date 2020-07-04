import sqlite3 as sq
import pathlib


class TimeManager:
    def __init__(self):
        path = (pathlib.Path().home() / pathlib.Path(".local/share/TimeManager"))
        path.mkdir(parents=True, exist_ok=True)
        self.conn = sq.connect(str(path / "times.sqlite"), detect_types=sq.PARSE_DECLTYPES | sq.PARSE_COLNAMES)
        self.curr = self.conn.cursor()

        # Clients table
        self.curr.execute(
            "create table if not exists 'clients' ('"
            "id' integer primary key, '"
            "name' text unique not NULL);")

        # Projects table
        self.curr.execute(
            "create table if not exists 'projects' ("
            "'id' integer primary key, "
            "'name' text not NULL, "
            "'client_id' integer not NULL,"
            "unique(name, client_id));")

        # Times table
        self.curr.execute(
            "create table if not exists times ("
            "'id' integer primary key, "
            "'client_id' integer, "
            "'project_id' integer, "
            "'start_time' timestamp, "
            "'end_time' timestamp, "
            "'work_time' float);")

        self.conn.commit()

    def get_clients(self):
        self.curr.execute("select name from 'clients'")
        return [x[0] for x in self.curr.fetchall()]

    def add_client(self, name):
        self.curr.execute(f"insert or ignore into clients(id, name) values(NULL, '{name}')")
        self.conn.commit()

    def get_client_projects(self, client):
        self.curr.execute(f"select id from clients where name = '{client}'")
        id = self.curr.fetchone()[0]

        self.curr.execute(f"select name from 'projects' where client_id ='{id}'")
        return [x[0] for x in self.curr.fetchall()]

    def add_project(self, client, name):
        self.curr.execute(f"select id from clients where name = '{client}'")
        id = self.curr.fetchone()

        if id is None:
            return

        id = id[0]

        self.curr.execute(f"insert or ignore into projects(id, name, client_id) values(NULL, '{name}', '{id}')")
        self.conn.commit()

    def add_time_entry(self, client, project, start_time, end_time, duration):
        self.curr.execute(f"select id from clients where name = '{client}'")
        client_id = self.curr.fetchone()
        client_id = client_id[0] if client_id is not None else None

        self.curr.execute(f"select id from projects where name = '{project}' and client_id = '{client_id}'")
        project_id = self.curr.fetchone()
        project_id = project_id[0] if project_id is not None else None

        self.curr.execute(f"insert into times(id, client_id, project_id, start_time, end_time, work_time) "
                          f"values(NULL, '{client_id}', '{project_id}', '{start_time}', '{end_time}', '{duration}')")
        self.conn.commit()