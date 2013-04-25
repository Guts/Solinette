#!/usr/bin/python
#-*- coding: utf-8 -*-

### importation
# standard library
from distutils.core import setup
import os
import sys
import subprocess
import shutil
from glob import glob

# third-party library
import py2exe

# custom modules
from modules import *

# options
py2exe_options = dict(
                      compressed=True,  # Compress library.zip
                      optimize = 2,
                      dist_dir = 'Solinette'
                      )
# setup settings
setup(
    name="Solinette",
    version="1.5.1",
    description=u"Geocoding for Lima and Callao",
    author="Julien Moura et Pierre Vernier",
    author_mail = "julien.moura@gmail.com",
    url = "https://github.com/Guts/Solinette",
    license="license GPL v3.0",
    data_files = [("temp", []),("", ["icone_Solinette.ico"]),("sources", ["sources/logo_Solinette.GIF"]),("documentacion",["documentation/Instalacion_PostGIS_UsoSolinette_ES.docx"])],
    options={'py2exe': py2exe_options},
    windows = [
        {
            "script": "Solinette.py",                    ### Main Python script
            "icon_resources": [(1, "icone_Solinette.ico")]     ### Icon to embed into the PE file.
        }
              ],
    )
