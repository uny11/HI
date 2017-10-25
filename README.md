
# HI (Holding Ideas)
## Current Status : Active
## Current Version : v0.1.2

Holding Ideas (o "hi") is my ultra-simple ToDoList for console.
Write in python 3.x, the main goal is erase from my head all tasks to do and wotk about other things.

### For install:
 - Download the master branch.
 - Unzip files into a folder (your working folder).
 - The main script is "hi.py". You can launch the program with "python hi.py [+arg]"

### Dependences
- Python 3.x or more

### How to use
- Reboot (or start) your tasks files:

      _python hi.py init_

- Add a task (argument = "+"):

      _python hi.py + this is my first task for @me #test <27/10/17>_

- List the current task (argument "ls" This is the most important thing! in program):

      _python hi.py ls_

- check a task due with argument "ok":

      _python hi.py ok personal 1_

- un-check a task with argument "N":

      _python hi.py N personal 1_

- archive a task with argument "-":

      _python hi.py - personal 1_

![for example:](https://github.com/uny11/HI/blob/master/example.png)


### files
- "mybrain.txt" contains the current task
- "myarchive.txt" contains the archive of all old task.
- hi.py and funcions.py are code of program in python.


### Recommendations

- In linux, add this in your ~/.bashrc file:

      _alias hi = python hi.py_

- In windows powershell, add this in your profile:

      _function hi {python hi.py $args}_

- Now it's possible to do:

      _hi ls_



### Legend
*Notation:*
 - '@' for persons.
 - '#' for subject/group.
 - '<>' for date.

*First argument:*
 - '+' for add task.
 - '-' for archive task.
 - 'ok' for check.
 - 'N' for un-check.
 - 'ls' for list all current task.
 - 'init' for reboot your tasks files.
