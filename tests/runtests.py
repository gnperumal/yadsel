#!/usr/bin/env python

"""
** not yet documented **
@author Marinho Brandao
@created 2007-06-02
"""

CASE_1 = False
CASE_2 = False
CASE_3 = False
CASE_4 = True

import os, sys

path = os.path.abspath('../')
versions_path = os.path.abspath('../examples/test1/')

if os.path.isdir(path):
    sys.path.append(path)

    try:
        yadsel = __import__('yadsel_src')
    except:
        import yadsel
else:
    import yadsel

from yadsel.core import Controller, FullVersionBuilder
from yadsel.drivers import *

if CASE_1:
    print 'Parsing:', versions_path

    controller = Controller(SQLite)
    controller.load_versions_from_path(versions_path)

    print "Upgrading..."

    script = controller.script_for_upgrade()
    versions_list = script.keys()
    versions_list.sort()

    for v in versions_list:
        print "/* Version", v, "*/"
        for cmd in script[v]:
            print "", cmd

    print "\nDowngrading..."

    script = controller.script_for_downgrade()
    versions_list = script.keys()
    versions_list.sort(lambda a,b: cmp(b,a))

    for v in versions_list:
        print "/* Version", v, "*/"
        for cmd in script[v]:
            print "", cmd

if CASE_2:
    print 'Parsing:', versions_path

    from pysqlite2 import dbapi2 as sqlite
    
    con = sqlite.connect('db.sqlite')

    controller = Controller(SQLite, connection=con)
    controller.load_versions_from_path(versions_path)

    controller.upgrade()

if CASE_3:
    print 'Full Version generating from SQLite database...'

    from pysqlite2 import dbapi2 as sqlite
    
    con = sqlite.connect('adoradores.sqlite')

    version = FullVersionBuilder(SQLite, connection=con, version_number=1)
    version.export_to_file('version1.py')

if CASE_4:
    print 'Full Version generating from Firebird database...'

    import kinterbasdb
    
    con = kinterbasdb.connect(
            host='localhost',
            database='phonus',
            user='sysdba',
            password='masterkey',
            dialect=3,
            charset='ISO88591',
            )

    version = FullVersionBuilder(Firebird, connection=con, version_number=1)
    version.export_to_file('version1.py')

