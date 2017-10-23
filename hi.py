# Leyenda de caracteres especiales:
# '@' para personas
# '#' para temas/proyectos
# '[]' para fechas
# Para el primer argumento:
#   - '+' añadir task
#   - '-' eliminar task
#   - 'fet' marcar como hecho!
#   - 'ls' listar.

from colorama import init, Fore, Back, Style
import sys
import re

brain = 'mybrain.txt'   # archivo principal para holding ideas! xD

init(autoreset=True)    # para reiniciar colores cada vez

if len(sys.argv) < 2:
    print(Fore.CYAN + Style.BRIGHT + '\nque volies fer alguna cosa?')
    print('''
    python hi.py [opcio] 'descripcio de la tasca'
    opcions:
        - '+' añadir task
        - '-' eliminar task
        - 'X' marcar como hecho!
        - 'ls' listar.
    paraules especials:
        - '@' per persones
        - '#' per temes/projectes
        - '[]' per dates\n''')
    quit()

if sys.argv[1] == '+':
    print('+')

elif sys.argv[1] == '-':
    print('-')

elif sys.argv[1] == 'X':
    print('X')

elif sys.argv[1] == 'ls':
    print('ls')

else:
    print(Fore.CYAN + Style.BRIGHT + '''
    \nperdona, que vols fer? recorda que la primera paraula ha de ser:
            - '+' añadir task
            - '-' eliminar task
            - 'X' marcar como hecho!
            - 'ls' verificar el meu magatzem d'ideas\n''')
