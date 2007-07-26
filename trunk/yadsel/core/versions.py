"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

from yadsel.core.dbms import Driver
from yadsel.core.fieldtypes import *
from yadsel.core.ddl import *

class Controller(object):
    connection = None
    driver = None
    current_version = 0
    version_classes = []
    interactive = False

    def __init__(self, driver, connection=None, current_version=None):
        self.connection = connection

        # Accept class name
        if issubclass(driver, Driver):
            self.driver = driver(self.connection)

        # Accept instance
        elif issubclass(driver.__class__, Driver):
            self.driver = driver

        # Does not accept another
        else:
            raise Exception("'driver' parameter is invalid. Please inform a Driver compatible instance or class.")

        self.current_version = current_version or self.current_version

    def load_versions_from_path(self, path):
        import os, sys
        path = os.path.abspath(path)

        if not os.path.isdir(path): return False

        if not sys.path.count(path):
            sys.path.append(path)
        
        for f in os.listdir(path):
            mod_name, ext = os.path.splitext(f)
            if ext == '.py':
                self.load_classes_version_from_module(mod_name)

    def load_classes_version_from_module(self, mod_name):
        module = __import__(mod_name)

        for m in module.__dict__.values():
            try:
                if issubclass(m, Version) and m != Version:
                    self.version_classes.append(m)
            except Exception:
                pass

    def script_for_upgrade(self, current=None, to=None):
        self.version_classes.sort(lambda a,b: cmp(a.version_number, b.version_number))

        self.current_version = current or self.current_version
        to = to or self.version_classes[-1].version_number
        
        versions = [c for c in self.version_classes if c.version_number > self.current_version and c.version_number <= to]
        
        return self.__generate_script(versions, 'up')

    def script_for_downgrade(self, current=None, to=None):
        self.version_classes.sort(lambda a,b: cmp(b.version_number, a.version_number))
        
        self.current_version = current or self.version_classes[0].version_number
        to = to or 0
        
        versions = [c for c in self.version_classes if c.version_number > to and c.version_number <= self.current_version]

        return self.__generate_script(versions, 'down')

    def __generate_script(self, versions, do='up'):
        from types import ListType

        ret = {};

        for cls in versions:
            obj = cls()

            if do == 'up':
                obj.do_up()
            else:
                obj.do_down()

            tmp = ret[str(obj.version_number)] = []

            # Parses commands
            for cmd in obj.commands:
                s = self.driver.generate_script(cmd)
                if type(s) == ListType:
                    tmp += s
                else:
                    tmp.append(s)

            # Parses additional scripts
            tmp += self.__sort_additional_scripts(self.driver.additional_scripts)

        return ret

    def __sort_additional_scripts(self, script_list):
        """Sort additional_scripts list by the order: first Primary Keys, later Foreign Keys"""

        # Primary keys
        pk_list = [s for s in script_list if s.find(' PRIMARY KEY ') > 0]

        # Foreign keys
        fk_list = [s for s in script_list if s.find(' FOREIGN KEY ') > 0]
        
        # Others scripts at last
        others = [s for s in script_list if s not in pk_list + fk_list]

        return pk_list + fk_list + others

    def __execute_command(self, command):
        try:
            self.driver.execute_command(command)
        except Exception, (errno, errmsg):
            print "When executing the following SQL command: '%s', following error ocurred: '%d - %s'" %( command, errno, errmsg )

        if self.interactive:
            print "Press any key to continue..."

    def __execute_script(self, script, versions_sequence):
        # Loop for sequence of versions
        for v in versions_sequence:
            # Loop for commands
            for cmd in script[v]:
                # Execute the single command each by time
                self.__execute_command(cmd)

    def upgrade(self, current=None, to=None):
        # Get the generated script
        script = self.script_for_upgrade()

        # Get valid version numbers
        versions_list = script.keys()

        # Sort version numbers for upgrading
        versions_list.sort()

        # Call the execution for script
        self.__execute_script(script, versions_list)

    def downgrade(self, current=None, to=None):
        # Get the generated script
        script = self.script_for_downgrade()

        # Get valid version numbers
        versions_list = script.keys()

        # Sort version numbers for upgrading
        versions_list.sort(lambda a,b: cmp(b,a))

        # Call the execution for script
        self.__execute_script(script, versions_list)

