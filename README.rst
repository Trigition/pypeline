========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/pypeline/badge/?style=flat
    :target: https://readthedocs.org/projects/pypeline
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/trigition/pypeline.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/trigition/pypeline

.. |coveralls| image:: https://coveralls.io/repos/trigition/pypeline/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/trigition/pypeline

.. |version| image:: https://img.shields.io/pypi/v/pypeline.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pypeline

.. |commits-since| image:: https://img.shields.io/github/commits-since/trigition/pypeline/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/trigition/pypeline/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pypeline.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pypeline

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pypeline.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pypeline

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pypeline.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pypeline


.. end-badges

A multiprocessing library representing independent processes in a graph.

* Free software: MIT license

Installation
============

::

    pip install pypeline

Documentation
=============

https://pypeline.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
