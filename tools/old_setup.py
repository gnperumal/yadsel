#!/usr/bin/env python

# Thanks to Washington Coutinho Correa by py2exe example published at:
# http://www.pythonbrasil.com.br/moin.cgi/Py2ExeSimples

from distutils.core import setup
import py2exe, sys, os

modules = ['yadseltool',]

options = {
    'py2exe': {
        'excludes': [],
        'packages': [
            'yadsel',
            'kinterbasdb',
            'pymssql',
            'MySQLdb',
            'pysqlite2',
            'simplejson',
            'mx',
            ]
        }
    }

execname = 'YadselTool'
description = 'Yadsel Tool'
version = '0.1'

setup(
    name=description,
    console=modules,
    zipfile="lib/shared.zip",
    description=description,
    version=version,
)

