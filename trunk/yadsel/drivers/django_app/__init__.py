from yadsel import core, drivers

def attach_command():
    pass

def yadsel_execute_manager(settings, argv):
    from django.db import connection
    driver = drivers.DRIVERS_PER_ENGINE[settings.__dict__.get('DATABASE_ENGINE', '')]

    if driver == SQLite:
        dsn = settings.DATABASE_NAME
    else:
        dsn = ''
        if settings.__dict__.get('DATABASE_ENGINE', ''): dsn += settings.DATABASE_HOST
        if settings.__dict__.get('DATABASE_PORT', ''): dsn += ':'+settings.DATABASE_PORT
        if settings.__dict__.get('DATABASE_NAME', ''): dsn += '/'+settings.DATABASE_NAME
        
    print driver
    print dsn

