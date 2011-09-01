=====================
Installing PyGraphics
=====================

.. topic:: Editors
    
    To edit code and use PyGraphics, you need an editor. The official Python 
    Wiki has a 
    `list of programmer's editors <http://wiki.python.org/moin/PythonEditors>`_
    and a `list of integrated development environments 
    <http://wiki.python.org/moin/IntegratedDevelopmentEnvironments>`_ .

.. toctree::
    :maxdepth: 1

Windows
=======

Download and install the 32bit Python 2.7 installer from `the 2.7 release page <http://www.python.org/download/releases/2.7/>`_ .

Download the Windows executable for PyGraphics `here <http://pypi.python.org/packages/any/P/PyGraphics/PyGraphics-2.0.win32.exe>`_ .
 
Run the installer. If Python is available on your computer, you should be able to move through the install screens without changing any settings.

Download and install the Python Imaging Library, PyGame, NumPy, and Ampy:

    * `PIL 1.1.7 <http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe>`_
    * `Pygame 1.9.2 <http://pygame.org/ftp/pygame-1.9.2a0.win32-py2.7.msi>`_
    * `Numpy 1.6.1 <http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.7.exe/download>`_
    * `Ampy <http://pygraphics.googlecode.com/files/ampy-1.2.3.win32.exe>`_

.. topic:: Nose

    If you wish to use the tests included in the PyGraphics package, you must download and install the Nose package. 
    
    First, `download setuptools <http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20>`_

    Next, open a DOS command prompt, and enter this command::

        C:\Python27\Scripts\easy_install.exe nose
      
    Nose should install automatically. 

Now you should be ready to use the PyGraphics package in your code.

Mac OS X
========

.. todo:: OS X installation guide.

Apple includes Python with Snow Leopard (Python 2.6) and Lion (Python 2.7). These instructions assume you are using one of these versions of Python.

Download and install the Python Imaging Library, its dependencies, and NumPy:

    * `PROJ Framework 4.7.0-2 <http://www.kyngchaos.com/files/software/frameworks/PROJ_Framework-4.7.0-2-snow.dmg>`_

    * `UnixImageIO Framework 1.3.0 <http://www.kyngchaos.com/files/software/frameworks/UnixImageIO_Framework-1.3.0-snow.dmg>`_
    * `FreeType_Framework 2.4.6-1 <http://www.kyngchaos.com/files/software/frameworks/FreeType_Framework-2.4.6-1-snow.dmg>`_
    * `PIL 1.1.7-2 <http://www.kyngchaos.com/files/software/python/PIL-1.1.7-2-snow.dmg>`_
    * `NumPy 1.6.1-1 <http://www.kyngchaos.com/files/software/python/NumPy-1.6.1-1-snow.dmg>`_

There are two separate PyGame installers, one for Lion and one for Snow Leopard.

    * `Snow Leopard (OS X 10.6): Pygame 1.9.2 <http://pygame.org/ftp/pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip>`_
    * `Lion (OS X 10.7): Pygame 1.9.2 <http://pygame.org/ftp/pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip>`_

Download and run the installation package for PyGraphics and ampy:

PyGraphics 2.0 and ampy 1.2.3
http://pypi.python.org/packages/any/P/PyGraphics/PyGraphics-2.0-py2.7-macosx10.7.dmg

.. topic:: Nose

    If you wish to use the tests included in the PyGraphics package, you must download and install the Nose package.

    Open Terminal.app (in Applications/Utilities) and type this:

        easy_install nose

        Now you should be ready to use the PyGraphics package in your code.

Linux
=====

.. admonition:: Note

   These instructions are tailored to Ubuntu and Ubuntu derivatives. If you use a different Linux distribution, the commands for installing various dependencies may differ.

Visit the `PyGraphics Downloads page <http://code.google.com/p/pygraphics/downloads/list>`_ and download the file named ``PyGraphics-2.0.tar.gz``.

Extract the file using Ark (or another archive tool).

Open a console window. In the main pygraphics folder, run the setup file to install PyGraphics to your local installation directory::

    python setup.py install --user

Download ``ampy-1.2.3.tar.gz`` from the `Downloads page <http://code.google.com/p/pygraphics/downloads/list>`_ , and follow the same procedure to install it as for PyGraphics.

Download and install Python's imaging package, NumPy, and PyGame. They are available via apt-get::

    apt-get install  python-imaging-tk python-numpy python-pygame

If you intend to run PyGraphic's test suite, install Nose::

    apt-get install python-nose

Now you and PyGraphics should be ready to make beautiful music (and pictures!) together. 
