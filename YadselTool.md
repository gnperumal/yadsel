# Introduction #

This tool provides the basic operations of version upgrading/downgrading by command line. A compiled tool called **yadseltool.exe** can be used and packaged with Windows applications, like some had developed on my job.

# Details #

This tool runs like others command lines tools: receives some arguments and its values and processes this arguments to do things.

The arguments be:

## path ##
Receives a directory or zip file path that contents modules with version classes.

Syntax:
path="

<version\_files\_path>

"

## dsn ##
Receives a DSN string for database connection.

Syntax:
dsn="

&lt;host&gt;

[/

&lt;port&gt;

]:<database\_name or database\_path>"

## user ##
Receives the user name to connect to database.

Syntax:
user=

&lt;username&gt;



## pass ##
Receives the password of user to connect to database.

Syntax:
pass=

&lt;password&gt;



## from ##
Receives the current version enforced to Controller consider for upgrading/downgrading. If this argument is empty or zero (0), the Controller will verify latest version change on database by the table yadsel\_versions, if **history** argument was typed.

optional

Syntax:
from=

<version\_number>



Default: latest version of history control

## to ##
Receives the version that Controller must upgrade or downgrade to. If this argument is empty or zero (0), the latest version available in versions **path** argumento will be assumed.

optional

Syntax:
to=

<version\_number>



Default: latest available version

## action ##
Receives the action that the user wants. Can be 'up' or 'down', respectively for **upgrade** and **downgrade**.

optional

Syntax:
action=[up|down]

Default: **up**

## mode ##
Receives the mode of action that yadseltool will. Can be one of below:

  * **output**
    * writes the script to screen, and does not persists to database;
  * **hidden**
    * persists changes to database without shows nothing on screen;
  * **steps**
    * persists changes to database, writing each step on screen (good for be used embedded in other applications;
  * **interactive**
    * persists changes to database, writing each step on screen for user confirmation

optional

Syntax:
mode=[output|hidden|steps|interactive]

Default: **hidden**

## test ##
If declared, no changes will persist.

optional

Syntax:
test

## history ##
If declared, turns on history control on database.

optional

Syntax:
history

## silent ##
If declared, hide error messages and let the process go on.

optional

Syntax:
silent

## log ##
If declared, turns on the logging system, that is saved on a table called 'yadsel\_log'.

optional

Syntax:
log

## Dependences ##

This module depends of py2exe extension **1**, for create an executable file to be packaged in Windows applications.

  1. http://www.py2exe.org/