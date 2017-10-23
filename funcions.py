
from colorama import init, Fore, Back, Style
import sys
import re

brain = 'mybrain.txt'   # archivo principal per enmagatzemar-ho tot! xD

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
