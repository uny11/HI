
from colorama import init, Fore, Back, Style
import sys
import re
from datetime import datetime

brain = 'mybrain.txt'   # archivo principal per enmagatzemar-ho tot! xD
archive = 'myarchive.txt'
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
    fhand.close()

    fhand = open(archive,'r')
    for line in fhand:
        paraules = line.split(';')
        idactual = paraules[1]
        temaactual = paraules[0]
        if tema == temaactual and idmax < int(idactual):
            idmax = int(idactual)
    fhand.close()

    return idmax

def print_task_incolor(task):
    words = task.split()
    task_in_color = ''
    for word in words:
        new_word = word
        if re.search('^#',word): new_word = Fore.GREEN + Style.BRIGHT + word + Style.RESET_ALL
        if re.search('^@',word): new_word = Fore.YELLOW + Style.BRIGHT + word + Style.RESET_ALL
        if re.search('^<.+>$',word): new_word = ''
        task_in_color = task_in_color + new_word + ' '

    return task_in_color

def convertir_fecha(data):
    # data = <dd/mm/aa>
    try:
        fecha = datetime.strptime(data, '<%d/%m/%y-%H:%Mh>')
    except:
        try:
            fecha = datetime.strptime(data, '<%d/%m/%Y-%H:%Mh>')
        except:
            fecha = datetime.strptime(data, '<%d/%m/%y>')
    hoy = datetime.now()
    if fecha < hoy:
        # in format ctime
        # fechafinal = Fore.RED + Style.BRIGHT + str(fecha.ctime())
        fechaf = fecha.strftime('%a %d%b%y %H:%Mh')
        fechafinal = Fore.RED + Style.BRIGHT + fechaf
    else:
        # in format ctime
        # fechafinal = Fore.CYAN + Style.BRIGHT + str(fecha.ctime())
        fechaf = fecha.strftime('%a %d%b%y %H:%Mh')
        fechafinal = Fore.CYAN + Style.BRIGHT + fechaf

    return fechafinal

def dif_fecha(data):
    # data = <dd/mm/aa>
    try:
        fecha = datetime.strptime(data, '<%d/%m/%y-%H:%Mh>')
    except:
        try:
            fecha = datetime.strptime(data, '<%d/%m/%Y-%H:%Mh>')
        except:
            fecha = datetime.strptime(data, '<%d/%m/%y>')
    hoy = datetime.now()
    diferencia = fecha - hoy

    return diferencia.days
