"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

from yadsel.core.dbms import Driver
from yadsel.core.fieldtypes import *
from yadsel.core.ddl import *

# Available actions to evolution of schema
ACTION_UP = 'up'
ACTION_DOWN = 'down'

class Controller(object):
    """This class control and make the effective changes of schema evolution"""
    connection = None
    driver = None
    current_version = 0
    version_classes = []
    cache = {}
    log = silent = False
    __version_errors = 0

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

        # Appends path to PYTHON_PATH environment variable (dynamicly)
        if not sys.path.count(path):
            sys.path.append(path)
        
        # Loads classes
        self.load_classes_version_from_module('yadsel_versions')

    def load_classes_version_from_module(self, module):
        from types import StringType, ModuleType

        if type(module) == StringType:
            module = __import__(module)
        elif type(module) != ModuleType:
            return False

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
        
        return self.__generate_script(versions, ACTION_UP)

    def script_for_downgrade(self, current=None, to=None):
        self.version_classes.sort(lambda a,b: cmp(b.version_number, a.version_number))
        
        self.current_version = current or self.version_classes[0].version_number
        to = to or 0
        
        versions = [c for c in self.version_classes if c.version_number > to and c.version_number <= self.current_version]

        return self.__generate_script(versions, ACTION_DOWN)

    def __generate_script(self, versions, do=ACTION_UP):
        from types import ListType

        ret = {};

        for cls in versions:
            obj = cls()
            self.driver.additional_scripts = []

            if do == ACTION_UP:
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

    def __execute_command(self, command, version_number=None):
        version_number = version_number or self.current_version

        try:
            # Log before execution
            self.register_log(command, version_number=version_number)

            self.driver.execute_command(command)
        except Exception, e:
            self.__version_errors += 1

            msg = "When executing the following SQL command: '%s', following error ocurred: '%s'" %( command, e )

            # Log exception message
            self.register_log(str(e), version_number=version_number)

            if self.silent:
                print msg
            else:
                raise Exception(msg)

    def __execute_script(self, script, versions_sequence):
        # Loop by sequence of versions
        for v in versions_sequence:
            self.__version_errors = 0

            # Log version started
            self.register_log('Version process started...', version_number=v)

            # Loop by commands
            for cmd in script[v]:
                # Execute the single command each by time
                self.__execute_command(cmd, version_number=v)

            # Log version finished
            self.register_log('Version process finished...', version_number=v)

            # Register version
            self.current_version = v
            self.register_version_history(self.current_version, errors=self.__version_errors)

    def upgrade(self, current=None, to=None, cacheable=False, force=False, step=None, test=False, silent=False, log=False):
        self.silent = silent
        self.log = log

        if not cacheable or force:
            # Get the generated script
            self.cache['script'] = self.script_for_upgrade()

            # Get valid version numbers
            self.cache['versions_list'] = self.cache['script'].keys()

            # Sort version numbers for upgrading
            self.cache['versions_list'].sort(lambda a, b: int(a) - int(b))

            # Slices the versions list between current and to args
            self.cache['versions_list'] = [v for v in self.cache['versions_list'] if (not current or int(v) > current) and (not to or int(v) <= to)]

            # Set steps count
            self.cache['steps_count'] = len(self.cache['versions_list'])

        # Exit if no versions found
        if not self.cache['versions_list']:
            return False

        versions_list = step is None and self.cache['versions_list'] or [self.cache['versions_list'][step]]

        # Call the execution for script
        if not test:
            self.__execute_script(self.cache['script'], versions_list)

    def downgrade(self, current=None, to=None, cacheable=False, force=False, step=None, test=False, silent=False):
        if not cacheable or force:
            # Get the generated script
            self.cache['script'] = self.script_for_downgrade()

            # Get valid version numbers
            self.cache['versions_list'] = self.cache['script'].keys()

            # Sort version numbers for upgrading
            self.cache['versions_list'].sort(lambda a,b: cmp(b,a))

            # Set steps count
            self.cache['steps_count'] = len(self.cache['versions_list'])

        versions_list = step is not None and self.cache['versions_list'] or self.cache['versions_list'][step]

        # Call the execution for script
        if not test:
            self.__execute_script(self.cache['script'], versions_list)

    def load_current_version_from_history(self):
        if not self.connection: return False

        # Instantiates history control
        history = self.driver.HistoryControl(self.connection)

        # Tries to prepare database for this (if not yet)
        history.prepare_database_elements()

        # Get latest version and change date/time
        latest_version = history.get_latest_version()

        # Set current version by latest version number
        self.current_version = latest_version and latest_version['version_number'] or 0

    def register_version_history(self, version_number, errors=0):
        if not self.connection: return False

        # Instantiates history control
        history = self.driver.HistoryControl(self.connection)

        # Tries to prepare database for this (if not yet)
        history.prepare_database_elements()

        # Register new version to history control
        return history.register_version(version_number, errors=errors)

    def register_log(self, msg, version_number=None):
        if not self.connection or not self.log: return False

        version_number = version_number or self.current_version

        # Instantiates log control
        log = self.driver.LogControl(self.connection)

        # Tries to prepare database for this (if not yet)
        log.prepare_database_elements()

        # Register new version to log control
        return log.register_log(version_number, msg)


class ExtensibleVersion(object):
    """
    ExtensibleVersion provides a generalizated way to script up creation,
    erasing and modifying database elements through resources of CoreAPI.
    Don't use this class for any reasons. Use specialization classes that
    are the right way.
    @author Marinho Brandao
    @creation 2007-05-24
    @modified 2007-07-28 (renamed from Version to ExtensibleVersion)
    """
    collation = None # Not yet implemented
    character_set = None # Not yet implemented
    commands = []
    partial_versions = [] # Aggregation of partial versions

    def do_up(self):
        """Prepare and calls ACTION_UP method"""
        self.commands = []

        # Calls ACTION_UP method for its commands
        self.up()

        # Get commands of partial version classes
        for pv_cls in self.partial_versions:
            pv = pv_cls()
            pv.do_up()
            self.commands += pv.commands

    def up(self):
        """Don't declare nothing here. Aways overrided by implementations"""
        pass

    def do_down(self):
        """Prepare and calls ACTION_DOWN method"""
        self.commands = []

        # Invert order of partial_versions classes
        partial_versions = self.partial_versions
        partial_versions.reverse()

        # Get commands of partial version classes
        for pv_cls in partial_versions:
            pv = pv_cls()
            pv.do_down()
            self.commands += pv.commands

        # Calls ACTION_UP method for its commands
        self.down()

    def down(self):
        """Don't declare nothing here. Aways overrided by implementations"""
        pass

class Version(ExtensibleVersion):
    """
    Version is the right way to write commands to create, erase or modify
    database elements, knowed by Controller class and must have the
    version_number value unique (each Version class must have a once value)
    @author Marinho Brandao
    @creation 2007-05-24
    @modified 2007-07-28 (renamed from Version to ExtensibleVersion, and extended from it)
    """
    version_number = None

class PartialVersion(ExtensibleVersion):
    """
    PartialVersion is the right way to write commands to create, erase or
    modify database elements, being a part of a unique Version class. This
    class is util for big modifications in once version_number, when you
    can declare much PartialVersion classes with part of code, and join them
    to a Version class.
    @author Marinho Brandao
    @creation 2007-07-28
    """

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

