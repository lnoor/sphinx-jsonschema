.. sphinx-jsonschema README
   Copyright: (C) 2017-2020, Leo Noordergraaf

=================
sphinx-jsonschema
=================

This package contains sphinx-jsonschema, an extension to Sphinx to allow
authors to display a `JSON Schema <http://json-schema.org>`_ in their
documentation.

A dockerized version can be found at: `Extended Sphinx <https://hub.docker.com/r/lnoor/sphinx-extended>`_.

It arose out of a personal itch and implements what I needed.
Some features of JSON Schema are (not yet) implemented.
Also I can imagine that other display layouts are desired.

Let me know in comments and perhaps pull requests.


Features
========

* Near complete support for all features of JSON Schema Draft 4.
* Supports inline schemas as well as external schemas loaded from a file or URL.
* Supports JSON Pointer notation on external resources to select a subschema.
* Supports cross references between schemas.
* Allows reStructuredText markup in ``title`` and ``description`` fields.
* Allows JSON Schema definitions in both JSON and YAML format.
* Supports the ``examples`` keyword from Draft 7.

Installation
============
Install the package using pip::

    pip install sphinx-jsonschema

and add it to the extensions list in your conf.py::

    extensions = [
        'sphinx-jsonschema'
    ]

Usage
=====

The extension adds a single directive to Sphinx: **jsonschema**.
You provide it with either an http URL to a schema or you may
embed the schema inline.

Example
=======

Display a schema fetched from a website::

    .. jsonschema:: http://some.domain/with/a/path/spec.json


Display a schema located in a file with an absolute path::

    .. jsonschema:: /home/leo/src/jsonschema/sample.json

A path relative to the referencing document::

    .. jsonschema:: jsonschema/sample.json

Or a schema defined in a python dict::

    .. jsonschema:: mod.pkg.SCHEMA

With all three of the above you may add JSON Pointer notation to display a subschema::

    .. jsonschema:: http://some.domain/with/a/path/spec.json#/path/to/schema
    .. jsonschema:: /home/leo/src/jsonschema/sample.json#/path/to/schema
    .. jsonschema:: jsonschema/sample.json#/path/to/schema
    .. jsonschema:: mod.pkg.SCHEMA#/path/to/schema

Alternatively you can embed the schema::

    .. jsonschema::

        {
            "$schema": "This field is ignored for now. Perhaps use it to indicate schema version in display?",
            "title": "Test data set 1: **Simple type**",
            "id": "http://this.better.be.a.regular.domain",
            "description": "These data sets exercise `JSON Schema <http://json-schema.org>`_ constructions and show how they are rendered.\n\nNote that it is possible to embed reStructuredText elements in strings.",
            "type": "string",
            "minLength": 10,
            "maxLength": 100,
            "pattern": "^[A-Z]+$"
        }

This notation does not support JSON Pointer.

JSON Schema extension
=====================

$$target
    sphinx-jsonschema extends JSON Schema with the ``$$target`` key.

    This key is only recognized at the outermost object of the schema.

JSON Schema uses the ``$ref`` key in combination with the ``$id`` key to cross-reference between schemas.

Sphinx-jsonschema ignores ``$id`` but uses the value of ``$ref`` to create a reStructuredText ``:ref:`` role.

For this to work you need to mark the target schema with the ``$$target`` key, the value of which must be
identical to the value of the corresponding ``$ref`` key.

So a schema::

    {
        "title": "Schema 1",
        "$ref": "#/definitions/schema2"
    }

will have its ``$ref`` replaced by a link pointing to::

    {
        "title": "Schema 2",
        "$$target": "#/definitions/schema2"
        ...
    }

Occasionally a schema will be addressed from several other schemas using different ``$ref`` values.
In that case the value of ``$$target`` should be a list enumerating all different references to the
schema.

$$description
   sphinx-jsonschema extends JSON Schema with the ``$$description`` key.

This key serves the same purpose as the ``description`` key and can be used in the same way.
It differs from ``description`` in that it allows an array of strings as value instead of a
single string.

This allows you to write::

   {
      ...
      "description": "+------------+------------+-----------+ \n| Header 1   | Header 2   | Header 3  | \n+============+============+===========+ \n| body row 1 | column 2   | column 3  | \n+------------+------------+-----------+ \n| body row 2 | Cells may span columns.| \n+------------+------------+-----------+ \n| body row 3 | Cells may  | - Cells   | \n+------------+ span rows. | - contain | \n| body row 4 |            | - blocks. | \n+------------+------------+-----------+",
      ...
   }

as::

   {
      ...
      "$$description": [
         "+------------+------------+-----------+",
         "| Header 1   | Header 2   | Header 3  |",
         "+============+============+===========+",
         "| body row 1 | column 2   | column 3  |",
         "+------------+------------+-----------+",
         "| body row 2 | Cells may span columns.|",
         "+------------+------------+-----------+",
         "| body row 3 | Cells may  | - Cells   |",
         "+------------+ span rows. | - contain |",
         "| body row 4 |            | - blocks. |",
         "+------------+------------+-----------+"
      ],
      ...
   }

Which clearly is much more readable and maintainable.

Licence
=======

Copyright Leo Noordergraaf, All rights reserved.

This software is made available under the GPL v3.


Changelog
=========

Version 1.18.0
--------------

Expanding on the work of `Pavel Odvody <https://github.com/shaded-enmity>`_ with JSON Pointer
the ``:pass_unmodified:`` option is included.
This option prevents escaping the string pointed at.

Version 1.17.2
--------------

`Ezequiel Orbe <https://github.com/eorbe>`_ found, reported and fixed a bug escaping backspaces.

Version 1.17.0
--------------

`Pavel Odvody <https://github.com/shaded-enmity>`_ contributed the ``:hide_key:`` directive option.
This option allows you to hide certain keys, specified by a JSON Path specification, to be excluded
from rendering.


Version 1.16.11
---------------

Removed debugging code left in, pointed out by `Kevin Landreth <https://github.com/CrackerJackMack>`.

Version 1.16.10
---------------

`iamdbychkov <https://github.com/iamdbychkov>`_ added the ``:encoding:`` directive option.
This option allows explicit control of the encoding used to read a file
instead of relying on the operating system default.

Version 1.16.9
--------------

Bugfix.

Version 1.16.8
--------------

`Jens Nielsen <https://github.com/jenshnielsen>`_ improved rendering of string values.

Version 1.16.5-6
----------------

Bugfix version.

Version 1.16.4
--------------

Introduces the ``:lift_title:`` directive option suggested by `ankostis <https://github.com/ankostis>`_.
Ankostis also provided an example on how to extend the formatter to handle custom properties.

Fixed a bug in rendering the ``items`` attribute of the ``array`` type reported by nijel (https://github.com/nijel).

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


Versions 1.12 and 1.13 and 1.14
-------------------------------

Solved several minor bugs.


Version 1.11
------------

Solved a divergence of the standard reported by bbasic (https://github.com/bbasics).

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
