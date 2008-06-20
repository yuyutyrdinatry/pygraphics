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
mod_path['PyG'] = os.path.join(root_path, 'PyGraphics-1.3.3.7', 'setup.py')

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
        print 'wing cmd ::', os.path.join(root_path, 'wing', 'win', wing_file['win']), '/SILENT'
    call([os.path.join(root_path, 'wing', 'win', wing_file['win']), '/SILENT'])
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
    WR.set_value("Path", path)
    
    if ( debug ):
        print 'registry'
        print '\tpath', path
        print '\tdir', python_path['win']
        
###### TODO
# Need to put all of the below into a command line script to run from the
# actual directory of each setup.py...bleh

#===============================================================================
# Build Module Install Commands
#===============================================================================
cmd_nose = 'python "%s" %s' % (mod_path['nose'], 'install')
cmd_PIL = 'python "%s" %s' % (mod_path['PIL'], 'install')
cmd_PyG = 'python "%s" %s' % (mod_path['PyG'], 'install')

if ( os.name == 'nt' ):
    cmd_win_script = os.path.join(root_path, 'install_modules.bat')
    f = open(cmd_win_script, 'w')
    
    write = "@ECHO OFF\n"
    write += '%s:\n' % root_path[0]
    write += 'cd /\n'
    write += 'cd "%s"\n' % root_path
    
    # nose
    write += 'cd nose\n'
    write += '%s\n' % cmd_nose
    write += 'cd ..\n'
    
    # PIL
    write += 'cd PIL\n'
    write += '%s\n' % cmd_PIL
    write += 'cd ..\n'
    
    # PyG
    write += 'cd PyGraphics-1.3.3.7\n'
    write += '%s\n' % cmd_PyG
    write += 'cd ..\n'
    
    f.write(write)
    f.close()
    
    call(cmd_win_script)
else:
    #===========================================================================
    # Install nose
    #===========================================================================
    print "Installing Nose"
    print cmd_nose
    print "____________________________________________________________________"    
    call(cmd_nose)
    print "\n\n\n"
    
    #===========================================================================
    # Install PIL
    #===========================================================================
    print "Installing PIL"
    print cmd_PIL
    print "____________________________________________________________________"    
    call(cmd_PIL)
    print "\n\n\n"
    
    #===========================================================================
    # Install PyGraphics
    #===========================================================================
    print "Installing PyG"
    print cmd_PyG
    print "____________________________________________________________________"    
    call(cmd_PyG)
    print "\n\n\n"