# Configuration options for the installer. Make sure all settings contained
# within this file, especially paths, are correct!

#===============================================================================
# Imports. Do NOT modify these!
import os
import sys
#===============================================================================

#===============================================================================
# General Installer Settings
#===============================================================================
INST_NAME = 'UofT CS Python Package'
INST_FILE = 'uoft_installer' # Will automatically append .exe/.pkg/etc...

#===============================================================================
# Windows Settings
#===============================================================================
WIN_PATH_NSIS = os.path.join('c:\\', 'Program Files', 'NSIS')
WIN_PATH_DEFAULT_INSTALL = "$PROGRAMFILES\uoft"

#===============================================================================
# Mac Settings
#===============================================================================