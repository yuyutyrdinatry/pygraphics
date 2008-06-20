#!/usr/bin/env python
#
# This script executes as soon as all the data is copied and extracted onto a
# MacOS system. It will then update the installation of Python to the bundled
# version.
#
# By: Hardeep Singh
# Note: This will only work on MacOS 10.2+, which comes pre-installed with
#       Python 2.3+
#
# Refer to: 
#    http://www.commandlinemac.com/article.php/20080127190435496
#    http://www.diveintopython.org/installing_python/macosx.html
#    http://developer.apple.com/internet/opensource/opensourcescripting.html

import os
from subprocess import call

#===============================================================================
# Parse (do not edit)
#===============================================================================
root_path = "$INSTALL_PATH"

#===============================================================================
# Configure
#===============================================================================
python_image = 'python-2.5.2-macosx.dmg'
mount_path = '/Volumes/Universal MacPython 2.5.2'

#===============================================================================
# Generate Commands
#===============================================================================
cmd_mount = "hdiutil mount %s" % os.path.join(root_path, 'mac', python_image)
#cmd_cp = "sudo cp -R \"/Volumes/Universal MacPython 2.5.2/Python.app\" /Applications" # need to figure out exact command for this

# Don't know if need the following yet:
cmd_install = 'sudo installer -package %s/MacPython.mpkg -target "%s"' % (
              mount_path, 
              os.path.join(root_path, 'Python'))

cmd_unmount_1 = "cd ~"
cmd_unmount_2 = "hdiutil unmount \"/Volumes/Universal MacPython 2.5.2/\""

# Test this:
cmd_post_install = "%s %s" % (os.path.join('usr', 'local', 'bin', 'python'), 
                              os.path.join(root_path, 'post_install.py'))
#===============================================================================
# Execute
#===============================================================================
call(cmd_mount)
#call(cmd_cp)
call(cmd_install)
call(cmd_unmount_1)
call(cmd_unmount_2)
call(cmd_post_install)