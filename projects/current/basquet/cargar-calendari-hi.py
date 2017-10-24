
import re

fhand = open('basquet/calendari17-18.txt','r')

i = 2
for line in fhand:
    if re.search('VILABASQUET V',line):
        words = line.split(maxsplit=2)
        equipos = words[2].split('-')
        data = '<'+words[0]+'-'+words[1]+'h>;'
        local = equipos[0]
        if re.search('VILABASQUET V',local): local = '@'+local
        visitante = equipos[1]
        if re.search('VILABASQUET V',visitante): visitante = '@'+visitante
        linea = '#basquet;'+str(i)+';N;'+data+' '+local+visitante
        i = i + 1
        fhand2 = open('mybrain.txt','a')
        fhand2.write(linea+'\n')
        fhand2.close()

    else:
        continue
