# quick script to build the installer
import os
from subprocess import call

# Path to IzPack build script
izPath = os.path.join('c:\\', 'Program Files', 'IzPack')

# Path to the install xml definition
izInstallXML = "izpack_installer.xml"

# Path to all executables required
izCompile = os.path.join(izPath, 'bin', 'compile.bat')
iz2EXE = os.path.join(izPath, 'utils', 'izpack2exe', 'izpack2exe.exe')
iz7ZA = os.path.join(izPath, 'utils', 'izpack2exe', '7za.exe')

# Create commands
cmd_compile = '"%s" "%s" %s %s %s' % (izCompile, izInstallXML, '-b .', '-o install.jar', '-k standard')
cmd_exe = '"%s" --file="%s" --output="%s" --with-7z="%s"' % \
            (iz2EXE,  
             'install.jar',  
             'install.exe',  
             iz7ZA)

# Run commands with output
print "\n\n\n"
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
a = raw_input("Done... press enter to close")