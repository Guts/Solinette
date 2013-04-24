#!/usr/bin/python
#-*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
import os
import sys
import subprocess
import shutil
from glob import glob
import modulefinder
from ..modules import Solinette_main
##mfcdir = r'C:\Python27\Lib\site-packages\pythonwin'
##mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", "Microsoft.VC90.MFC.manifest"]]

includes = ["encodings",
            "encodings.utf_8",
            ]

packages = r'C:\Documents and Settings\Utilisateur\Mes documents\GitHub\Solinette\modules\SolinetteGUI'

py2exe_options = dict(
                      packages = packages,
                      compressed=True,  # Compress library.zip
                      optimize = 2
                      )
setup(
    name="Solinette",
    version="1.5.1",
    description=u"Geocoding for Lima and Callao",
    author="Julien Moura et Pierre Vernier",
    license="license GPL v3.0",
    data_files = [("documentacion",["../documentation/Instalacion_PostGIS_UsoSolinette_ES.docx"])],
    options={'py2exe': py2exe_options},
    windows = [
        {
            "script": "../Solinette.py",                    ### Main Python script
            "icon_resources": [(1, "../icone_Solinette.ico")]     ### Icon to embed into the PE file.
        }
              ],
    )