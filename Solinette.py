# -*- coding: cp1252 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name :       Solinette
# Purpose :
# Authors :    Pierre Vernier et Julien M.
# Python :     2.7.x +
# Encoding:    latin1
# Created :    19/12/2011
# Updated :    23/03/2013
# Version :    1.4.2
#-------------------------------------------------------------------------------

###################################
##### Libraries and modules #######
###################################

# standard library
from os import environ as env, path, getcwd
from sys import exit

# external library
import psycopg2

# custom modules
from Solinette_main import SolinetteGUI

###################################
###### Functions definition #######
###################################

def construc_lista(lista):
    """Función para pasar de una lista de tuples (resultado de psycopg2)
    a una lista de listas"""
    i =0
    while i <len(lista):
        f = str(lista[i][0]).rstrip()
        lista.remove(lista[i])
        #try: # para guadar enteros ,por ejemplo en el caso de los id
            #lista.insert(i,int(f))
        #except:
        lista.insert(i, f)
        i = i+1
    # End of function
    return lista

def en_mayusculas(lista):
    """Función que permite transformar en mayusculas una cadena de caracteres.
    Necesita 1 argumento, una lista de listas que contienen
    una cadena de caracteres."""
    i = 0
    while i < len(lista):
        if type(lista[i][0]) == str:
            lista[i][0] = lista[i][0].upper()

        i = i+1
    # End of function
    return lista

def sin_accento(lista):
    """Función que permite quitar los accentos de una cadena de caracteres.
    Necesita 1 argumento, una lista de listas que contienen
    una cadena de caracteres."""
    accentos = ['Á', 'Ó', 'Í', 'É', 'Ú', 'Ü', 'À', 'Ò', 'Ì', 'È', 'Ù', 'š', 'ñ', 'Š', '#', "'"] # 'Š' = 'ª'
    sin_accentos = ['A', 'O', 'I', 'E', 'U', 'U','A', 'O', 'I', 'E', 'U', '°', 'Ñ', '', 'N°', '']
    i = 0
    while i < len(lista):
        #print 'i intern', i, lista[i]
        for letra in lista[i][0]:
            if letra in accentos:
                #print letra
                n_letra = sin_accentos[accentos.index(letra)]
                #print n_letra
                #print lista[i][0]
                try:
                    n_palabra = lista[i][0].replace(lista[i][0][lista[i][0].index(letra)], n_letra)
                    #print 'nouv ', n_palabra
                    lista[i][0] = n_palabra
                except:
                    pass
        i = i+1
    # End of function
    return lista, accentos, sin_accentos


def sentido_n_nm1(inicio_n, final_n, inicio_nm1, final_nm1):
    """Funcion para establecer si el sentido es correcto
    entre la cuadra n y la cuadra n-1"""
    global sentido
    if inicio_n == final_nm1: # or final_nm1 == inicio_n:
        #print "sentido correcto entre n y n-1"
        sentido = 'correcto'

    elif final_n == inicio_nm1 or inicio_n == inicio_nm1 or final_n == final_nm1:
        #print " sentido  no correcto entre n y n-1 "
        sentido = 'contrario'

    else:
        #print "  Bug entre n y n-1 "
        #print inicio_n, final_n
        #print inicio_nm1, final_nm1
        if 'MULTILINESTRING' in lista_coord_nm1[2]:
            if lista_startPoint[0] in lista_coord_nm1[2]:
                #print 'sentido correcto entre n y n-1 en la segunda vez'
                sentido = 'correcto'
            else:
                pass
                #print 'caso raro en n-1'
        else:
            pass
            #print 'caso raro en n-1'
    # End of function
    return inicio_n, inicio_nm1, final_n, final_nm1



def sentido_n_np1(inicio_n, final_n, inicio_np1, final_np1):
    """Funcion para establecer si el sentido es correcto entre
    la cuadra n y la cuadra n+1"""
    global sentido
    #print inicio_n, final_n, inicio_np1, final_np1
    if inicio_np1 == final_n : #or final_n == inicio_np1:
        #print "sentido correcto entre n y n+1"
        sentido = 'correcto'

    elif final_np1 == inicio_n or inicio_n == inicio_np1 or final_n == final_np1:
        #print " sentido  no correcto entre n y n+1 "
        sentido = 'contrario'

    else:
        #print "  Bug entre n y n+1 "
        #print inicio_n, final_n
        #print inicio_np1, final_np1
        if 'MULTILINESTRING' in lista_coord_np1[2]:
            if lista_startPoint[0] in lista_coord_np1[2]:
                #print 'sentido correcto entre n y n+1 en la segunda vez'
                sentido = 'correcto'
            else:
                pass
                #print 'caso raro en n+1'
        else:
            pass
            #print 'caso raro en n+1'
    # End of function
    return inicio_n, inicio_np1, final_n, final_np1, sentido, lista_coord_np1


def entre_puntos(cadena, tuplo):
    """Funcion para encontrar los 2 puntos de la cuadra entre los cuales se
    encuentra el punto a localizar y hacer el desplacamiento a la izq. o der.
    en funcion del número"""
    lista_pts =[]
    cadena2 = cadena.lstrip('LINESTRING(')
    cadena3 = cadena2.rstrip(')')
    lista = cadena3.split('),(')
    for e in lista:
        j = e.split(',')
        for t in j:
            x = t.split(' ')
            z = (float(x[0]), float(x[1]))
            lista_pts.append(z)

            del x


    tuplo_x = tuplo[0]
    tuplo_y = tuplo[1]

    v = 0
    encontrado = 'no'
    while v < len(lista_pts) and encontrado == 'no':
        #print 'v = ',v, '/', len(lista_pts)
        for e in lista_pts:
            if e <> lista_pts[v]:
                #print 'points : ', lista_pts[v], e
                x_e = e[0]
                y_e = e[1]
                x_v = lista_pts[v][0]
                y_v = lista_pts[v][1]
                a = (y_e - y_v)/(x_e - x_v)
                b = y_v - a*x_v

                if abs(tuplo_y - (a*tuplo_x +b)) < 0.5:
                    encontrado = 'si'
                    a_entre = a
                    b_entre = b
                    punto_1 = lista_pts[v]
                    punto_2 = e
                else:
                    pass
            else:
                pass

        v = v+1
        del e, x_e, y_e, x_v, y_v, a, b



    difH = punto_2[0] - punto_1[0] # la diferencia entre la x de los 2 puntos
    difV = punto_2[1] - punto_1[1] # la diferencia entre la y de los 2 puntos
    angRadian = atan2(difV , difH) # calculo del angulo en radians
    angGrado = angRadian *(180./pi) # convercion en grados



    a_perpen=-1/a_entre
    b_perpen=tuplo_y - a_perpen*tuplo_x
    deltaX = 5/sqrt(1+a_perpen**2)

    if lista_dir[2]/2 <> lista_dir[2]/2.:
        etat ='impar'

    else:
        etat ='par'

    global X_decal, Y_decal

    if sentido == 'contrario':

        if angGrado >0 and etat == 'par':
            X_decal = tuplo_x - deltaX


        if angGrado >0 and etat == 'impar':
            X_decal = tuplo_x + deltaX


        if angGrado <0 and etat == 'par':
            X_decal = tuplo_x + deltaX


        if angGrado <0 and etat == 'impar':
            X_decal = tuplo_x - deltaX



    else:


        if angGrado >0 and etat == 'par':
            X_decal = tuplo_x + deltaX


        if angGrado >0 and etat == 'impar':
            X_decal = tuplo_x - deltaX


        if angGrado <0 and etat == 'par':
            X_decal = tuplo_x - deltaX


        if angGrado <0 and etat == 'impar':
            X_decal = tuplo_x + deltaX


    Y_decal = a_perpen*X_decal + b_perpen

    coord = (X_decal, Y_decal)


    if coord not in lista_coords:
        lista_coords.append(coord)
    else:

        lado_X = random.triangular(-1,1)

        X_decal = X_decal + lado_X
        lado_Y2 = 1 - lado_X**2
        lado_Y = sqrt(lado_Y2)

        s = random.sample([-1,1],1)
        lado_Y = s[0] * lado_Y

        Y_decal = Y_decal + lado_Y
        coord = (X_decal, Y_decal)
        lista_coords.append(coord)

    # End of function
    return cadena, tuplo, lista_coords, lista_pts


####################################
######### Global variables #########
####################################

#### Retrieving connection settings and parameters from the GUI
app = SolinetteGUI()
app.mainloop()
params = app.dico_param

# test if there are parameters
if not params.get('pg_host'):
    exit()

#### Connection to database
conn = psycopg2.connect(host=params['pg_host'],
        port=params['pg_port'],
        dbname=params['pg_bd'],
        user=params['pg_usuario'],
        password=params['pg_pwd'])

curs = conn.cursor()

# Setting the encoding
c_set_encoding = "set client_encoding to 'LATIN1';"
curs.execute(c_set_encoding)

#### Creation of input table
# columns definition
cols = ''

dico_equival_type = {0:'char(255)',
                     1:'char(255)',
                     2:'numeric',
                     3:'date',
                     4:'boolean',
                     5:'None'}

for i in range(len(params.get('cols').keys())):
    cols = cols + params.get('cols').keys()[i].lower() + ' ' \
                + dico_equival_type.get(params.get('cols').values()[i]) + ', '

# input table creation
c_crea_tablaout = "create table " + params.get('tabla_out') + " ( " + cols[:-2] + ");"
curs.execute(c_crea_tablaout)

