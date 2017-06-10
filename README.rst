.. sphinx-jsonschema README
   Copyright: (C) 2017, Leo Noordergraaf

=================
sphinx-jsonschema
=================

This package contains sphinx-jsonschema, an extension to Sphinx to allow
authors to display a `JSON Schema <http://json-schema.org>`_ in their
documentation.

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

Or a path relative to the referencing document::

    .. jsonschema:: jsonschema/sample.json

With all three of the above you may add JSON Pointer notation to display a subschema::

    .. jsonschema:: http://some.domain/with/a/path/spec.json#/path/to/schema
    .. jsonschema:: /home/leo/src/jsonschema/sample.json#/path/to/schema
    .. jsonschema:: jsonschema/sample.json#/path/to/schema
    
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



Licence
=======

Copyright Leo Noordergraaf, All rights reserved.

This software is made available under the GPL v3.


Changelog
=========

Version 1.2
-----------

Improved formatting.
    
Version 1.1
-----------

Implemented schema cross referencing.
    
Version 1.0
-----------

Initial release of a functioning plugin.
    