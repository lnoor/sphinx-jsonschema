
Schema extensions
=================

After some experimentation I concluded that I needed to extend JSON Schema with a single key.
Most of the time sphinx-jsonschema just does the 'sensible' thing.

The ``$ref`` key in JSON Schema posed a problem.
It works in conjunction with the ``id`` keyword to implement a schema inclusion method.

I wanted to replace the schema inclusion with a hypertext link to the included schema.
Working on a number of large schemas I wanted to document the subschemas as type definitions
that are being referenced or used by the main schemas.
Therefore I wanted to be able to display the subschema on a different documentation page and
have the referring document display a clickable link.

In order to implement this I needed to add the **$$target** key to JSON Schema.
``$$target`` takes either a single string or an array of strings as parameter.

The string parameter must match the ``$ref`` parameter **exactly**.
So if you are using somewhere the schema::

    {
        ...
        "$ref": "#/definitions/sample",
        ...
    }

then the definitions section should read::

    {
        ...
        "definitions": {
            "sample": {
                "title": "A sample",
                "$$target": "#/definitions/sample"
                ...
            }
        }
    }

.. Note:: that ``$ref`` and ``$$target`` share exactly the same string.

.. Note:: also note the ``title`` field in ``sample``.
    This is required for the reference to work correctly.

When a referenced schema is used from more than one file it is possible
that the value of the ``$ref`` keywords is not equal.

Consider the case where ``schemas/service1/sample.json`` and ``schemas/service2/sample.json``
both reference a ``something`` subschema located in ``schemas/service1/referenced.json``
the objects may look like this in schemas/service1/sample.json::

    {
        ...
        "id": "schemas/service1/sample.json",
        "$ref": "referenced.json#/something",
        ...
    }

schemas/service2/sample.json would look like::

    {
        ...
        "id": "schemas/service2/sample.json",
        "$ref": "../service1/referenced.json#/something",
        ...
    }

This is why ``$target`` is allowed to have an array of strings as value in referenced.json::

    {
        ...
        "title": "Something",
        "$$target": ["referenced.json#/something", "../service1/referenced.json#/something"],
        ...
    }
    