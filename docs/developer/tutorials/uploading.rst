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

Versioning
==========

Before creating a release distributable, be sure to update the versions.
Version numbers can be found in ``setup.py`` and ``docs/conf.py``.
Update them as appropriate for the release.

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

The resulting packaged distribution will be available in the ``dist`` directory
that ``setup.py`` creates.

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

As with installer distributions, the resulting archives will be in the ``dist``
directory that ``setup.py`` creates.

Distributing the packages
=========================

Google Code has its own upload mechanism, if the files are to be hosted there,
all the packages must be uploaded manually.

If, on the other hand, PyPI will be the distribution host, distutils has a
built-in mechanism for uploading packages.

First, you need to be registered to PyPI, and listed on the PyGraphics
administrators. After that, put your PyPI login information in a 
``.pypirc`` file in your home directory, like this::

    [server-login]
    username:michael.b
    password:mylifeforaiur

You're set! In all the above ``setup.py`` commands, you can append ``upload``
to the command. For example::

    python setup.py sdist --format=zip,gztar upload

This will automatically upload the resulting zip and tar.gz files to PyPI.

Documentation
=============

The documentation system is not made using distutils, but using 
`Sphinx <http://sphinx.pocoo.org/>`_ . Sphinx is also used for the official
Python documentation.

In the ``docs`` directory of the PyGraphics project, you can create the html
documentation with the following command::

    make html

This tells sphinx to translate the documentation to HTML, and put it in the
``_build/html`` directory. You should manually put all the files in the html 
directory in a zip file. (Note: these should be at the top level of the zip
file. Do not add the html directory itself.)

If you have the :command:`zip` command line utility, the command is as follows::

    cd _build/html
    zip docs.zip -R "*"

Then, log in to PyPI and upload the documentation zip file.
Once this is done, the documentation will be available for browsing at the
PyPI website at http://packages.python.org/PyGraphics/ 