# saving modifications and cleaning up
conn.commit()
del c_crea_tablaout, cols, dico_equival_type, c_set_encoding

#### Fill in the table
c_crea_copy = "copy "+ params.get('tabla_out') \
                   + " from '" + path.join(getcwd(), params.get('archivo')) \
                   + "' DELIMITER E'\t' CSV HEADER QUOTE '\"';"
curs.execute(c_crea_copy)

# saving modifications and cleaning up
conn.commit()
del c_crea_copy

#### Bascis settings: DB columns
# nombre de las 2 tablas
tabla_direcciones = params.get('tabla_out')
tabla_vias = 'solinette_nombrevial_130421'
tabla_dir_geom = tabla_direcciones + '_geom'    # tabla de las direcciones encontradas (con geometria)
tabla_dir_multi = tabla_direcciones + '_multi'  # tabla de las direcciones encontradas pero con geometria 'MULTTILINESTRING'
tabla_dir_bug = tabla_direcciones + '_bug'      # tabla de las direcciones no encontradas (sin geometria)
tabla_dir_imposible = tabla_direcciones + '_imposible'  #  tabla de las direcciones imposibles de localizar (sin nombre o numero)

# columnas de la tabla de las direcciones
col_id = 'SOL_IDU'
col_direccion = params.get('direccion')
col_dist = params.get('distrito')

# columnas de la tabla de las vias
col_id_via = 'gid'
col_tipo_via = '"CATEG_VIA"'  #'categ_via'
col_nombre_via = '"NOMBRE_VIA"' #'nombre_via'
col_nombre_via_alt = '"NOMBRE_ALT"'  # 'nombre_alt' # nombre alternativo de la via
col_num_via = '"CUADRA"' # 'cuadra'
col_ubigeo_via = '"UBIGEO"' # 'ubigeo'
col_ubigeo2_via = 'ubigeo2'
col_dist_izq = '"IZQESQUEMA"' # 'izqesquema'
col_dist_der = '"DERESQUEMA"' # 'deresquema'



################################################################################
########### Main program ###########
####################################

## Agrego los 4 campos que voy a llenar
# Agrego una nueva columna en la cual pongo el tipo de la via
c_add_tipo = "begin; ALTER TABLE " + tabla_direcciones \
                                  + " ADD COLUMN sol_tipo varchar(10);"
curs.execute(c_add_tipo)

# Agrego una nueva columna en la cual pongo el numero de la via
c_add_nom = "ALTER TABLE " + tabla_direcciones \
                          + " ADD COLUMN sol_nombre varchar(120);"
curs.execute(c_add_nom)

# Agrego una nueva columna en la cual pongo el numero de la via
c_add_numero = "ALTER TABLE " + tabla_direcciones \
                             + " ADD COLUMN sol_numero int;"
curs.execute(c_add_numero)

# Agrego una nueva columna en la cual pongo el complemento de la direccion
c_add_complemento = "ALTER TABLE " + tabla_direcciones \
                                  + " ADD COLUMN sol_compdir varchar(200);"
curs.execute(c_add_complemento)

# saving changes and cleaning up
curs.commit()
del c_add_complemento, c_add_nom, c_add_numero, c_add_tipo

c_sel_all = "select " + col_direccion + " from " + tabla_direcciones \
                                 + " order by " + col_id + ";"
curs.execute(c_sel_all)
li_direcciones = curs.fetchall()

# Necesito los id para poder insertar nuevos valores en los nuevos campos segun
# ellos. Es mas seguro que segun los i
c_sel_id = "select " + col_id + " from " + tabla_direcciones + " order by " + col_id + ";"
curs.execute(c_sel_id)
li_id = curs.fetchall()

# Transformo la lista de tuple en lista de listas
construc_lista(li_id)

# Inicio - Esa parte hace lo mismo que la funcion construc_lista() que no funciona aqui, no se porque
lista2=[]
i = 0
while i < len(li_direcciones):
    lista2.append([])
    i=i+1

i = 0
while i < len(li_direcciones):
    if li_direcciones[i] <> (None,):
        if li_direcciones[i][0][0] =='\xa0':
            #print li_direcciones[i]
            lista2[i].append(li_direcciones[i][0][1:].rstrip())
            #print lista2[i]
        else:
        #print lista2[i]
            lista2[i].append(li_direcciones[i][0].rstrip())
        #print lista2[i]

    else:
        lista2[i].append('ninguna')
    i=i+1
# Fin - Esa parte hace lo mismo que la funcion construc_lista() que no funciona aqui, no se porque


del li_direcciones

en_mayusculas(lista2)


sin_accento(lista2)



####### Aca edito las direcciones para poner un espacio despues de un '.', un '°' o un '?'
for direc in lista2:

    for string in direc:
        string2 = ''
        for e in string:
            try:
                if (e == '.' or e == '°' or e == '?') and string[string.index(e)+1] <> ' ':
                    string2 = string2 + e + ' '
                else:
                    string2 = string2 + e
            except:
                pass
    direc[0] = string2

del direc, string, e
#####################

i = 0
while i < len(lista2):
    lista2[i] = lista2[i][0].split(' ')
    try:
        lista2[i].remove('')
    except:
        pass
    #print lista2[i]
    i = i+1

print "Edición de la tabla de direcciones"

# esta parte es para extraer los complementos de direccion.
# He quitado 'PARQUE' porque existen las avenidas parque sur y parque norte.
lista_comple = ['COMPLEMENTO', 'AA', 'A.H','URB', 'MZ', 'MZA', 'MANZANA', 'OF', 'PARCELA', 'LOTE', 'LT', '(', 'INT.', \
                'INTERIOR', 'SECTOR', 'ZONA', 'Z.I', 'PISO', 'KM', 'KILOMETRO', 'DPTO', 'COOP', \
                'PT', 'ALT', 'BLOCK', 'APARTADO', 'ESQ.', 'ESQUINA']

i =0
while i < len(lista2):
    #print 'i=', i
    j = 0
    #print 'et la?'
    while j < len(lista2[i]) :

        #print 'j et valeur en j = ',j ,lista2[i][j]
        for comple in lista_comple:
            if lista2[i][j].find(comple) == 0 and j <> -1: # 0 significa que la sub cadena se encuentra al incio de la cadena de referencia
                #print 'je suis dedans'
                dir_comple = lista2[i][j]
                del lista2[i][j]
                while j < len(lista2[i]):
                    dir_comple = dir_comple+' '+lista2[i][j]
                    del lista2[i][j]

                cons_compl = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(dir_comple)+ "'"+ " where " + \
                         col_id + " = "+ str(lista_id[i])+';'
                curs.execute(cons_compl)
                del comple, cons_compl, dir_comple
                j = -1
                if  i <len(lista2)-1:
                    #print 'je suis dans le 2eme i+1',i
                    i = i+1
                    #print 'je suis dans le 2eme i+1',i
                else:
                    pass
                #print 'i int', i
        #if len(lista2[i])>0:
        j=j+1
        #print 'je suis apres le j+1', j+1
    #if  i <len(lista2)-1:
    i = i+1
    #print 'i apres', i
    #else:
       #pass




# Abajo las listas de los tipos de vias. La segunda es normalizada
lista_tipo = ['CALLE', 'CA', 'CAL', 'CALL', 'C/', 'AVENIDA', 'AV', 'JIRON', 'JR',\
              'PASAJE', 'PSJE', 'PS', 'PJ', 'PSJ', 'PJE', 'PROLONGACION', 'PRL', 'PROLG', \
              'PROLONG', 'MALECON', 'MLC', 'PUENTE']

lista_tipo_norm = ['2', '2', '2', '2', '2', '1', '1', '3', '3',\
                   '4', '4', '4', '4', '4','6', '6', '6', \
              '6', '6', '6', '10']



# Para extraer el tipo de la via
i =0
while i < len(lista2):
    if len(lista2[i]) == 0: # si la lista esta vacia (es decir solo habia un complemento de direccion)
        pass
    else:
        try:
            if lista2[i][0][len(lista2[i][0])-1] ==  '.': #and len(lista2[i][0]) >0: # si la lista no esta vacia y el ultimo caracter es un '.'
                lista2[i][0] = lista2[i][0].rstrip('.') # quito el '.'
            else:
                pass
        except:
            pass
        if lista2[i][0] in lista_tipo: # si el tipo de via es conocido
            nv_valor = lista_tipo_norm[lista_tipo.index(lista2[i][0])]
            cons_i = "UPDATE " + tabla_direcciones + " SET tipo_via = "+ "'"+str(nv_valor)+ "'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
            curs.execute(cons_i)
            del cons_i, nv_valor

            del lista2[i][0]
        else:
            pass

    i = i+1


# Para extraer el numero y nombre de la via

lista_num = ['N', 'N°', 'NRO.', 'NRO', 'NO', 'N?', 'Nª', 'N\xaa', 'NÂ°', 'N\xb0', 'NO.', 'NUM.', 'CDR', 'CDRA', 'CDRA.','CUADRA']

i =0

