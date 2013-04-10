# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien Moura, Pierre Vernier
#
# Created:     09/04/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

###################################
##### Libraries importation #######
###################################

# standard library
from Tkinter import *    # GUI modules
from tkFileDialog import askopenfilename
from tkMessageBox import showerror
from ttk import Combobox

from os import environ as env, path

# external library
import xlrd

from modules import *

###################################
####### Classes definition ########
###################################

class Solinette(Tk):
    def __init__(self):
        # basics settings
        Tk.__init__(self)               # constructor of parent graphic class
        inutile = ['Esperando que se elige ela rchivo Excel']
        # Hola
        Label(self, text = 'Hola! '
                    + env.get(u'USERNAME')).grid(row = 0, column = 0,
                                                 columnspan = 2, sticky = N+S+W+E,
                                                 padx = 2, pady = 1)
        # target folder
        labtarg = Label(self, text = u'Archivo Excel (.xls): ')
        self.target = Entry(self, width = 35)
        self.browsetarg = Button(self,
                                 text = 'Explorar',
                                 command = self.setpathtarg)

        # Drop-down lists of columns
        labdir = Label(self, text = u'Columna dirección: ')
        self.ddl_dir = Combobox(self, values = inutile)
##        self.ddl_dir.current(0)
        labdis = Label(self, text = u'Columna distrito: ')
        self.ddl_dis = Combobox(self, values = inutile)

        # nombre de la tabla en PostgreSQL
        labtabl = Label(self, text = u'Nombre de la tabla: ')
        self.tabl = Entry(self, width = 35)

        # Basic buttons
        settings = Button(self,
                          text = 'Parametros de conexión a la base de datos PostgreSQL',
                          command = self.settings)

        self.val = Button(self, text = u'Dale!',
                                relief= 'raised',
                                command = self.bell)
        can = Button(self, text = 'Cancel (quit)',
                                relief= 'groove',
                                command = self.destroy)

        # widgets placement
        labtarg.grid(row = 1, column = 1, columnspan = 1)
        self.target.grid(row = 1, column = 2, columnspan = 1)
        self.browsetarg.grid(row = 1, column = 3, columnspan = 1)
        labdir.grid(row = 2, column = 1)
        self.ddl_dir.grid(row = 2, column = 2)
        labdis.grid(row = 3, column = 1)
        self.ddl_dis.grid(row = 3, column = 2)
        labtabl.grid(row = 4, column = 1)
        self.tabl.grid(row = 4, column = 2, columnspan = 2)
        self.val.grid(row = 5, column = 1, columnspan = 2,
                            sticky = N+S+W+E, padx = 2, pady = 5)
        can.grid(row = 5, column = 3, sticky = N+S+W+E, padx = 2, pady = 5)

        settings.grid(row= 7, column = 1)

    def setpathtarg(self):
        """ ...browse and insert the path of target folder """
        self.xls = askopenfilename(parent = self,
                                   title = u'Seleccionar el archivo Excel',
                                   filetypes = (("Archivos Excel (2003)", "*.xls"),
                                                ("All files", "*.*")),
                                   initialdir = '../Sources')

        if path.splitext(self.xls)[1] == '.xls':
##            try:
            self.target.insert(0, self.xls)
            self.licolumns()
            self.tabl.insert(0, path.basename(self.xls).split('.')[0])
##            except:
##                showerror(title = 'Error de archivo',
##                          message = u'Ningun archivo indicado')
        # end of function
        return self.xls

    def licolumns(self):
        book = xlrd.open_workbook(self.target.get())   # lectura del archivo
        if book.nsheets > 1:
            print book.sheets()
        ish = 0
        sheet = book.sheet_by_index(ish)    # ouverture de la feuille 1
        cols = [sheet.cell(0, cl).value for cl in range(sheet.ncols)]
        self.ddl_dir['values'] = cols
        self.ddl_dis['values'] = cols
        # End of function
        return


    def settings(self):
        params = SolinetteGUI()
        print params.renvoi.h
        return params.renvoi()

if __name__ == '__main__':
    app = Solinette()
    app.mainloop()

