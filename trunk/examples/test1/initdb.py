#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite

if __name__ == '__main__':
    con = sqlite.connect('db.sqlite')

    print "Database file created."