lista_a_borrar = []
while i < len(lista2):
    j = 0

    while j < len(lista2[i]):
        #print i, lista2[i]
        if lista2[i][j] in lista_num: # en el caso en el cual el numero esta con un caracter tipo 'N°'
            #print lista2[i]
            #print lista2[i][j]
            #print lista_num
            lista_a_borrar.append(i)
            try:
                lista2[i][j+1] = lista2[i][j+1].rstrip(',')
            except:
                pass
            try:
                int(lista2[i][j+1])
                #print 'cas n°'

                if int(lista2[i][j+1]) < 100: # Si el numero que tengo es inferior a 100, signica que es un número de cuadra
                    lista2[i][j+1] = str(int(lista2[i][j+1])*100 + 50) # Entonces en este caso, pongo mi punto en el medio de la cuadra, de lado par



                cons_j = "UPDATE " + tabla_direcciones + " SET numero = "+str(lista2[i][j+1])+ " where " + col_id + " = "+ str(lista_id[i])+';'
                curs.execute(cons_j)
                del cons_j
                # Aca tengo que llenar el campo "nombre via" hasta i-1 y eventualmente los complementos a partir de i+2. Y luego borrarlos
                g = 0
                nombre = ''
                while g < j:
                    if lista2[i][g] not in lista_tipo:
                        nombre = nombre + lista2[i][g]+' '
                    else:
                        pass
                    g = g+1
                nombre = nombre.rstrip(' ')
                if len(nombre)>2:
                    cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    curs.execute(cons_j)
                    del cons_j
                if len(nombre)<=2:
                    cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE '||"+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    curs.execute(cons_j)
                    del cons_j

                if j+1 < len(lista2[i])-1: # si hay un complemento mas
                    #print 'id =', i+1
                    f = j+2
                    compl2 = ''
                    while f < len(lista2[i]):
                        compl2 = compl2 + lista2[i][f]+' '
                        f = f+1
                    compl2 = compl2.rstrip(' ')
                    if compl2 <> '-':

                        cons_verif = "SELECT complemento_dir from " + tabla_direcciones + " where " + col_id + " = "+ str(lista_id[i])+';'
                        curs.execute( cons_verif)
                        lista_verif = curs.fetchall()
                        #print lista_verif
                        if lista_verif[0] == (None,):
                            cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                            #print cons_f
                            curs.execute(cons_f)
                            del cons_f, compl2

                        else:
                            cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " ||' '|| complemento_dir where " + col_id + " = "+ str(lista_id[i])+';'
                            #print cons_f
                            curs.execute(cons_f)
                            del cons_f, compl2, cons_verif, lista_verif

                # Por el momento no borro los numeros, nombres y segundos complementos de direccion

                #print 'avant :', lista2[i]
                #while len(lista2[i])>0:
                    #del  lista2[i][0]
                #print 'apres :', lista2[i]



            except: # Si hay una 'N' pero la cadena siguiente no es de tipo int (hay un '-' por ejemplo'
                # Este caso esta tomado en cuenta cuando trato los con '-'. No agregara los 'N'
                pass


        if len(lista2[i][j]) >0 and lista2[i][j][0] =='#': # en el caso en el cual el numero esta caracterizado por el caracter '#'
            lista_a_borrar.append(i)

            try:
                int(lista2[i][j][1:len(lista2[i][j])])
                #print lista2[i][j]
                #print int(lista2[i][j][1:len(lista2[i][j])])

                if int(lista2[i][j][1:len(lista2[i][j])]) < 100: # Si el numero que tengo es inferior a 100, signica que es un número de cuadra
                    lista2[i][j][1:len(lista2[i][j])] = str(int(lista2[i][j][1:len(lista2[i][j])])*100 + 50) # Entonces en este caso, pongo mi punto en el medio de la cuadra, de lado par


                cons_j = "UPDATE " + tabla_direcciones + " SET numero = "+str(lista2[i][j][1:len(lista2[i][j])])+ " where " + col_id + " = "+ str(lista_id[i])+';'
                curs.execute(cons_j)
                del cons_j

                # Aca tengo que llenar el campo "nombre via" hasta i-1 y eventualmente los complementos a partir de i+1. Y luego borrarlos
                g = 0
                nombre = ''
                while g < j:
                    if lista2[i][g] not in lista_tipo:
                        nombre = nombre + lista2[i][g]+' '
                    else:
                        pass
                    g = g+1
                nombre = nombre.rstrip(' ')
                if len(nombre)>2:
                    cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    curs.execute(cons_j)
                    del cons_j
                if len(nombre)<=2:
                    cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE '||"+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    curs.execute(cons_j)
                    del cons_j

                if j+1 < len(lista2[i])-1: # si hay un complemento mas
                    #print 'id =', i+1
                    f = j+1
                    compl2 = ''
                    while f < len(lista2[i]):
                        compl2 = compl2 + lista2[i][f]+' '
                        f = f+1
                    compl2 = compl2.rstrip(' ')
                    if compl2 <> '-':

                        cons_verif = "SELECT complemento_dir from " + tabla_direcciones + " where " + col_id + " = "+ str(lista_id[i])+';'
                        curs.execute( cons_verif)
                        lista_verif = curs.fetchall()
                        #print lista_verif
                        if lista_verif[0] == (None,):
                            cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                            #print cons_f
                            curs.execute(cons_f)
                            del cons_f, compl2

                        else:
                            cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " ||' '|| complemento_dir where " + col_id + " = "+ str(lista_id[i])+';'
                            #print cons_f
                            curs.execute(cons_f)
                            del cons_f, compl2, cons_verif, lista_verif





            except:
                #print 'cas # mais pas num'
                pass

        if '-' in lista2[i][j] and lista2[i][j] <> '-': # Si no hay ni 'N' ni '#' antes y hay varios numeros con un '-'
            lista_a_borrar.append(i)
            l = lista2[i][j].split('-')
            t =0
            #print i+1, lista2[i], l
            while t <len(l):
                try:
                    int(l[t])

                    if int(l[t]) < 100: # Si el numero que tengo es inferior a 100, signica que es un número de cuadra
                        l[t] = str(int(l[t])*100 + 50) # Entonces en este caso, pongo mi punto en el medio de la cuadra, de lado par

                    cons_t = "UPDATE " + tabla_direcciones + " SET numero = "+str(l[t])+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    curs.execute(cons_t)
                    del cons_t
                    del l[t]
                    cad =''
                    for e in l:
                        #print 'elem', e
                        cad = cad+e+' '
                        #cad = cad.rstrip(' ')
                    t = len(l)
                    #print 'new liste', l

                    # Aca tengo que llenar el campo "nombre via" hasta i-1 y eventualmente los complementos a partir de i+1. Y luego borrarlos
                    g = 0
                    nombre = ''
                    while g < j:

                        if lista2[i][g] not in lista_tipo and lista2[i][g] not in lista_num: # Para no agregar el tipo de via o la plabar 'N' que me ha escapado antes
                            lista2[i][g] = lista2[i][g].rstrip(',')
                            nombre = nombre + lista2[i][g]+' '
                        else:
                            pass
                        g = g+1
                    nombre = nombre.rstrip(' ')
                    if len(nombre)>2:
                        cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                        curs.execute(cons_j)
                        del cons_j
                    if len(nombre)<=2:
                        cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE '||"+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                        curs.execute(cons_j)
                        del cons_j

                    if j+1 < len(lista2[i])-1: # si hay un complemento mas a añadir
                        f = 0
                        compl2 = ''
                        while f < len(l):
                            l[f] = l[f].rstrip(',')
                            compl2 = compl2 + l[f]+' '
                            f = f+1
                        compl2 = compl2.rstrip(' ')
                        if compl2 <> '-':
                            cons_verif = "SELECT complemento_dir from " + tabla_direcciones + " where " + col_id + " = "+ str(lista_id[i])+';'
                            curs.execute( cons_verif)
                            lista_verif = curs.fetchall()
                            if lista_verif[0] == (None,): # Si no hay complementos todavia
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                                #print cons_f
                                curs.execute(cons_f)
                                del cons_f, compl2, cons_verif, lista_verif
                            else: # Si ya existen complementos
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " ||' '|| complemento_dir where " + col_id + " = "+ str(lista_id[i])+';'
                                curs.execute(cons_f)
                                #print cons_f
                                del cons_f, compl2
                        else:
                            pass

                    else: # Si no hay complemento a añadir
                        f = j+1
                        compl2 = ''
                        while f < len(lista2[i]):
                            compl2 = compl2 + lista2[i][f]+' '
                            f = f+1
                        compl2 = compl2.rstrip(' ')
                        #print 'complemento else : ',compl2, 'dddd', nombre
                        if compl2 <> '-':

                            cons_verif = "SELECT complemento_dir from " + tabla_direcciones + " where " + col_id + " = "+ str(lista_id[i])+';'
                            curs.execute( cons_verif)
                            lista_verif = curs.fetchall()
                            if lista_verif[0] == (None,): # Si no hay complementos todavia
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(cad+compl2)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                                #print cons_f
                                curs.execute(cons_f)
                                del cons_f, compl2, cons_verif, lista_verif
                            else: # Si ya existen complementos
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(cad+compl2)+"'"+ " ||' '|| complemento_dir where " + col_id + " = "+ str(lista_id[i])+';'
                                curs.execute(cons_f)
                                del cons_f, compl2
                        else:
                            pass

                except: # Si el primer elemento no es de tipo numerico, no me interesa y paso al siguiente
                    t = t+1


        if 'S/N' in lista2[i]: # Por el momento en este caso no lleno el campo numero. tal vez cambiar su tipo a char y poner 'S/N
            lista_a_borrar.append(i)
            #print i+1, lista2[i]
            g = 0
            nombre = ''
            while lista2[i][g] <> 'S/N':
                if lista2[i][g] not in lista_tipo and lista2[i][g] not in lista_num: # Para no agregar el tipo de via o la plabar 'N' que me ha escapado antes
                    nombre = nombre + lista2[i][g]+' '
                else:
                    pass
                g = g+1

            nombre = nombre.rstrip(' ')
            if len(nombre)>2:
                cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                curs.execute(cons_j)
                del cons_j
            if len(nombre)<=2:
                cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE '||"+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                curs.execute(cons_j)
                del cons_j

            # A priori no es necesario añadir otro complemento. Por si acaso añadir codigo aca.


        j = j+1
    i = i+1

