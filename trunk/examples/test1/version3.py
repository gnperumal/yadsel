"""
That version implements Insert DML statement
@author Marinho Brandao
@creation 2007-05-26
"""

from yadsel.core import *

class Version3(Version):
    version_number = 3

    def up(self):
        Insert('streets',
                id = 1,
                name = '1st Street',
                city_id = 27,
            ).append_to(self)

    def down(self):
        Delete('streets',
                Where(id=1),
            ).append_to(self)

