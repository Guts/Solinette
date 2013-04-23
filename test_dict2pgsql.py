import psycopg2
from collections import OrderedDict as OD


conn = psycopg2.connect(host='10.0.6.46',
        port='5432',
        dbname='solinette',
        user='postgres',
        password='pacivur')

curs = conn.cursor()

# http://wiki.postgresql.org/wiki/Psycopg2_Tutorial
#A last item I would like to show you is how to insert multiple rows using a dictionary. If you had the following:

cols = u'sol_idu char(55), gid numeric, direccion char(255), distrito char(255), idmunici numeric, ccdd numeric, ccpp numeric, ccdi numeric, dpto_nombr char(255), prov_nombr char(255), catmuni numeric, vfi numeric, p04 numeric, p11 char(255)'

valores = OD([(1, [u'1', 0.0, u'Av. Carlos Alberto Izaguirre N\xba 813', u'LOS OLIVOS', 19160.0, 15.0, 1.0, 17.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'FELIPE BALDOMERO CASTILLO ALFARO']), (2, [u'2', 22.0, u'Av. Riva Aguero N\xba 1358', u'EL AGUSTINO', 19156.0, 15.0, 1.0, 11.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'VICTOR MODESTO SALCEDO RIOS']), (3, [u'3', 8.0, u'Av. Joaqu\xedn Madrid N\xba 200', u'SAN BORJA', 19173.0, 15.0, 1.0, 30.0, u'LIMA', u'LIMA', 2.0, 1.0, 1.0, u'CARLOS ALBERTO TEJADA NORIEGA']), (4, [u'4', 18.0, u'Av. Petit Thouars 651-699, Parque de Reserva  Urb. Santa Beatriz ', u'Cercado de Lima', 19158.0, 15.0, 1.0, 14.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'Empresa Municipal Inmobiliaria de Lima (EMILIMA)  ']), (5, [u'5', 19.0, u'Pasaje Acu\xf1a 127, piso 4', u'Cercado de Lima', 19158.0, 15.0, 1.0, 14.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'Instituto Metropolitano Protransporte de Lima  '])])


nametup = ({"first_name":"Joshua", "last_name":"Drake"},
            {"first_name":"Steven", "last_name":"Foo"},
            {"first_name":"David", "last_name":"Bar"})

# SOL_IDU	gid	direccion	distrito	IDMUNICI	CCDD	CCPP	CCDI	DPTO_NOMBR	PROV_NOMBR	CATMUNI	VFI	P04	P11	fecha
curs.executemany('INSERT INTO myTable (key, value) VALUES (%s, %s)', mydictionary.items())


#You could easily insert all three rows within the dictionary by using:
curs.executemany("""INSERT INTO bar(first_name,last_name) VALUES (%(first_name)s, %(last_name)s)""", nametup)
