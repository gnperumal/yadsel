# Introduction #

This is our first driver, where we are testing the concept behind the scenes in a real case.

# Details #

Module path: **yadsel.drivers.firebird**
Main class: **yadsel.drivers.Firebird**

Class tree:

  * FirebirdDriver(yadsel.drivers.GenericDriver)
  * FirebirdInspector(yadsel.core.dbms.SchemaInspector)
  * FirebirdFieldParser(object)
  * FirebirdConstraintParser(object)

# Dependences #

This module depends of **kinterbasdb** library, the most popular driver for Firebird on Python language. You can see more about **(and download it)** on its official website: [1](1.md)

[1](1.md) http://kinterbasdb.sourceforge.net/