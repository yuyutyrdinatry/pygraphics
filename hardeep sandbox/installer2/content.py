#===============================================================================
# Do NOT modify these!
import os
import sys
from itools import *

DO = DataObjects()

OS_CURR = sys.platform
OS_WIN = 'win32'
OS_MAC = 'darwin'
OS_ALL = -1

INSTALL_DIR = '$INSTDIR'
#===============================================================================

#### SEE README.txt FOR USAGE ####

install_data_path = os.path.join('D:\\', 'workspace', 'hardeep sandbox', 'installer2', 'data') 

#===============================================================================
# Python (win32)
#===============================================================================
python_file = 'python-2.5.2.msi'
python_path =  os.path.join(install_data_path, python_file)
python_cmds = {}
python_cmds['nsis_install'] = 'msiexec /i "%(PATH)s\%(FILE)s" /qb! /log "%(PATH)s\python_install.log" TARGETDIR="%(PATH)s\python"' % {'PATH' : INSTALL_DIR, 'FILE' : python_file}

# These execute in order appended.
python_cmds['post_install'] = []
python_cmds['post_install'].append('ENV::A::PATH::%(PATH)s\python' % {'PATH' : INSTALL_DIR})
python_cmds['post_install'].append('DEL::%(PATH)s\%(FILE)s' % {'PATH' : INSTALL_DIR, 'FILE' : python_file})
                              
DO.add_data('Python', python_path, OS_WIN, cmds=python_cmds, required=True)

#===============================================================================
# WingIDE (win32)
#===============================================================================
wing_file = 'wingide-101-3.1.3-1.exe'
wing_path = os.path.join(install_data_path, wing_file)
wing_cmds = {}
wing_cmds['nsis_install'] = '"%(PATH)s\%(FILE)s" /SILENT /DIR="%(PATH)s\wingide"' % {'PATH' : INSTALL_DIR,'FILE' : wing_file}
wing_cmds['post_install'] = 'DEL::%(PATH)s\%(FILE)s' % {'PATH' : INSTALL_DIR, 'FILE' : wing_file}
                            
DO.add_data('WingIDE 101', wing_path, OS_WIN, cmds=wing_cmds)

#===============================================================================
# Python Modules (temp solution)
# This method is being used for now until I can get compilation with visual
# studio working again. It's kind of hacky...but it works.
#===============================================================================
path = os.path.join(install_data_path, 'python')
DO.add_data('Required Python Modules', path, OS_ALL, recurse=True, 
            cmds={'PYTHON_DATA_COPY' : 0}, required=True)

##===============================================================================
## Python Modules
## Note that the path must be the path in which the setup.py file resides.
##===============================================================================
#
##-------------------------------------------------------------------------- Nose
#nose_path = os.path.join(install_data_path, 'nose-0.10.3')
#DO.add_data('Nose 0.10.3', nose_path, OS_ALL, recurse=True, 
#            cmds={'PYTHON_MODULE_SRC' : 0}, required=True)
#
##-------------------------------------------------------- Python Imaging Library
## Unfortunately, PIL is a special case and either needs to be pre-compiled
## with Visual Studio...or we distribute the .exe they give us. And I don't have
## Visual Studio at the moment to compile it with :/
#PIL_file = 'PIL-1.1.6.win32-py2.5.exe'
#PIL_path = os.path.join(install_data_path, PIL_file)
#PIL_cmds = {}
#PIL_cmds['nsis_install'] = '"%(PATH)s\%(FILE)s" /SILENT' % {'PATH' : INSTALL_DIR,'FILE' : PIL_file}
#PIL_cmds['post_install'] = 'DEL::%(PATH)s\%(FILE)s' % {'PATH' : INSTALL_DIR, 'FILE' : PIL_file}
#                            
#DO.add_data('Python Imaging Library 1.1.6', PIL_path, OS_WIN, cmds=PIL_cmds, required=True)