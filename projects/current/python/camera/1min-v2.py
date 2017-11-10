# Fent servir un sleep, el programa gasta muuuchossss menos recursooosssss

import cv2
from datetime import datetime
from time import sleep
from colorama import init, Fore, Back, Style

def sacar_foto (string):
    cap = cv2.VideoCapture(0)
    ret = cap.set(3,320)
    ret = cap.set(4,170)
    ret,frame = cap.read()
    fichero = 'f'+str(string)+'.png'
    cv2.imwrite(fichero,frame)
    cap.release()
    cv2.destroyAllWindows()
    print('Creada la imagen',fichero)


print(Fore.CYAN + Style.BRIGHT + '\nMyRepeatFotos v0.1\n' + Style.RESET_ALL)
freq = input('¿con que frecuencia quieres una foto? (en segundos): ')
try:
    freq = int(freq)
except:
    print('Ups, introduce un valor válido!. Bye!')
    exit()
total = input('Cuantas fotos quieres hacer en total? ')
try:
    total = int(total)
except:
    print('Ups, introduce un valor válido!. Bye!')
    exit()

if (total*freq) > 60:
    minutos = float(total*freq)/60.0
    print("El programa tardara %i segundos" %(total*freq), ', es decir, ',minutos,'minutos.\n')
else:
    print("El programa tardara %i segundos\n" %(total*freq))
respuesta = input(Fore.CYAN + Style.BRIGHT +'Seguimos? (s/n) > '+ Style.RESET_ALL)

if respuesta == 's' or respuesta == 'S':
    print(Fore.CYAN + Style.BRIGHT +'\nAdelante!' + Style.RESET_ALL)
    for foto in range(total):
        now = datetime.now()
        string_fichero = datetime.strftime(now,'_%d%m%y_%H%M%S')
        sleep(freq)
        sacar_foto(string_fichero)
    print(Fore.CYAN + Style.BRIGHT +'Hecho!'+ Style.RESET_ALL)
else:
    print(Style.BRIGHT +'\nOk, pues mejor en otro momento.\nBye!\n'+ Style.RESET_ALL)
    quit()
