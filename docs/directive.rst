
Directive
=========

The extension adds a single directive to Sphinx: **jsonschema**.
You provide it with either a file name, an HTTP(S) URL to a schema
or you may embed the schema inline.

The schemas are read by a YAML parser.
This means that you can write the schemas in either json or yaml notation
and they will be processed identically.

Usage
-----

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

Lastly, you can use the ``jsonschema`` directive to render a schema from a Python
object:

.. code-block:: python
    :caption: ``example.py``

        SCHEMA = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "An example",
            "id": "http://example.com/schemas/example.json",
            "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nYes that's right you can use *reStructuredText* in a description.",
            "type": "string",
            "minLength": 10,
            "maxLength": 100,
            "pattern": "^[A-Z]+$"
        }

with the following usage of the directive:

.. code-block:: rst

    .. jsonschema:: sphinx-jsonschema.example.SCHEMA

which should render as:

.. jsonschema:: sphinx-jsonschema.example.SCHEMA

Options
-------

There a couple of options implemented in **sphinx-jsonschema** that control the way a schema is rendered or processed.
These options are:

lift_title (default: True)
    Uses the title to create a new section in your document and creates an anchor you can refer to using jsonschema's
    ``$ref`` or ReStructuredText's ``:ref:`` notation.
    When `False` the title becomes part of the table rendered from the schema, the table cannot be referenced and the
    option ``:lift_description:`` is ignored.

lift_description (default: False)
    Places the description between the title and the table rendering the schema.
    This option is ignored when ``:lift_title:`` is `False`.

lift_definitions (default: False)
    Removed the items under the ``definitions`` key and renders each of them separately as if they are top-level
    schemas.

auto_target (default: False)
    Automatically generate values for the ``$$target`` key.
    Especially useful in combination with ``:lift_definitions:``.

auto_reference (default: False)
    Automatically resolves references when possible.
    Works well with ``:auto_target:`` and ``:lift_definitions:``.

hide_key: (default: None)
    Hide parts of the schema matching comma separated list of JSON pointers

hide_key_if_empty: (default: None)
    Hide parts of the schema matching comma separated list of JSON pointers if the value is empty

encoding (default: None)
    Allows you to define the encoding used by the file containing the json schema.

Lift Title
++++++++++

By default the schema's top level title is displayed above the table containing the remainder of the schema.
This title becomes a section that can be included in the table of contents and the index.
It is also used to resolve references to the schema from either other schemas of from elsewhere in the documentation.

This option mainly exists to suppress this behaviour.
One place where this is desirable is when using jsonschema to validate and document function parameters.
See `issue 48 <https://github.com/lnoor/sphinx-jsonschema/issues/48>`_ for an example.

Lift Description
++++++++++++++++

Lifts the ``description`` from the table and places it between the title and the table.
You will need to have a title defined and the flag **\:lift_description:** otherwise it will be included into
the table:

.. code-block::

    .. jsonschema::
        :lift_description:

        {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "id": "http://example.com/schemas/example.json",
            "title": "Example Separate Description",
            "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nWhereby the description can shown as text outside the table, and you can still use *reStructuredText* in a description.",
            "type": "string",
            "minLength": 10,
            "maxLength": 100,
            "pattern": "^[A-Z]+$"
        }

which renders:

.. jsonschema::
    :lift_description:

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "http://example.com/schemas/example.json",
        "title": "Example Separate Description",
        "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nWhereby the description can shown as text outside the table, and you can still use *reStructuredText* in a description.",
        "type": "string",
        "minLength": 10,
        "maxLength": 100,
        "pattern": "^[A-Z]+$"
    }

Lift Definitions
++++++++++++++++

To separate the ``definitions`` from the table you will need to have the flag **\:lift_definitions:** included.
For each item inside the ``definitions`` it will make a new section with title and a table of the items inside.
It's advised to also use the **\:auto_reference:** flag to auto link ``$ref`` to a local ``definitions`` title.

.. code-block:: rst

    .. jsonschema::
        :lift_definitions:

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
    :lift_definitions:

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

