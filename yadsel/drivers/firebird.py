"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-11
"""

import re

from yadsel.core import *
from generic import GenericDriver

class FirebirdInspector(SchemaInspector):
    def get_tables_list(self):
        result = self.connection.cursor().execute('SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0')
        return [l['RDB$RELATION_NAME'] for l in result.fetchallmap()]

    def get_fields_list(self, table_name):
        ret = []

        result = self.connection.cursor().execute('\
                SELECT RF.* \
                FROM RDB$RELATION_FIELDS RF \
                WHERE RF.RDB$RELATION_NAME = \'%s\'\
                ')

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

class FirebirdDriver(GenericDriver):
    class Inspector(FirebirdInspector): pass

    def __init__(self, connection=None):
        super(FirebirdDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of KInterbasDB extension package, available at:
        http://kinterbasdb.sourceforge.net/
        """
        super(FirebirdDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

