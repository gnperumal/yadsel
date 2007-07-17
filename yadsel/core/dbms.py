"""
This module haves the Driver superclass, who must be inherited
by every driver class. This class only defines the signature,
and let the implementation for inherit responsability.

@author Marinho Brandao
@creation 2007-05-24
"""

class Driver(object):
    terminate_delimiter = ";"
    connection = None
    additional_scripts = []

    def __init__(self, connection=None):
        self.connection = connection
        self.additional_scripts = []

    def generate_script(self, command):
        pass

    def execute_command(self, command):
        pass

    class FieldParser:
        pass

    class ConstraintParser:
        pass

    class ActionParser:
        pass

    class ValueParser:
        pass

    class ClauseParser:
        pass

    class Inspector:
        pass

class SchemaInspector:
    driver = None
    connection = None

    def __init__(self, driver):
        self.driver = driver
        self.connection = self.driver.connection

    def get_tables_list(self):
        pass

    def get_fields_list(self, table_name):
        pass

    def get_constraints_list(self, table_name):
        pass

    def get_indexes_list(self, table_name):
        pass

    def get_index_info(self, index_name):
        return None

    def get_domains_list(self):
        pass

