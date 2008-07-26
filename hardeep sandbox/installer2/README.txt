# CONTENTS #####################################################################
1. Intro
	a. Requirements
		i   Windows
		ii  Mac
		iii Linux
2. Usage
    a. config.py
    b. content.py
################################################################################

1. INTRO
-----------------------------------
This script is intended to ease the creation of both Mac and Windows installers.

	a. Requirements
	-----------------------------------
	The following is a list of all tools required to build the installers and their
	current versions (if available) as of this writing.
	
		i. WINDOWS
		-----------------------------------
		 * NSIS 2.38 : http://nsis.sourceforge.net/Download
		 
		ii. MAC
		-----------------------------------
		 
		iii. LINUX
		-----------------------------------
		

2. Usage
-----------------------------------
There are two main steps to setting up the builder.

    a. config.py
    -----------------------------------
    First, make sure that the file config.py is modified to match your system
    settings. It should be pretty much self explainatory, and anything that is a
    bit more complex will have in-line comments in the config.py file itself.
    
    b. content.py
    -----------------------------------
    This file defines all the actual files and commands that will be run by the
    installers.