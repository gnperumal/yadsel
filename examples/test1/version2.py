"""
That version implements Alter Table DDL statement
@author Marinho Brandao
@creation 2007-05-25
"""

from yadsel.core import *

class Version2(Version):
    version_number = 2

    def up(self):
        AlterTable('states',
                Add('percent_tax', Decimal(5,2, required=False)),
                Add('age', Integer(default=0)),
            ).append_to(self)

        CreateTable('streets',
                id = Integer(required=True),
                name = Varchar(length=50, required=True),
                city_id = Integer(required=True),
            ).append_to(self)

    def down(self):
        DropTable('streets').append_to(self)

        AlterTable('states',
                DropColumn('percent_tax'),
            ).append_to(self)

