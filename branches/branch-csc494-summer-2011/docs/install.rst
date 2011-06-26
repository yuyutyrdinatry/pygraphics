=====================
Installing Pygraphics
=====================

Windows
=======

Ensure that you have Python 2.6 installed on your computer. You can download 2.6.4 from http://www.python.org/download/releases/2.6.4/.

Download the Windows executable for PyGraphics here: http://pygraphics.googlecode.com/files/PyGraphics-1.5.win32.exe
Run the installer. If Python is available on your computer, you should be able to move through the install screens without changing any settings.

Download and install Wing, the IDE typically used with PyGraphics: http://wingware.com/pub/wingide-101/3.1.3/wingide-101-3.1.3-1.exe

Download and install the Python Imaging Library, PyGame, and NumPy:

    * http://effbot.org/downloads/PIL-1.1.6.win32-py2.6.exe
    * http://pygame.org/ftp/pygame-1.9.1.win32-py2.6.msi
    * http://sourceforge.net/projects/numpy/files/NumPy/1.4.0/numpy-1.4.0-win32-superpack-python2.6.exe/download] 

If you wish to use the tests included in the PyGraphics package, you must download and install the Nose package. 
  
First, download setuptools: http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11.win32-py2.6.exe#md5=1509752c3c2e64b5d0f9589aafe053dc 

Next, open a DOS command prompt, switch to the C:\Python26\Scripts folder, and enter this command::

    easy_install nose
  
Nose should install automatically. 

Now you should be ready to use the PyGraphics package in your code.

Mac OS X
========

.. todo:: OS X installation guide.

Linux
=====

.. admonition:: Note

   These instructions are particularly tailored to Ubuntu and Ubuntu derivatives. If you use a different Linux distribution, the instructions for installing various packages may differ.

If you do not already have Wing, you may wish to install it. Wing is the Python IDE that has been most thoroughly tested with PyGraphics. It is available here: http://wingware.com/downloads/wingide-101/3.2

Visit the Downloads page at http://code.google.com/p/pygraphics/downloads/list and download the file named 'PyGraphics?-1.5.tar.gz'.

Extract the file using Ark (or another archive tool).

Open a console window. In the main pygraphics folder, install the setup file: 'python setup.py install'. Use sudo if you are not logged in as root.

Download and install Nose, NumPy, and PyGame, if you do not already have those packages. They are available via apt-get under the names python-nose, python-numpy, and python-pygame. In each case, 'apt-get install packagename'. Note: Nose is required only if you intend to use the test suite.

Download and install Python's Tk imaging package: 'apt-get install python-imaging-tk'. 

