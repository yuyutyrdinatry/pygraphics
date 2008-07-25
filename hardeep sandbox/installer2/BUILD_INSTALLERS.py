# Builds the installers.
# Do NOT modify this file unless you know what you are doing!

import os
import sys
from content import *
from installer_builder import *
        
Builder = InstallerBuilder(DO)
Builder.generate()