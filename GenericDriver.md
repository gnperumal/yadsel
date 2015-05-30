# Introduction #

This is the base class driver, that is where we implement all standards SQL, based on ANSI SQL and/or SQL-99, until is possible

# Details #

Module path: **dbmigrations.drivers.generic**
Main class: **dbmigrations.drivers.Generic**

Class tree:

  * FieldParser(object)
    * for\_create()
    * for\_alter()
    * for\_rename()
  * ActionParser(object)
    * for\_alter()
  * ValueParser(object)
    * for\_insert()
  * ClauseParser(object)
    * parse\_clause()
    * parse\_expression()
    * for\_parser()
    * for\_select()
    * for\_update()
    * for\_delete()
  * GenericDriver(dbmigrations.core.Driver)
    * generate\_script()
    * generate\_script\_for\_createtable()
    * generate\_script\_for\_altertable()
    * generate\_script\_for\_droptable()
    * generate\_script\_for\_createindex()
    * generate\_script\_for\_dropindex()
    * generate\_script\_for\_insert()
    * generate\_script\_for\_select()

# Dependences #

Has no dependences,