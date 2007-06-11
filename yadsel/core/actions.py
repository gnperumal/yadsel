"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

class Action(object):
    def __init__(self):
        pass

class Add(Action):
    name = None
    object = None

    def __init__(self, name, obj):
        self.name = name
        self.object = obj
        self.object.name = name

class AlterColumn(Action):
    name = None
    object = None

    def __init__(self, name, obj):
        self.name = name
        self.object = obj

class DropColumn(Action):
    name = None

    def __init__(self, name):
        self.name = name

class RenameColumn(Action):
    name = None
    new_name = None
    object = None

    def __init__(self, name, new_name, object):
        self.name = name
        self.new_name = new_name
        self.object = object
        self.object.name = self.new_name

