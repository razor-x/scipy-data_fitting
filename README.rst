Data Fitting with SciPy
=======================

|PyPI| |GitHub-license| |Requires.io| |CircleCI| |Coverage|

    Built from `makenew/python-package <https://github.com/makenew/python-package>`__.

.. |PyPI| image:: https://img.shields.io/pypi/v/scipy-data_fitting.svg
   :target: https://pypi.python.org/pypi/scipy-data_fitting
   :alt: PyPI
.. |GitHub-license| image:: https://img.shields.io/github/license/razor-x/scipy-data_fitting.svg
   :target: ./LICENSE.txt
   :alt: GitHub license
.. |Requires.io| image:: https://img.shields.io/requires/github/razor-x/scipy-data_fitting.svg
   :target: https://requires.io/github/razor-x/scipy-data_fitting/requirements/
   :alt: Requires.io
.. |CircleCI| image:: https://img.shields.io/circleci/project/razor-x/scipy-data_fitting.svg?maxAge=2592000
   :target: https://circleci.com/gh/razor-x/scipy-data_fitting
   :alt: CircleCI
.. |Coverage| image:: https://img.shields.io/codecov/c/github/razor-x/scipy-data_fitting.svg?maxAge=2592000
   :target: https://codecov.io/gh/razor-x/scipy-data_fitting
   :alt: Codecov

Description
-----------

Complete pipeline for easy data fitting with Python.

Installation
------------

This package is registered on the `Python Package Index (PyPI)`_
as scipy_data_fitting_.

Add this line to your application's requirements.txt

::

    scipy_data_fitting

and install it with

::

    $ pip install -r requirements.txt

If you are writing a Python package which will depend on this,
add this to your requirements in ``setup.py``.

Alternatively, install it directly using pip with

::

    $ pip install scipy_data_fitting

.. _scipy_data_fitting: https://pypi.python.org/pypi/scipy-data_fitting
.. _Python Package Index (PyPI): https://pypi.python.org/

Development and Testing
-----------------------

Source Code
~~~~~~~~~~~

The `scipy-data_fitting source`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/razor-x/scipy-data_fitting.git

.. _scipy-data_fitting source: https://github.com/razor-x/scipy-data_fitting

Requirements
~~~~~~~~~~~~

You will need `Python 3`_ with pip_.

Install the development dependencies with

::

    $ pip install -r requirements.devel.txt

.. _pip: https://pip.pypa.io/
.. _Python 3: https://www.python.org/

Tests
~~~~~

Lint code with

::

    $ python setup.py lint


Run tests with

::

    $ python setup.py test

Contributing
------------

Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/razor-x/scipy-data_fitting/fork).
2. Create your feature branch (``git checkout -b my-new-feature``).
3. Make changes. Write and run tests.
4. Commit your changes (``git commit -am 'Add some feature'``).
5. Push to the branch (``git push origin my-new-feature``).
6. Create a new Pull Request.

License
-------

This Python package is licensed under the MIT license.

Warranty
--------

This software is provided "as is" and without any express or implied
warranties, including, without limitation, the implied warranties of
merchantibility and fitness for a particular purpose.
