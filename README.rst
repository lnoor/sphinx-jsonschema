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


Usage
=====

The extension adds a single directive to Sphinx: **jsonschema**.
You provide it with either an http URL to a schema or you may
embed the schema inline.

Example
=======

::

    .. jsonschema:: http://some.domain/with/a/path/spec.json
    
Would fetch the `spec.json` file and display its contents.

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

Licence
=======

Copyright Leo Noordergraaf, All rights reserved.

This software is made available under the GPL v3.
