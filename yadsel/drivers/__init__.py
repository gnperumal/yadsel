"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-25
"""

from generic import GenericDriver as Generic
from mysql import MySQLDriver as MySQL
from sqlite import SQLiteDriver as SQLite
from firebird import FirebirdDriver as Firebird
from mssql import MSSQLDriver as MSSQL
from pgsql import PostgresDriver as Postgres

DRIVERS_PER_ENGINE = {
        'postgresql_psycopg2': 'postgres',
        'postgresql': 'postgres',
        'mysql': 'mysql',
        'sqlite3': 'sqlite',
        'oracle': None,
        '': None,
        }

