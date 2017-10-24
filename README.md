
# HI (Holding Ideas)
## Current Status : Active

Holding Ideas (o "hi") is my ultra-simple ToDoList for console.
Write in python 3.x, the main goal is erase from my head all tasks..

### For install:
 - Download the master branch.
 - Unzip files into a folder (your working folder).
 - The main script is "hi.py". You can launch the program with "python hi.py [+arg]"

### Dependences
- Python 3.x or more

### How to use
- Add a task:

**python hi.py + this is my first task for @me #test <27/10/17>**

- List the current task (This is the Heart of program):

**python hi.py ls**

- check a task

**python hi.py ok personal 1**

- un-check a task

**python hi.py N personal 1**

- archive a task

**python hi.py - personal 1**

!(https://github.com/uny11/HI/blob/master/example.png)


### files
- "mybrain.txt" contains the current task
- "myarchive.txt" contains the archive of all old task.
- hi.py and funcions.py are code of program in python.


### Recommendations

- In linux, add this in your ~/.bashrc file:

    **alias hi = python hi.py**

- In windows powershell, add this in your profile:

    **function hi {python hi.py $args}**

Now it's possible to do:

**hi ls**



### Legend
**Notation:**
 - '@' for persons.
 - '#' for subject/group.
 - '<>' for date.

**First argument:**
 - '+' for add task.
 - '-' for archive task.
 - 'ok' for check.
 - 'N' for un-check.
 - 'ls' for list all current task.
 - 'init' for reboot your tasks files.