# Aca paso la lista 'lista_a_borrar' que contiene todas las direcciones ya editadas y las borro
# Asi me quedaran solo las sin 'N', '#' o '-'

for lista in lista_a_borrar:
    #print lista+1, lista2[lista]
    while len(lista2[lista]) <> 0:
        del lista2[lista][0]



while len(lista_a_borrar) <> 0:
    del lista_a_borrar[0]

i = 0 # Aca edito las direcciones con um numero solo (sin ningun caracter para anunciarlo)
while i < len(lista2):
    j = 0

    if len(lista2[i]) >0:
        #num = 'no'

        while j < len(lista2[i]):
            lista2[i][j] = lista2[i][j].rstrip(',')
            try:
                int(lista2[i][j])

                #print lista2[i][j]
                # Abajo son casos particulares que contienen numeros (fecha) en su nombre. Si se edita se debe editar abajo tambien
                if (int(lista2[i][j]) == 1 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 13 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 18 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 19 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 21 and 'MARZO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'ABRIL' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 27 and 'ABRIL' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 2 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 3 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 5 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 26 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 7 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 10 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 13 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'JULIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 26 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 28 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 1 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 5 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 6 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 22 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'SEPTIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'SETIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 23 and 'SEPTIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 23 and 'SETIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 3 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 8 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 9 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 12 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 12 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 17 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 20 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 26 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 6 and 'DICIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 9 and 'DICIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 25 and 'DICIEMBRE' in lista2[i][j+2]):
                       pass # Si el numero es una fecha, no lo tomo en cuenta y sigo en la cadena para encontrar el verdadero numero


                else: # Si el nombre de la calle no es una fecha
                    if j ==0 and len(lista2[i])<=2: # Aca asumo que si el nombre de la calle solo es un numero noy hay numero de direccion (es una manzana, lote)
                        if i not in lista_a_borrar:
                            lista_a_borrar.append(i)
                        #print 'el nombre de la calle es el numero : ',lista2[i]
                        cons_nombre = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE ' ||"+ "'"+str(lista2[i][j])+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                        #print cons_nombre
                        curs.execute(cons_nombre)
                        del cons_nombre


                    if j ==0 and len(lista2[i])>2:
                        # No comentar este print. Es una alerta
                        print 'Alerta : Esa calle : ',lista2[i] ,'cuyo nombre es un solo número tiene tambien un número para ubicar la direccion: No esta previsto en esta  \
                        versión del programa. A cambiar'




            except:
                pass

            j = j+1


    else:
        pass
    i = i+1

for lista in lista_a_borrar:
    #print lista+1, lista2[lista]
    while len(lista2[lista]) <> 0:
        del lista2[lista][0]


###############################################################################################################################################################


while len(lista_a_borrar) <> 0:
    del lista_a_borrar[0]
#print lista_a_borrar

i = 0 # Aca edito las direcciones con um numero solo (sin ningun caracter para anunciarlo)
while i < len(lista2):
    j = 0
    if len(lista2[i]) >0:
        #num = 'no'

        while j < len(lista2[i]):
            lista2[i][j] = lista2[i][j].rstrip(',')
            try:
                int(lista2[i][j])

                #print i+1, lista2[i], lista2[i][j]
                # Abajo son casos particulares que contienen numeros (fecha) en su nombre
                if (int(lista2[i][j]) == 1 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 13 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 18 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 19 and 'ENERO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 21 and 'MARZO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'ABRIL' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 27 and 'ABRIL' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 2 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 3 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 5 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 26 and 'MAYO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 7 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 10 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 13 and 'JUNIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'JULIO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 15 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 26 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 28 and 'JULIO' in lista2[i][j+2]) \
                   or (int(lista2[i][j]) == 1 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 5 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 6 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 22 and 'AGOSTO' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'SEPTIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'SETIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 23 and 'SEPTIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 23 and 'SETIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 3 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 8 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 9 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 12 and 'OCTUBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 1 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 12 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 17 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 20 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 26 and 'NOVIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 6 and 'DICIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 9 and 'DICIEMBRE' in lista2[i][j+2])\
                   or (int(lista2[i][j]) == 25 and 'DICIEMBRE' in lista2[i][j+2]):

                    pass # Si el numero es una fecha, no lo tomo en cuenta y sigo


                else: # Si en el nombre de la calle no es una fecha
                    if i not in lista_a_borrar:
                        lista_a_borrar.append(i)
                    #print '...................................',lista2[i], lista2[i][j]
                    #Todo lo que se encunetra antes del mumero es el nombre, depues es un complemento de direccion.

                    if int(lista2[i][j]) < 100: # Si el numero que tengo es inferior a 100, signica que es un número de cuadra
                        lista2[i][j] = str(int(lista2[i][j])*100 + 50) # Entonces en este caso, pongo mi punto en el medio de la cuadra, de lado par

                    cons_num = "UPDATE " + tabla_direcciones + " SET numero = "+str(lista2[i][j])+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    #print cons_num
                    curs.execute(cons_num)
                    del cons_num

                    # Aca tengo que llenar el campo "nombre via" hasta i-1 y eventualmente los complementos a partir de i+1. Y luego borrarlos
                    g = 0
                    nombre = ''
                    while g < j:
                        if lista2[i][g] not in lista_tipo and lista2[i][g] not in lista_num: # Para no agregar el tipo de via o la plabar 'N' que me ha escapado antes
                            nombre = nombre + lista2[i][g]+' '
                        else:
                            pass
                        g = g+1
                    nombre = nombre.rstrip(' ')
                    cons_g = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                    #print cons_g
                    curs.execute(cons_g)
                    del cons_g




                    if j+1 < len(lista2[i]): # si hay un complemento mas a añadir

                        f = j+1
                        compl2 = ''
                        while f < len(lista2[i]):
                            if lista2[i][f] <> '-':
                                compl2 = compl2 + lista2[i][f]+' '
                            else:
                                pass
                            f = f+1
                        compl2 = compl2.rstrip(' ')
                        if compl2 <> '-':
                            cons_verif = "SELECT complemento_dir from " + tabla_direcciones + " where " + col_id + " = "+ str(lista_id[i])+';'
                            curs.execute( cons_verif)
                            lista_verif = curs.fetchall()
                            #print 'compl2 :' , compl2, len(compl2)
                            if lista_verif[0] == (None,)and len(compl2) >0 : # Si no hay complementos todavia
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
                                #print cons_f
                                curs.execute(cons_f)
                                del cons_f, compl2, cons_verif, lista_verif
                            else: # Si ya existen complementos
                                cons_f = "UPDATE " + tabla_direcciones + " SET complemento_dir = "+ "'"+str(compl2)+"'"+ " ||' '|| complemento_dir where " + col_id + " = "+ str(lista_id[i])+';'
                                curs.execute(cons_f)
                                #print cons_f
                                del cons_f, compl2
                        else:
                            pass





            except: # si el nombre no es un número ?
                pass

            j = j+1


    else:
        pass
    i = i+1

for lista in lista_a_borrar:
    #print lista+1, lista2[lista]
    while len(lista2[lista]) <> 0:
        del lista2[lista][0]

while len(lista_a_borrar) <> 0:
    del lista_a_borrar[0]


###############################################################################################################################################################


# Abajo me quedan las direcciones sin numero. Asumo que lo que queda es el nombre de la via


i = 0 # Aca edito las direcciones con um numero solo (sin ningun caracter para anunciarlo)
while i < len(lista2):
    j = 0
    if len(lista2[i]) >0:
        #print i+1, lista2[i]
        if i not in lista_a_borrar:
            lista_a_borrar.append(i)
        # Aca tengo que llenar el campo "nombre via" hasta i-1 y eventualmente los complementos a partir de i+1. Y luego borrarlos
        nombre = ''
        while j < len(lista2[i]):
            if lista2[i][j] not in lista_tipo and lista2[i][j] not in lista_num: # Para no agregar el tipo de via o la palabra 'N' que me ha escapado antes
                nombre = nombre + lista2[i][j]+' '
            else:
                pass
            j = j+1
        nombre = nombre.rstrip(' ')
        if len(nombre)>2:
            cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = "+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
            curs.execute(cons_j)
            del cons_j
        if len(nombre)<=2:
            cons_j = "UPDATE " + tabla_direcciones + " SET nombre_via = 'CALLE '||"+ "'"+str(nombre)+"'"+ " where " + col_id + " = "+ str(lista_id[i])+';'
            curs.execute(cons_j)
            del cons_j

    i = i+1

for lista in lista_a_borrar:
    #print lista+1, lista2[lista]
    while len(lista2[lista]) <> 0:
        del lista2[lista][0]

while len(lista_a_borrar) <> 0:
    del lista_a_borrar[0]






########### Fin de la parte parsing de direcciones #############
print "*****************"


## Ahora edito los distritos para que sean normalizados
print "Creacion de los codigos UBIGEO en funcion de los nombres de distrito"

