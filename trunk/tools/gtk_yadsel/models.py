# -*- coding: iso-8859-1 -*-

"""
Model classes module container
@author Marinho Brandao
@creation 2007-07-21
"""

import simplejson

class Project(object):
    initial_version = 0
    latest_version = None
    description = ''
    connections = []
    version_files = []

    def __init__(self):
        pass

    def __str__(self):
        return self.description

    def clear(self):
        pass

    def save_to_file(self, filename):
        instance = {
            'connections': [{'driver_class': c.driver_class, 'dsn': c.dsn} for c in self.connections],
            'initial_version': self.initial_version,
            'latest_version': self.latest_version,
            'description': self.description,
            }
        json = simplejson.dumps(instance)

        f = file(filename, 'w')
        f.write(json)
        f.close()

    def load_from_file(self, filename):
        f = file(filename)
        cont = f.read()
        f.close()

        json = simplejson.loads(cont)

        self.initial_version = json['initial_version']
        self.latest_version = json['latest_version']
        self.description = json['description']

        self.connections = [Connection(c['driver_class'], c['dsn']) for c in json['connections']]

    def add_connection(self, conn=None):
        conn = conn or Connection()

        self.connections.append(conn)
        conn.project = self

        return conn

class Connection(object):
    project = None
    driver_class = None # firebird, sqlite, mysql, postgres, etc.
    driver = None
    dsn = 'protocol:user:pass@host:port'
    is_new = True

    def __init__(self, driver_class=None, dsn=''):
        self.driver_class, self.dsn = driver_class, dsn or self.dsn

    def __str__(self):
        return self.dsn

    def remove_from_project(self):
        if self.project and self in self.project.connections:
            self.project.connections.remove(self)

class VersionFile(object):
    project = None

