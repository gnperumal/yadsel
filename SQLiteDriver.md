# Introduction #

This is the driver for SQLite support.

# Details #

Module path: **yadsel.drivers.sqlite**
Main class: **yadsel.drivers.SQLite**

Class tree:

  * SQLiteDriver(yadsel.drivers.GenericDriver)
  * SQLiteInspector(yadsel.core.dbms.SchemaInspector)

# Dependences #

This module depends of **pySQLite** library, the most popular driver for SQLite on Python language. You can see more about **(and download it)** on its official website: [1](1.md)

The introspection does through the PRAGMA statements suplied by SQLite protocol (described in [2](2.md)).

[1](1.md) http://www.initd.org/tracker/pysqlite/wiki/pysqlite
[2](2.md) http://www.sqlite.org/pragma.html#schema