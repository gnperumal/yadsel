# -*- coding: iso-8859-1 -*-

"""
Project options form
@author Marinho Brandao
@creation 2007-07-24
"""

import sys

try:
    import pygtk
    pygtk.require('2.0')
    import gtk, gtk.glade, gobject
except:
    sys.exit(1)

import utils, app, forms, models

class FormOptions(forms.Form):
    app = None
    window = None
    widget_name = 'formOptions'
    widgets = ('inputInitialVersion','inputLatestVersion','editorDescription',)
    project = None

    def __init__(self, app, project):
        self.project = project
        
        super(FormOptions, self).__init__(app)

    def on_btnCancel_clicked(self, widget):
        self.close()

    def on_btnOk_clicked(self, widget):
        self.project.initial_version = self.inputInitialVersion.get_text()
        self.project.latest_version = self.inputLatestVersion.get_text()

        buffer = self.editorDescription.get_buffer()
        self.project.description = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), include_hidden_chars=True)

        self.close()

        self.app.forms['formMain'].update_widgets()
        
    # ------------------------------------------------------------------
    # Callbacks

    def on_form_show(self, widget):
        self.inputInitialVersion.set_text(self.project.initial_version)
        self.inputLatestVersion.set_text(self.project.latest_version)

        buffer = self.editorDescription.get_buffer()
        buffer.set_text(self.project.description)