## A hacer de manera que sea facultativo. Si ya hay un campo ubigeo no usar esta parte
cons_dist = "SELECT "+ col_dist +" from " + tabla_direcciones + " order by "+ col_id +";"
curs.execute(cons_dist)
lista_dist = curs.fetchall()


cons_id = "SELECT "+ col_id +" from " + tabla_direcciones + " order by "+ col_id +";"
curs.execute(cons_id)
lista_id_dist = curs.fetchall()


construc_lista(lista_dist)
construc_lista(lista_id_dist)

lista2_dist=[]
i = 0
while i < len(lista_dist):
    lista2_dist.append([])
    i=i+1

i = 0
while i < len(lista_dist):
    lista2_dist[i].append(lista_dist[i].lstrip(' '))
    #print lista2_dist[i]
    i=i+1


en_mayusculas(lista2_dist)

sin_accento(lista2_dist)


col_distref = '"NOMBRE"'
col_distref2 = '"NOMBRE2"'
col_ubiref = '"UBIGEO"'

cons_distref = "SELECT "+ col_distref+" from distritos_bd;"
curs.execute(cons_distref)
lista_distref = curs.fetchall()

cons_distref2 = "SELECT "+ col_distref2+" from distritos_bd;"
curs.execute(cons_distref2)
lista_distref2 = curs.fetchall()

cons_ubiref = "SELECT "+ col_ubiref+" from distritos_bd;"
curs.execute(cons_ubiref)
lista_ubiref = curs.fetchall()

construc_lista(lista_distref)
construc_lista(lista_distref2)
construc_lista(lista_ubiref)

lista2_distref=[]
i = 0
while i < len(lista_distref):
    lista2_distref.append([])
    i=i+1

i = 0
while i < len(lista_distref):
    lista2_distref[i].append(lista_distref[i].lstrip(' '))
    i=i+1


'''
# solo para los tests
cons_dropubiego = "ALTER TABLE " + tabla_direcciones + " DROP column ubigeo;"
curs.execute(cons_dropubiego)
'''

cons_addubiego = "ALTER TABLE " + tabla_direcciones + " ADD column ubigeo varchar(6);"
curs.execute(cons_addubiego)

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

i =0
while i < len(lista2_dist):
    if lista2_dist[i][0] in lista_distref:
        cons_updateubiego = "UPDATE " + tabla_direcciones + " SET ubigeo = '" + lista_ubiref[lista_distref.index(lista2_dist[i][0])]+"' where " + col_id + " = " + str(i+1)+";"
        #print cons_updateubiego
        curs.execute(cons_updateubiego)
    else:
        #print 'je suis dans ce cas'
        if lista2_dist[i][0] in lista_distref2:
            cons_updateubiego = "UPDATE " + tabla_direcciones + " SET ubigeo = '" + lista_ubiref[lista_distref2.index(lista2_dist[i][0])]+"' where " + col_id + " = " + str(i+1)+";"
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










## Fin de la parte de normalizacion de los distritos
print "*****************"

##Creo una tabla conteniendo todas las direcciones que tienen sea el campo nombre vacio o sea el campo numero vacio
## Estas direcciones no se pueden ubicar con el programa.


cons_tabimposible = "CREATE table " + tabla_dir_imposible + " as ( select * from " +tabla_direcciones +" where nombre_via is null or \
                    numero is null);"

curs.execute(cons_tabimposible)




conn.commit()
del curs






################## Inicio de la geolocalizacion de direcciones ################
print "Localisazión de las direcciones"

from math import atan2, pi, sqrt
import random


conn2 = psycopg2.connect('host=localhost port=5432 dbname=geolocalizacion user=postgres password=pacivur')
curs2 = conn2.cursor()



###################################################

cons_createtable = "CREATE TABLE "+ tabla_dir_geom +" as \
select * from "+ tabla_direcciones +"; \
SELECT AddGeometryColumn('public', '"+ tabla_dir_geom +"','the_geom',32718, 'POINT',2);"
curs2.execute(cons_createtable)

cons_createtable_bug = "CREATE TABLE "+ tabla_dir_bug +" as \
select * from "+ tabla_direcciones +";"
curs2.execute(cons_createtable_bug)


cons_createtable_multi = "CREATE TABLE "+ tabla_dir_multi +" as \
select * from "+ tabla_direcciones +";"
curs2.execute(cons_createtable_multi)



lista_coords = [] # Esta lista almacena las coordenadas de las direcciones que voy a localizar.
# Necesario para no poner dos (o mas) mismas direcciones al mismo punto. hago un pequeño 'decalage'.
# Pero no chequeo si todos los campos son iguales (caso de un 'doublon')

