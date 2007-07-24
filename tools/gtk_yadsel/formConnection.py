# -*- coding: iso-8859-1 -*-

"""
Connection edit/new form
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

class FormConnection(forms.Form):
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

        # Driver combobox value setting
        if self.connection.driver_class:
            i = utils.DRIVER_CLASSES.values().index(self.connection.driver_class) # .__name__
            self.comboDriver.set_active(i)

        # DSN entry value setting
        self.inputDSN.set_text(self.connection.dsn)

