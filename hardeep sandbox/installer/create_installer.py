# One-click (or command :P) builder for the installer. Paths may need to be
# configured first!
#  - Hardeep Singh

import os
from subprocess import call
from shutil import copy2

#===============================================================================
# Paths (configure me)
#===============================================================================
# Path to izPack Installation Root
izPath = os.path.join('c:\\', 'Program Files', 'IzPack')

# Path to the PyGraphics Root. This folder should contain both a setup.py file
# and the cpython folder!
pyGraphicsPath = os.path.join('s:\\', 'workspace', 'PyGraphics')

# Windows-specific path settings
pyGraphicsPathDrive = 's' #i.e. c, d, x, etc... only the drive letter!

# For windows only! Must have valid ImgBurn install
# ImgBurn: http://www.imgburn.com/
img_burn = os.path.join('C:\\', 'Program Files', 'ImgBurn', 'ImgBurn.exe')
# For linux, consider using http://en.wikipedia.org/wiki/Cdrkit
# For mac, use built in tools
#    http://www.macosxhints.com/article.php?story=20020311215452999
#    http://pymachine.blogspot.com/2007/05/creating-image-disk-dmg-from-command.html
#        hdiutil create -fs HFS+ -srcfolder SRCFOLDER -volname VOLNAME IMGNAME

#===============================================================================
# Path to the install xml definition
#===============================================================================
izInstallXML = "izpack_installer.xml"

#===============================================================================
# Path to all executables required
#===============================================================================
izCompile = os.path.join(izPath, 'bin', 'compile.bat')
iz2EXE = os.path.join(izPath, 'utils', 'izpack2exe', 'izpack2exe.exe')
iz2APP = os.path.join(izPath, 'utils', 'izpack2app', 'izpack2app.exe')
iz7ZA = os.path.join(izPath, 'utils', 'izpack2exe', '7za.exe')

#===============================================================================
# Create commands
#===============================================================================
cur_dir = os.getcwd()
cmd_compile = '"%s" "%s" %s %s %s' % (izCompile, izInstallXML, '-b .', 
                                      '-o install.jar', '-k standard')
cmd_exe = '"%s" --file="%s" --output="%s" --with-7z="%s"' % \
            (iz2EXE,  
             'install.jar',  
             'install.exe',  
             iz7ZA)
cmd_app = '"%s" "%s" "%s"' % \
            (iz2APP,  
             'install.jar',  
             'install.app')
cmd_img = '%s /MODE BUILD /BUILDMODE IMAGEFILE /SRC "%s\\" /DEST "%s" /FILESYSTEM "ISO9660 + UDF" /UDFREVISION "2.50" /VOLUMELABEL "UofT" /CLOSESUCCESS /RECURSESUBDIRECTORIES YES /NOSAVESETTINGS /ROOTFOLDER YES /OVERWRITE YES /START /LOG "%s"' % (
          img_burn,                                                                                                                                                                                                              
          os.path.join(os.getcwd(), 'install.app', ''), 
          os.path.join(os.getcwd(), 'install.dmg'), 
          os.path.join(os.getcwd(), 'ImgBurn.log'))

cmd_pygraphics = 'python "%s" sdist' % os.path.join(pyGraphicsPath, 'setup.py')
cmd_pygraphics_win = os.path.join(pyGraphicsPath, 'win_compile.bat')
            
#===============================================================================
# Create the PyGraphics distutils package and copy to data folder
#===============================================================================
if ( os.name == 'nt' ):
    out = '%s:\n cd \\\n cd \"%s\"\n python setup.py sdist' % (
           pyGraphicsPathDrive, pyGraphicsPath)
    
    f = open(cmd_pygraphics_win, 'w')
    f.write(out)
    f.close()
    
    cmd_pygraphics = cmd_pygraphics_win
else:
    os.chroot(pyGraphicsPath)
    
print "Compiling PyGraphics distributable..."
print cmd_pygraphics
print "________________________________________________________________________"
call(cmd_pygraphics)
print "\n\n\n"

# Copy file to data folder
dist_path = os.path.join(pyGraphicsPath, 'dist')
files = os.listdir(dist_path)

print "Copy distributable file to data folder..."
print "Copy [%s] -> [%s]" % (os.path.join(dist_path, files[0]), 
                             os.path.join(os.getcwd(), 'data', 'PyGraphics.zip'))
print "________________________________________________________________________"
copy2(os.path.join(dist_path, files[0]), os.path.join(os.getcwd(), 'data', 
                                                      'PyGraphics.zip'))
print "\n\n\n"

if ( os.name != 'nt' ):
    os.chroot(cur_dir)
#===============================================================================
# Run commands with output
#===============================================================================
print "Compiling installer jar..."
print cmd_compile
print "________________________________________________________________________"
call(cmd_compile)
print "\n\n\n"

print "Creating self-extracting executable"
print cmd_exe
print "________________________________________________________________________"
call(cmd_exe)
print "\n\n\n"

print "Creating MacOS .app"
print cmd_app
print "________________________________________________________________________"
call(cmd_app)
print "\n\n\n"

#===============================================================================
# Create ISO from MacOS .app folder (only windows supported so far)
#===============================================================================
if ( os.name == 'nt' ):
    print "Creating ISO"
    print cmd_img
    print "________________________________________________________________________"
    call(cmd_img)
    print "\n\n\n"
    
# Consider creating pkg file for mac os?
# http://www.osxgnu.org/info/osxpackages.html

a = raw_input("Done... press enter to close")