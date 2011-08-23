=======================
Distributing PyGraphics
=======================

PyGraphics uses `distutils <http://docs.python.org/library/distutils.html>`_
for installation/packaging.

This means that PyGraphics has a :file:`setup.py` file at the top level. If you
have the PyGraphics source code, and the :file:`setup.py` file, then the command
for installing PyGraphics is ``python setup.py install`` (if you're root), or
``python setup.py install --user`` (if you're not root and on python 2.6+).

This same file is used for all the other commands involved with packaging and
distributing PyGraphics. It can create Windows installers, upload to the web,
etc.

For more information on producing distributions, confer with the distutils
documentation on
`distribution <http://docs.python.org/distutils/builtdist.html>`_

Installers
==========

:file:`setup.py` can produces installers for various OSes. These can be used
with the package manager to install software in a standard way.

Installers are not always the appropriate thing. In particular, on Linux,
it's better (i.e. works on more OSes) to distribute a source di-stribution.

On windows::

    python setup.py bdist_msi

On RPM Linuxes::

    python setup.py bdist_rpm

Source distributions
====================

A source distribution is just an archive file that contains all the source code.
After it is unarchived, it should be installed via ``python setup.py install``
as described above.

The basic command for producing a source distribution is the following::

    python setup.py sdist

On Windows, this will produce a ``.zip`` file. On Linux, this will produce a
``.tar.gz`` file. To produce a nondefault format, use the :option:`--format`
option to setup.py::

    python setup.py sdist --format=zip,gztar # both .zip and .tar.gz

.. Distributing the packates
   =========================

Documentation
=============

The documentation system is not made using distutils, but using 
`Sphinx <http://sphinx.pocoo.org/>`_ . Sphinx is also used for the official
Python documentation.

.. todo:: how-to
