Short Explanations and TO-DOs for the modules of pygraphics:

__init__.py
    
    This module makes pygraphics importable as a package. It also allows imports
    to use the syntax pygraphics.media to import specific modules
    
    TO-DO: Nothing
    
color.py

    This module contains the Color class and a series of pre-specified color
    classes
    
    TO-DO: Nothing
    
media.py

    This module contains global functions that aid in manipulation of Pictures,
    Sounds, Colors, Pixels, and Samples. Not all of the methods of each are 
    included as global functions. This module imports all from picture.py,
    sound.py, and color.py. It also import mediawindows as mw.
    
    On import or run this module initializes the mediawindows.py, picture.py, and
    sound.py modules.
    
    TO-DO: There is an issue with synchronicity when a python script that imports
    this module, creates a Sound, and plays it is run. For some reason the script
    tries to create the Sound before Python has fully initialized the pygame.mixer.
    
    Places to look for the solution are mediawindows, as the mediawindows thread
    initializes the mixer, and pygame. NOTE: This is an issue despite the request
    queue that the thread uses blocking until the function has completed. Perhaps
    problem is in pygamer.mixer.init()
    
mediawindows.py

    This module contains the thread support and the thread that is used to run
    the display of pictures by Tkinter and initialization of pygamer.mixer. It 
    also contains a series of Tkinter display widgets and support classes. Namely
    it contains the PictureWindow and associated support classes for displaying
    Pictures in a threaded window, and it contains the PictureInspector and
    associated support classes for displaying and inspecting Pictures.
    
    It also contains various choose_* functions that allow users to choose files,
    folders, save_as filenames, and colors. NOTE: These are what are called in
    media.py's equivalent choose_* functions.
    
    TO-DO: Major clean up necessary. The code logic is inconsistent (PictureWindow
    and PictureInspector function in vastly different ways) and documentation is
    needed for much of the module. Also, the Tkinter code should be cleaned up
    to make the windows behave as wanted (add scrollbars, fix proportions, etc)
    
    ALSO TO-DO: Add ask and say functions for A3
    
picture.py

    This module contains the Picture class and a series of helper functions to
    help with the interface between PIL and Picture. This module must be
    initialized before use. The init_picture() functions does this by initializing
    the mediawindows thread. Even if the mediawindows thread has been separately
    initialized this should be run to set the appropriate variables.
    
    TO-DO: Keep it consistent with changes in mediawindows.py
    
pixel.py

    This module contains the Pixel class that support the Picture class.
    
    TO-DO: Nothing, but keep up to date with Picture changes if necessary.
    
sample.py
    
    This module contains the MonoSample and StereoSample classes that support
    the Sound class.
    
    TO-DO: Nothing, but keep up to date with Sound changes if necessary.
    
sound.py

    This module contains the Sound class, the Note class, and helper functions
    that support those classes. This module must be initialized before use. The 
    init_sound() functions does this by initializing the mediawindows thread, then
    initializing the pygame.mixer.
    
     TO-DO: Fix synchronicity issue with pygamer.mixer initialization when run
     from scripts. See media.py TO-DO.
     
setup.py

    This module is used to install pygraphics and create binary or source
    distributions. To do so run the following in the shell:
    
    python setup.py install
    -OR-
    python setup.py sdist
    -OR-
    python setup.py bdist --format=zip
    
    NOTE the correct setup.py to use is in the cpython folder on the repository
