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
    import gtk
    import gtk.glade
except:
    sys.exit(1)

PROJECT_FILE_EXTENSION = 'yadsel'
PYTHON_FILE_EXTENSION = 'py'
DRIVER_CLASSES = {0: 'Firebird', 1: 'MySQL', 2: 'SQLite',}

def show_save_dialog():
    dialog = gtk.FileChooserDialog(
            'Choose a file name to save...', None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        )
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    # Filters
    filter = gtk.FileFilter()
    filter.set_name("Project files")
    filter.add_pattern("*.%s" % PROJECT_FILE_EXTENSION)
    dialog.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)
        
    if dialog.run() == gtk.RESPONSE_OK:
        filename = dialog.get_filename()

        if not filename.endswith("."+PROJECT_FILE_EXTENSION):
            filename += "."+PROJECT_FILE_EXTENSION
    else:
        filename = ''

    dialog.destroy()

    return filename

def show_open_dialog(default_extension=PROJECT_FILE_EXTENSION):
    dialog = gtk.FileChooserDialog(
            'Choose a file name to open...', None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        )
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    # Filters
    if default_extension == PROJECT_FILE_EXTENSION:
        filter = gtk.FileFilter()
        filter.set_name("Project files")
        filter.add_pattern("*.%s" % PROJECT_FILE_EXTENSION)
        dialog.add_filter(filter)
    else:
        filter = gtk.FileFilter()
        filter.set_name("Python files")
        filter.add_pattern("*.%s" % PYTHON_FILE_EXTENSION)
        dialog.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)
        
    if dialog.run() == gtk.RESPONSE_OK:
        filename = dialog.get_filename()

        if not filename.endswith("."+default_extension):
            filename += "."+default_extension
    else:
        filename = ''

    dialog.destroy()

    return filename