lista_palab =['Y', 'DE', 'LOS', 'LAS', 'LA', 'EL' ,'DEL', 'AL'] # palabras de 3 letras max que no tomo en cuenta en mis\
lista_mes =['ENRERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'SETIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
            # consultas con un like

i =0

while i < len(lista2):

    cons_dir = "SELECT tipo_via, nombre_via, numero, ubigeo from " + tabla_direcciones +" where "+ col_id + " = "+ str(i+1) +";"
    #curs3 = conn2.cursor()
    curs2.execute(cons_dir)
    #print cons_dir
    lista_dir = curs2.fetchall()
    lista_dir = lista_dir[0] # Eso transforma mi lista en tuple. Lo hago para tener un nivel menos. Ser mas practico después
    print i+1#, lista_dir

    # Aca extraigo la cuadra a partir del numero de la direccion
    if len(str(lista_dir[2])) == 3 and type(lista_dir[2]) == int:
        cuadra = str(lista_dir[2])[0]
        a_interpol = str(lista_dir[2])[1:]
    elif len(str(lista_dir[2])) == 4 and type(lista_dir[2]) == int:
        cuadra = str(lista_dir[2])[0:2]
        a_interpol = str(lista_dir[2])[2:]
    elif len(str(lista_dir[2])) <> 3 and len(str(lista_dir[2])) <> 4 : # Significa que un numero otro que el numero correcto paso. Es un error
        cuadra = ''
    if lista_dir[2] == None:
        cuadra = ''
    #print cuadra
    if cuadra <> '':
        #print '........................',lista_dir[2]
        #print '.............a interpoler', a_interpol
        if lista_dir[2]/2. == lista_dir[2]/2: # caso par
            fraccion = float(a_interpol)/98

        else: # caso impar
            fraccion = float(a_interpol)/99

        #print 'fraction du point a interpoler :', fraccion


    else:
        #print 'i = ', i+1
        pass
        #print 'je ne peux pas interpoler'
        #cons_deletelinea = "DELETE FROM "+ tabla_dir_geom +" where "+ col_id + " = "+ str(i+1) +";"
        #curs2.execute(cons_deletelinea)


    if lista_dir[1] <> None:
        nbre_fecha = ''
        rempl = ''
        rempl = lista_dir[1]
        rempl = rempl.replace('.', ' ')
        rempl = rempl.replace(',', ' ')
        rempl = rempl.replace(';', ' ')
        rempl = rempl.replace(':', ' ')
        rempl = rempl.replace('-', ' ')
        rempl = rempl.replace('_', ' ')
        rempl = rempl.rstrip(' ') # si hay un espacio al final, lo quito
        direccion = rempl.split(' ')

        long_elem =[] # para recuperar la longitud de cada cadena de caracter de la lista
        for e in direccion:
            if e in lista_mes :
                nbre_fecha = 'si'
            long_elem.append(len(e))
        long_elem.sort(reverse=True) # la longitud max se encuentra al inicio de la lista

        cad_nombre = ' like '+"'"+'%'
        cad_nombre_2 = '%'

        if (len(direccion) <=2 and long_elem[0]<= 3) or 'CALLE' in direccion or nbre_fecha == 'si': # si tengo al maximo 2 palabras \
            # de maximo 3 letras o la palabra 'CALLE', no hago un like
            cad_nombre = ' = '+ "'" + lista_dir[1]

        else: # en los otros casos puedo hacer un like.
            for e in  direccion:
                    if e not in lista_palab: # no tomo en cuenta las palabras de 3 o menos letras.
                        # lista_palab se encuentra mas arriba
                        cad_nombre = cad_nombre + str(e) + cad_nombre_2
                    else:
                        pass

        #print cad_nombre




    else:
        direccion = ''
        pass


    #print direccion
    # Ahora tengo toda la informacion necesaria para encontrar mi cuadra en la tabla vias

    # Abajo hago mi consulta segun esa informacion
    if cuadra <> '' and lista_dir[1] <> '' and lista_dir[1] <> None and lista_dir[3] <> '': # si tengo una cuadra y un nombre puedo localizar el punto


        # Abajo consulta con nombre_via =
        # Extrao los start y end points de la cuadra. Podria ser extraer todos. Talvez da mejores resultados
        # Significa modificar las 3 consultas siguientes

        # 1era consulta, busco excatamente el nombre, la cuadra, el tipo de via y el distrito 1
        cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                   ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "+ \
                   col_nombre_via + " = "+ "'"+str(lista_dir[1])+ "' and "\
                     + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                    + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "'"
        curs2.execute(cons_via)

        lista_via = curs2.fetchall()
        if len(lista_via) >0: # Si encuentro al menos una cuadra
            #print "j ai trouve a la 1"
            pass

        if len(lista_via) == 0: # Si no encuentro la cuadra
            del cons_via, lista_via

            # 2nda consulta, busco excatamente el nombre, la cuadra, el tipo de via y el distrito 2
            cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                   ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "+ \
                   col_nombre_via + " = "+ "'"+str(lista_dir[1])+ "' and "\
                     + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                    + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "'"
            curs2.execute(cons_via)

            lista_via = curs2.fetchall()
            if len(lista_via) >0: # Si encuentro al menos una cuadra
                #print "j ai trouve a la 2"
                pass
            if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]: # Si no encuentro la cuadra
                del cons_via, lista_via
            ##############

                # 3ra consulta, busco el nombre con un like, la cuadra, el tipo de via y el distrito 1
                cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                           ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "\
                       + col_nombre_via + cad_nombre + "' and "\
                       + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                        + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "';"

                curs2.execute(cons_via)
                lista_via = curs2.fetchall()

                if len(lista_via) >0: # Si encuentro al menos una cuadra con mi consulta con 'like'
                    #print "j ai trouve a la 3"

                    pass


                if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]: # Si todavia no encuentro nada
                    del cons_via, lista_via

                    # 4rta consulta, busco el nombre con un like, la cuadra, el tipo de via y el distrito 2
                    cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                           ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "\
                                            + col_nombre_via + cad_nombre + "' and "\
                                            + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                        + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "';"
                    curs2.execute(cons_via)
                    lista_via = curs2.fetchall()


                    if len(lista_via) >0: # Si encuentro al menos una cuadra despues de la 4ra consulta
                        #print "j ai trouve a la 4"
                        pass

                    if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]:
                        del cons_via, lista_via

                        # 5ta consulta, busco el nombre con un like, la cuadra, el distrito 1 pero sin el tipo de via
                        cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+\
                                           col_dist_izq +", " + col_dist_der\
                                           +", " + col_id_via +", st_astext(the_geom)  from " + tabla_vias +\
                                        " where " + col_nombre_via + cad_nombre + "' and "\
                           + col_num_via + " = '"+ str(cuadra)+ "' and "\
                                + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "'"
                        curs2.execute(cons_via)
                        lista_via = curs2.fetchall()

                        if len(lista_via) >0: # Si encuentro al menos una cuadra despues de la 5ta consulta
                            #print "j ai trouve a la 5"
                            pass

                        if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]:
                            del cons_via, lista_via

                            # 6ta consulta, busco el nombre con un like, la cuadra, el distrito 2 pero sin el tipo de via
                            cons_via = "SELECT "+ col_nombre_via + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+\
                                               col_dist_izq +", " + col_dist_der\
                                               +", " + col_id_via +", st_astext(the_geom)  from " + tabla_vias +\
                                            " where " + col_nombre_via + cad_nombre + "' and "\
                                            + col_num_via + " = '"+ str(cuadra)+ "' and "\
                                            + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "'"
                            curs2.execute(cons_via)
                            lista_via = curs2.fetchall()

			################################################################################
                            if len(lista_via) >0: # Si encuentro al menos una cuadra despues de la 6ta consulta
                                #print "j ai trouve a la 6"
                                pass

                            if len(lista_via) == 0:
                                # 7ta consulta, busco excatamente el nombre alt, la cuadra, el tipo de via y el distrito 1
                                cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                                           ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "+ \
                                           col_nombre_via_alt + " = "+ "'"+str(lista_dir[1])+ "' and "\
                                             + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                                            + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "'"
                                curs2.execute(cons_via)

                                lista_via = curs2.fetchall()
                                if len(lista_via) >0: # Si encuentro al menos una cuadra
                                    #print "j ai trouve a la 7"
                                    pass

                                if len(lista_via) == 0: # Si no encuentro la cuadra
                                    del cons_via, lista_via

                                    # 8va consulta, busco excatamente el nombre alt, la cuadra, el tipo de via y el distrito 2
                                    cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                                           ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "+ \
                                           col_nombre_via_alt + " = "+ "'"+str(lista_dir[1])+ "' and "\
                                             + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                                            + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "'"
                                    curs2.execute(cons_via)

                                    lista_via = curs2.fetchall()
                                    if len(lista_via) >0: # Si encuentro al menos una cuadra
                                        #print "j ai trouve a la 8"
                                        pass
                                    if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]: # Si no encuentro la cuadra
                                        del cons_via, lista_via
                                    ##############

                                        # 9na consulta, busco el nombre alt con un like, la cuadra, el tipo de via y el distrito 1
                                        cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                                                   ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "\
                                               + col_nombre_via_alt + cad_nombre + "' and "\
                                               + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                                                + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "';"

                                        curs2.execute(cons_via)
                                        lista_via = curs2.fetchall()

                                        if len(lista_via) >0: # Si encuentro al menos una cuadra con mi consulta con 'like'
                                            #print "j ai trouve a la 9"

                                            pass


                                        if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]: # Si todavia no encuentro nada
                                            del cons_via, lista_via

                                            # 10ma consulta, busco el nombre alt con un like, la cuadra, el tipo de via y el distrito 2
                                            cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+col_dist_izq +", " + col_dist_der+\
                                                   ", " + col_id_via +", st_astext(the_geom) from " + tabla_vias +" where "\
                                                                    + col_nombre_via_alt + cad_nombre + "' and "\
                                                                    + col_num_via + " = '"+ str(cuadra)+ "' and "+ col_tipo_via + " = '"+ str(lista_dir[0])+ "' and "\
                                                + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "';"
                                            curs2.execute(cons_via)
                                            lista_via = curs2.fetchall()


                                            if len(lista_via) >0: # Si encuentro al menos una cuadra despues de la 10ma consulta
                                                #print "j ai trouve a la 10"
                                                pass

                                            if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]:
                                                del cons_via, lista_via

                                                # 11a consulta, busco el nombre alt con un like, la cuadra, el distrito 1 pero sin el tipo de via
                                                cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+\
                                                                   col_dist_izq +", " + col_dist_der\
                                                                   +", " + col_id_via +", st_astext(the_geom)  from " + tabla_vias +\
                                                                " where " + col_nombre_via_alt + cad_nombre + "' and "\
                                                   + col_num_via + " = '"+ str(cuadra)+ "' and "\
                                                        + col_ubigeo_via + " = '"+ str(lista_dir[3])+ "'"
                                                curs2.execute(cons_via)
                                                lista_via = curs2.fetchall()

                                                if len(lista_via) >0: # Si encuentro al menos una cuadra despues de la 11a consulta
                                                    #print "j ai trouve a la 11"
                                                    pass

                                                if len(lista_via) == 0 and 'CALLE' not in lista_dir[1]:
                                                    del cons_via, lista_via

                                                    # 12a consulta, busco el nombre alt con un like, la cuadra, el distrito 2 pero sin el tipo de via
                                                    cons_via = "SELECT "+ col_nombre_via_alt + ", st_astext(st_StartPoint(the_geom)), st_astext(st_EndPoint(the_geom)), "+\
                                                                       col_dist_izq +", " + col_dist_der\
                                                                       +", " + col_id_via +", st_astext(the_geom)  from " + tabla_vias +\
                                                                    " where " + col_nombre_via_alt + cad_nombre + "' and "\
                                                                    + col_num_via + " = '"+ str(cuadra)+ "' and "\
                                                                    + col_ubigeo2_via + " = '"+ str(lista_dir[3])+ "'"
                                                    curs2.execute(cons_via)
                                                    lista_via = curs2.fetchall()

                                                    if len(lista_via) >0:# Si encuentro al menos una cuadra despues de la 12a consulta
                                                        #print "j ai trouve a la fin"
                                                        pass

                                                    if len(lista_via) == 0 :
                                                        #print "a la fin je n ai rien trouve"
                                                        pass






                        ################################################################################




        # Aca tengo que hacer mis manipulaciones sobre la o las cuadras encontradas




        if len(lista_via) > 0:
            #if len(lista_via) > 1: # en el caso de una via doble
            #print 'caso de una via doble', len(lista_via)

            div = lista_dir[2]/2. # para saber si es un numero par o impar

            if int(div) == div:
                #print "nombre pair"
                lado = 'Der'
            else:
                #print "nombre impair"
                lado = 'Izq'
            if len(lista_via) > 1: # en el caso donde tengo mas de una via
                #print 'caso via doble'
                #print lista_via
                lado_der, lado_izq, lado_nulo, lado_doble = -1, -1, -1, -1
                for e in lista_via:
                    if e[3] == 0 and e[4] == 2:
                        lado_der = lista_via.index(e)
                    if e[3] == 1 and e[4] == 0:
                        lado_izq = lista_via.index(e)
                    if e[3] == 0 and e[4] == 0:
                        lado_nulo = lista_via.index(e)
                    if e[3] == 1 and e[4] == 2:
                        lado_doble = lista_via.index(e)
                #print lado
                #print lado_der, lado_izq, lado_nulo, lado_doble
                    #print lista_via
                if lado_der <> -1 and lado == 'Der' and lado_doble == -1:
                    lista_via = lista_via[lado_der]
                    #print lista_via
                if lado_izq <> -1 and lado == 'Izq' and lado_doble == -1:
                    lista_via = lista_via[lado_izq]

                if lado_doble <> -1:
                    lista_via = lista_via[lado_doble]

                #para tratar los casos raros, es una tentativa
                if lado_der <> -1 and lado_izq == -1 and lado == 'Izq' and lado_doble == -1:
                    #print'je suis bien de ce cas rare'
                    lista_via = lista_via[lado_der]
                if lado_izq <> -1 and lado_der == -1 and lado == 'Der' and lado_doble == -1:
                    lista_via = lista_via[lado_izq]

                #else: # mis condiciones no son bien hechas para localisar los casos raros no previstos
                    #print 'caso no previsto en: ',i+1, lista_via
                del lado_der, lado_izq, lado_nulo, lado_doble, lado
                #print lista_via
            else: # pongo else pero es si len(lista_via) == 1, es igual en este caso
                lista_via = lista_via[0] ## A ver porque puse eso! no me recuerdo!!

                #print lista_via[1], lista_via[2]
                # Abajo para extraer las coordenadfas start y end de la cuadra en formato float. No se si lo necesitare


            if 'MULTILINESTRING'  in lista_via[6]:
                # En este caso, pongo las direcciones en la tabla conteniendo las cuadras "multilinestring"

                # A ver si esta bien
                cons_deletelineas_bug = "DELETE FROM "+ tabla_dir_bug +" WHERE "+col_id + " = "+str(i+1)+";"
                curs2.execute(cons_deletelineas_bug)

                cons_deletelineas_geom = "DELETE FROM "+ tabla_dir_geom +" WHERE "+col_id + " = "+str(i+1)+";"
                curs2.execute(cons_deletelineas_geom)

            else:


                cad_startPoint2 = lista_via[1].lstrip('POINT(')
                cad_startPoint = cad_startPoint2.rstrip(')')
                cad_endPoint2 = lista_via[2].lstrip('POINT(')
                cad_endPoint = cad_endPoint2.rstrip(')')
                lista_startPoint = cad_startPoint.split(' ')
                lista_endPoint = cad_endPoint.split(' ')
                start_X = float(lista_startPoint[0])
                start_Y = float(lista_startPoint[1])
                end_X = float(lista_endPoint[0])
                end_Y = float(lista_endPoint[1])
                #print 'gid : ', lista_via[5]
                c_n_start = (start_X, start_Y)
                c_n_end = (end_X, end_Y)
                #print 'coords point :', start_X, start_Y, end_X, end_Y

