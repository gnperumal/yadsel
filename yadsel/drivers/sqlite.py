"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-01
"""

import re

from yadsel.core import *
from generic import GenericDriver

MASTER_TABLE = 'SQLite_Master'

class SQLiteInspector(SchemaInspector):
    """
    Thanks for Luiz Carlos Geron and SQLAlchemy team for some 
    ideas about that wrapper, available here:
    http://www.sqlalchemy.org/trac/browser/sqlalchemy/trunk/lib/sqlalchemy/databases/sqlite.py
    """
    def get_tables_list(self):
        result = self.connection.cursor().execute('SELECT * FROM %s' % MASTER_TABLE)
        return [l[1] for l in result.fetchall() if l[0] == 'table']

    def get_fields_list(self, table_name):
        ret = []

        result = self.connection.cursor().execute('PRAGMA table_info(%s)' % table_name)

        for r in result.fetchall():
            match = re.match(r'(\w+)(\(.*?\))?', r[2])

            ft = match.group(1).upper()
            args = str(match.group(2))

            if args != "":
                args = re.findall('(\d+)', args)

            if ft == 'VARCHAR':
                col = Varchar(int(args[0]))
            elif ft == 'CHAR':
                col = Char(int(args[0]))
            elif ft == 'INTEGER':
                col = Integer()
            elif ft == 'SMALLINT':
                col = SmallInt()
            elif ft in ['DECIMAL', 'NUMERIC']:
                col = Decimal(int(args[0]), int(args[1]))
            elif ft == 'TEXT':
                col = Text()
            elif ft == 'DATE':
                col = Date()
            elif ft == 'TIME':
                col = Time()
            elif ft == 'DATETIME':
                col = DateTime()
            elif ft == 'TIMESTAMP':
                col = Timestamp()
            elif ft == 'BOOL':
                col = Boolean()
            else:
                print "Field type not identified: %s %s" %( r[1], r[2] )
                continue

            col.name = r[1]
            col.required = r[3] != 0
            col.default = r[4]
            col.primary_key = r[5] == 1
            
            ret.append(col)

        return ret

    def get_constraints_list(self, table_name):
        ret = []

        result = self.connection.cursor().execute('PRAGMA foreign_key_list(%s)' % table_name)

        for r in result.fetchall():
            ret.append( ForeignKey(r[1], r[3], r[2]) )

        return ret

    def get_indexes_list(self, table_name):
        result = self.connection.cursor().execute('PRAGMA index_list(%s)' % table_name)

        return [r[1] for r in result.fetchall()]

    def get_index_info(self, index_name):
        return None
        #result = self.connection.cursor().execute('PRAGMA index_info(%s)' % index_name)

        #return [r[2] for r in result.fetchall()]

    def get_domains_list(self):
        return []


class SQLiteConstraintParser(object):
    constraint = None

    def __init__(self, obj):
        self.constraint = obj

    def get_fields(self):
        ret = ''.join([",%s" % f for f in self.constraint.fields])
        return ret[1:]

    def get_foreign_fields(self):
        ret = ''.join([",%s" % f for f in self.constraint.foreign_fields])
        return ret[1:]

    def for_create(self):
        return ''

    def for_alter(self):
        return self.for_create()

    def for_rename(self):
        return self.for_create()


class SQLiteDriver(GenericDriver):
    class Inspector(SQLiteInspector): pass
    class ConstraintParser(SQLiteConstraintParser): pass

    def __init__(self, connection=None):
        super(SQLiteDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of pySQLite module, available at:
        http://www.initd.org/tracker/pysqlite
        """
        super(SQLiteDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

