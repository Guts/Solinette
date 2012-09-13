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

class GUI_Solinette:
    u""" Interfaz gráfica para la la Solinette """
    def __init__(self):
        # inicialización ventana
        self.root = Tk()
        # Parámetros ventana
        self.root.title(u"Parámetros de conexión a la base PostGIS")
        self.root.iconbitmap('Icone_Solinette.ico')
        self.root.resizable(width = False, height = False)
        self.root.geometry("350x200+300+0")

        # Variables
        self.root.host = StringVar()
        self.root.port = IntVar()
        self.root.dbnb = StringVar()
        self.root.usua = StringVar()
        self.root.mdpa = StringVar()

        # Etiquetas
        Label(self.root,
              text = u'CONEXIÓN A LA BASE POSTGIS').grid(row = 0,
                                                         column = 0,
                                                         columnspan = 3,
                                                         padx = 2,
                                                         pady = 2,
                                                         sticky = N+W+S+E)
        Label(self.root, text = u'Host: ').grid(row = 1,
                                           column = 1,
                                           padx = 2,
                                           pady = 2,
                                           sticky = W)
        Label(self.root, text = u'Puerto: ').grid(row = 2,
                                             column = 1,
                                             padx = 2,
                                             pady = 2,
                                             sticky = W)
        Label(self.root, text = u'Base de datos: ').grid(row = 3,
                                                    column = 1,
                                                    padx = 2,
                                                    pady = 2,
                                                    sticky = W)
        Label(self.root, text = u'Usuario: ').grid(row = 4,
                                              column = 1,
                                              padx = 2,
                                              pady = 2,
                                              sticky = W)
        Label(self.root, text = u'Contraseña: ').grid(row = 5,
                                                 column = 1,
                                                 padx = 2,
                                                 pady = 2,
                                                 sticky = W)

        # Formulario
        self.root.H = Entry(self.root, textvariable = self.root.host)
        self.root.H.grid(row = 1,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.root.P = Entry(self.root, textvariable = self.root.port)
        self.root.P.delete(0, END)
        self.root.P.insert(0, 5432)
        self.root.P.grid(row = 2,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.root.D = Entry(self.root, textvariable = self.root.dbnb)
        self.root.D.grid(row = 3,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.root.U = Entry(self.root, textvariable = self.root.usua)
        self.root.U.insert(0, 'postgres')
        self.root.U.grid(row = 4,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        self.root.M = Entry(self.root, textvariable = self.root.mdpa, show='*')
        self.root.M.grid(row = 5,
                    column = 2,
                    padx = 2,
                    pady = 2,
                    sticky = W+E)
        # Imagen
        self.root.icone = PhotoImage(file = r'Sources\Icone_Solinette.GIF')
        Label(self.root, borderwidth = 2,
                    relief = 'ridge',
                    image = self.root.icone).grid(row = 1,
                                             rowspan = 5,
                                             column = 0,
                                             padx = 2,
                                             pady = 2,
                                             sticky = W)

        # Validación
        Button(self.root, text = u'Conectarse',
                     relief='groove',
                     borderwidth = 3,
                     command=self.check_campos).grid(row = 6,
                                                     column = 1,
                                                     columnspan = 2,
                                                     padx = 2,
                                                     pady = 2,
                                                     sticky = N+W+S+E)
        # Inicialización
        self.root.mainloop()

    def check_campos():
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
            print 'champ(s) non rempli(s)'
        else:
            renvoi()

    def renvoi():
        host = self.host.get()
        # Fin de fonction
        return host




if __name__ == '__main__':
    from Tkinter import *
    test = GUI_Solinette()


