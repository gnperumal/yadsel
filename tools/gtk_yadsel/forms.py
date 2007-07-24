# -*- coding: iso-8859-1 -*-

"""
'Form' class module container
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
        self.widget_tree = gtk.glade.XML('%s.glade' % self.widget_name)

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

