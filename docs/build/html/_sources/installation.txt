Installation
============

This is a brief guide for installing ``Equibel``.

The following steps assume that you have the ``pip`` Python package manager installed.
If you don't have ``pip``, you can get it `here <https://pip.pypa.io/en/latest/installing.html>`__.

``Equibel`` currently supports Mac OS X and Linux (32-bit and 64-bit), with Python 2.7.x or Python 3.

Quick Install
-------------

System-Wide Installation
~~~~~~~~~~~~~~~~~~~~~~~~

To install ``Equibel`` into the system-wide set of Python packages, simply use::

    $ pip install equibel


Virtual Environments
~~~~~~~~~~~~~~~~~~~~

In order to keep the dependencies of ``Equibel`` separate from those of other Python packages on your 
system, you may wish to install Equibel inside a *virtual environment*. Virtual environments 
provide isolation between different Python projects, allowing you to have separate installations 
of Python for each project. To create a virtual environment, you must first install ``virtualenv``::

    $ pip install virtualenv

Once ``virtualenv`` is installed, you can create a project directory and initialize a 
virtual environment in it as follows::

    $ mkdir try_equibel
    $ cd try_equibel
    $ virtualenv venv --python=python2.7

Before you can install packages into the virtual environment, you must *activate* it::

    $ source venv/bin/activate

When you do this, your terminal prompt will update so that it is prepended by ``(venv)``.
Whenever you want to exit the virtual environment and return to the system-wide Python 
installation, simply use::

    (venv)$ deactivate

With a virtual environment activated, you can simply install ``Equibel`` using ``pip``::

    (venv)$ pip install equibel


Installing from Source
----------------------




Optional Packages
-----------------

The following packages are optional, and are used by ``Equibel`` to provide additional functions.

Matplotlib
~~~~~~~~~~

``Matplotlib`` is a 2D plotting library in Python. When installed alongside ``Equibel``, it
enables visualization of graphs and associated scenarios, as well as model graphs.
``Matplotlib`` is available on `PyPI <https://pypi.python.org/pypi/matplotlib>`__, and can
be installed using::
    
    $ pip install matplotlib


