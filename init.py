
from colorama import init, Fore, Back, Style
import sys

# Para que los colores se reinicien en cada ocasion
init(autoreset=True)

for word in sys.argv:
    print (word)