###############################################################################################
################ A continuación, busco las cuadras vecinas n-1 y n+1 ##########################
###############################################################################################

                # Ahora necesito encontrar una cuadra vecina para saber el sentido de las cuadras
                #if cuadra == 1:
                    #print 'La cuadra es la número 1, no existe cuadra n-1'
                # Busco primero la cuadra n-1. Puedo encontrar varias
                sentido_nm1 = 'normal' # Eso me sierve mas bajo para saber si interpolo de manera normal o en el otro sentido
                cons_cuad_nm1 = "SELECT gid from " + tabla_vias +" where "\
                   + col_nombre_via + cad_nombre + "' and "\
                   + col_num_via + " = '"+ str(int(cuadra)-1)+ "';"

                curs2.execute(cons_cuad_nm1)
                lista_cuad_nm1 = curs2.fetchall()
                construc_lista(lista_cuad_nm1)
                #print ' la liste de la cuadra n-1 :', lista_cuad_nm1



                # Busco la cuadra n+1 ahorita. Puedo encontrar varias.
                sentido_np1 = 'normal'
                cons_cuad_np1 = "SELECT gid from " + tabla_vias +" where "\
                   + col_nombre_via + cad_nombre + "' and "\
                   + col_num_via + " = '"+ str(int(cuadra)+1)+ "';"

                curs2.execute(cons_cuad_np1)
                lista_cuad_np1 = curs2.fetchall()
                construc_lista(lista_cuad_np1)

                id_cuad_nm1 = -1
                if len(lista_cuad_nm1) <> 0: # Si hay una cuadra vecina n-1, busco la única buena
                    # Abajo version con st_intersection
                    t =0
                    lista_intersec = ['GEOMETRYCOLLECTION EMPTY']
                    #id_cuad_nm1 = -1
                    while t <len(lista_cuad_nm1) and lista_intersec == ['GEOMETRYCOLLECTION EMPTY']:
                        #print 'avance = ', str(t)+'/'+ str(len(lista_cuad_nm1))
                        cons_intersec = "SELECT st_astext(st_intersection(g1, g2)) from \
                              (select the_geom as g1 from " + tabla_vias +" where " + col_id_via +" = "+str(lista_via[5])+ \
                              ") as sel1 , (select the_geom as g2 from " + tabla_vias +" where " + col_id_via +" = "+ str(lista_cuad_nm1[t])+\
                              ") as sel2"
                        curs2.execute(cons_intersec)
                        lista_intersec = curs2.fetchall()
                        construc_lista(lista_intersec)
                        #print 'voici lista intersec', lista_intersec
                        id_cuad_nm1 = lista_cuad_nm1[t] # porq????

                        t = t+1
                    del t

                else:
                    pass
                    #print "No hay una cuadra n-1 adequada"

                id_cuad_np1 = -1
                if len(lista_cuad_np1) <> 0: # Si hay una cuadra vecina n+1, busco la única buena
                    # Abajo version con st_intersection
                    tp =0
                    lista_intersecp = ['GEOMETRYCOLLECTION EMPTY']
                    #id_cuad_np1 = -1
                    while tp <len(lista_cuad_np1) and lista_intersecp == ['GEOMETRYCOLLECTION EMPTY']:
                        #print 'avance = ', str(t)+'/'+ str(len(lista_cuad_nm1))
                        cons_intersecp = "SELECT st_astext(st_intersection(g1, g2)) from \
                              (select the_geom as g1 from " + tabla_vias +" where " + col_id_via +" = "+str(lista_via[5])+ \
                              ") as sel1 , (select the_geom as g2 from " + tabla_vias +" where " + col_id_via +" = "+ str(lista_cuad_np1[tp])+\
                              ") as sel2"
                        curs2.execute(cons_intersecp)
                        lista_intersecp = curs2.fetchall()
                        construc_lista(lista_intersecp)
                        id_cuad_np1 = lista_cuad_np1[tp]  ##porq???

                        tp = tp+1

                    del tp

                else:
                    pass
                    #print "No hay una cuadra n+1 adequada"



                sentido =''
                # Empiezo por la cuadra n-1
                if id_cuad_nm1 <> -1: # en este caso tengo una cuadra vecina n-1 a la cuadra n. Busco el buen sentido
                    # Abajo extraigo todas las coordenadas de n-1
                    cons_coord_nm1 = "SELECT st_astext(st_startpoint(the_geom)), st_astext(st_endpoint(the_geom)), \
                    st_astext(the_geom) from "  + tabla_vias + " where " + col_id_via + " = "+ str(id_cuad_nm1)+ ";"
                    curs2.execute(cons_coord_nm1)
                    lista_coord_nm1 = curs2.fetchall()
                    lista_coord_nm1 = lista_coord_nm1[0] # Las coordenadas start y end de la cuadra n-1 no procesadas
                    #print 'lista coord n-1 :',lista_coord_nm1




                    c_nm1_startPoint2 = lista_coord_nm1[0].lstrip('POINT(')
                    c_nm1_startPoint = c_nm1_startPoint2.rstrip(')')
                    c_nm1_endPoint2 = lista_coord_nm1[1].lstrip('POINT(')
                    c_nm1_endPoint = c_nm1_endPoint2.rstrip(')')
                    lista_c_nm1_startPoint = c_nm1_startPoint.split(' ')
                    lista_c_nm1_endPoint = c_nm1_endPoint.split(' ')
                    start_X_c_nm1 = float(lista_c_nm1_startPoint[0])
                    start_Y_c_nm1 = float(lista_c_nm1_startPoint[1])
                    end_X_c_nm1 = float(lista_c_nm1_endPoint[0])
                    end_Y_c_nm1 = float(lista_c_nm1_endPoint[1])
                    c_nm1_start = (start_X_c_nm1, start_Y_c_nm1)
                    c_nm1_end = (end_X_c_nm1, end_Y_c_nm1)
                    #print 'coords start y end n-1 :',start_X_c_nm1, start_Y_c_nm1, end_X_c_nm1, end_Y_c_nm1 # Las coordenadas start y end de la cuadra n-1 procesadas

                    sentido_n_nm1(c_n_start, c_n_end, c_nm1_start, c_nm1_end)
                    #print 'sens n-1 : ',sentido

                    #if 'MULTILINESTRING' in lista_coord_nm1[2]:
                        #if lista_startPoint[0] in lista_coord_nm1[2]:
                           # print 'sentido ok entre n y n-1 en la segunda vez'

                else:
                    pass
                    #print "No hay una cuadra n-1 que toca la cuadra n"



                # Ahora busco por la cuadra n+1
                if id_cuad_np1 <> -1: # en este caso tengo una cuadra vecina n+1 a la cuadra n. Busco el buen sentido
                    # Abajo extraigo todas las coordenadas de n+1
                    cons_coord_np1 = "SELECT  st_astext(st_startpoint(the_geom)), st_astext(st_endpoint(the_geom)), \
                    st_astext(the_geom)  from " \
                                    + tabla_vias + " where " + col_id_via + " = "+ str(id_cuad_np1)+ ";"
                    curs2.execute(cons_coord_np1)
                    lista_coord_np1 = curs2.fetchall()
                    lista_coord_np1 = lista_coord_np1[0]
                    #print 'lista coord n+1 :',lista_coord_np1


                    c_np1_startPoint2 = lista_coord_np1[0].lstrip('POINT(')
                    c_np1_startPoint = c_np1_startPoint2.rstrip(')')
                    c_np1_endPoint2 = lista_coord_np1[1].lstrip('POINT(')
                    c_np1_endPoint = c_np1_endPoint2.rstrip(')')
                    lista_c_np1_startPoint = c_np1_startPoint.split(' ')
                    lista_c_np1_endPoint = c_np1_endPoint.split(' ')
                    start_X_c_np1 = float(lista_c_np1_startPoint[0])
                    start_Y_c_np1 = float(lista_c_np1_startPoint[1])
                    end_X_c_np1 = float(lista_c_np1_endPoint[0])
                    end_Y_c_np1 = float(lista_c_np1_endPoint[1])
                    c_np1_start = (start_X_c_np1, start_Y_c_np1)
                    c_np1_end = (end_X_c_np1, end_Y_c_np1)
                    #print 'coords start y end n+1 :',start_X_c_np1, start_Y_c_np1, end_X_c_np1, end_Y_c_np1
                    #print sentido
                    if sentido <> 'correcto':
                        sentido_n_np1(c_n_start, c_n_end, c_np1_start, c_np1_end)

                    #print 'sens n+1 : ',sentido

                else:
                    pass
                    #print "No hay una cuadra n+1 que toca la cuadra n"



                ##########################################################################
                ################ A continuación, empiezo la interpolacion ################
                ##########################################################################



                if sentido <> 'contrario':

                    #cons_interpol = "SELECT st_astext(ST_Line_Interpolate_Point(the_geom,"+ str(fraccion)+ ")) from "  + tabla_vias + "\
                    #where " + col_id_via + " = "+ str(lista_via[5])+ ";"
                    #curs2.execute(cons_interpol)
                    #lista_interpol = curs2.fetchall()
                    #print 'resultat de linterpolation', lista_interpol

                    cons_interpol = "SELECT st_X(st_astext(ST_Line_Interpolate_Point(the_geom,"+ str(fraccion)+ "))), \
                    st_Y(st_astext(ST_Line_Interpolate_Point(the_geom,"+ str(fraccion)+ "))) from "  + tabla_vias + "\
                    where " + col_id_via + " = "+ str(lista_via[5])+ ";"
                    curs2.execute(cons_interpol)
                    lista_interpol = curs2.fetchall()
                    lista_interpol = lista_interpol[0]

                else:
                    #interpolation 1-l
                    #print '.............................caso sentido contrario :', fraccion, 1-fraccion
                    cons_interpol = "SELECT st_X(st_astext(ST_Line_Interpolate_Point(the_geom,"+ str(1-fraccion)+ "))), \
                    st_Y(st_astext(ST_Line_Interpolate_Point(the_geom,"+ str(1-fraccion)+ "))) from "  + tabla_vias + "\
                    where " + col_id_via + " = "+ str(lista_via[5])+ ";"
                    curs2.execute(cons_interpol)
                    lista_interpol = curs2.fetchall()
                    lista_interpol = lista_interpol[0]
                #print 'resultat de linterpolation', lista_interpol
                #print type(lista_interpol)

                #print 'long interpol : ', len(lista_interpol)
                if len(lista_interpol)<>0:

                    try:

                        #remp_geom= "UPDATE "+ tabla_direcciones +" set the_geom = ST_PointFromText('"+"POINT("+str(lista_interpol[0])+' '+\
                        #str(lista_interpol[1])+")', 32718) where "+col_id + " = "+str(i+1)+";"
                        #curs2.execute(remp_geom)
                        #print 'avant :', lista_interpol
                        entre_puntos(lista_via[6], lista_interpol)

                        #print 'apres :', lista_interpol

                        # La siguiente consulta pone un punto en el lugar de la interpolacion, sin movimiento al lado

                        #remp_geom= "UPDATE "+ tabla_dir_geom +" set the_geom = ST_PointFromText('"+"POINT("+str(lista_interpol[0])+' '+\
                        #str(lista_interpol[1])+")', 32718) where "+col_id + " = "+str(i+1)+";"
                        #curs2.execute(remp_geom)
                        #lista_remp_geom = curs2.fetchall()
                        #print lista_remp_geom



                        remp_geom= "UPDATE "+ tabla_dir_geom +" set the_geom = ST_PointFromText('"+"POINT("+str(X_decal)+' '+\
                        str(Y_decal)+")', 32718) where "+col_id + " = "+str(i+1)+";"
                        curs2.execute(remp_geom)
                        #print remp_geom
                        #print '*********************************************'



                        cons_deletelineas_bug = "DELETE FROM "+ tabla_dir_bug +" WHERE "+col_id + " = "+str(i+1)+";"
                        curs2.execute(cons_deletelineas_bug)

                        cons_deletelineas_multi = "DELETE FROM "+ tabla_dir_multi +" WHERE "+col_id + " = "+str(i+1)+";"
                        curs2.execute(cons_deletelineas_multi)






                    except:
                        pass

                else:
                    pass







        else: # si no tengo una cuadra no puedo localizar el punto
            pass

        del lista_via


    else:
        pass



    del cuadra, direccion



    i = i+1


