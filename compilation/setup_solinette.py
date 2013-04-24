#!/usr/bin/python
#-*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
import os
import sys
import subprocess
import shutil
from glob import glob

#### si le fichier bundlepmw.py contient l'importation regsub (qui n'existe plus depuis la version 2.5 de Python)
#### Vous pouvez sinon le faire à la main en remplaçant "regsub" par "re" et "gsub" par "sub"
##fp = open(sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/bin/bundlepmw.py")
##a = fp.read().replace("regsub", "re").replace("gsub", "sub")
##fp.close()
##ft = open(sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/bin/bundlepmw.py", "w")
##ft.write(a)
##ft.close()

#### Création du fichier Pmw.py dans le répertoire courant
##subprocess.call([sys.executable, sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/bin/bundlepmw.py",
##                 sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/lib"])
#### On copie les 2 fichiers PmwBlt.py et PmwColor.py dans le répertoire courant
##shutil.copyfile(sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/lib/PmwBlt.py", "PmwBlt.py")
##shutil.copyfile(sys.prefix + os.sep + "Lib/site-packages/Pmw/Pmw_1_3/lib/PmwColor.py", "PmwColor.py")

mfcdir = r'C:\Python27\Lib\site-packages\pythonwin'
mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", "Microsoft.VC90.MFC.manifest"]]

includes = ["encodings",
            "encodings.utf_8"]

py2exe_options = dict(
                      includes = includes,
                      dll_excludes = ['MSVCP90.dll'],
                      packages = '..\Solinette_main.py',
                      compressed=True,  # Compress library.zip
                      optimize = 2
                      )
setup(
    name="Metadator",
    version="1.9",
    description=u"Automatisation de la création de fiches de métadonnées pour les fichiers shapefiles",
    author="Julien M.",
    license="license GPL v3.0",
    data_files=[("Microsoft.VC90.MFC", mfcfiles)],
    options={'py2exe': py2exe_options},
    windows = [
        {
            "script": "../Solinette.py",                    ### Main Python script
            "icon_resources": [(1, "../icone_Solinette.ico")]     ### Icon to embed into the PE file.
        }
              ],
    )