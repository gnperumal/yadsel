# -*- coding: iso-8859-1 -*-

"""
'Application' class module container
@author Marinho Brandao
@creation 2007-07-21
"""

import sys

try:
    import pygtk
    pygtk.require('2.0')
    import gtk, gtk.glade, gobject
except:
    sys.exit(1)

import utils

class Application:
    forms = {}

    def __init__(self):
        # Initialize main form
        self.forms['formMain'] = FormMain(self)

    def show_form_main(self):
        gtk.main()

    def show_form_by_name(self, form_class, form_name):
        form = self.forms.get(form_name, form_class(self, form_name))
        form.show()

class Form(object):
    name = None
    app = None
    window = None
    widget_name = None
    widget_tree = None
    widgets = ('treeviewObjects',)
    is_main_form = False

    def __init__(self, app, name=None):
        self.app = app
        self.name = name or self.widget_name

        # Attach form instance to application
        self.app.forms[self.name] = self

        # Initialize the form from glade file and make connections
        self.initialize()

    def initialize(self):
        # Initialize widget tree from glade file
        self.widget_tree = gtk.glade.XML('glade/%s.glade' % self.widget_name)

        # Get the Main Window
        self.window = self.widget_tree.get_widget(self.widget_name)

        # Connect the 'destroy' event
        if self.window:
            self.window.connect('destroy', self.on_form_destroy)

        # Get widgets defined in tuple
        for w in self.widgets:
            obj = self.widget_tree.get_widget(w)
            setattr(self, w, obj)
            
        # Autoconnect Signals and Callbacks
        self.widget_tree.signal_autoconnect(self)

        self.prepare()

    def prepare(self):
        self.window.show_all()
        
    # ------------------------------------------------------------------
    # Methods

    def show(self):
        self.prepare()

        self.window.show()

    def close(self):
        self.window.destroy()

    # ------------------------------------------------------------------
    # Callbacks

    def on_form_show(self, widget):
        pass

    def on_form_close(self, widget):
        pass

    def on_form_destroy(self, widget):
        if self.is_main_form:
            gtk.main_quit(widget)
        else:
            del self.app.forms[self.name]


class FormMain(Form):
    app = None
    window = None
    widget_name = 'formMain'
    project = None
    is_main_form = True

    def __init__(self, app):
        super(FormMain, self).__init__(app)

    def initialize(self):
        super(FormMain, self).initialize()

    # ------------------------------------------------------------------
    # Methods

    def show(self):
        super(FormMain, self).show()

    def close(self):
        super(FormMain, self).close()

    def update_widgets(self):
        # TreeView -----------------------------------------------------
        # Create model
        if not self.treeviewObjects.get_model():
            model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
            self.treeviewObjects.set_model(model)
        else:
            model = self.treeviewObjects.get_model()
        
        # Clear model
        model.clear()

        # Columns
        if not self.treeviewObjects.get_columns():
            rend1 = gtk.CellRendererText()
            col1 = gtk.TreeViewColumn('Name', rend1, text=0)
            self.treeviewObjects.append_column(col1)

        # Fills model
        nodeConn = model.append(None)
        model.set_value(nodeConn, 0, 'Connections')

        for conn in self.project.connections:
            node = model.append(nodeConn)
            model.set_value(node, 0, conn.driver_class)
            model.set_value(node, 1, conn)

        nodeVers = model.append(None)
        model.set_value(nodeVers, 0, 'Versions')

    # ------------------------------------------------------------------
    # Callbacks 

    def on_form_show(self, widget):
        self.project = Project()

        if len(sys.argv) > 1:
            self.project.load_from_file(sys.argv[1])

        self.update_widgets()

    def on_mniNewProject_activate(self, widget):
        self.project = Project()

        self.update_widgets()

    def on_mniNewVersionFile_activate(self, widget):
        print 'on_mniNewVersionFile_activate'

    def on_mniNewConnection_activate(self, widget):
        form = self.app.forms.get('formConnection', FormConnection(self.app, self.project.add_connection()))

    def on_mniOpenProject_activate(self, widget):
        self.project.load_from_file(filename)

        self.update_widgets()

    def on_mniSave_activate(self, widget):
        filename = utils.show_save_dialog()

        if filename:
            self.project.save_to_file(filename)

    def on_mniSaveAs_activate(self, widget):
        self.project.save_to_file(filename)

    def on_mniExit_activate(self, widget):
        self.close()

    def on_btnSave_clicked(self, widget):
        self.on_mniSave_activate(widget)

    def on_btnExit_clicked(self, widget):
        self.on_mniExit_activate(widget)


class FormConnection(Form):
    app = None
    window = None
    widget_name = 'formConnection'
    widgets = ('comboDriver','inputDSN',)
    connection = None

    def __init__(self, app, connection):
        self.connection = connection
        
        super(FormConnection, self).__init__(app)

    def on_btnCancel_clicked(self, widget):
        if self.connection.is_new:
            del self.connection

        self.close()

    def on_btnTestConnection_clicked(self, widget):
        print 'on_btnTestConnection_clicked'

    def on_btnOk_clicked(self, widget):
        self.connection.driver_class = utils.DRIVER_CLASSES[self.comboDriver.get_active()]
        self.connection.dsn = self.inputDSN.get_text()
        self.connection.is_new = False

        self.close()

        self.app.forms['formMain'].update_widgets()
        
    # ------------------------------------------------------------------
    # Callbacks

    def on_form_show(self, widget):
        if not self.connection: return

        if self.connection.driver_class:
            i = utils.DRIVER_CLASSES.values().find(self.connection.driver_class.__name__)
            self.comboDriver.set_active(i)

        self.inputDSN.set_text(self.connection.dsn)


class Project(object):
    connections = []
    initial_version = 0
    latest_version = None
    description = ''

    def __init__(self):
        pass

    def clear(self):
        pass

    def save_to_file(self, filename):
        print "saving to ... '%s'" % filename

    def load_from_file(self, filename):
        pass

    def add_connection(self, conn=None):
        conn = conn or Connection()

        self.connections.append(conn)
        conn.project = self

        return conn

class Connection(object):
    project = None
    driver_class = None # firebird, sqlite, mysql, postgres, etc.
    driver = None
    dsn = 'protocol:user:pass@host:port'

    def __init__(self, driver_class=None, dsn=''):
        self.driver_class, self.dsn = driver_class, dsn or self.dsn

    def __str__(self):
        return self.dsn