With the **\:auto_target:** flag there will be a target created with filename and optional pointer.
When you would include auto target on multiple JSON schemas with identical file names it will cause a conflict
within your build only the last build target will be used by the references.
This also applies if you would embed the schema directly into your documentation; in that case the document name is used
as the file name.

With the **\:auto_reference:** flag there will be more logic applied to reduce the amount of undefined label warnings.
It will check if it is referencing to itself and if there would be a title to link to,
when there are titles in the same page that have an identical name it will cause linking issues.
If you didn't separate definitions from the schema the ``$ref`` will become a text field without a linked reference.
If the ``$ref`` would point to an other schema from the path it will extract the filename it expected
to be included into your documentation with **\:auto_target:**.

Mainly the **\:auto_reference:** flag influences behavior of the existing ``$$target`` method and could potentially break links.

| See below the schema whereby both options are included.
  For each section it will create a target in this example filename of the document as the schema is added as context and it's pointer if there would be one.
| :ref:`directive.rst` this link as raw text using reStructuredText format would be: **\:ref:`directive.rst`**.
| And for the definition :ref:`directive.rst#/definitions/person` the raw text would be:  **\:ref:`directive.rst#/definitions/person`**.

.. code-block:: rst

    .. jsonschema::
        :lift_definitions:
        :auto_reference:
        :auto_target:

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
    :lift_definitions:
    :auto_reference:
    :auto_target:

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

Setting default values
++++++++++++++++++++++
When you want to use the options \:lift_definitions: \:lift_description, \:auto_target
and \:auto_reference in most schema renderings it is more convenient to set them once
for your whole project.

The ``conf.py`` option **jsonschema_options** lets you do so.
It takes a dict as value the boolean valued keys of which have the same name as the options.

So, in ``conf.py`` you can state:

.. code-block:: python
    :caption: ``conf.py``

    jsonschema_options = {
        'lift_description': True,
        'aut_reference': True
    }

By default all four options are False.

Overruling defaults
^^^^^^^^^^^^^^^^^^^
The default values for the options can be overruled by setting the directive options.
They accept an optional argument which can be one of the words ``On``, ``Off``, ``True``
or ``False``. The default value for the argument is ``True``.

Declare file encoding
+++++++++++++++++++++
The ``:encoding:`` option allows you to define the encoding used by the file containing
the json schema. When the operating system default encoding does not produce correct
results then this option allows you to specify the encoding to use.
When omitted the operating system default is used as it always has been. But it is now
possible to explicitly declare the expected encoding using ``:encoding: utf8``.
You can use any encoding defined by Python's codecs for your platform.

Hiding parts of the schema
++++++++++++++++++++++++++
Sometimes we want to omit certain keys from rendering to make the table more succicnt.
This can be achieved using the ``:hide_key:`` and ``:hide_key_if_empty:`` options to hide
all matching keys or all matching keys with empty associated value, respectively.
The options accept comma separated list of JSON pointers. Matching multiple keys
is possible using the wildcard syntax ``*`` for single level matching and ``**`` for
deep matching.

.. code-block:: rst

    .. jsonschema::
        :hide_key: /**/examples

This example will hide all ``examples`` fields regardless of where they are located
in the schema.
If your JSON pointer contains comma you need to place it inside quotes:

.. code-block:: rst

    .. jsonschema::
        :hide_key: /**/examples,"/**/with, comma"

It is also possible to hide a key if their value is empty using ``:hide_key_if_empty:``.

.. code-block:: rst

    .. jsonschema::
        :hide_key_if_empty: /**/defaults

Prevent escaping of strings
+++++++++++++++++++++++++++
Strings are sometimes subject to multiple evaluation passes when rendering.
This happens because `sphinx-jsonschema` renders a schema by transforming in into a table
and then recursively call on Sphinx to render the table.
To prevent unintended modifications due to this second pass some characters (such as '_'
and '*' are escaped before the second pass.

Sometimes that doesn't work out well and you don't want to escape those characters.
The option ``:pass_unmodified:`` accepts one or more JSON pointers and prevents the strings
pointed at to be escaped.

.. code-block:: rst

    .. jsonschema::
        :pass_unmodified: /examples/0

        {
            "examples": [
                "unescaped under_score",
                "escaped under_score"
            ]
        }