print "*****************"
print "Creacion de las tablas finales"
# Aca selecciono todas las lineas que no tienen una geometria (las direcciones imposibles a localizar)
# para luego borrar las de la tabla.
busca_geom_vacio= "SELECT  "+ col_id + " from " + tabla_dir_geom +" where st_astext(the_geom) IS NULL;"
curs2.execute(busca_geom_vacio)
lista_busca_geom_vacio = curs2.fetchall()

construc_lista(lista_busca_geom_vacio)
lista_busca_geom_vacio.sort()

for e in lista_busca_geom_vacio:
    cons_deletelineas_vacias = "DELETE FROM "+ tabla_dir_geom +" WHERE "+col_id + " = "+str(e)+";"
    curs2.execute(cons_deletelineas_vacias)


extra_id_bug = "SELECT  "+ col_id + " from " + tabla_dir_bug +";"
curs2.execute(extra_id_bug)
lista_extra_id_bug = curs2.fetchall()

construc_lista(lista_extra_id_bug)
lista_extra_id_bug.sort()

extra_id_multi = "SELECT  "+ col_id + " from " + tabla_dir_multi +";"
curs2.execute(extra_id_multi)
lista_extra_id_multi = curs2.fetchall()

construc_lista(lista_extra_id_multi)
lista_extra_id_multi.sort()

for e in lista_extra_id_multi:
    if e in lista_extra_id_bug:
        cons_deletelineas_multi = "DELETE FROM "+ tabla_dir_multi +" WHERE "+col_id + " = "+str(e)+";"
        curs2.execute(cons_deletelineas_multi)


#######################################################
delete_imposible= "SELECT  "+ col_id + " from " + tabla_dir_imposible +";"
curs2.execute(delete_imposible)
lista_delete_imposible = curs2.fetchall()

construc_lista(lista_delete_imposible)
lista_delete_imposible.sort()

for e in lista_delete_imposible:
    cons_deletelineas_vacias = "DELETE FROM "+ tabla_dir_bug +" WHERE "+col_id + " = "+str(e)+";"
    curs2.execute(cons_deletelineas_vacias)


#######################################################


# Ahora tengo mis 2 tablas limpias. A continuacion hago una verificación para ver si no hay una direccion que se encuentra
# en las dos tablas y si la suma de las 2 tablas (geom + bug) = la tbla inicial de direcciones.


# Extraigo los id de la tabla geom y los id de la tabla bug para ver si todos estan diferentes
# y la suma de los 2 = el numero de los elementos iniciales

busca_geom= "SELECT  "+ col_id + " from " + tabla_dir_geom +";"
curs2.execute(busca_geom)
lista_busca_geom = curs2.fetchall()

construc_lista(lista_busca_geom)
lista_busca_geom.sort()

busca_bug= "SELECT  "+ col_id + " from " + tabla_dir_bug +";"
curs2.execute(busca_bug)
lista_busca_bug = curs2.fetchall()

construc_lista(lista_busca_bug)
lista_busca_bug.sort()


busca_multi= "SELECT  "+ col_id + " from " + tabla_dir_multi +";"
curs2.execute(busca_multi)
lista_busca_multi = curs2.fetchall()

construc_lista(lista_busca_multi)
lista_busca_multi.sort()

## nuevo
busca_imposible= "SELECT  "+ col_id + " from " + tabla_dir_imposible +";"
curs2.execute(busca_imposible)
lista_busca_imposible = curs2.fetchall()

construc_lista(lista_busca_imposible)
lista_busca_imposible.sort()


if len(lista_busca_geom) + len(lista_busca_bug) + len(lista_busca_multi) + len(lista_busca_imposible) == len(lista2):
    pass

else:
    print 'Hay un problema. Hay al menos una direccion que esta en varias tablas'


lista_dobles = []
for e in lista_busca_geom:
    if e in lista_busca_bug or e in lista_busca_multi or e in lista_busca_imposible:
        lista_dobles.append(e)

if len(lista_dobles) >0:
    print 'hay un problema con las direcciones :'
    for doble in lista_dobles:
        print dobles


conn2.commit()


## Export to shapefile



################################################################################
## Ending program
print "*****************"
print "Listo !"

print '*** Resumen ***'
print 'Sobre ',len(lista2),' direcciones :'
print '- ',len(lista_busca_geom), ' han sido localizadas'
print '- ',len(lista_busca_multi), ' necesitan que se edite la tabla de vias para poder ser localizadas'
print '- ',len(lista_busca_bug), ' no tienen su equivalente en la tabla de vias'
print '- ',len(lista_busca_imposible), ' no tienen un nombre o un numero y no pueden ser localizadas con este programa'
















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
