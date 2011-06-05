'''distutils setup for PyGraphics.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: setup.py 1855 2008-03-01 11:29:25Z Paul Gries $'

VERSION='2.0'

long_description='''PyGraphics provides a set of easy-to-use procedural media
manipulation tools and is intended for new programmers.  It is based on a
Jython library developed by Mark Guzdial at Georgia Tech.'''

from distutils.core import setup
setup(name='PyGraphics',
      version=VERSION,
      author='Jen Campbell, Paul Gries, Leo Kaliazine, Chris Maddison, Hardeep Singh',
      license='GPL',
      url='http://code.google.com/p/pygraphics',
      author_email='pgries@cs.toronto.edu',
      description='Easily-accessible library for media manipulation',
      long_description=long_description,
      extra_path = "pygraphics",
      classifiers=[
        #'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: New programmers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows', # XP
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        #'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      packages = ['', 'UnitTests'],
      package_dir = {'': 'cpython'},
      )