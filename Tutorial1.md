# Getting started #

Yadsel is a library that includes an API similar to SQL ANSI standards to versionate a database and tools for manage them.

Yadsel is writed with Python language and was inspired on Ruby on Rails Migrations package.

The Core package contains a set of class that you can use, appending to 2 different methods on a version class: **up()** and **down()** - respectively to upgrade and downgrade a database.

The Drivers package contains one Generic driver and some others do some DBMS and/or ORM systems. The Firebird driver is the most stable at now. Each driver is a class inherited from Generic driver, altough, only the DBMS specific features are implemented in.

So, you need a DBMS connection and a database created, and some version classes in a package called 'yadsel\_versions', and execute a tool or directly the commands in Python to upgrade or downgrade or database.

# Installing Yadsel #

## Dependences ##

## Yadsel on Linux (or another **unix based OS) ##**

## Yadsel on Windows ##

# Creating the database #

# Creating the first database version #