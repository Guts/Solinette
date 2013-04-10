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
from tkMessageBox import showerror, showinfo
from ttk import Combobox

from os import environ as env, path

# external library
import xlrd
import psycopg2 as pg

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

        # Frames
        self.FrPath = LabelFrame(self, name ='primero',
                            text = u'1: las direcciones para geolocalizar',
                            padx = 5, pady = 5)
        self.FrAttr = LabelFrame(self, name ='segundo',
                            text = u'2: columnas indispensables',
                            padx = 5, pady = 5)
        self.FrConn = LabelFrame(self, name ='tercero',
                            text = u'3: parámetros de conexión a la base de datos',
                            padx=5, pady=5)

        # Variables
        inutile = ['Esperando que se elige ela rchivo Excel']
        self.host = StringVar()
        self.port = IntVar()
        self.dbnb = StringVar()
        self.usua = StringVar()
        self.mdpa = StringVar()

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
        labdir.grid(row = 1, column = 1, sticky = N+S+W, padx = 2, pady = 2)
        self.ddl_dir.grid(row = 1, column = 2, sticky = N+S+W+E, padx = 2, pady = 2)
        labdis.grid(row = 2, column = 1, sticky = N+S+W, padx = 2, pady = 2)
        self.ddl_dis.grid(row = 2, column = 2, sticky = N+S+W+E, padx = 2, pady = 2)
        labtabl.grid(row = 3, column = 1, sticky = N+S+W, padx = 2, pady = 2)
        self.tabl.grid(row = 3, column = 2, sticky = N+S+W+E, padx = 2, pady = 2)

            ## Frame 3

        # Etiquetas
        Label(self.FrConn, text = u'Host: ').grid(row = 1, column = 1,
                                                  padx = 2, pady = 2,
                                                  sticky = N+S+W)
        Label(self.FrConn, text = u'Puerto: ').grid(row = 2, column = 1,
                                             padx = 2, pady = 2,
                                             sticky = N+S+W)
        Label(self.FrConn, text = u'Base de datos: ').grid(row = 3,
                                                    column = 1,
                                                    padx = 2,
                                                    pady = 2,
                                                    sticky = N+S+W)
        Label(self.FrConn, text = u'Usuario: ').grid(row = 4,
                                              column = 1,
                                              padx = 2,
                                              pady = 2,
                                              sticky = N+S+W)
        Label(self.FrConn, text = u'Contraseña: ').grid(row = 5,
                                                 column = 1,
                                                 padx = 2,
                                                 pady = 2,
                                                 sticky = N+S+W)

        # Formulario
        self.H = Entry(self.FrConn, textvariable = self.host)
        self.P = Entry(self.FrConn, textvariable = self.port)
        self.D = Entry(self.FrConn, textvariable = self.dbnb)
        self.U = Entry(self.FrConn, textvariable = self.usua)
        self.M = Entry(self.FrConn, textvariable = self.mdpa, show='*')
        # pre relleno
        self.host.set('localhost')
        self.port.set('5432')
        self.usua.set('postgres')
        # widgets placement
        self.H.grid(row = 1, column = 2, padx = 3, pady = 5, sticky = N+S+W+E)
        self.P.grid(row = 2, column = 2, padx = 3, pady = 5, sticky = N+S+W+E)
        self.D.grid(row = 3, column = 2, padx = 3, pady = 5, sticky = N+S+W+E)
        self.U.grid(row = 4, column = 2, padx = 3, pady = 5, sticky = N+S+W+E)
        self.M.grid(row = 5, column = 2, padx = 3, pady = 5, sticky = N+S+W+E)


            ## Global frame
        # Hola
        Label(self, text = '¡Hola! ' + env.get(u'USERNAME')).grid(row = 0, column = 0,
                                                 columnspan = 2, sticky = W+E,
                                                 padx = 2, pady = 5)
        # Imagen
        self.icone = PhotoImage(file = r'sources/logo_Solinette.GIF')
        Label(self, borderwidth = 2, relief = 'ridge',
                                     image = self.icone).grid(row = 1,
                                                              rowspan = 4,
                                                              column = 0,
                                                              padx = 1,
                                                              pady = 1,
                                                              sticky = W)

        # Basic buttons
        self.val = Button(self, text = u'Probar la conexión',
                                relief= 'raised',
                                command = self.process,
                                state = DISABLED)
        can = Button(self, text = 'Cancel (quit)',
                                relief= 'groove',
                                command = self.destroy)

        # widgets placement
        self.FrPath.grid(row = 2, column = 1, sticky = N+S+W+E, padx = 2, pady = 2)
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
            self.target.config(state=DISABLED)
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

    def check_campos(self):
        u""" Verifica que los campos del formulario son bien rellenos """
        # conteo y mensaje de los errores
        err = 0
        msj = u'Rellenar todos los campos'
        # checkeo de los campos vacios
        if self.host.get() == u'':
            self.H.configure(background = 'red')
            err = err +1
        if self.port.get() == 0:
            self.P.configure(background = 'red')
            err = err +1
        if self.dbnb.get() == u'':
            self.D.configure(background = 'red')
            err = err +1
        if self.usua.get() == u'':
            self.U.configure(background = 'red')
            err = err +1
        if self.mdpa.get() == u'':
            self.M.configure(background = 'red')
            err = err +1
        if self.tabl.get() == u'':
            self.tabl.configure(background = 'red')
            err = err +1
        if self.ddl_dir.get() == u'':
            self.ddl_dir.configure(background = 'red')
            err = err +1
        if self.ddl_dis.get() == u'':
            self.ddl_dis.configure(background = 'red')
            err = err +1
        # se colunas direcciones y distrito son diferentes
        if self.ddl_dir.get() == self.ddl_dis.get():
            msj = msj + u'\nLas dos columnas no deben ser iguales'
            err = err +1

        # Acción según si hay error(es) o no
        if err != 0:
            showerror(title = u'Error: campo(s) vacío(s)',
                      message = msj)
        # End of function
        return err

    def testconnexion(self):
        """ testing connection settings """
        try:
            conn = pg.connect(host = self.host.get(), dbname = self.dbnb.get(),
                              port = self.port.get(), user = self.usua.get(),
                              password = self.mdpa.get())
            # información al usuario
            showinfo(title = u'Prueba de conexión ',
                     message = u'Prueba de conexión terminó con éxito')
            self.val.conf(text='¡Dale!')
            print conn.server_version
            # clausura de la conexión
            conn.close()

        except pg.OperationalError, e:
            showerror(title = u'Prueba de conexión ',
                      message = 'Prueba de conexión fracasó. Mensaje de error:\n' + str(e))
            return

        except ImportError , e:
            return None

    def process(self):
        if self.check_campos() != 0:
            return
        self.testconnexion()
        return self.target.get(), self.ddl_dir.get(), self.ddl_dis.get(), \
                self.host.get(), self.port.get(), self.usua.get(), \
                self.mdpa.get(), self.dbnb.get(), self.tabl.get()

if __name__ == '__main__':
    app = Solinette()
    app.mainloop()

