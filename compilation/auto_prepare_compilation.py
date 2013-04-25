#!/usr/bin/python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     24/04/2013
# Copyright:   (c) Utilisateur 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

### importation
# standard library
import os
import sys
import shutil
import subprocess

### preparation
# creating a root-near directory
tmp = os.environ.get('TEMP')    # system temporary folder
os.mkdir(os.path.join(tmp, 'py_compilations'), 644)
dest = os.path.abspath(os.path.join(tmp, 'py_compilations'))
# creating sub-folders
os.mkdir(os.path.join(dest, 'temp'), 644)
os.mkdir(os.path.join(dest, 'sources'), 644)
# copying necesary files
shutil.copy2(r'..\Solinette.py', dest)
shutil.copy2(r'..\icone_Solinette.ico', dest)
shutil.copy2(r'setup_solinette.py', dest)
shutil.copy2(r'..\sources\logo_Solinette.GIF', os.path.join(dest, 'sources\\'))
shutil.copytree(r'..\modules\\', os.path.join(dest,  'modules'))


### Creating the executable (py2exe part)
os.chdir(dest)
sys.argv=["python", "setup_solinette.py","py2exe"]
execfile(dest + "\setup_solinette.py")


#### Finalizing
# zipping the final folder


# copying the zip archive


# removing work directory
os.chdir(tmp)
##try:
##    shutil.rmtree(dest)
##except Exception, e:
##    print e