#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Julien M.
#
# Created:     05/09/2012
# Copyright:   G. Swinnen
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import psycopg2, sys

class GestionBD:
    u"""Mise en place et interfaçage d'une base de données MySQL"""
    def __init__(self, dbName, user, passwd, host, port =3306):
        u"""Établissement de la connexion - Création du curseur"""
        try:
            self.baseDonn = MySQLdb.connect(db =dbName,
                                            user =user,
                                            passwd =passwd,
                                            host =host,
                                            port =port)
        except Exception, err:
            print 'La connexion avec la base de données a échoué :\n'\
                  'Erreur détectée :\n%s' % err
            self.echec =1
        else:
            self.cursor = self.baseDonn.cursor() # création du curseur
            self.echec = 0

    def creerTables(self, dicTables):
        u"""Création des tables décrites dans le dictionnaire <dicTables>."""
        for table in dicTables: # parcours des clés du dict.
            req = "CREATE TABLE %s (" % table
            pk =''
            for descr in dicTables[table]:
                nomChamp = descr[0] # libellé du champ à créer
                tch = descr[1] # type de champ à créer
                if tch =='i':
                    typeChamp ='INTEGER'
                elif tch =='k':
                    # champ 'clé primaire' (incrémenté automatiquement)
                    typeChamp ='INTEGER AUTO_INCREMENT'
                    pk = nomChamp
                else:
                    typeChamp ='VARCHAR(%s)' % tch
                    req = req + "%s %s, " % (nomChamp, typeChamp)
            if pk == '':
                req = req[:-2] + ")"
            else:
                req = req + "CONSTRAINT %s_pk PRIMARY KEY(%s))" % (pk, pk)
            self.executerReq(req)

    def supprimerTables(self, dicTables):
        u"""Suppression de toutes les tables décrites dans <dicTables>"""
        for table in dicTables.keys():
            req ="DROP TABLE %s" % table
            self.executerReq(req)
        self.commit() # transfert -> disque

    def executerReq(self, req):
        u"""Exécution de la requête <req>, avec détection d'erreur éventuelle"""
        try:
            self.cursor.execute(req)
        except Exception, err:
            # afficher la requête et le message d'erreur système :
            print "Requête SQL incorrecte :\n%s\nErreur détectée :\n%s"\
                   % (req, err)
            return 0
        else:
            return 1

    def resultatReq(self):
        u"""renvoie le résultat de la requête précédente (un tuple de tuples)"""
        return self.cursor.fetchall()

    def commit(self):
        if self.baseDonn:
            self.baseDonn.commit() # transfert curseur -> disque

    def close(self):
        if self.baseDonn:
            self.baseDonn.close()