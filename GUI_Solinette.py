# -*- coding: UTF-8 -*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Julien M.
#
# Created:     03/09/2012
# Updated:
#-------------------------------------------------------------------------------


###################################
##### Libraries importation #######
###################################

# standard library
from Tkinter import *
from tkMessageBox import showerror

# third party

###################################
####### Classes definition ########
###################################

class SolinetteGUI(Tk):
    u""" Interfaz gráfica para la la Solinette """
    def __init__(self):
        # basicos
        Tk.__init__(self)   # constructor of parent graphic class
        self.title(u'Parámetros de conexión a la base PostGIS')
        self.iconbitmap('Icone_Solinette.ico')
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

        # Imagen
        self.icone = PhotoImage(file = r'sources\Icone_Solinette.GIF')
        Label(self, borderwidth = 2, relief = 'ridge',
                                     image = self.icone).grid(row = 1,
                                                              rowspan = 5,
                                                              column = 0,
                                                              padx = 2,
                                                              pady = 2,
                                                              sticky = W)
        # Validación
        Button(self, text = u'Conectarse',
                     relief='ridge',
                     borderwidth = 3,
                     command=self.check_campos).grid(row = 6,
                                                     column = 1,
                                                     columnspan = 2,
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
        for widget in self.children:
            print widget.name
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
        else:
            renvoi()

    def renvoi():
        host = self.host.get()
        # Fin de fonction
        return host


###################################
### Main program initialization ###
###################################

if __name__ == '__main__':
    app = SolinetteGUI()
    app.mainloop()


