
from colorama import init, Fore, Back, Style
import sys
import re
from datetime import datetime
import funcions # funciones del programa

brain = 'mybrain.txt'   # archivo principal
archive = 'myarchive.txt'   # archivo para guardar tareas eliminadas

init(autoreset=True)

if len(sys.argv) < 2:
    print(Fore.RED + Style.BRIGHT + '\nsorry, do you want to do something?')
    print('''
    python hi.py [option] [description of task]\n
    options:
        - 'init' fot reboot your warehouse of tasks.
        - '+' for add task
        - '-' for archive task
        - 'ok' for check task due
        - 'N' for uncheck task.
        - 'ls' for list current tasks
    Some char specials:
        - '@' for persons
        - '#' for themes/subject or groups.
        - '<>' for dates\n''')
    quit()

if sys.argv[1] == '+':

    if len(sys.argv) == 2:
        print(Fore.RED + Style.BRIGHT + '\nsorry, the task is empty :S\n')
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
                        print(Fore.RED + '''\nthe format of date is not correct, you can use:
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

    if len(sys.argv) < 4:
        print(Fore.RED + Style.BRIGHT + '\nsorry, what task do you want to archive?\n','python hi.py - [theme] [idtask]\n')
        quit()

    tema = sys.argv[2]
    idtasca = sys.argv[3]

    tasca = '^#'+tema+';'+idtasca+';'
    delline = ''

    fhand = open(brain,'r')
    for line in fhand:
        if re.search(tasca, line):
            delline = line

    if delline == '': quit()
    fhand.seek(0)
    sopa = fhand.read()
    sopa = sopa.replace(delline,'')
    fhand.close()
    fhand = open(brain,'w')
    fhand.write(sopa)
    fhand.close()

    fhand2 = open(archive,'a')
    fhand2.write(delline)
    fhand2.close()


elif sys.argv[1] == 'ok':

    if len(sys.argv) < 4:
        print(Fore.RED + Style.BRIGHT + '\nsorry, what task do you want to check due?\n','python hi.py ok [theme] [idtask]\n')
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
        print(Fore.RED + Style.BRIGHT + '\nsorry, what task do you want to uncheck?\n','python hi.py N [theme] [idtask]\n')
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

    print(Fore.RED + Style.BRIGHT + '\nAre you sure to empty "myarchive.txt"?')
    op = input('(y/n default "n" >> ')
    if op == 'y' or op == 'Y':
        fhand = open(archive,'w')
        fhand.close()
        print(Fore.GREEN + Style.BRIGHT + '"myarchive.txt" is ready now!\n')
    else:
        print('Ok, nothing done.')

    print(Fore.RED + Style.BRIGHT + '\nAre you sure to empty "mybrain.txt"?')
    op = input('(y/n default "n" >> ')
    if op == 'y' or op == 'Y':
        fhand = open(brain,'w')
        fhand.close()
        print(Fore.GREEN + Style.BRIGHT + '"mybrain.txt" is ready now!\n')
        quit()
    else:
        print('Ok, nothing done.\n')
        quit()

elif sys.argv[1] == 'ls':

    temas = []
    fhand = open(brain,'r')

    for line in fhand:
         paraules = line.split(';')
         if paraules[0] != '\n':
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
                        datap = funcions.convertir_fecha(data)
                        difp = funcions.dif_fecha(data)
                        task = paraules[4]
                        printtask = funcions.print_task_incolor(task)
                        print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']   ',difp,' ',datap,'     ',printtask)
                if re.search('^'+subject,line):
                    paraules = line.split(';')
                    if paraules[0] == tema:
                        idactual = paraules[1]
                        estat = paraules[2]
                        if estat == 'N': estat = Fore.RED + estat
                        data = paraules[3]
                        datap = funcions.convertir_fecha(data)
                        difp = funcions.dif_fecha(data)
                        task = paraules[4]
                        printtask = funcions.print_task_incolor(task)
                        print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']   ',difp,' ',datap,'     ',printtask)
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
                    datap = funcions.convertir_fecha(data)
                    difp = funcions.dif_fecha(data)
                    task = paraules[4]
                    printtask = funcions.print_task_incolor(task)
                    print(Fore.YELLOW + Style.BRIGHT + idactual,'    [',estat,']   ',difp,' ',datap,'     ',printtask)
            fhand.close()
        print(' ')

else:
    print(Fore.CYAN + Style.BRIGHT + '''
    \sorry, what do you want to do?
            - 'init' fot reboot your warehouse of tasks.
            - '+' for add task
            - '-' for archive task
            - 'ok' for check task due
            - 'N' for uncheck task.
            - 'ls' for list current tasks\n''')
