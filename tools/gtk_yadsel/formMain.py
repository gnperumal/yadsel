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

import utils, app, forms, models
from formConnection import FormConnection


class FormMain(forms.Form):
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
        self.project = models.Project()

        if len(sys.argv) > 1:
            self.project.load_from_file(sys.argv[1])

        self.update_widgets()

    def on_mniNewProject_activate(self, widget):
        self.project = models.Project()

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


