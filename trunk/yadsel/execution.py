import sys
from yadsel import core, drivers

try:
    import simplejson
except ImportError, e:
    pass

AVAILABLE_ACTIONS = ( core.ACTION_UP, core.ACTION_DOWN, )
MODE_HIDDEN = 'hidden'
MODE_STEPS = 'steps'
MODE_INTERACTIVE = 'interactive'
MODE_OUTPUT = 'output'
AVAILABLE_MODES = ( MODE_HIDDEN, MODE_STEPS, MODE_INTERACTIVE, MODE_OUTPUT )
DEFAULT_YADSEL_FILENAME = '.yadsel'

def print_if( condition, s ):
    if condition: print s

def do(versions_path, driver_type, dsn, user, passwd, action, current_version, 
        new_version, mode, test, history, silent, log):
    """Executes the upgrade or downgrade"""
    versions_path = versions_path or '.'
    action = action or 'up'

    if not dsn:
        print "Invalid DSN!"
        sys.exit(1)

    connection = None

    if driver_type == "firebird":
        try:
            import kinterbasdb
        except:
            print "A Python extension called 'kinterbasdb' was not found!"
            sys.exit(1)

        if dsn:
            connection = kinterbasdb.connect(dsn=dsn, user=user, password=passwd)
            
        driver = drivers.Firebird
    elif driver_type == "mssql":
        try:
            import pymssql
        except:
            print "A Python extension called 'pymssql' was not found!"
            sys.exit(1)

        if dsn:
            connection = None #pymssql.connect(dsn=dsn, user=user, password=passwd)
            
        driver = drivers.MSSQL
    elif driver_type == "mysql":
        try:
            import MySQLdb
        except:
            print "A Python extension called 'MySQLdb' was not found!"
            sys.exit(1)

        if dsn:
            connection = MySQLdb.connect(dsn.split('/')[0], user, passwd)
            connection.select_db(dsn.split('/')[1])
            
        driver = drivers.MySQL
    elif driver_type == "sqlite":
        try:
            from pysqlite2 import dbapi2 as sqlite
        except:
            print "A Python extension called 'pysqlite2' was not found!"
            sys.exit(1)

        if dsn:
            connection = sqlite.connect(dsn)

        driver = drivers.SQLite
    else:
        print "Only drivers 'Firebird', 'MySQL' and 'SQLite' are supported!"
        sys.exit(1)

    # Instantiates version controller
    controller = core.Controller(driver, connection=connection)

    print_if( mode != MODE_HIDDEN, "Driver: %s" % controller.driver.__class__.__name__ )

    # Gets current version
    if history and not current_version:
        controller.load_current_version_from_history()
    else:
        controller.current_version = current_version

    controller.load_versions_from_path(versions_path)

    if action == core.ACTION_UP:
        print_if( mode != MODE_HIDDEN, "Upgrading..." )

        # Prints script if mode is 'output'
        if mode == MODE_OUTPUT:
            script = controller.script_for_upgrade(to=new_version)

            # Print scripts
            for v in script:
                print "/* Version", v, "*/"
                for cmd in script[v]:
                    print "", cmd
        elif mode == MODE_HIDDEN:
            controller.upgrade(current=current_version, to=new_version, test=test, silent=silent, log=log)
        elif mode == MODE_STEPS:
            # First step for build scripts for cache and gets steps count
            controller.upgrade(current=current_version, to=new_version, cacheable=True, force=True, step=0, test=test, silent=silent, log=log)
            print 'Step %d of %d: ""' %( 1, controller.cache['steps_count'] )

            # Loop for next steps (if exists)
            if controller.cache['steps_count'] > 1:
                for i in range(1, controller.cache['steps_count']):
                    controller.upgrade(cacheable=True, step=i, test=test, silent=silent, log=log)
                    print 'Step %d of %d: "%s"' %( i+1, controller.cache['steps_count'], "" )
        else:
            controller.upgrade(current=current_version, to=new_version, test=test, silent=silent, log=log)
            
    elif action == core.ACTION_DOWN:
        print_if( mode != MODE_HIDDEN, "Downgrading..." )

        # Prints script if mode is 'output'
        if mode == MODE_OUTPUT:
            script = controller.script_for_downgrade(to=new_version)

            # Print scripts
            for v in script:
                print "/* Version", v, "*/"
                for cmd in script[v]:
                    print "", cmd
        elif mode == MODE_HIDDEN:
            controller.downgrade(test=test)
        elif mode == MODE_STEPS:
            # First step for build scripts for cache and gets steps count
            controller.downgrade(cacheable=True, force=True, step=0, test=test)
            print 'Step %d of %d: ""' %( 1, controller.cache['steps_count'] )

            # Loop for next steps (if exists)
            if controller.cache['steps_count'] > 1:
                for i in range(1, controller.cache['steps_count']):
                    controller.downgrade(cacheable=True, step=i, test=test)
                    print 'Step %d of %d: "%s"' %( i+1, controller.cache['steps_count'], "" )
        else:
            controller.downgrade(test=test)

def do_from_dict(keys):
    # Does the (up|down)grade
    do(versions_path=keys.get('path', None),
       driver_type=keys.get('driver', '').lower(),
       dsn=keys.get('dsn', None),
       action=keys.get('action', None),
       user=keys.get('user', None),
       passwd=keys.get('pass', None),
       current_version=keys.get('from', None),
       new_version=keys.get('to', None),
       mode=keys.get('mode', None),
       test=keys.get('test', False),
       history=keys.get('history', False),
       silent=keys.get('silent', False),
       log=keys.get('log', False),
       )

def do_from_file(filename, namespace=None):
    """Executes from a project file"""
    fp = file(filename)
    cont = fp.read()
    fp.close()

    json = simplejson.loads(cont)

    if namespace:
        do_from_dict(json[namespace])
    else:
        for keys in json.values():
            try:
                do_from_dict(keys)
            except Exception, e:
                print e, "\n"

