#!/usr/bin/env python

"""
This module provide a tool for doing migration by a shell line
@author Marinho Brandao
@creation 2007-05-25
"""

import sys
from yadsel import core, drivers

def print_header():
    print "Yadsel // http://code.google.com/p/yadsel/\n"

def print_help():
    temp = [
            "Invalid syntax. You must declare required parameters, like below:",
            "",
            "  path=<version_files_path>\trequired",
            "  dsn=<dsn>\t\t\trequired",
            "  user=<username>\t\trequired",
            "  pass=<password>\t\toptional. Default: empty",
            "  from=<current_version>\trequired",
            "  to=<new_version_number>\toptional. Default: latest available version",
            "  action=[up|down]\t\toptional. Default: up",
           ]

    print ''.join([l+"\n" for l in temp])

def do(versions_path, driver_type, dsn, user, passwd, action, current_version, new_version):
    if driver_type == "firebird":
        try:
            import kinterbasdb
        except:
            print "A Python extension called 'kinterbasdb' was not found!"
            sys.exit(1)

        connection = kinterbasdb.connect(dsn=dsn, user=user, password=passwd)
        driver = drivers.Firebird
    elif driver_type == "mssql":
        try:
            import pymssql
        except:
            print "A Python extension called 'pymssql' was not found!"
            sys.exit(1)

        connection = None #pymssql.connect(dsn=dsn, user=user, password=passwd)
        driver = drivers.MSSQL
    elif driver_type == "mysql":
        driver = drivers.MySQL
    elif driver_type == "sqlite":
        driver = drivers.SQLite
    else:
        print "Only drivers 'Firebird', 'MySQL' and 'SQLite' are supported!"
        sys.exit(1)

    controller = core.Controller(driver, connection=connection)

    print "Driver: %s" % controller.driver.__class__.__name__

    controller.current_version = current_version
    controller.load_versions_from_path(versions_path)

    if action == 'up':
        print "Upgrading..."
        script = controller.script_for_upgrade(to=new_version)
        #controller.upgrade()
    elif action == 'down':
        print "Downgrading..."
        script = controller.script_for_downgrade(to=new_version)
        #controller.downgrade()

    for v in script:
        print "/* Version", v, "*/"
        for cmd in script[v]:
            print "", cmd

if __name__ == '__main__':
    print_header()

    versions_path = dsn = user = current_version = None
    action = 'up'
    new_version = 0
    passwd = ''

    for arg in sys.argv:
        if arg.startswith('path='):
            versions_path = arg.split('=')[1]
        elif arg.startswith('driver='):
            driver_type = arg.split('=')[1].lower()
        elif arg.startswith('dsn='):
            dsn = arg.split('=')[1]
        elif arg.startswith('user='):
            user = arg.split('=')[1] or action
        elif arg.startswith('pass='):
            passwd = arg.split('=')[1]
        elif arg.startswith('action='):
            action = arg.split('=')[1] or passwd
        elif arg.startswith('from='):
            current_version = int(arg.split('=')[1])
        elif arg.startswith('to='):
            new_version = int(arg.split('=')[1]) or new_version

    if not(versions_path or dsn or user or current_version):
        print_help()
        sys.exit(1)

    # Does the (up|down)grade
    do(versions_path=versions_path,
       driver_type=driver_type,
       dsn=dsn,
       action=action,
       user=user,
       passwd=passwd,
       current_version=current_version,
       new_version=new_version
       )

