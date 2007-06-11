"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

class Command(object):
    def __init__(self):
        pass

    def append_to(self, version):
        if hasattr(version, 'commands'):
            version.commands.append(self)

