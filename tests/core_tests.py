#!/usr/bin/env python

"""
** not yet documented **
@author Marinho Brandao
@created 2007-07-31
"""

from yadsel.core import * 
from yadsel.drivers import * 

class Tables(PartialVersion):
    def up(self):
        CreateTable('categories',
            id = Integer(primary_key=True),
            name = Varchar(length=30),
        ).append_to(self)

        CreateTable('persons',
            id = Integer(primary_key=True),
            first_name = Varchar(length=30),
            last_name = Varchar(length=30),
            category_id = Integer(required=False),
            fk_persons_categories = ForeignKey(('category_id',), 'categories', ('id',)),
        ).append_to(self)

    def down(self):
        DropTable('persons').append_to(self)
        DropTable('categories').append_to(self)


class Data(PartialVersion):
    def up(self):
        Insert('categories',
            id = 1,
            name = 'default',
        ).append_to(self)

    def down(self):
        Delete('categories',
            Where(id = 1),
        ).append_to(self)


class TestVersion(Version):
    version_number = 1

    def __init__(self):
        self.partial_versions = [Tables, Data]

    
if __name__ == '__main__':
    import doctest
    doctest.testfile('core_tests_partial_versions.txt')
    doctest.testfile('core_tests_persistence.txt')
    doctest.testfile('core_tests_zipfile_versions.txt')
    doctest.testfile('core_tests_parseutils.txt')
    doctest.testfile('core_tests_dml.txt')
    doctest.testfile('core_tests_firebird.txt')

