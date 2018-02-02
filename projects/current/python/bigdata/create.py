
import sqlite3
#from datetime import datetime, timedelta
#from colorama import init, Fore, Back, Style
from os import walk, path

def init_base_global():
    # Creamos las tablas necesarias
    conn = sqlite3.connect('global.sqlite99')
    cur = conn.cursor()

    # tabla partidos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS partidos
                (MatchID INTEGER PRIMARY KEY, MatchType INTEGER, SourceSystem TEXT, MatchDate TEXT, HomeTeamID INTEGER,
                HomeGoals INTEGER, AwayTeamID INTEGER, AwayGoals INTEGER, TacticTypeHome INTEGER,
                TacticSkillHome INTEGER, TacticTypeAway INTEGER, TacticSkillAway INTEGER, expulsiones INTEGER,
                lesiones INTEGER, PossessionFirstHalfHome INTEGER,
                PossessionFirstHalfAway INTEGER, PossessionSecondHalfHome INTEGER, PossessionSecondHalfAway INTEGER,
                RatingIndirectSetPiecesDefHome INTEGER, RatingIndirectSetPiecesAttHome INTEGER, RatingIndirectSetPiecesDefAway INTEGER,
                RatingIndirectSetPiecesAttAway INTEGER)
                ''')

    # tabla eventos
    cur.execute('''
                CREATE TABLE IF NOT EXISTS eventos
                (MatchID INTEGER, IndexEv INTEGER, Minute INTEGER, EventTypeID INTEGER,
                SubjectTeamID INTEGER, SubjectPlayerID INTEGER, ObjectPlayerID INTEGER, SubPorteria INTEGER,
                SubDefensa INTEGER, SubJugadas INTEGER, SubLateral INTEGER, SubPases INTEGER,
                SubAnotacion INTEGER, SubBP INTEGER, SubXP INTEGER, SubForma INTEGER, SubResistencia INTEGER, SubSpecialty INTEGER, SubLoyalty INTEGER, SubMotherClubBonus TEXT, ObjPorteria INTEGER, ObjDefensa INTEGER,
                ObjJugadas INTEGER, ObjLateral INTEGER, ObjPases INTEGER,
                ObjAnotacion INTEGER, ObjXP INTEGER, ObjForma INTEGER, ObjResistencia INTEGER, ObjSpecialty INTEGER, ObjLoyalty INTEGER, ObjMotherClubBonus TEXT, ObjBP INTEGER,
                UNIQUE(MatchID, IndexEv))
                ''')
    try:
        cur.execute('''ALTER TABLE eventos ADD COLUMN SubAff INTEGER''')
        cur.execute('''ALTER TABLE eventos ADD COLUMN ObjAff INTEGER''')
    except:
        None

    # tabla alineacion
    cur.execute('''
                CREATE TABLE IF NOT EXISTS alineacion
                (MatchID INTEGER, RoleTeam INTEGER, RoleID INTEGER, PlayerID INTEGER,
                UNIQUE(MatchID, RoleTeam, RoleID))
                ''')
    try:
        cur.execute('''ALTER TABLE alineacion ADD COLUMN Behaviour INTEGER''')
    except:
        None

    # tabla tarjetas
    cur.execute('''
                CREATE TABLE IF NOT EXISTS tarjetas
                (MatchID INTEGER, IndexTarjeta INTEGER, PlayerID INTEGER, TeamID INTEGER, BookingType INTEGER, BookingMinute INTEGER,
                UNIQUE(MatchID, IndexTarjeta))
                ''')

    # tabla lesiones
    cur.execute('''
                CREATE TABLE IF NOT EXISTS lesiones
                (MatchID INTEGER, IndexInjury INTEGER, PlayerID INTEGER, TeamID INTEGER, InjuryType INTEGER, InjuryMinute INTEGER,
                UNIQUE(MatchID, IndexInjury))
                ''')

    # tabla sustituciones
    cur.execute('''
                CREATE TABLE IF NOT EXISTS sustituciones
                (MatchID INTEGER, TeamID INTEGER, SubjectPlayerID INTEGER, ObjectPlayerID INTEGER, NewPositionId INTEGER, MatchMinute INTEGER,
                UNIQUE(MatchID, TeamID, SubjectPlayerID))
                ''')
    try:
        cur.execute('''ALTER TABLE sustituciones ADD COLUMN NewPositionBehaviour INTEGER''')
    except:
        None


    # tabla jugadores
    cur.execute('''
                CREATE TABLE IF NOT EXISTS jugadores
                (PlayerID INTEGER PRIMARY KEY, Agreeability INTEGER, Aggressiveness INTEGER, Honesty INTEGER, Leadership INTEGER, Specialty INTEGER)
                ''')

    # tabla Porteros
    cur.execute('''
                CREATE TABLE IF NOT EXISTS porteros
                (MatchID INTEGER, PlayerID INTEGER, Porteria INTEGER,
                Defensa INTEGER, Jugadas INTEGER, Lateral INTEGER, Pases INTEGER, Anotacion INTEGER, BP INTEGER, XP INTEGER,
                Forma INTEGER, Resistencia INTEGER, Specialty INTEGER, Loyalty INTEGER, MotherClubBonus TEXT,
                UNIQUE(MatchID, PlayerID))
                ''')
    try:
        cur.execute('''ALTER TABLE porteros ADD COLUMN PlayerAff INTEGER''')
    except:
        None

    # tabla SE
    cur.execute('''
                CREATE TABLE IF NOT EXISTS SE
                (EventTypeID INTEGER PRIMARY KEY, EventName TEXT, TypeSEBD TEXT)
                ''')
    try:
        cur.execute('SELECT EventTypeID FROM SE WHERE EventTypeID = 19')
        test = cur.fetchone()[0]
    except:
        fhand = open('EventList.txt')
        for line in fhand:
            valores = line.split(';')
            if valores[2][:2] == 'SE':
                cur.execute('INSERT INTO SE (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2][:2]))
            else:
                cur.execute('INSERT INTO SE (EventTypeID, EventName, TypeSEBD) VALUES (?, ?, ?)',(valores[0], valores[1], valores[2]))

    # vista alineacion_all con minutos jugados de todos los jugadores incluidas las susticiones!
    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all as
                select a.MatchID, a.RoleTeam, a.RoleID as Pos, a.PlayerID as Player, b.Specialty,
                case when c.MatchMinute is null then 90 when c.MatchMinute > 90 then 90 else c.MatchMinute end as Minutos
                from alineacion as a
                left join jugadores as b ON a.PlayerID = b.PlayerID
                left join sustituciones as c ON a.MatchID = c.MatchID AND a.PlayerID = c.SubjectPlayerID
                UNION ALL
                select a.MatchID, a.RoleTeam, c.NewPositionId as Pos, c.ObjectPlayerID as Player, d.Specialty,
                case when c.MatchMinute is null then 0 when c.MatchMinute > 90 then 0 else 90-c.MatchMinute end as Minutos
                from alineacion as a
                left join jugadores as b ON a.PlayerID = b.PlayerID
                left join sustituciones as c ON a.MatchID = c.MatchID AND a.PlayerID = c.SubjectPlayerID
                left join jugadores as d ON c.ObjectPlayerID = d.PlayerID
                where Minutos > 0
                ''')

    # vista anterior con posiciones contrarias exactas en letras
    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all_contrarios as
                select * from ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos = 106 then "ED" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "EI" when Pos > 110 then "F" when Pos = 101 then "DLD" when Pos = 105 then "DLI" when Pos > 101 and Pos < 105 then "DC" end as PosLetras,
                case when Pos = 106 then "DLI" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "DLD" when Pos > 110 then "DC" when Pos = 101 then "EI" when Pos = 105 then "ED" when Pos > 101 and Pos < 105 then "F" end as PosConLetras
                from alineacion_all) as a
                left join ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos = 106 then "ED" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "EI" when Pos > 110 then "F" when Pos = 101 then "DLD" when Pos = 105 then "DLI" when Pos > 101 and Pos < 105 then "DC" end as PosLetras,
                case when Pos = 106 then "DLI" when Pos > 106 and Pos < 110 then "Inner" when Pos = 110 then "DLD" when Pos > 110 then "DC" when Pos = 101 then "EI" when Pos = 105 then "ED" when Pos > 101 and Pos < 105 then "F" end as PosConLetras
                from alineacion_all) as b ON a.MatchID = b.MatchID and a.RoleContrario = b.RoleTeam and a.PosConLetras = b.PosLetras
                ''')

    cur.execute('''
                CREATE VIEW IF NOT EXISTS alineacion_all_contrarios_tec_cab as
                select * from ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos > 105 then "E_I_F" else "no" end as PosLetras,
                case when Pos > 100 and Pos < 110 and Pos <> 106 then "D_I" else "no" end as PosConLetras
                from alineacion_all) as a
                left join ( select *, case	when RoleTeam = 1 then 2 when RoleTeam = 2 then 1 end as RoleContrario,
                case when Pos > 105 then "E_I_F" else "no" end as PosLetras,
                case when Pos > 100 and Pos < 110 and Pos <> 106 then "D_I" else "no" end as PosConLetras
                from alineacion_all) as b ON a.MatchID = b.MatchID and a.RoleContrario = b.RoleTeam and a.PosConLetras = b.PosLetras
                ''')

    conn.commit()
    cur.close()


#Creamos la base global que nos servira de base
init_base_global()

listaDir = []
listaBases = []

listaDir = walk('.')

# iniciamos lista de bases en la carpeta de la version 0.x.x
for root, dirs, files in listaDir:
    for base in files:
        (nombreFichero, extension) = path.splitext(base)
        if (extension == '.sqlite'):
            listaBases.append(nombreFichero+extension)


conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

print(listaBases)

for base in listaBases:
    conn2 = sqlite3.connect(base)
    cur2 = conn2.cursor()

    #Introducimos tabla alineacion
    ListaMatchID = []
    cur.execute('SELECT DISTINCT MatchID FROM alineacion')
    for row in cur:
        ListaMatchID.append(row[0])

    cur2.execute('SELECT * FROM alineacion')
    for row in cur2:
        if row[0] in ListaMatchID:
            None
        else:
            cur.execute('INSERT INTO alineacion (MatchID, RoleTeam, RoleID, PlayerID) VALUES (?, ?, ?, ?)',(row[0],row[1],row[2],row[3]))

    #Introducimos tabla jugadores
    ListaPlayerID = []
    cur.execute('SELECT DISTINCT PlayerID FROM jugadores')
    for row in cur:
        ListaPlayerID.append(row[0])

    cur2.execute('SELECT * FROM jugadores')
    for row in cur2:
        if row[0] in ListaPlayerID:
            None
        else:
            cur.execute('INSERT INTO jugadores (PlayerID, Agreeability, Aggressiveness, Honesty, Leadership, Specialty) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla lesiones
    ListaLesiones = []
    cur.execute('SELECT DISTINCT MatchID,IndexInjury FROM lesiones')
    for row in cur:
        ListaLesiones.append(str(row[0])+str(row[1]))

    cur2.execute('SELECT * FROM lesiones')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaLesiones:
            None
        else:
            cur.execute('INSERT INTO lesiones (MatchID, IndexInjury, PlayerID, TeamID, InjuryType, InjuryMinute) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla partidos
    ListaMatchID2 = []
    cur.execute('SELECT DISTINCT MatchID FROM partidos')
    for row in cur:
        ListaMatchID2.append(row[0])

    cur2.execute('SELECT * FROM partidos')
    for row in cur2:
        if row[0] in ListaMatchID2:
            None
        else:
            cur.execute('INSERT INTO partidos (MatchID, MatchType, SourceSystem, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals, TacticTypeHome, TacticSkillHome, TacticTypeAway, TacticSkillAway, expulsiones, lesiones, PossessionFirstHalfHome, PossessionFirstHalfAway, PossessionSecondHalfHome, PossessionSecondHalfAway, RatingIndirectSetPiecesDefHome, RatingIndirectSetPiecesAttHome, RatingIndirectSetPiecesDefAway, RatingIndirectSetPiecesAttAway) VALUES (?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21]))

    #Introducimos tabla sustituciones
    ListaSus = []
    cur.execute('SELECT DISTINCT MatchID,TeamID,SubjectPlayerID FROM sustituciones')
    for row in cur:
        ListaSus.append(str(row[0])+str(row[1])+str(row[2]))

    cur2.execute('SELECT * FROM sustituciones')
    for row in cur2:
        if str(row[0])+str(row[1])+str(row[2]) in ListaSus:
            None
        else:
            cur.execute('INSERT INTO sustituciones (MatchID, TeamID, SubjectPlayerID, ObjectPlayerID, NewPositionId, MatchMinute) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla tarjetas
    ListaTarjetas = []
    cur.execute('SELECT DISTINCT MatchID,IndexTarjeta FROM tarjetas')
    for row in cur:
        ListaTarjetas.append(str(row[0])+str(row[1]))

    cur2.execute('SELECT * FROM tarjetas')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaTarjetas:
            None
        else:
            cur.execute('INSERT INTO tarjetas (MatchID, IndexTarjeta, PlayerID, TeamID, BookingType, BookingMinute) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla eventos
    ListaEventos = []
    cur.execute('SELECT DISTINCT MatchID,IndexEv FROM eventos')
    for row in cur:
        ListaEventos.append(str(row[0])+str(row[1]))
    cur2.execute('SELECT * FROM eventos')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaEventos:
            None
        else:
            cur.execute('INSERT INTO eventos (MatchID, IndexEv, Minute, EventTypeID, SubjectTeamID, SubjectPlayerID, ObjectPlayerID, SubPorteria, SubDefensa, SubJugadas, SubLateral, SubPases, SubAnotacion, SubBP, SubXP, SubForma, SubResistencia, SubSpecialty, SubLoyalty, SubMotherClubBonus, ObjPorteria, ObjDefensa, ObjJugadas, ObjLateral, ObjPases, ObjAnotacion, ObjXP, ObjForma, ObjResistencia, ObjSpecialty, ObjLoyalty, ObjMotherClubBonus, ObjBP) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32]))

    #Introducimos tabla eventosSub
    ListaEventosSub = []
    cur2.execute('SELECT DISTINCT MatchID,IndexEv,SubPorteria FROM eventos')
    for row in cur2:
        if row[2] != None and row[2] != -1:
            ListaEventosSub.append(str(row[0])+str(row[1])+str(row[2]))

    cur.execute('SELECT * FROM eventos')
    for row in cur:
        if str(row[0])+str(row[1])+str(row[7]) in ListaEventosSub:
            cur2.execute('SELECT * FROM eventos WHERE MatchID=? and IndexEv=? LIMIT 1',(row[0], row[1]))
            Hab = cur2.fetchone()
            SubPor=Hab[7]
            SubDef=Hab[8]
            SubJug=Hab[9]
            SubLat=Hab[10]
            SubPas=Hab[11]
            SubAno=Hab[12]
            SubBP=Hab[13]
            SubXP=Hab[14]
            SubFor=Hab[15]
            SubRes=Hab[16]
            SubSpe=Hab[17]
            SubLoy=Hab[18]
            SubMot=Hab[19]
            cur.execute('UPDATE eventos SET SubPorteria=?, SubDefensa=?, SubJugadas=?, SubLateral=?, SubPases=?, SubAnotacion=?, SubBP=?, SubXP=?, SubForma=?, SubResistencia=?, SubSpecialty=?, SubLoyalty=?, SubMotherClubBonus=? WHERE MatchID=? and IndexEv=?',(SubPor,SubDef,SubJug,SubLat,SubPas,SubAno,SubBP,SubXP,SubFor,SubRes,SubSpe,SubLoy,SubMot,row[0],row[1]))
        else:
            None

    #Introducimos tabla eventosObj
    ListaEventosObj = []
    cur2.execute('SELECT DISTINCT MatchID,IndexEv,ObjPorteria FROM eventos')
    for row in cur2:
        if row[2] != None and row[2] != -1:
            ListaEventosObj.append(str(row[0])+str(row[1])+str(row[2]))

    cur.execute('SELECT * FROM eventos')
    for row in cur:
        if str(row[0])+str(row[1])+str(row[7]) in ListaEventosObj:
            cur2.execute('SELECT * FROM eventos WHERE MatchID=? and IndexEv=? LIMIT 1',(row[0], row[1]))
            Hab = cur2.fetchone()
            ObjPor= Hab[20]
            ObjDef=Hab[21]
            ObjJug=Hab[22]
            ObjLat=Hab[23]
            ObjPas=Hab[24]
            ObjAno=Hab[25]
            ObjXP=Hab[26]
            ObjFor=Hab[27]
            ObjRes=Hab[28]
            ObjSpe=Hab[29]
            ObjLoy=Hab[30]
            ObjMot=Hab[31]
            ObjBP=Hab[32]
            cur.execute('UPDATE eventos SET ObjPorteria=?, ObjDefensa=?, ObjJugadas=?, ObjLateral=?, ObjPases=?, ObjAnotacion=?, ObjXP=?, ObjForma=?, ObjResistencia=?, ObjSpecialty=?, ObjLoyalty=?, ObjMotherClubBonus=?, ObjBP=? WHERE MatchID=? and IndexEv=?',(ObjPor,ObjDef,ObjJug,ObjLat,ObjPas,ObjAno,ObjXP,ObjFor,ObjRes,ObjSpe,ObjLoy,ObjMot,ObjBP, row[0], row[1]))
        else:
            None

    conn2.commit()
    cur2.close()

    print('La base de datos:'+base+' ha sido añadida')

conn.commit()
cur.close()

print('Proceso terminado para las bases v.0.x.x\n')


# iniciamos lista de bases en la carpeta de la version 1.x.x
listaDir3 = []
listaDir3 = walk('.')
listaBases3 = []

for root, dirs, files in listaDir3:
    for base in files:
        (nombreFichero, extension) = path.splitext(base)
        if (extension == '.sqlite3'):
            listaBases3.append(nombreFichero+extension)


conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

print(listaBases3)

for base in listaBases3:
    conn2 = sqlite3.connect(base)
    cur2 = conn2.cursor()

    #Introducimos tabla alineacion
    ListaMatchID = []
    cur.execute('SELECT DISTINCT MatchID FROM alineacion')
    for row in cur:
        ListaMatchID.append(row[0])

    cur2.execute('SELECT * FROM alineacion')
    for row in cur2:
        if row[0] in ListaMatchID:
            None
        else:
            cur.execute('INSERT INTO alineacion (MatchID, RoleTeam, RoleID, PlayerID, Behaviour) VALUES (?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4]))

    #Introducimos tabla jugadores
    ListaPlayerID = []
    cur.execute('SELECT DISTINCT PlayerID FROM jugadores')
    for row in cur:
        ListaPlayerID.append(row[0])

    cur2.execute('SELECT * FROM jugadores')
    for row in cur2:
        if row[0] in ListaPlayerID:
            None
        else:
            cur.execute('INSERT INTO jugadores (PlayerID, Agreeability, Aggressiveness, Honesty, Leadership, Specialty) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla lesiones
    ListaLesiones = []
    cur.execute('SELECT DISTINCT MatchID,IndexInjury FROM lesiones')
    for row in cur:
        ListaLesiones.append(str(row[0])+str(row[1]))

    cur2.execute('SELECT * FROM lesiones')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaLesiones:
            None
        else:
            cur.execute('INSERT INTO lesiones (MatchID, IndexInjury, PlayerID, TeamID, InjuryType, InjuryMinute) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla partidos
    ListaMatchID2 = []
    cur.execute('SELECT DISTINCT MatchID FROM partidos')
    for row in cur:
        ListaMatchID2.append(row[0])

    cur2.execute('SELECT * FROM partidos')
    for row in cur2:
        if row[0] in ListaMatchID2:
            None
        else:
            cur.execute('INSERT INTO partidos (MatchID, MatchType, SourceSystem, MatchDate, HomeTeamID, HomeGoals, AwayTeamID, AwayGoals, TacticTypeHome, TacticSkillHome, TacticTypeAway, TacticSkillAway, expulsiones, lesiones, PossessionFirstHalfHome, PossessionFirstHalfAway, PossessionSecondHalfHome, PossessionSecondHalfAway, RatingIndirectSetPiecesDefHome, RatingIndirectSetPiecesAttHome, RatingIndirectSetPiecesDefAway, RatingIndirectSetPiecesAttAway) VALUES (?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21]))

    #Introducimos tabla sustituciones
    ListaSus = []
    cur.execute('SELECT DISTINCT MatchID,TeamID,SubjectPlayerID FROM sustituciones')
    for row in cur:
        ListaSus.append(str(row[0])+str(row[1])+str(row[2]))

    cur2.execute('SELECT * FROM sustituciones')
    for row in cur2:
        if str(row[0])+str(row[1])+str(row[2]) in ListaSus:
            None
        else:
            cur.execute('INSERT INTO sustituciones (MatchID, TeamID, SubjectPlayerID, ObjectPlayerID, NewPositionId, MatchMinute, NewPositionBehaviour) VALUES (?, ?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5], row[6]))

    #Introducimos tabla tarjetas
    ListaTarjetas = []
    cur.execute('SELECT DISTINCT MatchID,IndexTarjeta FROM tarjetas')
    for row in cur:
        ListaTarjetas.append(str(row[0])+str(row[1]))

    cur2.execute('SELECT * FROM tarjetas')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaTarjetas:
            None
        else:
            cur.execute('INSERT INTO tarjetas (MatchID, IndexTarjeta, PlayerID, TeamID, BookingType, BookingMinute) VALUES (?, ?, ?, ?, ?, ?)',(row[0],row[1],row[2],row[3],row[4], row[5]))

    #Introducimos tabla eventos
    ListaEventos = []
    cur.execute('SELECT DISTINCT MatchID,IndexEv FROM eventos')
    for row in cur:
        ListaEventos.append(str(row[0])+str(row[1]))
    cur2.execute('SELECT * FROM eventos')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaEventos:
            None
        else:
            cur.execute('INSERT INTO eventos (MatchID, IndexEv, Minute, EventTypeID, SubjectTeamID, SubjectPlayerID, ObjectPlayerID, SubPorteria, SubDefensa, SubJugadas, SubLateral, SubPases, SubAnotacion, SubBP, SubXP, SubForma, SubResistencia, SubSpecialty, SubLoyalty, SubMotherClubBonus, ObjPorteria, ObjDefensa, ObjJugadas, ObjLateral, ObjPases, ObjAnotacion, ObjXP, ObjForma, ObjResistencia, ObjSpecialty, ObjLoyalty, ObjMotherClubBonus, ObjBP) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32]))

    #Introducimos tabla eventosSub
    ListaEventosSub = []
    cur2.execute('SELECT DISTINCT MatchID,IndexEv,SubPorteria FROM eventos')
    for row in cur2:
        if row[2] != None and row[2] != -99:
            ListaEventosSub.append(str(row[0])+str(row[1])+str(row[2]))

    cur.execute('SELECT * FROM eventos')
    for row in cur:
        if str(row[0])+str(row[1])+str(row[7]) in ListaEventosSub:
            cur2.execute('SELECT * FROM eventos WHERE MatchID=? and IndexEv=? LIMIT 1',(row[0], row[1]))
            Hab = cur2.fetchone()
            SubPor=Hab[7]
            SubDef=Hab[8]
            SubJug=Hab[9]
            SubLat=Hab[10]
            SubPas=Hab[11]
            SubAno=Hab[12]
            SubBP=Hab[13]
            SubXP=Hab[14]
            SubFor=Hab[15]
            SubRes=Hab[16]
            SubSpe=Hab[17]
            SubLoy=Hab[18]
            SubMot=Hab[19]
            cur.execute('UPDATE eventos SET SubPorteria=?, SubDefensa=?, SubJugadas=?, SubLateral=?, SubPases=?, SubAnotacion=?, SubBP=?, SubXP=?, SubForma=?, SubResistencia=?, SubSpecialty=?, SubLoyalty=?, SubMotherClubBonus=? WHERE MatchID=? and IndexEv=?',(SubPor,SubDef,SubJug,SubLat,SubPas,SubAno,SubBP,SubXP,SubFor,SubRes,SubSpe,SubLoy,SubMot,row[0],row[1]))
        else:
            None

    #Introducimos tabla eventosObj
    ListaEventosObj = []
    cur2.execute('SELECT DISTINCT MatchID,IndexEv,ObjPorteria FROM eventos')
    for row in cur2:
        if row[2] != None and row[2] != -99:
            ListaEventosObj.append(str(row[0])+str(row[1])+str(row[2]))

    cur.execute('SELECT * FROM eventos')
    for row in cur:
        if str(row[0])+str(row[1])+str(row[7]) in ListaEventosObj:
            cur2.execute('SELECT * FROM eventos WHERE MatchID=? and IndexEv=? LIMIT 1',(row[0], row[1]))
            Hab = cur2.fetchone()
            ObjPor= Hab[20]
            ObjDef=Hab[21]
            ObjJug=Hab[22]
            ObjLat=Hab[23]
            ObjPas=Hab[24]
            ObjAno=Hab[25]
            ObjXP=Hab[26]
            ObjFor=Hab[27]
            ObjRes=Hab[28]
            ObjSpe=Hab[29]
            ObjLoy=Hab[30]
            ObjMot=Hab[31]
            ObjBP=Hab[32]
            cur.execute('UPDATE eventos SET ObjPorteria=?, ObjDefensa=?, ObjJugadas=?, ObjLateral=?, ObjPases=?, ObjAnotacion=?, ObjXP=?, ObjForma=?, ObjResistencia=?, ObjSpecialty=?, ObjLoyalty=?, ObjMotherClubBonus=?, ObjBP=? WHERE MatchID=? and IndexEv=?',(ObjPor,ObjDef,ObjJug,ObjLat,ObjPas,ObjAno,ObjXP,ObjFor,ObjRes,ObjSpe,ObjLoy,ObjMot,ObjBP, row[0], row[1]))
        else:
            None

    #Introducimos tabla porteros
    ListaPorteros = []
    cur.execute('SELECT DISTINCT MatchID,PlayerID FROM porteros')
    for row in cur:
        ListaPorteros.append(str(row[0])+str(row[1]))
    cur2.execute('SELECT * FROM porteros')
    for row in cur2:
        if str(row[0])+str(row[1]) in ListaPorteros:
            None
        else:
            cur.execute('INSERT INTO porteros (MatchID, PlayerID, Porteria, Defensa, Jugadas, Lateral, Pases, Anotacion, BP, XP, Forma, Resistencia, Specialty, Loyalty, MotherClubBonus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))

    #Introducimos tabla porteros_ok
    ListaPorterosOK = []
    cur2.execute('SELECT DISTINCT MatchID,PlayerID,Porteria FROM porteros')
    for row in cur2:
        if row[2] != None and row[2] != -99:
            ListaPorterosOK.append(str(row[0])+str(row[1])+str(row[2]))

    cur.execute('SELECT * FROM porteros')
    for row in cur:
        if str(row[0])+str(row[1])+str(row[2]) in ListaPorterosOK:
            cur2.execute('SELECT * FROM porteros WHERE MatchID=? and PlayerID=? LIMIT 1',(row[0], row[1]))
            Hab = cur2.fetchone()
            SubPor=Hab[2]
            SubDef=Hab[3]
            SubJug=Hab[4]
            SubLat=Hab[5]
            SubPas=Hab[6]
            SubAno=Hab[7]
            SubBP=Hab[8]
            SubXP=Hab[9]
            SubFor=Hab[10]
            SubRes=Hab[11]
            SubSpe=Hab[12]
            SubLoy=Hab[13]
            SubMot=Hab[14]
            cur.execute('UPDATE porteros SET Porteria=?, Defensa=?, Jugadas=?, Lateral=?, Pases=?, Anotacion=?, BP=?, XP=?, Forma=?, Resistencia=?, Specialty=?, Loyalty=?, MotherClubBonus=? WHERE MatchID=? and PlayerID=?',(SubPor,SubDef,SubJug,SubLat,SubPas,SubAno,SubBP,SubXP,SubFor,SubRes,SubSpe,SubLoy,SubMot,row[0],row[1]))
        else:
            None

    conn2.commit()
    cur2.close()

    print('La base de datos:'+base+' ha sido añadida')

conn.commit()
cur.close()

print('Proceso terminado para las bases v.1.x.x\n')


#Vamos a limpiar la base global de partidos sin datos
conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('DELETE FROM partidos WHERE TacticTypeHome is null')
print('Eliminados los partidos sin datos de la tabla partidos')

conn.commit()
cur.close()

#Vamos a limpiar la base global de partidos los partidos con WO
conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('DELETE FROM alineacion WHERE matchID IN (select MatchId from partidos_wo)')
print('Eliminados los partidos WO de la tabla de alineacion')

conn.commit()
cur.close()

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('DELETE FROM partidos WHERE matchID IN (select MatchId from partidos_wo)')
print('Eliminados los partidos WO de la tabla de partidos')

conn.commit()
cur.close()

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('DELETE FROM eventos WHERE matchID IN (select MatchId from partidos_wo)')
print('Eliminados los partidos WO de la tabla de eventos')

conn.commit()
cur.close()

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('UPDATE eventos SET SubSpecialty=(SELECT Specialty FROM jugadores WHERE PlayerID=eventos.SubjectPlayerID) WHERE SubSpecialty=-99 or SubSpecialty is null')
print('Actualizadas las especialidadas con -99')

conn.commit()
cur.close()

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('UPDATE porteros SET Specialty=(SELECT Specialty FROM jugadores WHERE PlayerID=porteros.PlayerID) WHERE Specialty=-99 or Specialty is null')
print('Actualizadas las especialidadas con -99 de porteros')

conn.commit()
cur.close()

# conn = sqlite3.connect('global.sqlite3')
# cur = conn.cursor()
#
# cur.execute('DROP TABLE partidos_ptotal_sobre_all')
# cur.execute('CREATE TABLE partidos_ptotal_sobre_all AS SELECT matchID, ev05,ev06,ev08,ev09,ev15,ev16,ev19,ev25,ev37,ev38,ev39,cast(pTOTAL as real) as ptotal_sobre FROM partidos_plus_pbase_ptotal')
# cur.execute('DROP TABLE  partidos_ptotal_sobre')
# cur.execute('CREATE TABLE partidos_ptotal_sobre as select a.matchID, ev05,ev06,ev08,ev09,ev15,ev16,ev19,ev25,ev37,ev38,ev39,ptotal_sobre from partidos_ptotal_sobre_all as a inner join partidos as b ON a.matchID=b.matchid where b.TacticTypeHome<>7 and b.TacticTypeAway<>7')
#
# print('Reconstruida la tabla de pbase sobredimensionadas')
#
# conn.commit()
# cur.close()

conn = sqlite3.connect('global.sqlite99')
cur = conn.cursor()

cur.execute('''drop table players_hab''')
cur.execute('''create table players_hab as select * from players_ok''')
cur.execute('''update eventos
set SubPorteria=(select POR from players_hab where player=eventos.SubjectPlayerID)
where SubPorteria=-99 or SubPorteria is null''')
cur.execute('''update eventos
set SubDefensa=(select DEF from players_hab where player=eventos.SubjectPlayerID)
where SubDefensa=-99 or SubDefensa=-99''')
cur.execute('''update eventos
set SubJugadas=(select JUG from players_hab where player=eventos.SubjectPlayerID)
where SubJugadas=-99 or SubJugadas is null''')
cur.execute('''update eventos
set SubLateral=(select LAT from players_hab where player=eventos.SubjectPlayerID)
where SubLateral=-99 or SubLateral is null''')
cur.execute('''update eventos
set SubPases=(select PAS from players_hab where player=eventos.SubjectPlayerID)
where SubPases=-99 or SubPases is null''')
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
