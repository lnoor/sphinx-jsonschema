
Introduction
============

This Sphinx extension allows authors to embed a `JSON Schema <http://json-schema.org>`_ in their documentation.

It arose out of a personal itch and implements what I needed.
Some features of JSON Schema are (not yet) implemented.
Also I can imagine that other display layouts are desired.

I only tested it for use with the `draft 4 <http://json-schema.org/specification-links.html#draft-4>`_ specification of JSON Schema.
I was pleasantly surprised to find that the software is useful to others as well.
Therefore it made sense to document its intended use.

Contents
========

.. toctree::
    :maxdepth: 2

    installation
    directive
    schemakeywords
    organization
    extensions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Changelog
=========

Version 1.16.5-6
----------------

Bugfix version.

Version 1.16.4
--------------

Introduces the ``:lift_title:`` directive option suggested by `ankostis <https://github.com/ankostis>`_.
Ankostis also provided an example on how to extend the formatter to handle custom properties.

Fixed a bug in rendering the ``items`` attribute of the ``array`` type reported by `nijel <https://github.com/nijel>`_.

Version 1.16.1-3
----------------

Fixed bugs rendering the ``default`` and ``examples`` keywords.

Introduced the configuration entry ``jsonschema_options`` setting default values for the directive options
introduced in 1.16. The options now can accept a parameter to explicitly turn the option on or off.

Version 1.16
------------

`WouterTuinstra <https://github.com/WouterTuinstra>`_ reimplemented support for ``dependencies`` and properly this time.
He also improved error handling and reporting and added a couple of options improving the handling of references.

The most important additions are the directive options ``:lift_description:``, ``:lift_definitions:``,
``:auto_target:`` and ``:auto_reference:``.

In addition to all that he also implemented support for the ``if``, ``then`` and ``else`` keywords.

Version 1.15
------------

Add support for the ``dependencies`` key.

Versions 1.12, 1.13 and 1.14
----------------------------

Solved several minor bugs.

Version 1.11
------------

Solved a divergence of the standard reported by `bbasic <https://github.com/bbasics>`_.

Version 1.10
------------

`Ivan Vysotskyy <https://github.com/ivysotskyi>`_ contributed the idea to use an array with
the ``description`` key resulting in the new ``$$description`` key.

Version 1.9
-----------

`Tom Walter <https://github.com/EvilPuppetMaster>`_ contributed the ``example`` support.

Version 1.4
-----------

`Chris Holdgraf <https://github.com/choldgraf>`_ contributed Python3 and yaml support.

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
