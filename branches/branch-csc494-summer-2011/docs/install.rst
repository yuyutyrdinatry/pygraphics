=====================
Installing Pygraphics
=====================

.. toctree::
    :maxdepth: 1

Windows
=======

Download and install the 32bit Python 2.7 installer from `the 2.7 release page <http://www.python.org/download/releases/2.7/>`_ .

Download the Windows executable for PyGraphics `here <http://pygraphics.googlecode.com/files/PyGraphics-2.0.win32.exe>`_ .
 
Run the installer. If Python is available on your computer, you should be able to move through the install screens without changing any settings.

Download and install the Python Imaging Library, PyGame, NumPy, and Ampy:

    * `PIL 1.1.7 <http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe>`_
    * `Pygame 1.9.2 <http://pygame.org/ftp/pygame-1.9.2a0.win32-py2.7.msi>`_
    * `Numpy 1.6.0 <http://sourceforge.net/projects/numpy/files/NumPy/1.6.0/numpy-1.6.0-win32-superpack-python2.7.exe/download>`_
    * Ampy

.. topic:: Nose

    If you wish to use the tests included in the PyGraphics package, you must download and install the Nose package. 
    
    First, `download setuptools <http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20>`_

    Next, open a DOS command prompt, and enter this command::

        C:\Python27\Scripts\easy_install.exe nose
      
    Nose should install automatically. 

.. topic:: Editors
    
    To edit code, you need an editor. The official Python Wiki has a 
    `list of programmer's editors <http://wiki.python.org/moin/PythonEditors>`_
    and a `list of integrated development environments 
    <http://wiki.python.org/moin/IntegratedDevelopmentEnvironments>`_ .

Now you should be ready to use the PyGraphics package in your code.

Mac OS X
========

.. todo:: OS X installation guide.

Linux
=====

.. admonition:: Note

   These instructions are tailored to Ubuntu and Ubuntu derivatives. If you use a different Linux distribution, the commands for installing various dependencies may differ.

If you do not already have Wing, you may wish to install it. Wing is the Python IDE that has been most thoroughly tested with PyGraphics. It is available here: http://wingware.com/downloads/wingide-101/3.2

Visit the `PyGraphics Downloads page <http://code.google.com/p/pygraphics/downloads/list>`_ and download the file named ``PyGraphics-1.5.tar.gz``.

Extract the file using Ark (or another archive tool).

Open a console window. In the main pygraphics folder, run the setup file to install PyGraphics to your local installation directory::

    python setup.py install --user

Download ``ampy-1.2.3.tar.gz`` from the `Downloads page <http://code.google.com/p/pygraphics/downloads/list>`_ , and follow the same procedure to install it as for PyGraphics.

Download and install Python's imaging package, NumPy, and PyGame. They are available via apt-get::

    apt-get install  python-imaging-tk python-numpy python-pygame

If you intend to run PyGraphic's test suite, install Nose::

    apt-get install python-nose

Now you and PyGraphics should be ready to make beautiful music (and pictures!) together. 
