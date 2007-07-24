# -*- coding: iso-8859-1 -*-

"""
Model classes module container
@author Marinho Brandao
@creation 2007-07-21
"""

class Project(object):
    connections = []
    initial_version = 0
    latest_version = None
    description = ''

    def __init__(self):
        pass

    def clear(self):
        pass

    def save_to_file(self, filename):
        print "saving to ... '%s'" % filename

    def load_from_file(self, filename):
        pass

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

    def __init__(self, driver_class=None, dsn=''):
        self.driver_class, self.dsn = driver_class, dsn or self.dsn

    def __str__(self):
        return self.dsn

