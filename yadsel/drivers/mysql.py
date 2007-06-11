"""
** not yet documented **
@author Marinho Brandao
@creation 2007-06-11
"""

from yadsel.core import *
from generic import GenericDriver

class MySQLInspector(SchemaInspector):
    def get_tables_list(self):
        result = self.connection.cursor().execute('SHOW TABLES')
        return [l[0] for l in result.fetchall()]

    def get_fields_list(self, table_name):
        ret = []

        result = self.connection.cursor().execute('SHOW COLUMNS FROM %s' % table_name)

        for r in result.fetchall():
            match = re.match(r'(\w+)(\(.*?\))?', r[1])

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

            col.name = r[0]
            col.required = r[2] == "NO"
            col.default = r[4]
            col.primary_key = r[3] == "PRI"
            
            ret.append(col)

        return ret

    def get_constraints_list(self, table_name):
        ret = []

        return ret

        #result = self.connection.cursor().execute('PRAGMA foreign_key_list(%s)' % table_name)

        #for r in result.fetchall():
        #    ret.append( ForeignKey(r[1], r[3], r[2]) )

    def get_indexes_list(self, table_name):
        result = self.connection.cursor().execute('SHOW INDEX FROM %s' % table_name)

        return [r[2] for r in result.fetchall() if r[2] != "PRIMARY"]

    def get_index_info(self, index_name):
        return None
        #result = self.connection.cursor().execute('PRAGMA index_info(%s)' % index_name)

        #return [r[2] for r in result.fetchall()]

    def get_domains_list(self):
        return []

class MySQLDriver(GenericDriver):
    class Inspector(MySQLInspector): pass

    def __init__(self, connection=None):
        super(MySQLDriver, self).__init__(connection)

    def execute_command(self, command):
        """
        This method haves a dependency of MySQLdb module, available at:
        http://mysql-python.sourceforge.net/
        """
        super(MySQLDriver, self).execute_command(command)

        if self.connection:
            cur = self.connection.cursor()
            result = cur.execute(command)

            # Verify this ****
            self.connection.commit()

            return result
        else:
            return command

