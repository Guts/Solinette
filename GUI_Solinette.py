#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien M.
#
# Created:     03/09/2012
# Updated:
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from Tkinter import *
from re import compile, IGNORECASE          # expressions régulières

class GUI_Solinette(Tk):
    u""" Interfaz gráfica para la la Solinette """
    def __init__(self):
        Tk.__init__(self)
        self.title(u"Parámetros de conexión a la base PostGIS")
        self.iconbitmap('Icone_Solinette.ico')
        self.resizable(width = False, height = False)
        self.geometry("350x200+300+0")
        self.host = StringVar()
        self.port = IntVar()
        self.dbnb = StringVar()
        self.usua = StringVar()
        self.mdpa = StringVar()

        # Etiquetas
        Label(self,
              text = u'CONEXIÓN A LA BASE POSTGIS').grid(row = 0,
                                                         column = 1,
                                                         columnspan = 2,
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
        self.H.grid(row = 1,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.P = Entry(self, textvariable = self.port)
        self.P.grid(row = 2,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.D = Entry(self, textvariable = self.dbnb)
        self.D.grid(row = 3,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.U = Entry(self, textvariable = self.usua)
        self.U.grid(row = 4,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.M = Entry(self, textvariable = self.mdpa, show='*')
        self.M.grid(row = 5,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = E+W)
        # Imagen
        self.icone = PhotoImage(file = r'Sources\Icone_Solinette.GIF')
        Label(self, borderwidth = 2,
                    relief = 'ridge',
                    image = self.icone).grid(row = 1,
                                             rowspan = 5,
                                             column = 0,
                                             padx = 2,
                                             pady = 2,
                                             sticky = W)

        # Validación
        Button(self, text = u'Conectarse',
                     relief='groove',
                     borderwidth = 3,
                     command=self.check_campos).grid(row = 6,
                                                     column = 1,
                                                     columnspan = 2,
                                                     padx = 2,
                                                     pady = 2,
                                                     sticky = N+W+S+E)

    def check_campos(self):
        u""" Verifica que los campos del formulario son bien rellenos """
        renum = compile('[0:9]')
        if self.host.get() == u'':
            self.H.configure(background = 'red')
        if self.port.get() == 0:
            self.P.configure(background = 'red')
        if self.dbnb.get() == u'':
            self.D.configure(background = 'red')
        if self.usua.get() == u'':
            self.U.configure(background = 'red')
        if self.mdpa.get() == u'':
            self.M.configure(background = 'red')
        print 'check'






if __name__ == '__main__':
    test = GUI_Solinette()
    test.mainloop()


