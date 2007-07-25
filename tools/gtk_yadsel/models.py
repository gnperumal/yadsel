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
            'version_files': [v.filename for v in self.version_files],
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

        self.initial_version = json.get('initial_version', 0)
        self.latest_version = json.get('latest_version', 0)
        self.description = json.get('description', '')

        self.connections = [Connection(c['driver_class'], c['dsn'], project=self) for c in json.get('connections', [])]
        self.version_files = [VersionFile(v, project=self) for v in json.get('version_files', [])]

    def add_connection(self, conn=None):
        conn = conn or Connection(project=self)

        return conn

    def add_version_file(self, vers=None):
        vers = vers or VersionFile(project=self)

        return vers

class Connection(object):
    project = None
    driver_class = None # firebird, sqlite, mysql, postgres, etc.
    driver = None
    dsn = 'protocol:user:pass@host:port'
    is_new = True

    def __init__(self, driver_class=None, dsn='', project=None):
        self.driver_class, self.dsn, self.project = driver_class, dsn or self.dsn, project

        if project:
            project.connections.append(self)

    def __str__(self):
        return self.driver_class

    def remove_from_project(self):
        if self.project and self in self.project.connections:
            self.project.connections.remove(self)

class VersionFile(object):
    project = None
    content = ''
    filename = None
    version_number = None

    def __init__(self, filename=None, project=None):
        self.filename, self.project = filename, project

        if project:
            project.version_files.append(self)

    def save_to_file(self, filename):
        self.filename = filename or self.filename

        f = file(filename, 'w')
        f.write(self.content)
        f.close()

    def load_from_file(self, filename):
        self.filename = filename or self.filename

        f = file(filename)
        self.content = f.read()
        f.close()

    def __str__(self):
        return "%s" %( self.version_number or self.project.version_files.index(self) )

    def remove_from_project(self):
        if self.project and self in self.project.version_files:
            self.project.version_files.remove(self)

