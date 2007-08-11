#By: Leo Kaliazine
#Date: August 11, 2007

from distutils.core import setup
setup(name='PyGraphics',
      version='1.3',
      extra_path = "PyGraphics",
      package_dir={"": "PyGraphics"},
      py_modules=['picture'],
      )