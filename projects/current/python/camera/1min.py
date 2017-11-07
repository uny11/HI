# The goal es hacer un script para hacer fotos cada x tiempo.

import cv2
from colorama import init, Fore, Back, Style
from datetime import datetime


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


init(autoreset=True)    # reiniciar colores

print(Style.BRIGHT+'\nHola uny11!')
freq = input('bien, ¿con que frecuencia quieres hacer una foto? (en segundos): ')
total = input('Cuantas fotos quieres hacer? ')
total = int(total)

now = datetime.now()
str_t_inicial = datetime.strftime(now,'%S')
t_inicial = int(str_t_inicial)
t_siguiente = t_inicial + int(freq)
if t_siguiente > 59: t_siguiente = t_siguiente - 60

count = 0
while True:
    now = datetime.now()
    str_t_now = datetime.strftime(now,'%S')
    t_now = int(str_t_now)
    string_fichero = datetime.strftime(now,'_%d_%m_%y_%H_%M_%S')
    if t_now == t_siguiente:
        sacar_foto(string_fichero)
        t_siguiente = t_siguiente + int(freq)
        if t_siguiente > 59: t_siguiente = t_siguiente - 60
        count += 1
    if count == total:
        break
