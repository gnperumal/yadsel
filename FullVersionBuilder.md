# Introduction #

This resource haves the goal for supply a efficient way to get the database schema and generate a full script version, with CreateTable, CreateDomain and CreateIndex statements.

It was started, first for SQLite Driver, but MySQL and Firebird is near :)

# Details #

For see this resource, loot following classes:

  * yadsel.core.versions.FullVersionBuilder
  * yadsel.core.dbms.SchemaInspector
  * yadsel.core.dbms.Driver.Inspector
  * yadsel.drivers.sqlite.SQLiteInspector