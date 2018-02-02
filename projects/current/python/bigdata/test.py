import sqlite3

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('''update eventos
set SubAnotacion=(select ANO from players_hab where player=eventos.SubjectPlayerID)
where SubAnotacion=-99 or SubAnotacion is null''')
cur.execute('''update eventos
set SubBP=(select BP from players_hab where player=eventos.SubjectPlayerID)
where SubBP=-99 or SubBP is null''')
cur.execute('''update eventos
set SubXP=(select XP from players_hab where player=eventos.SubjectPlayerID)
where SubXP=-99 or SubXP is null''')
cur.execute('''update eventos
set SubForma=(select FOR from players_hab where player=eventos.SubjectPlayerID)
where SubForma=-99 or SubForma is null''')
cur.execute('''update eventos
set SubResistencia=(select RES from players_hab where player=eventos.SubjectPlayerID)
where SubResistencia=-99 or SubResistencia is null''')
cur.execute('''update eventos
set SubLoyalty=(select FID from players_hab where player=eventos.SubjectPlayerID)
where SubLoyalty=-99 or SubLoyalty is null''')
cur.execute('''update eventos
set SubMotherClubBonus=(select MCB from players_hab where player=eventos.SubjectPlayerID)
where SubMotherClubBonus='false' or SubMotherClubBonus is null ''')

print('Revisadas las habilidades de los Subject')

cur.execute('''update eventos
set ObjPorteria=(select POR from players_hab where player=eventos.ObjectPlayerID)
where ObjPorteria=-99 or ObjPorteria is null''')
cur.execute('''update eventos
set ObjDefensa=(select DEF from players_hab where player=eventos.ObjectPlayerID)
where ObjDefensa=-99 or ObjDefensa is null''')
cur.execute('''update eventos
set ObjJugadas=(select JUG from players_hab where player=eventos.ObjectPlayerID)
where ObjJugadas=-99 or ObjJugadas is null''')
cur.execute('''update eventos
set ObjLateral=(select LAT from players_hab where player=eventos.ObjectPlayerID)
where ObjLateral=-99 or ObjLateral is null''')
cur.execute('''update eventos
set ObjPases=(select PAS from players_hab where player=eventos.ObjectPlayerID)
where ObjPases=-99 or ObjPases is null''')
cur.execute('''update eventos
set ObjAnotacion=(select ANO from players_hab where player=eventos.ObjectPlayerID)
where ObjAnotacion=-99 or ObjAnotacion is null''')
cur.execute('''update eventos
set ObjBP=(select BP from players_hab where player=eventos.ObjectPlayerID)
where ObjBP=-99 or ObjBP is null''')
cur.execute('''update eventos
set ObjXP=(select XP from players_hab where player=eventos.ObjectPlayerID)
where ObjXP=-99 or ObjXP is null''')
cur.execute('''update eventos
set ObjForma=(select FOR from players_hab where player=eventos.ObjectPlayerID)
where ObjForma=-99 or ObjForma is null''')
cur.execute('''update eventos
set ObjResistencia=(select RES from players_hab where player=eventos.ObjectPlayerID)
where ObjResistencia=-99 or ObjResistencia is null''')
cur.execute('''update eventos
set ObjLoyalty=(select FID from players_hab where player=eventos.ObjectPlayerID)
where ObjLoyalty=-99 or ObjLoyalty is null''')
cur.execute('''update eventos
set ObjMotherClubBonus=(select MCB from players_hab where player=eventos.ObjectPlayerID)
where ObjMotherClubBonus='false' or ObjMotherClubBonus is null''')

print('Revisadas las habilidades de los Object')

conn.commit()
cur.close()


conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('''DROP TABLE porteros_hab''')
cur.execute('''CREATE TABLE porteros_hab as select * from porteros_ok''')
cur.execute('''update porteros
set Porteria=(select POR from porteros_hab where player=porteros.PlayerID)
where Porteria=-99 or Porteria is null''')
cur.execute('''update porteros
set Defensa=(select DEF from porteros_hab where player=porteros.PlayerID)
where Defensa=-99 or Defensa is null''')
cur.execute('''update porteros
set Jugadas=(select JUG from porteros_hab where player=porteros.PlayerID)
where Jugadas=-99 or Jugadas is null''')
cur.execute('''update porteros
set Lateral=(select LAT from porteros_hab where player=porteros.PlayerID)
where Lateral=-99 or Lateral is null''')
cur.execute('''update porteros
set Pases=(select PAS from porteros_hab where player=porteros.PlayerID)
where Pases=-99 or Pases is null''')
cur.execute('''update porteros
set Anotacion=(select ANO from porteros_hab where player=porteros.PlayerID)
where Anotacion=-99 or Anotacion is null''')
cur.execute('''update porteros
set BP=(select BP from porteros_hab where player=porteros.PlayerID)
where BP=-99 or BP is null''')
cur.execute('''update porteros
set XP=(select XP from porteros_hab where player=porteros.PlayerID)
where XP=-99 or XP is null''')
cur.execute('''update porteros
set Forma=(select FOR from porteros_hab where player=porteros.PlayerID)
where Forma=-99 or Forma is null''')
cur.execute('''update porteros
set Resistencia=(select RES from porteros_hab where player=porteros.PlayerID)
where Resistencia=-99 or Resistencia is null''')
cur.execute('''update porteros
set Loyalty=(select FID from porteros_hab where player=porteros.PlayerID)
where Loyalty=-99 or Loyalty is null''')
cur.execute('''update porteros
set MotherClubBonus=(select MCB from porteros_hab where player=porteros.PlayerID)
where MotherClubBonus='false' or MotherClubBonus is null ''')

print('Revisadas las habilidades de los porteros')

conn.commit()
cur.close()
