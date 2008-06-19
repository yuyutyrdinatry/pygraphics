# This script executes after all the data has been copied over and Python has
# been installed.

import os
from subprocess import call

#===============================================================================
# Parse (do not modify)
#===============================================================================
root_path = "$INSTALL_PATH"
#root_path = "C:\\Program Files\\UofT CSC Dev Pack 2008" # testing only
debug = True

#===============================================================================
# Config (edit as needed)
#===============================================================================
wing_file = {}
wing_file['win'] = 'wingide-101-3.1.1-1.exe'
wing_file['mac'] = 'wingide-101-3.1.1-1-i386.dmg'

python_path = {}
python_path['win'] = os.path.join('c:\\', 'Python25') # default python install location
python_path['mac'] = os.path.join('usr', 'bin') # probably same as linux...not sure

mod_path = {}
mod_path['nose'] = os.path.join(root_path, 'nose', 'setup.py')
mod_path['PIL'] = os.path.join(root_path, 'PIL', 'setup.py')
mod_path['PyG'] = os.path.join(root_path, 'PyGraphics', 'setup.py')

# ---------------------------------------------------------------------------- #
# You shouldn't need to edit below this line
# ---------------------------------------------------------------------------- #

if ( debug ):
    print 'root_path', root_path
    print 'wing_file', wing_file
    print 'python_path', python_path
    print 'mod_path', mod_path

#===============================================================================
# Install Wing
#===============================================================================
if ( os.name == 'nt' ): #Windows
    install_path = os.path.join(root_path, "wing-ide")
    if ( debug ):
        print 'wing cmd ::', os.path.join(root_path, 'wing', 'win', wing_file['win']), '/SILENT /dir=%s' % install_path
        print 'install_path', install_path
    call([os.path.join(root_path, 'wing', 'win', wing_file['win']), '/SILENT /dir=%s' % install_path])
elif ( os.name == 'mac' ): #MacOS
    if ( debug ):
        print 'wing cmd ::', os.path.join(root_path, 'wing', 'mac', wing_file['mac'])
    call([os.path.join(root_path, 'wing', 'mac', wing_file['mac'])]) # Figure out if this actually works...
else:
    # Not going to support linux at this time
    raise Exception("Unsupported OS")

#===============================================================================
# Set Python Paths (windows)
#===============================================================================
if ( os.name == 'nt' ):
    from sys import getwindowsversion
    major, minor, rev, a, b = getwindowsversion()
    
    if ( major != 6 and major != 5 ): # Not Vista/XP/2000/2003
        raise Exception("Unsupported Windows OS")
    
    from win_reg_edit import *
    WR = WinRegistry()
    path = WR.get_value("Path")
    path = path + ';' + python_path['win']
    WR.set_value("Path", path, None, _winreg.REG_EXPAND_SZ)
    
    if ( debug ):
        print 'registry'
        print '\tpath', path
        print '\tdir', python_path['win']

#===============================================================================
# Install nose
#===============================================================================
call(['python', mod_path['nose'], 'install'])

#===============================================================================
# Install PIL
#===============================================================================
call(['python', mod_path['PIL'], 'install'])

#===============================================================================
# Install PyGraphics
#===============================================================================
call(['python', mod_path['PyG'], 'install'])

a = raw_input('done...')