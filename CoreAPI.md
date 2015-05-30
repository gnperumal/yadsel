# Introduction #

The Core API is a class system, that support DBMS's drivers, DDL and DML statements e version control system.

# Base #
  * [Driver](Driver.md)
  * [SchemaInspector](SchemaInspector.md)
  * [ExtensibleVersion](ExtensibleVersion.md)
  * [Version](Version.md)
  * [PartialVersion](PartialVersion.md)
  * [Controller](Controller.md)
  * [Command](Command.md)
  * [Action](Action.md)
  * [FieldType](FieldType.md)

# SQL Statements #

## DDL ##

  * Commands
    * Create Table
    * Alter Table
    * Drop Table
    * Rename Table
    * Create Index
    * Drop Index

  * Actions
    * Add
    * Rename Column
    * Alter Column
    * Drop Column

  * Field Types
    * Integer
    * Varchar
    * Char
    * Timestamp
    * Date
    * Time
    * DateTime?
    * Text
    * Boolean
    * Decimal
    * Numeric

  * Constraints
    * Foreign Key
    * Primary Key

## DML ##

  * Commands
    * Select
    * Insert
    * Update
    * Delete
    * Merge
    * ClearAllData
    * DropAllObjects
    * ExecuteSQL
  * Clauses
    * Where
    * And
    * Or
    * Not
    * Expression
  * Operations
    * =
    * >
    * >=
    * <
    * <=
    * like

![http://yadsel.googlecode.com/files/core%20package%20diagram.png](http://yadsel.googlecode.com/files/core%20package%20diagram.png)