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
        result = self.connection.cursor().execute("\
                SELECT rdb$relation_name as table_name \
                FROM rdb$relations \
                WHERE rdb$system_flag = 0 \
                ")
        return [l['table_name'] for l in result.fetchallmap()]

    def get_fields_list(self, table_name):
        ret = []

        result = self.connection.cursor().execute("\
                SELECT \
                 RF.rdb$field_name as field_name, \
                 RF.rdb$default_source as default_source, \
                 F.rdb$field_length as length, \
                 F.rdb$field_scale * -1 as scale, \
                 F.rdb$field_type as type_code, \
                 T.rdb$type_name as type_name, \
                 T.rdb$null_flag as required \
                FROM rdb$relation_fields RF \
                JOIN rdb$fields F ON RF.rdb$field_source = F.rdb$field_name \
                JOIN rdb$types T ON F.rdb$field_type = T.rdb$type \
                                AND T.rdb$field_name = 'RDB$FIELD_TYPE' \
                WHERE RF.rdb$relation_name = '%s' \
                ORDER BY RF.rdb$field_id \
                ")

        for r in result.fetchallmap():
            """
            missing: QUAD, CSTRING, BLOB_ID
            """
            if r['type_name'] == 'VARYING':
                col = Varchar(r['length'])
            elif ft == 'TEXT':
                col = Char(r['length'])
            elif ft == 'LONG':
                col = Integer()
            elif ft == 'DATE':
                col = Date()
            elif ft in ['INT64']:
                col = Decimal(r['length'], r['scale'])
            elif ft == 'SHORT':
                col = SmallInt()
            elif ft == 'TIME':
                col = TimeInt()
            elif ft == 'TIMESTAMP':
                col = TimestampInt()
            elif ft == 'FLOAT':
                col = FloatInt()
            elif ft == 'DOUBLE': # to be verified
                col = FloatInt()
            elif ft == 'BLOB':
                col = TextInt()
            else:
                print "Field type not identified: %s %s" %( r[1], r[2] )
                continue

            col.name = r['field_name']
            col.required = r['required'] == 1
            #col.default = r[4]
            #col.primary_key = r[5] == 1
            
            ret.append(col)

        return ret

    def get_constraints_list(self, table_name):
        ret = []

        #result = self.connection.cursor().execute('PRAGMA foreign_key_list(%s)' % table_name)

        #for r in result.fetchall():
        #    ret.append( ForeignKey(r[1], r[3], r[2]) )

        return ret

    def get_indexes_list(self, table_name):
        return []
        #result = self.connection.cursor().execute('PRAGMA index_list(%s)' % table_name)

        #return [r[1] for r in result.fetchall()]

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

