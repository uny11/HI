# Leyenda de caracteres especiales:
# '@' para personas
# '#' para temas/proyectos
# '<>' para fechas
# Para el primer argumento:
#   - '+' añadir task
#   - '-' eliminar task
#   - 'fet' marcar como hecho!
#   - 'ls' listar.

from colorama import init, Fore, Back, Style
import sys
import re
import funcions

brain = 'mybrain.txt'   # archivo principal per enmagatzemar-ho tot! xD

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
        - '<>' per dates\n''')
    quit()

if sys.argv[1] == '+':

    if len(sys.argv) == 2:
        print(Fore.RED + '\nla tasca a afegir esta buida :S\n')
        quit()

    tema = '#general'
    data = '<buida>'
    descripcio = ''

    for paraula in sys.argv[2:]:
        if re.search('^#',paraula): tema = paraula
        if re.search('^<.+>$',paraula): data = paraula
        descripcio = descripcio + paraula + ' '

    idmax = funcions.buscar_id(tema)
    idnew = idmax + 1
    fhand = open(brain, 'a')
    fhand.write(tema + ';' + str(idnew) + ';N;' + data + ';' + descripcio+';\n')
    fhand.close()


elif sys.argv[1] == '-':
    print('-')

elif sys.argv[1] == 'X':
    print('X')

elif sys.argv[1] == 'ls':

    temas = []
    fhand = open(brain,'r')

    for line in fhand:
         paraules = line.split(';')
         if paraules[0] not in temas:
             temas.append(paraules[0])
             temas.sort()
    fhand.close()

    for tema in temas:
        print('\n' + Fore.CYAN + Style.BRIGHT + tema)
        fhand = open(brain,'r')
        for line in fhand:
            paraules = line.split(';')
            if paraules[0] == tema:
                idactual = paraules[1]
                estat = paraules[2]
                data = paraules[3]
                descripcion = paraules[4]
                print(Fore.BLACK + Back.WHITE + Style.BRIGHT + idactual,'    [',estat,']     ',Fore.GREEN + data,'     ',descripcion)
        fhand.close()
    print(' ')

else:
    print(Fore.CYAN + Style.BRIGHT + '''
    \nperdona, que vols fer? recorda que la primera paraula ha de ser:
            - '+' añadir task
            - '-' eliminar task
            - 'X' marcar como hecho!
            - 'ls' verificar el meu magatzem d'ideas\n''')
