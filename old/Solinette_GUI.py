# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         Solinette_GUI
# Purpose:      Graphic User Interface for Solinette.
#               Allows a more user-friendly usage.
# Author:       Julien Moura
# Python:       2.7.x
# Created:      03/09/2012
# Updated:      22/03/2013
#-------------------------------------------------------------------------------


###################################
##### Libraries importation #######
###################################

# standard library
from Tkinter import *
from tkMessageBox import showerror, showinfo

# external library
import psycopg2 as pg

###################################
####### Classes definition ########
###################################

class SolinetteGUI(Toplevel):
    u""" Interfaz gráfica para la la Solinette """
    def __init__(self):
        # basicos
        Toplevel.__init__(self)   # constructor of parent graphic class
        self.title(u'Parámetros de conexión a la base PostGIS')
##        self.iconbitmap('../icone_Solinette.ico')
        self.resizable(width = False, height = False)
        self.geometry("350x200+300+0")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Variables
        self.host = StringVar()
        self.port = IntVar()
        self.dbnb = StringVar()
        self.usua = StringVar()
        self.mdpa = StringVar()
        # Etiquetas
        Label(self, text = u'CONEXIÓN A LA BASE POSTGIS').grid(row = 0,
                                                               column = 0,
                                                               columnspan = 3,
                                                               padx = 2,
                                                               pady = 2,
                                                               sticky = N+W+S+E)
        Label(self, text = u'Host: ').grid(row = 1,
                                           column = 1,
                                           padx = 2,
                                           pady = 2,
                                           sticky = W)
        Label(self, text = u'Puerto: ').grid(row = 2,
                                             column = 1,
                                             padx = 2,
                                             pady = 2,
                                             sticky = W)
        Label(self, text = u'Base de datos: ').grid(row = 3,
                                                    column = 1,
                                                    padx = 2,
                                                    pady = 2,
                                                    sticky = W)
        Label(self, text = u'Usuario: ').grid(row = 4,
                                              column = 1,
                                              padx = 2,
                                              pady = 2,
                                              sticky = W)
        Label(self, text = u'Contraseña: ').grid(row = 5,
                                                 column = 1,
                                                 padx = 2,
                                                 pady = 2,
                                                 sticky = W)

        # Formulario
        self.H = Entry(self, textvariable = self.host)
        self.P = Entry(self, textvariable = self.port)
        self.D = Entry(self, textvariable = self.dbnb)
        self.U = Entry(self, textvariable = self.usua)
        self.M = Entry(self, textvariable = self.mdpa, show='*')

##        # Imagen
##        self.icone = PhotoImage(file = r'..\sources\Icone_Solinette.GIF')
##        Label(self, borderwidth = 2, relief = 'ridge',
##                                     image = self.icone).grid(row = 1,
##                                                              rowspan = 5,
##                                                              column = 0,
##                                                              padx = 1,
##                                                              pady = 1,
##                                                              sticky = W)
        # Botones básicos
        Button(self, text = u'Cancelar',
                     relief = 'flat',
                     command = self.destroy).grid(row = 6,
                                                  column = 0,
                                                  padx = 5,
                                                  pady = 5,
                                                  sticky = N+W+S+E)

        Button(self, text = u'Probar la conexión',
                     relief = 'groove',
                     command = self.testconnexion).grid(row = 6,
                                                        column = 1,
                                                        padx = 2,
                                                        pady = 2,
                                                        sticky = N+W+S+E)

        Button(self, text = u'Conectarse',
                     relief='ridge',
                     borderwidth = 3,
                     command=self.check_campos).grid(row = 6,
                                                     column = 2,
                                                     columnspan = 1,
                                                     padx = 2,
                                                     pady = 2,
                                                     sticky = N+W+S+E)



        # pre relleno
        self.H.insert(0, 'localhost')
        self.P.delete(0, END)
        self.P.insert(0, '5432')
        self.U.insert(0, 'postgres')

        # organización de los elementos
        self.H.grid(row = 1, column = 2, padx = 2, pady = 2, sticky = W+E)
        self.P.grid(row = 2, column = 2, padx = 2, pady = 2, sticky = W+E)
        self.D.grid(row = 3, column = 2, padx = 2, pady = 2, sticky = W+E)
        self.U.grid(row = 4, column = 2, padx = 2, pady = 2, sticky = W+E)
        self.M.grid(row = 5, column = 2, padx = 2, pady = 2, sticky = W+E)

    def check_campos(self):
        u""" Verifica que los campos del formulario son bien rellenos """
        # conteo de los errores
        err = 0

        # checkeo de los campos
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

        # Acción según si hay error(es) o no
        if err != 0:
            showerror(title = u'Error: campo(s) vacío(s)',
                      message = u'Rellenar todos los campos')
            return err
        else:
##             self.host, self.port, self.mdpa, self.dbnb, self.usua
            return



    def testconnexion(self):
        """ testing connection settings """
        if self.check_campos() != 0:
            return
        try:
            conn = pg.connect(host = self.host.get(), dbname = self.dbnb.get(),
                              port = self.port.get(), user = self.usua.get(),
                              password = self.mdpa.get())
            # información al usuario
            showinfo(title = u'Prueba de conexión ',
                     message = u'Prueba de conexión terminó con éxito')
            # clausura de la conexión
            conn.close()

        except pg.OperationalError, e:
            showerror(title = u'Prueba de conexión ',
                      message = 'Prueba de conexión fracasó. Mensaje de error:\n' + str(e))
            return

        except ImportError , e:
            return None


    def renvoi(self):
        """ final function """
        h = self.host.get()
        p = self.port.get()
        db = self.dbnb.get()
        u = self.usua.get()
        m = self.mdpa.get()
        # Fin de fonction
        return h, p, db, u, m

###################################
### Main program initialization ###
###################################

if __name__ == '__main__':
    app = Tk()
    app.withdraw()
    SolinetteGUI()
    app.mainloop()


