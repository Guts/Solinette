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

class GUI_Solinette(Tk):
    u""" Interfaz gráfica para la la Solinette """
    def __init__(self):
        Tk.__init__(self)
        self.title(u"Parámetros de conexión a la base PostGIS")
        self.host = StringVar()
        self.port = IntVar()
        self.dbnb = StringVar()
        self.usua = StringVar()
        self.mdpa = StringVar()

        # Etiquetas
        Label(self, text=u'Parámetros de conexión a la base PostGIS').grid(row=0, column=1, columnspan=2)
        Label(self, text=u'Host: ').grid(row=1, column=1)
        Label(self, text=u'Puerto: ').grid(row=2, column=1)
        Label(self, text=u'Base de datos: ').grid(row=3, column=1)
        Label(self, text=u'Usuario: ').grid(row=4, column=1)
        Label(self, text=u'Contraseña: ').grid(row=5, column=1)

        # Formulario
        Entry(self, textvariable = self.host).grid(row=1, column=2)
        Entry(self, textvariable = self.port).grid(row=2, column=2)
        Entry(self, textvariable = self.dbnb).grid(row=3, column=2)
        Entry(self, textvariable = self.usua).grid(row=4, column=2)
        Entry(self, textvariable = self.mdpa, show='*').grid(row=5, column=2)
        # Validación
        Button(self, text = u'Conectarse', command=self.check_campos).grid(row=6, column=1, columnspan=2)

    def check_campos(self):
        u""" Verifica que los campos del formulario son bien rellenos """
        if self.host == u'':
            print u'Host invalide'
        print 'check'






if __name__ == '__main__':
    test = GUI_Solinette()
    test.mainloop()


