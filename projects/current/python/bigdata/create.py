
import sqlite3
#from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
from os import walk, path

def init_base_global():
    # Creamos las tablas necesarias
    conn = sqlite3.connect('global.sqlite3')
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

    # tabla alineacion
    cur.execute('''
                CREATE TABLE IF NOT EXISTS alineacion
                (MatchID INTEGER, RoleTeam INTEGER, RoleID INTEGER, PlayerID INTEGER,
                UNIQUE(MatchID, RoleTeam, RoleID))
                ''')

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

    # tabla jugadores
    cur.execute('''
                CREATE TABLE IF NOT EXISTS jugadores
                (PlayerID INTEGER PRIMARY KEY, Agreeability INTEGER, Aggressiveness INTEGER, Honesty INTEGER, Leadership INTEGER, Specialty INTEGER)
                ''')

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

# iniciamos lista de bases en la carpeta
for root, dirs, files in listaDir:
    for base in files:
        (nombreFichero, extension) = path.splitext(base)
        if (extension == '.sqlite'):
            listaBases.append(nombreFichero+extension)


# conn = sqlite3.connect('global.sqlite')
# cur = conn.cursor()
# conn.commit()
# cur.close()

conn = sqlite3.connect('global.sqlite3')
cur = conn.cursor()

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

print('Proceso terminado')
