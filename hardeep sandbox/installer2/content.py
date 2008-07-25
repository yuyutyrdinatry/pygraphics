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
python_cmds['nsis_install'] = '"%(PATH)s\%(FILE)s" /qb! /log ' + \
                              '"%(PATH)s\python_install.log" TARGETDIR=' + \
                              '"%(PATH)s\python"' % {'PATH' : INSTALL_DIR, \
                                                     'FILE' : python_file}

# These execute in order appended.
python_cmds['post_install'] = []
python_cmds['post_install'].append('SETENV PATH %(PATH)s\python' % \
                                   {'PATH' : '%PATH%;' + INSTALL_DIR})
python_cmds['post_install'].append('DEL %(PATH)s\%(FILE)s' % \
                                   {'PATH' : INSTALL_DIR, 
                                    'FILE' : python_file})
                              
DO.add_data('Python', python_path, OS_WIN, cmds=python_cmds, main=True)

#===============================================================================
# WingIDE (win32)
#===============================================================================
wing_file = 'wingide-101-3.1.2-1.exe'
wing_path = os.path.join('D:\\', 'workspace', 'PyGraphics', 'hardeep sandbox', 
                    'installer2', 'install_data', wing_file)
wing_cmds = {}
wing_cmds['nsis_install'] = '"%(PATH)s\%(FILE)s" /SILENT /DIR=' + \
                            '"%(PATH)s\wingide"' % {'PATH' : INSTALL_DIR,
                                                   'FILE' : python_file}
wing_cmds['post_install'] = 'DEL %(PATH)s\%(FILE)s' % {'PATH' : INSTALL_DIR, 
                                                     'FILE' : wing_file}
                            
DO.add_data('WingIDE 101', wing_path, OS_WIN, cmds=wing_cmds)