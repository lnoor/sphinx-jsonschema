
Directive
=========

The extension adds a single directive to Sphinx: **jsonschema**.
You provide it with either a file name, an HTTP(S) URL to a schema
or you may embed the schema inline.

The schemas are read by a YAML parser.
This means that you can write the schemas in either json or yaml notation
and they will be processed identically.

Useage
------

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

.. code-block:: rst

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

Options
-------

There a couple of options implemented into jsonschema that change the display or functionality of the schema.
The options are:

- seperate_description
- seperate_definitions
- enable_auto_target
- enable_auto_reference

Seperate Description
++++++++++++++++++++

To seperate the ``description`` from the table you will need to have a title defined and the 
flag **\:seperate_description:** otherwise it will be included into the table:

.. code-block::

    .. jsonschema::
        :seperate_description:

        {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "id": "http://example.com/schemas/example.json",
            "title": "Example Seperate Description",
            "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nWhereby the description can shown as text outside the table, and you can still use *reStructuredText* in a description.",
            "type": "string",
            "minLength": 10,
            "maxLength": 100,
            "pattern": "^[A-Z]+$"
        }

which renders:

.. jsonschema::
    :seperate_description:

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "http://example.com/schemas/example.json",
        "title": "Example Seperate Description",
        "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nWhereby the description can shown as text outside the table, and you can still use *reStructuredText* in a description.",
        "type": "string",
        "minLength": 10,
        "maxLength": 100,
        "pattern": "^[A-Z]+$"
    }

Seperate Definitions
++++++++++++++++++++

To seperate the ``definitions`` from the table you will need to have the flag **\:seperate_description:** included. 
For each item inside the ``definitions`` it will make a new section with title and a table of the items inside.
It's advised to enable also **\:enable_auto_reference:** flag to auto link ``$ref`` to a local ``definitions`` title. 

.. code-block:: rst

    .. jsonschema::
        :seperate_definitions:

        {
            "title": "Example with definitions",
            "definitions": {
                "football_player": {
                    "type": "object",
                    "required": ["first_name", "last_name", "age"],
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                },
                "football_team": {
                    "type": "object",
                    "required": ["team", "league"],
                    "properties": {
                        "team": {"type": "string"},
                        "league": {"type": "string"},
                        "year_founded": {"type": "integer"}
                    }
                }
            }
        }

which renders:

.. jsonschema::
    :seperate_definitions:

    {
        "title": "Example with definitions",
        "definitions": {
            "football_player": {
                "type": "object",
                "required": ["first_name", "last_name", "age"],
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "age": {"type": "integer"}
                }
            },
            "football_team": {
                "type": "object",
                "required": ["team", "league"],
                "properties": {
                    "team": {"type": "string"},
                    "league": {"type": "string"},
                    "year_founded": {"type": "integer"}
                }
            }
        }
    }

Auto Target and Reference
+++++++++++++++++++++++++

With the **\:enable_auto_target:** flag there will be a target created with filename and optional pointer. 
When you would include auto target on multiple JSON schema with identical filenames it will cause a conflict 
within your build only the last build target will be used by the references. 
this also applies if you would embed the schema directly into your documentation only the filename will be the document name.

With the **\:enable_auto_reference:** flag there will be more logic applied to reduce the amount of undefined label warnings.
It will check if it's referencing to it self and if there would be a title to link to,
when there are titles in the same page that have an identical name it will cause linking issues. 
If you didn't seperate definitions from the schema the ``$ref`` will become a text field without a linked reference.
if the ``$ref`` would point to an other schema from the path it will extract the filename it expected 
to be included into your documentation with a **\:enable_auto_target:**.

Mainly the **\:enable_auto_reference:** flag infuence behavoir of the existing ``$$target`` methode and could potentially break links.

| See below the schema whereby both options are included.
  For each section it will create a target in this example filename of the document as the schema is added as context and it's pointer if there would be one.
| :ref:`directive.rst` this link as raw text using reStructuredText format would be: **\:ref:`directive.rst`**.
| And for the definition :ref:`directive.rst#/definitions/person` the raw text would be:  **\:ref:`directive.rst#/definitions/person`**.

.. code-block:: rst

    .. jsonschema::
        :seperate_definitions:
        :enable_auto_reference:
        :enable_auto_target:

    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title":  "Example of Target & Reference",
        "type": "object",
        "properties": {
            "person": { "$ref": "#/definitions/person" }
        },
        "definitions": {
            "person": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" },
                    "children": {
                        "type": "array",
                        "items": { "$ref": "#/definitions/person" },
                        "default": []
                    }
                }
            }
        }
    }

which renders:

.. jsonschema::
    :seperate_definitions:
    :enable_auto_reference:
    :enable_auto_target:

    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Example of Target & Reference",
        "type": "object",
        "properties": {
            "person": { "$ref": "#/definitions/person" }
        },
        "definitions": {
            "person": {
                "type": "object",
                "properties": {
                    "name": { "type": "string" },
                    "children": {
                        "type": "array",
                        "items": { "$ref": "#/definitions/person" },
                        "default": []
                    }
                }
            }
        }
    }