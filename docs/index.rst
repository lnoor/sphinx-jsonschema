
Introduction
============

This Sphinx extension allows authors to embed a `JSON Schema <http://json-schema.org>`_ in their documentation.

It arose out of a personal itch and implements what I needed.
Some features of JSON Schema are (not yet) implemented.
Also I can imagine that other display layouts are desired.

I only tested it for use with the `draft 4 <http://json-schema.org/specification-links.html#draft-4>`_ specification of JSON Schema.
I was pleasantly surprised to find that the software is useful to others as well.
Therefore it made sense to document intended use.

Contents
========

.. toctree::
    :maxdepth: 2

    installation
    directive
    schemakeywords
    organization

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Changelog
=========

Version 1.10
------------

Ivan Vysotskyy (https://github.com/ivysotskyi) contributed the idea to use an array with
the ``description`` key resulting in the new ``$$description`` key.


Version 1.9
-----------

Tom Walter (https://github.com/EvilPuppetMaster) contributed the ``example`` support.

Version 1.4
-----------

Chris Holdgraf (https://github.com/choldgraf) contributed Python3 and yaml support.

Version 1.3
-----------

Add unicode support.

Version 1.2
-----------

Improved formatting.

Version 1.1
-----------

Implemented schema cross referencing.

Version 1.0
-----------

Initial release of a functioning plugin.
