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
    print "GTK 2.0 required! Exiting from application..."
    sys.exit(1)

import utils
from formConnection import FormConnection
from formMain import FormMain

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