class Version(object):
    version_number = None
    collation = None
    character_set = None
    commands = []

    def do_up(self):
        """Prepare and calls 'up' method"""
        self.commands = []

        self.up()

    def up(self):
        """Don't declare nothing here. Aways overrided by implementations"""
        pass

    def do_down(self):
        """Prepare and calls 'down' method"""
        self.commands = []

        self.down()

    def down(self):
        """Don't declare nothing here. Aways overrided by implementations"""
        pass

FULLVERSION_TEMPLATE = "\
\"\"\" \n\
* Full Version generated by Yadsel v. {{ YADSEL_VERSION }} * \n\
@creation {{ WHEN }} \n\
\"\"\" \n\
from yadsel.core import * \n\
\n\
class Version1(Version): \n\
    version_number = {{ VERSION_NUMBER }} \n\
\n\
    def up(self): \n\
{{ FULLVERSION_SCRIPT }} \
\n\
    def down(self): \n\
        pass \n\
"

class FullVersionBuilder(object):
    """
    This class find for database objects from a connection, through
    a driver's SchemaInspector

    @author Marinho Brandao
    @creation 2007-06-05
    """
    connection = None
    driver = None
    version = None
    inspector = None

    def __init__(self, driver, connection=None, version_number=1):
        self.connection = connection

        # Accept class name
        if issubclass(driver, Driver):
            self.driver = driver(self.connection)

        # Accept instance
        elif issubclass(driver.__class__, Driver):
            self.driver = driver

        # Does not accept another
        else:
            raise Exception("'driver' parameter is invalid. Please inform a Driver compatible instance or class.")

        self.version = Version()
        self.version.version_number = version_number

    def do(self):
        # Get the inspector
        self.inspector = self.driver.Inspector(self.driver)

        # Get tables
        self.__get_tables()

        # Get domains
        self.__get_domains()

    def __get_tables(self):
        lst = self.inspector.get_tables_list()

        for table_name in lst:
            cmd = CreateTable(table_name)

            # Get the constraints list
            cmd.constraints = self.__get_constraints(table_name)

            # Get the fields list
            cmd.fields = self.__get_fields(table_name)

            self.version.commands.append(cmd)

    def __get_fields(self, table_name):
        return self.inspector.get_fields_list(table_name)

    def __get_constraints(self, table_name):
        return self.inspector.get_constraints_list(table_name)

    def __get_indexes(self, table_name):
        pass

    def __get_domains(self):
        lst = self.inspector.get_domains_list()

        for domain_name in lst:
            ft = None # ...
            cmd = CreateDomain(domain_name, ft)
            self.version.commands.append(cmd)

    def export_to_file(self, filename=None, template_file=None):
        """
        This method generates a Python script with the objects in commands list
        in same sequence, for utilize as the Full Version script
        """
        from datetime import datetime
        from yadsel import VERSION

        # Do...
        self.do()

        # Get scripts from objects
        commands = [cmd.to_script() for cmd in self.version.commands]

        # Load template from file
        if template_file:
            f = file(template_file, 'r')
            script = f.readlines()
            f.close()
        else:
            script = FULLVERSION_TEMPLATE

        # Fill script with macros
        script = script.replace('{{ YADSEL_VERSION }}', "%d.%d-%s"%VERSION)
        script = script.replace('{{ WHEN }}', str(datetime.now()))
        script = script.replace('{{ VERSION_NUMBER }}', str(self.version.version_number))
        script = script.replace('{{ FULLVERSION_SCRIPT }}', ''.join([c+"\n" for c in commands]))

        if filename:
            f = file(filename, 'w')
            f.write(script)
            f.close()
        else:
            print script

