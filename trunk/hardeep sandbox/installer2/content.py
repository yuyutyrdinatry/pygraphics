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

#===============================================================================
# Python (win32)
#===============================================================================
python_file = 'python-2.5.2.msi'
python_path = os.path.join('D:\\', 'workspace', 'PyGraphics', 'hardeep sandbox', 
                           'installer2', 'install_data', python_file)
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
wing_file = 'wingide-101-3.1.2-1.exe'
wing_path = os.path.join('D:\\', 'workspace', 'PyGraphics', 'hardeep sandbox', 
                         'installer2', 'install_data', wing_file)
wing_cmds = {}
wing_cmds['nsis_install'] = '"%(PATH)s\%(FILE)s" /SILENT /DIR="%(PATH)s\wingide"' % {'PATH' : INSTALL_DIR,'FILE' : wing_file}
wing_cmds['post_install'] = 'DEL::%(PATH)s\%(FILE)s' % {'PATH' : INSTALL_DIR, 'FILE' : wing_file}
                            
DO.add_data('WingIDE 101', wing_path, OS_WIN, cmds=wing_cmds)

#===============================================================================
# Python Modules
#===============================================================================
nose_path = os.path.join('D:\\', 'workspace', 'PyGraphics', 'hardeep sandbox',
                         'installer2', 'install_data', 'nose-0.10.3')
DO.add_data('Nose 0.10.3', nose_path, OS_ALL, recurse=True, 
            cmds={'PYTHON_MODULE_SRC' : 0}, required=True)

PIL_path = os.path.join('D:\\', 'workspace', 'PyGraphics', 'hardeep sandbox',
                         'installer2', 'install_data', 'Imaging-1.1.6', 'Imaging-1.1.6')
DO.add_data('Python Imaging Library 1.1.6', PIL_path, OS_ALL, recurse=True, 
            cmds={'PYTHON_MODULE_SRC' : 0}, required=True)