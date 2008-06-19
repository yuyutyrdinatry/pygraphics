# quick script to build the installer
import os
from subprocess import call

#===============================================================================
# Paths (configure me)
#===============================================================================
izPath = os.path.join('c:\\', 'Program Files', 'IzPack')

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
            
#===============================================================================
# Create the PyGraphics distutils package
#===============================================================================
# call('python setup.py sdist')

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