﻿# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals

### imports
import psycopg2
from collections import OrderedDict as OD

import xlrd
import datetime

### functions definition

def xls2dict(xlspath):
    u""" export values from ab Excel 2003 file (.xls) into a dictionary """
    global dico_vals, values
    with xlrd.open_workbook(xlspath) as book:
        print book.encoding
        sh = book.sheet_by_index(0)
        for row in range(1, sh.nrows):
            dico_vals[row] = []
            for col in range(sh.ncols):
                if sh.cell_type(row, col) is 1:
                    dico_vals[row].append(unicode(sh.cell_value(row, col)))
                elif sh.cell_type(row, col) is 2:
                    dico_vals[row].append(unicode(sh.cell_value(row, col)))
                elif sh.cell_type(row, col) is 3:
                    date = xlrd.xldate_as_tuple(sh.cell_value(row, col), book.datemode)
                    dico_vals[row].append(unicode('-'.join([unicode(i) for i in date[:3]])))
                elif sh.cell_type(row, col) is 4:
                    dico_vals[row].append(unicode(int(sh.cell_value(row, col))))
                elif sh.cell_type(row, col) is 0:
                    dico_vals[row].append(unicode('NULL'))
    # End of function
    return book, dico_vals

### variables
# basic operators
conn = psycopg2.connect(host='localhost',
        port='5432',
        dbname='solinette',
        user='postgres',
        password='pacivur')

curs = conn.cursor()

# columns definition
cols_u = u'sol_idu char(255), gid numeric, direccion char(255), distrito char(255), idmunici numeric, ccdd numeric, ccpp numeric, ccdi numeric, dpto_nombr char(255), prov_nombr char(255), catmuni numeric, vfi numeric, p04 numeric, p11 char(255), '
##cols_s = 'sol_idu char(255), gid numeric, direccion char(255), distrito char(255), idmunici numeric, ccdd numeric, ccpp numeric, ccdi numeric, dpto_nombr char(255), prov_nombr char(255), catmuni numeric, vfi numeric, p04 numeric, p11 char(255), '

# path to excel file for test
##xlspath = r'temp\ParaSolinette_municipalidades_multi.xls'
xlspath = r'temp\ParaSolinette_agencias_scotiabank_lima_callao.xls'

# data dictionary / list
dico_vals = {}
values = []

### main program
# check existing databases
curs.execute("""SELECT datname from pg_database""")
print curs.fetchall()

# check if destination table already exists
query = "select %s from information_schema.tables where 'sql_identifier' LIKE 'public';"
curs.execute(query, (u'test',))
li_tables = curs.fetchone()

# setting the encoding
##set_s = "set client_encoding to 'LATIN1';"
set_u = u"set client_encoding to 'UTF8';"
curs.execute(set_u)

# setting memmory use
work_mem = 2048
curs.execute('SET work_mem TO %s', (work_mem,))

# creating a test table
try:
    test_u = u'test'
    ##test_s = 'test'
    curs.execute(u"CREATE TABLE test (" + cols_u[:-2] + ");")
except Exception, e:
    print e.pgerror
    pass

# saving changes to database
conn.commit()

# data test
coldef = (u'SOL_IDU', u'gid', u'direccion', u'distrito', u'IDMUNICI', u'CCDD', u'CCPP', u'CCDI', u'DPTO_NOMBR', u'PROV_NOMBR',u'CATMUNI',u'VFI', u'P04', u'P11')
data_u = (u'001', u'0', u'Av. Carlos Alberto Izaguirre N°813', u'LOS OLIVOS', u'19160', u'15', u'1', u'17', u'LIMA', u'LIMA', u'2', u'1', u'0', u'FELIPE BALDOMERO CASTILLO ALFARO')
##data_s = ('001', '0', 'Av. Carlos Alberto Izaguirre N°813', 'LOS OLIVOS', '19160', '15', '1', '17', 'LIMA', 'LIMA', '2', '1', '0', 'FELIPE BALDOMERO CASTILLO ALFARO')

## inserting  simple data
### method 1
##curs.execute("INSERT INTO test VALUES %s", (data_u,)) # correct

# method 2: best practice (no quotes, no modulo)
c_insert = u"INSERT INTO test VALUES %s;" # Note: no quotes
curs.execute(c_insert, (data_u,)) # Note: no % operator

### method 3
##c_insert = u"INSERT INTO %s VALUES %s;" # Note: no quotes
##curs.execute(c_insert, (test_u, data_u)) # Note: no % operator

# saving changes to database
conn.commit()


## inserting multiple data
# retrieving data from xls file
xls2dict(xlspath)
# tuplization
valores = tuple(tuple(dico_vals.get(i)) for i in dico_vals.keys())


for i in valores:
    for j in i:
        print j, type(j)


try:
    curs.executemany(u"INSERT INTO test (" + cols_u[:-2] + ") VALUES %s;", valores)
except Exception, e:
    print e, u' => executemany does"nt work: just execute first value to test'
##    curs.execute(u"INSERT INTO test VALUES %s", (valores[0],))
    for val in range(len(valores)):
        curs.execute(u"INSERT INTO test VALUES %s", (valores[val],))
        conn.commit()













### Ending program
conn.commit()
curs.close()

























################################################################################
###################### former codlines and documentation


## => http://wiki.postgresql.org/wiki/Psycopg2_Tutorial


###A last item I would like to show you is how to insert multiple rows using a dictionary. If you had the following:
##
##
##
##valores = OD([(1, [u'1', 0.0, u'Av. Carlos Alberto Izaguirre N\xba 813', u'LOS OLIVOS', 19160.0, 15.0, 1.0, 17.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'FELIPE BALDOMERO CASTILLO ALFARO']), (2, [u'2', 22.0, u'Av. Riva Aguero N\xba 1358', u'EL AGUSTINO', 19156.0, 15.0, 1.0, 11.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'VICTOR MODESTO SALCEDO RIOS']), (3, [u'3', 8.0, u'Av. Joaqu\xedn Madrid N\xba 200', u'SAN BORJA', 19173.0, 15.0, 1.0, 30.0, u'LIMA', u'LIMA', 2.0, 1.0, 1.0, u'CARLOS ALBERTO TEJADA NORIEGA']), (4, [u'4', 18.0, u'Av. Petit Thouars 651-699, Parque de Reserva  Urb. Santa Beatriz ', u'Cercado de Lima', 19158.0, 15.0, 1.0, 14.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'Empresa Municipal Inmobiliaria de Lima (EMILIMA)  ']), (5, [u'5', 19.0, u'Pasaje Acu\xf1a 127, piso 4', u'Cercado de Lima', 19158.0, 15.0, 1.0, 14.0, u'LIMA', u'LIMA', 2.0, 1.0, 0.0, u'Instituto Metropolitano Protransporte de Lima  '])])
##
##
##nametup = ({"first_name":"Joshua", "last_name":"Drake"},
##            {"first_name":"Steven", "last_name":"Foo"},
##            {"first_name":"David", "last_name":"Bar"})

### SOL_IDU	gid	direccion	distrito	IDMUNICI	CCDD	CCPP	CCDI	DPTO_NOMBR	PROV_NOMBR	CATMUNI	VFI	P04	P11	fecha
##curs.executemany('INSERT INTO myTable (key, value) VALUES (%s, %s)', mydictionary.items())
##
##
###You could easily insert all three rows within the dictionary by using:
##curs.executemany("""INSERT INTO bar(first_name,last_name) VALUES (%(first_name)s, %(last_name)s)""", nametup)
