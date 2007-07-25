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
    import gtk, gtk.glade, gobject, pango
except:
    sys.exit(1)

import utils, app, forms, models
from formConnection import FormConnection
from formOptions import FormOptions


class FormMain(forms.Form):
    app = None
    window = None
    widget_name = 'formMain'
    project = None
    is_main_form = True
    widgets = (
        'notebookMain',
        'treeviewObjects',
        'labelInitialVersion',
        'labelLatestVersion',
        'labelDescription',
        )

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
        # Connections
        nodeConn = model.append(None)
        model.set_value(nodeConn, 0, 'Connections')

        for conn in self.project.connections:
            node = model.append(nodeConn)
            model.set_value(node, 0, str(conn))
            model.set_value(node, 1, conn)

        # Versions
        nodeVers = model.append(None)
        model.set_value(nodeVers, 0, 'Versions')

        for vers in self.project.version_files:
            node = model.append(nodeVers)
            model.set_value(node, 0, str(vers))
            model.set_value(node, 1, vers)

        # Project attributes
        self.labelInitialVersion.set_text(str(self.project.initial_version))
        self.labelLatestVersion.set_text(str(self.project.latest_version))
        self.labelDescription.set_text(self.project.description)

    def show_version_editor(self, version_file):
        editor = gtk.TextView()
        editor.show()
        editor.modify_font(pango.FontDescription('Courier New'))

        buffer = editor.get_buffer()
        buffer.set_text(version_file.content)

        label = gtk.Label('Version %s' % str(version_file))

        self.notebookMain.append_page(editor, label)
        self.notebookMain.set_current_page(self.notebookMain.get_n_pages()-1)

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
        vers = self.project.add_version_file()

        self.update_widgets()

        self.show_version_editor(vers)

    def on_mniEditVersion_activate(self, widget):
        sel = self.treeviewObjects.get_selection()
        model, iter = sel.get_selected()
        vers = model.get_value(iter, 1)

        if isinstance(vers, models.VersionFile):
            self.show_version_editor(vers)

    def on_mniDeleteVersion_activate(self, widget):
        sel = self.treeviewObjects.get_selection()
        model, iter = sel.get_selected()
        vers = model.get_value(iter, 1)

        if isinstance(vers, models.VersionFile):
            vers.remove_from_project()
            self.update_widgets()

    def on_mniCloseVersion_activate(self, widget):
        page = self.notebookMain.get_current_page()

        if page > 0:
            self.notebookMain.remove_page(page)

    def on_mniOpenProject_activate(self, widget):
        filename = utils.show_open_dialog()

        if filename:
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

    def on_btnOpenProject_clicked(self, widget):
        self.on_mniOpenProject_activate(widget)

    def on_btnSave_clicked(self, widget):
        self.on_mniSave_activate(widget)

    def on_btnExit_clicked(self, widget):
        self.on_mniExit_activate(widget)

    def on_mniNewConnection_activate(self, widget):
        self.app.forms.get('formConnection', FormConnection(self.app, self.project.add_connection()))

    def on_mniEditConnection_activate(self, widget):
        sel = self.treeviewObjects.get_selection()
        model, iter = sel.get_selected()
        conn = model.get_value(iter, 1)

        if isinstance(conn, models.Connection):
            form = self.app.forms.get('formConnection', FormConnection(self.app, conn))

    def on_mniDeleteConnection_activate(self, widget):
        sel = self.treeviewObjects.get_selection()
        model, iter = sel.get_selected()
        conn = model.get_value(iter, 1)

        if isinstance(conn, models.Connection):
            conn.remove_from_project()
            self.update_widgets()

    def on_mniProjectOptions_activate(self, widget):
        self.app.forms.get('formOptions', FormOptions(self.app, self.project))
        self.update_widgets()

