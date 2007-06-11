"""
That version implements Create Table DDL statements 2 times
@author Marinho Brandao
@creation 2007-05-25
"""

from yadsel.core import *

class Version1(Version):
    version_number = 1

    def up(self):
        CreateTable('states',
                id = Integer(required=True),
                short_name = Char(2, required=True),
                name = Varchar(50, required=True),
            ).append_to(self)

        CreateTable('cities',
                id = Integer(required=True),
                name = Varchar(50, required=True),
                state_id = Integer(required=True),
            ).append_to(self)

    def down(self):
        DropTable('cities').append_to(self)
        DropTable('states').append_to(self)

