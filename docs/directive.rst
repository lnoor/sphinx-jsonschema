
Directive
=========

The extension adds a single directive to Sphinx: **jsonschema**.
You provide it with either a file name, an HTTP(S) URL to a schema
or you may embed the schema inline.

The schemas are read by a YAML parser.
This means that you can write the schemas in either json or yaml notation
and they will be processed identically.


To display a schema fetched from a website:

.. code-block:: rst

    .. jsonschema:: http://example.com/project/schema.json

To display a schema in a file referenced by an absolute path use:

.. code-block:: rst

    .. jsonschema:: /var/www/project/schema.json

or with a path relative to the current document:

.. code-block:: rst

    .. jsonschema:: schemas/sample.json

this assumes that next to the .rst file containing the above statement there
is a subdirectory ``schemas`` containing ``sample.json``.


With any of the above references you can use `JSON Pointer <https://tools.ietf.org/html/rfc6901>`_
notation to display a subschema:

.. code-block:: rst

    .. jsonschema:: http://example.com/project/schema.json#/definitions/sample

    .. jsonschema:: /var/www/project/schema.json#/definitions/sample

    .. jsonschema:: schemas/sample.json#/definitions/sample

Alternatively you can embed the schema directly into your documentation:

.. code-block:: rst

    .. jsonschema::

        {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "An example",
            "id": "http://example.com/schemas/example.json",
            "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nYes that's right you can use *reStructuredText* in a description.",
            "type": "string",
            "minLength": 10,
            "maxLength": 100,
            "pattern": "^[A-Z]+$"
        }

which should render as:

.. jsonschema::

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "An example",
        "id": "http://example.com/schemas/example.json",
        "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nYes that's right you can use *reStructuredText* in a description.",
        "type": "string",
        "minLength": 10,
        "maxLength": 100,
        "pattern": "^[A-Z]+$"
    }

It is also possible to render just a part of an embedded schema using a json pointer (per request `Issue 17 <https://github.com/lnoor/sphinx-jsonschema/issues/17>`_:

.. clode-block:: rst

    .. jsonschema:: #/date

        {
            "title" : "supertitle1",
            "type": "object",
            "properties": {
                "startdate": {"$ref": "#/date"},
                "enddate": {"$ref": "#/date"},
                "manualdate_to1": {"$ref" : "#/manualdate"},
                "definitions1": {"$ref" : "#/definitions/bind"},
                "definitions3": {"$ref" : "#/locbind"}
            },
            "date": {
                "title": "Date",
                "$$target": ["#/date"],
                "description": "YYYY-MM-DD",
                "type": "string"
            }
        }

which renders:

.. jsonschema:: #/date

    {
        "title" : "supertitle1",
        "type": "object",
        "properties": {
            "startdate": {"$ref": "#/date"},
            "enddate": {"$ref": "#/date"},
            "manualdate_to1": {"$ref" : "#/manualdate"},
            "definitions1": {"$ref" : "#/definitions/bind"},
            "definitions3": {"$ref" : "#/locbind"}
        },
        "date": {
            "title": "Date",
            "$$target": ["#/date"],
            "description": "YYYY-MM-DD",
            "type": "string"
        }
    }
