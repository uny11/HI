
from colorama import init, Fore, Back, Style
import sys
import re
from datetime import datetime
import funcions # funciones del programa

brain = 'mybrain.txt'   # archivo principal
archive = 'myarchive.txt'   # archivo para guardar tareas eliminadas

init(autoreset=True)

if len(sys.argv) < 2:
    print(Fore.RED + Style.BRIGHT + '\nque volies fer alguna cosa?')
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
        print(Fore.RED + Style.BRIGHT + '\nla tasca a afegir esta buida :S\n')
        quit()

    tema = '#personal'
    data = '<27/06/1982-13:00h>'
    descripcio = ''

    for paraula in sys.argv[2:]:
        if re.search('^#',paraula): tema = paraula
        if re.search('^<.+>$',paraula):
            data = paraula
            try:
                test = datetime.strptime(paraula, '<%d/%m/%y-%H:%Mh>')
            except:
                try:
                    test2 = datetime.strptime(paraula, '<%d/%m/%Y-%H:%Mh>')
                except:
                    try:
                        test3 = datetime.strptime(paraula, '<%d/%m/%y>')
                    except:
                        print(Fore.RED + '''\nel format de la data introduida no es aceptada, fer servir:
                            - <%d/%m/%y-%H:%Mh>
                            - <%d/%m/%Y-%H:%Mh>
                            - o <%d/%m/%y>\n''')
                        quit()

        descripcio = descripcio + paraula + ' '

    idmax = funcions.buscar_id(tema)
    idnew = idmax + 1
    fhand = open(brain, 'a')
    fhand.write(tema + ';' + str(idnew) + ';N;' + data + ';' + descripcio+';\n')
    fhand.close()


elif sys.argv[1] == '-':
    print('-')

elif sys.argv[1] == 'ok':

    if len(sys.argv) < 4:
        print(Fore.RED + Style.BRIGHT + '\nquina tasca/tema vols marcar?\n','python hi.py ok [tema] [idtasca]\n')
        quit()

    tema = sys.argv[2]
    idtasca = sys.argv[3]
    fhand = open(brain,'r+')
    sopa = fhand.read()
    textorigen = '#'+tema+';'+idtasca+';N;'
    textfinal = '#'+tema+';'+idtasca+';OK;'
    sopa = sopa.replace(textorigen,textfinal)
    textorigen = tema+';'+idtasca+';N;'
    textfinal = tema+';'+idtasca+';OK;'
    sopa = sopa.replace(textorigen,textfinal)
    fhand.seek(0)
    fhand.write(sopa)
    fhand.close()

elif sys.argv[1] == 'N':

    if len(sys.argv) < 4:
        print(Fore.RED + Style.BRIGHT + '\nquina tasca/tema vols desmarcar?\n','python hi.py N [tema] [idtasca]\n')
        quit()

    tema = sys.argv[2]
    idtasca = sys.argv[3]
    fhand = open(brain,'r+')
    sopa = fhand.read()
    textorigen = '#'+tema+';'+idtasca+';OK;'
    textfinal = '#'+tema+';'+idtasca+';N;'
    sopa = sopa.replace(textorigen,textfinal)
    textorigen = tema+';'+idtasca+';OK;'
    textfinal = tema+';'+idtasca+';N;'
    sopa = sopa.replace(textorigen,textfinal)
    fhand.seek(0)
    fhand.write(sopa)
    fhand.close()

elif sys.argv[1] == 'init':
    print('Estas seguro en reiniciar "mybrain.txt"?')
    op = input('(s/n por defecto "n" >> ')
    if op == 's' or op == 'S':
        fhand = open(brain,'w')
        fhand.close()
    print('Ok, mejor en otro momento')

elif sys.argv[1] == 'ls':

    temas = []
    fhand = open(brain,'r')

    for line in fhand:
         paraules = line.split(';')
         if paraules[0] not in temas:
             temas.append(paraules[0])
             temas.sort(reverse=True)
    fhand.close()

    try:
        subject = sys.argv[2]
        for tema in temas:
            if tema == subject or tema == '#'+subject:
                print('\n' + Fore.GREEN + Style.BRIGHT + tema)
            fhand = open(brain,'r')
            for line in fhand:
                if re.search('^#'+subject,line):
                    paraules = line.split(';')
                    if paraules[0] == tema:
                        idactual = paraules[1]
                        estat = paraules[2]
                        if estat == 'N': estat = Fore.RED + estat
                        data = paraules[3]
                        data = funcions.convertir_fecha(data)
                        task = paraules[4]
                        printtask = funcions.print_task_incolor(task)
                        print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']     ',data,'     ',printtask)
                if re.search('^'+subject,line):
                    paraules = line.split(';')
                    if paraules[0] == tema:
                        idactual = paraules[1]
                        estat = paraules[2]
                        if estat == 'N': estat = Fore.RED + estat
                        data = paraules[3]
                        data = funcions.convertir_fecha(data)
                        task = paraules[4]
                        printtask = funcions.print_task_incolor(task)
                        print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']     ',data,'     ',printtask)
            fhand.close()
        print(' ')

    except:
        for tema in temas:
            print('\n' + Fore.GREEN + Style.BRIGHT + tema)
            fhand = open(brain,'r')
            for line in fhand:
                paraules = line.split(';')
                if paraules[0] == tema:
                    idactual = paraules[1]
                    estat = paraules[2]
                    if estat == 'N': estat = Fore.RED + estat
                    data = paraules[3]
                    data = funcions.convertir_fecha(data)
                    task = paraules[4]
                    printtask = funcions.print_task_incolor(task)
                    print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']     ',data,'     ',printtask)
            fhand.close()
        print(' ')

else:
    print(Fore.CYAN + Style.BRIGHT + '''
    \hola, que vols fer? recorda que la primera paraula ha de ser:
            - '+' añadir task
            - '-' eliminar task
            - 'ok' marcar com fet!
            - 'N' per desmarcar com fet
            - 'ls' verificar el meu magatzem d'ideas\n''')
