.. LoincHpo documentation master file, created by
   sphinx-quickstart on Tue Jun 28 13:53:25 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to LoincHpo's documentation!
====================================
|PyPI version shields.io| |Anaconda-Server Badge shields.io|

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/loinchpo.svg
   :target: https://pypi.python.org/pypi/loinchpo/
.. |Anaconda-Server Badge shields.io| image:: https://anaconda.org/conda-forge/loinchpo/badges/version.svg
   :target: https://anaconda.org/conda-forge/loinchpo

A simple and efficient library for mapping loinc test results to hpo terms.

Documentation: https://thejacksonlaboratory.github.io/loinchpo/

# Requirements

Python > 3.5 && < 3.11

 Installing with PIP::

   pip install loinchpo

 Installing with Conda::

   conda config --add channels conda-forge
   conda config --set channel_priority strict
   conda install loinchpo


.. toctree::
   :maxdepth: 4

   usage
   omop
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
