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
        self.title(u'Solinette: geolocalizar direcciones en Lima y Callo')
        self.iconbitmap('icone_Solinette.ico')
        self.resizable(width = False, height = False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frames
        self.FrPath = LabelFrame(self,
                            text = u'1: las direcciones para geolocalizar',
                            padx = 5, pady = 5)
        self.FrAttr = LabelFrame(self,
                            text = u'2: columnas indispensables',
                            padx = 5, pady = 5)
        self.FrConn = LabelFrame(self,
                            text = u'3: parámetros de conexión a la base de datos',
                            padx=5, pady=5)


        # Variables
        inutile = ['Esperando que se elige ela rchivo Excel']



            ## Frame 1
        # target folder
        labtarg = Label(self.FrPath, text = u'Archivo Excel (.xls): ')
        self.target = Entry(self.FrPath, width = 35)
        self.browsetarg = Button(self.FrPath,
                                 text = 'Explorar',
                                 command = self.setpathtarg)

        # widgets placement
        labtarg.grid(row = 1, column = 1, columnspan = 1, sticky = N+S+W+E, padx = 2, pady = 2)
        self.target.grid(row = 1, column = 2, columnspan = 1, sticky = N+S+W+E, padx = 2, pady = 2)
        self.browsetarg.grid(row = 1, column = 3, columnspan = 1, sticky = N+S+W+E, padx = 2, pady = 2)

            ## Frame 2
        # Drop-down lists of columns
        labdir = Label(self.FrAttr, text = u'Columna dirección: ')
        self.ddl_dir = Combobox(self.FrAttr, values = inutile)
        labdis = Label(self.FrAttr, text = u'Columna distrito: ')
        self.ddl_dis = Combobox(self.FrAttr, values = inutile)

        # nombre de la tabla en PostgreSQL
        labtabl = Label(self.FrAttr, text = u'Nombre de la tabla: ')
        self.tabl = Entry(self.FrAttr, width = 35)

        # widgets placement
        labdir.grid(row = 1, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
        self.ddl_dir.grid(row = 1, column = 2, sticky = N+S+W+E, padx = 2, pady = 2)
        labdis.grid(row = 2, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
        self.ddl_dis.grid(row = 2, column = 2, sticky = N+S+W+E, padx = 2, pady = 2)
        labtabl.grid(row = 3, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
        self.tabl.grid(row = 3, column = 2, columnspan = 2, sticky = N+S+W+E, padx = 2, pady = 2)

            ## Frame 3
        settings = Button(self.FrConn,
                          text = 'Parametros de conexión a la base de datos PostgreSQL',
                          command = self.settings)


        # widgets placement
        settings.grid(row= 1, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)

            ## Global frame
        # Hola
        Label(self, text = 'Hola! '
                    + env.get(u'USERNAME')).grid(row = 0, column = 0,
                                                 columnspan = 2, sticky = W+E,
                                                 padx = 2, pady = 5)
        # Imagen
        self.icone = PhotoImage(file = r'sources/logo_Solinette.GIF')
        Label(self, borderwidth = 2, relief = 'ridge',
                                     image = self.icone).grid(row = 1,
                                                              rowspan = 5,
                                                              column = 0,
                                                              padx = 1,
                                                              pady = 1,
                                                              sticky = W)

        # Basic buttons
        self.val = Button(self, text = u'Dale!',
                                relief= 'raised',
                                command = self.bell,
                                state = DISABLED)
        can = Button(self, text = 'Cancel (quit)',
                                relief= 'groove',
                                command = self.destroy)

        # widgets placement
        self.FrPath.grid(row = 2, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
##        self.FrAttr.grid(row = 3, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
##        self.FrConn.grid(row = 4, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)

        self.val.grid(row = 5, column = 1, columnspan = 2,
                            sticky = N+S+W+E, padx = 2, pady = 5)
        can.grid(row = 5, column = 0, sticky = N+S+W+E, padx = 2, pady = 5)



    def setpathtarg(self):
        """ ...browse and insert the path of target folder """
        self.xls = askopenfilename(parent = self,
                                   title = u'Seleccionar el archivo Excel',
                                   filetypes = (("Archivos Excel (2003)", "*.xls"),
                                                ("All files", "*.*")),
                                   initialdir = '../Sources')

        if path.splitext(self.xls)[1] == '.xls':
            self.target.insert(0, self.xls)
            self.licolumns()
            self.browsetarg.config(state=DISABLED)
            self.FrAttr.grid(row = 3, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
            self.FrConn.grid(row = 4, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
            self.tabl.insert(0, path.basename(self.xls).split('.')[0])
            self.val.config(state = ACTIVE)
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

