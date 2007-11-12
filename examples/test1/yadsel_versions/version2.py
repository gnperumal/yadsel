"""
That version implements Alter Table DDL statement
@author Marinho Brandao
@creation 2007-11-11
"""

from yadsel.core import *

class Version2(Version):
    version_number = 2

    def up(self):
        AlterTable('states',
                Add('percent', Decimal(15, 5, default=0)),
            ).append_to(self)

    def down(self):
        AlterTable('states',
                DropColumn('percent'),
            ).append_to(self)

