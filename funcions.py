
from colorama import init, Fore, Back, Style
import sys
import re

brain = 'mybrain.txt'   # archivo principal per enmagatzemar-ho tot! xD
init(autoreset=True)    # para reiniciar colores cada vez

def buscar_id (tema):
    # OBJ: retornar el valor del id mes alt actualment dins de brain.
    fhand = open(brain,'r')
    idmax = 0
    for line in fhand:
        paraules = line.split(';')
        idactual = paraules[1]
        temaactual = paraules[0]
        if tema == temaactual and idmax < int(idactual):
            idmax = int(idactual)

    return idmax

def print_task_incolor(task):
    words = task.split()
    task_in_color = ''
    for word in words:
        new_word = word
        if re.search('^#',word): new_word = Fore.YELLOW + Style.BRIGHT + word + Style.RESET_ALL
        if re.search('^@',word): new_word = Fore.MAGENTA + Style.BRIGHT + word + Style.RESET_ALL
        if re.search('^<.+>$',word): new_word = ''
        task_in_color = task_in_color + new_word + ' '

    return task_in_color
