############################### FORMER codelines


### Este comentario en bloque es a quitar en la version final. Aca solo para los tests
##
##conn = psycopg2.connect('host=localhost port=5432 dbname=geolocalizacion user=postgres password=pacivur')
##curs = conn.cursor()
##
##
### encoding, muy importante
##cons_encoding = "set client_encoding to 'LATIN1';"
##curs.execute(cons_encoding)


##1 'XL_CELL_TEXT',cell_contents(sheet,1)
##2 'XL_CELL_NUMBER',cell_contents(sheet,2)
##3 'XL_CELL_DATE',cell_contents(sheet,3)
##0 'XL_CELL_BLANK',cell_contents(sheet,6)
##4 'XL_CELL_BOOLEAN',cell_contents(sheet,4)
##5 'XL_CELL_ERROR',cell_contents(sheet,5)


#copy empresas_mml from '\\Compartido\sig\Processos y herramientas\solinette\datos a ubicar\empresas_MML.csv' DELIMITER ';' CSV HEADER;


# A continuacion para agregar un campo id si no hay. No es obligatorio
'''
cons_sequence = "CREATE TEMPORARY SEQUENCE serial_id START 1;"
curs.execute(cons_sequence)

cons_add_id = "ALTER TABLE " + tabla_direcciones + " ADD COLUMN "+ col_id + " int;"
curs.execute(cons_add_id)

cons_fill_id = "UPDATE " + tabla_direcciones + " SET "+ col_id + " = nextval('serial_id');"
curs.execute(cons_fill_id)'''


# A continuacion para agregar un campo id si no hay. No es obligatorio
'''
cons_sequence = "CREATE TEMPORARY SEQUENCE serial_id START 1;"
curs.execute(cons_sequence)

cons_add_id = "ALTER TABLE " + tabla_direcciones + " ADD COLUMN "+ col_id + " int;"
curs.execute(cons_add_id)

cons_fill_id = "UPDATE " + tabla_direcciones + " SET "+ col_id + " = nextval('serial_id');"
curs.execute(cons_fill_id)
'''
# Fin de la parte para agregar y llenar el campo id


'''
# para quitar la columna, solo durantes los tests
consX = "ALTER TABLE " + tabla_direcciones + " DROP COLUMN tipo_via; ALTER TABLE " + tabla_direcciones + " DROP COLUMN numero; \
ALTER TABLE " + tabla_direcciones + " DROP COLUMN complemento_dir; ALTER TABLE " + tabla_direcciones + " DROP COLUMN nombre_via;"
curs.execute(consX)
'''



##aarchiv =  open(path.join(getcwd(), params.get('archivo')), 'wb')
##aarchiv.readline()
##datos = aarchiv.readlines()
###[unicode(s).encode("latin1") for s in sheet.row_values(row)]
##for line in datos:
##    data = tuple(line.split('\t'))
##    c_crea_insert = "insert into "+ params.get('tabla_out') + " VALUES " + str(data) + ";"
##    curs.execute(c_crea_insert)
##    del c_crea_insert

##datos = tuple(aarchiv.readline().split('\t'))
##print datos
##c_crea_insert = "insert into "+ params.get('tabla_out') + " VALUES " +str(datos)+ ";"
##curs.execute(c_crea_insert)


'''
# solo para los tests
cons_dropubiego = "ALTER TABLE " + tabla_direcciones + " DROP column ubigeo;"
curs.execute(cons_dropubiego)
'''

'''
i =0
while i < len(lista2_dist):
    if lista2_dist[i][0] in lista_distref:
        cons_updateubiego = "UPDATE " + tabla_direcciones + " SET ubigeo = '" + lista_ubiref[lista_distref.index(lista2_dist[i][0])]+"' where " + col_id + " = " + str(i+1)+";"
        #print cons_updateubiego
        curs.execute(cons_updateubiego)
    else:
        distrit = lista2_dist[i][0].split(' ')
        j =0
        while j <len(distrit):
            if  len(distrit[j]) > 3 or distrit[j] == 'ATE':
                if distrit[j] == 'CERCADO' or distrit[j] == 'JUAN' or distrit[j] == 'SANTA':
                    pass
                else:

                    for t in lista_distref:
                        if distrit[j] in t:
                            cons_updateubiego = "UPDATE " + tabla_direcciones + " SET ubigeo = '" + lista_ubiref[lista_distref.index(t)]+"' where " + col_id + " = " + str(i+1)+";"
                            #print cons_updateubiego
                            curs.execute(cons_updateubiego)
                            #j = len(distrit)-1

            j =j+1


    i = i+1
'''

