# This script executes after all the data has been copied over and Python has
# been installed.
#
# Registry modification code obtained from:
# http://agiletesting.blogspot.com/2005/06/handling-path-windows-registry-value.html

import os
from sys import getwindowsversion
from subprocess import call

#===============================================================================
# Parse and config
#===============================================================================
root_path = "$INSTALL_PATH"
root_path = "C:\\Program Files\\UofT CSC Dev Pack 2008" #testing only

python_path = {}
python_path['win'] = 'c:\\Python25\\' # default python install location
python_path['mac'] = '' #probably same as linux...not sure
python_path['nix'] = '/usr/bin/python'

nose_path = os.path.join(root_path, 'nose', 'setup.py')
PIL_path = os.path.join(root_path, 'PIL', 'setup.py')
PyG_path = os.path.join(root_path, 'PyGraphics', 'setup.py')
setx_path = os.path.join(root_path, 'tools', 'setx2k.exe')
#===============================================================================
# Install Wing
#===============================================================================
if ( os.name == 'nt' ): #Windows
    call([os.path.join(root_path, 'wing', 'win', 'wingide-101-3.1.1-1.exe'), '/SILENT'])
elif ( os.name == 'mac' ): #MacOS
    call([os.path.join(root_path, 'wing', 'mac', 'wingide-101-3.1.1-1-i386.dmg')]) # Figure out if this actually works...
else:
    raise Exception("Unsupported OS")

#===============================================================================
# Set Python Path
#===============================================================================
if ( os.name == 'nt' ):
    major, minor, rev, a, b = getwindowsversion()
    if ( major == 6 ):
        call(['setx', 'PATH', '"%PATH%;' + python_path['win']])
    elif ( major == 5 ):
        call([setx_path, 'PATH', '"%PATH%;' + python_path['win']])
    else:
        raise Exception("Unsupported Windows OS")

#===============================================================================
# Install nose
#===============================================================================
call(['python', nose_path, 'install'])

#===============================================================================
# Install PIL
#===============================================================================
call(['python', PIL_path, 'install'])

#===============================================================================
# Install PyGraphics
#===============================================================================
call(['python', PyG_path, 'install'])

a = raw_input('done...')