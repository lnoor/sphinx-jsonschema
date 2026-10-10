sphinx-jsonschema demo
======================

This document demonstrates the ``jsonschema`` directive.
It is meant to be built (HTML and LaTeX) and inspected visually.
All schemas live in separate files in the ``schemas`` directory and are included by file name.

The document has three parts:

1. a minimal example,
2. variations of the configuration (directive options),
3. the supported schema elements, rendered with the default configuration.

Part 1: Minimal example
-----------------------

The smallest possible use of the directive: one schema file, no options.

.. literalinclude:: schemas/minimal.json
   :language: json
   :caption: Source: schemas/minimal.json

.. code-block:: rst

   .. jsonschema:: schemas/minimal.json

.. jsonschema:: schemas/minimal.json

Part 2: Configuration variations
--------------------------------

The directive options ``lift_title``, ``lift_description``, ``lift_definitions``, ``auto_target`` and ``auto_reference`` are also available as the global configuration value ``jsonschema_options`` in ``conf.py``.
A directive option always overrides the global value, so every variation below is shown with a directive option.
The demo ``conf.py`` deliberately sets no global options.

Default
~~~~~~~

This example shows the inclusion of ``schemas/config-base.json`` without options.
The title is lifted into a section heading, which is the default.
The description stays in the table.

.. literalinclude:: schemas/config-base.json
   :language: json
   :caption: Source: schemas/config-base.json

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json

.. jsonschema:: schemas/config-base.json

Title not lifted
~~~~~~~~~~~~~~~~

``lift_title: off`` keeps the title inside the table instead of creating a section.
This example uses the same schema as the previous section.

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json
      :lift_title: off

.. jsonschema:: schemas/config-base.json
   :lift_title: off

Description lifted
~~~~~~~~~~~~~~~~~~

``lift_description`` moves the description below the section heading, outside the table.
This example uses the same schema as the previous section.

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json
      :lift_description:

.. jsonschema:: schemas/config-base.json
   :lift_description:

Definitions lifted
~~~~~~~~~~~~~~~~~~

``lift_definitions`` renders each entry of ``definitions`` as a section of its own.
This example uses the same schema as the previous section.

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json
      :lift_definitions:

.. jsonschema:: schemas/config-base.json
   :lift_definitions:

Description and definitions lifted
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both lift options combined.
This example uses the same schema as the previous section.

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json
      :lift_description:
      :lift_definitions:

.. jsonschema:: schemas/config-base.json
   :lift_description:
   :lift_definitions:

Automatic target
~~~~~~~~~~~~~~~~

``auto_target`` creates a label from the file name, so the schema can be referenced from elsewhere with ``:ref:``.

.. literalinclude:: schemas/config-base-b.json
   :language: json
   :caption: Source: schemas/config-base-b.json

.. code-block:: rst

   This is a reference to the schema below: :ref:`config-base-b.json`.

   .. jsonschema:: schemas/config-base-b.json
      :auto_target:

This is a reference to the schema below: :ref:`config-base-b.json`.

.. jsonschema:: schemas/config-base-b.json
   :auto_target:

Automatic references with titles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``lift_definitions``, ``auto_target`` and ``auto_reference`` combined: each ``$ref`` becomes a link to the titled section of its target.
A separate copy of the schema is used because the labels are derived from the file name.

.. literalinclude:: schemas/config-base-c.json
   :language: json
   :caption: Source: schemas/config-base-c.json

.. code-block:: rst

   .. jsonschema:: schemas/config-base-c.json
      :lift_definitions:
      :auto_target:
      :auto_reference:

.. jsonschema:: schemas/config-base-c.json
   :lift_definitions:
   :auto_target:
   :auto_reference:

Automatic references without titles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``lift_title: off`` the references point to the automatically created targets instead of titles.

.. literalinclude:: schemas/config-base-d.json
   :language: json
   :caption: Source: schemas/config-base-d.json

.. code-block:: rst

   .. jsonschema:: schemas/config-base-d.json
      :lift_title: off
      :auto_target:
      :auto_reference:

.. jsonschema:: schemas/config-base-d.json
   :lift_title: off
   :auto_target:
   :auto_reference:

JSON pointer
~~~~~~~~~~~~

A file name followed by ``#/json/pointer`` renders only that part of the file.

.. literalinclude:: schemas/config-multi.json
   :language: json
   :caption: Source: schemas/config-multi.json

.. code-block:: rst

   .. jsonschema:: schemas/config-multi.json#/definitions/a

.. jsonschema:: schemas/config-multi.json#/definitions/a

The same pointer with ``lift_title: off``:

.. code-block:: rst

   .. jsonschema:: schemas/config-multi.json#/definitions/b
      :lift_title: off

.. jsonschema:: schemas/config-multi.json#/definitions/b
   :lift_title: off

Hiding keys
~~~~~~~~~~~

Here is the base schema without options, for comparison:

.. literalinclude:: schemas/config-hide.json
   :language: json
   :caption: Source: schemas/config-hide.json

.. jsonschema:: schemas/config-hide.json

``hide_key`` removes the keys at the given JSON paths.
Here the description of ``name`` is removed.

.. code-block:: rst

   .. jsonschema:: schemas/config-hide.json
      :hide_key: /properties/name/description

.. jsonschema:: schemas/config-hide.json
   :hide_key: /properties/name/description

``hide_key_if_empty`` removes keys only if their value is empty.
The empty description and enum of ``color`` disappear, the enum of ``size`` is empty as well, but its description is kept.

.. code-block:: rst

   .. jsonschema:: schemas/config-hide.json
      :hide_key_if_empty: /properties/color/description,/properties/color/enum,/properties/size/enum

.. jsonschema:: schemas/config-hide.json
   :hide_key_if_empty: /properties/color/description,/properties/color/enum,/properties/size/enum

Special characters and pass_unmodified
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Descriptions are interpreted as reST.
Values of ``default``, ``enum``, ``examples`` and ``pattern`` are escaped, so reST markup in them is shown literally.
This example also exercises special characters in LaTeX output.

.. literalinclude:: schemas/config-markup.json
   :language: json
   :caption: Source: schemas/config-markup.json

.. code-block:: rst

   .. jsonschema:: schemas/config-markup.json

.. jsonschema:: schemas/config-markup.json

``pass_unmodified`` skips the escaping for the given paths, so the markup in the default value of ``markup`` is interpreted as reST.

.. code-block:: rst

   .. jsonschema:: schemas/config-markup.json
      :pass_unmodified: /properties/markup/default

.. jsonschema:: schemas/config-markup.json
   :pass_unmodified: /properties/markup/default

YAML source
~~~~~~~~~~~

The schema can be written in YAML.

.. literalinclude:: schemas/config-source.yaml
   :language: yaml
   :caption: Source: schemas/config-source.yaml

.. code-block:: rst

   .. jsonschema:: schemas/config-source.yaml

.. jsonschema:: schemas/config-source.yaml

Encoding
~~~~~~~~

``encoding`` selects the character encoding of the schema file.
This file is stored as ISO-8859-1.

.. literalinclude:: schemas/config-latin1.json
   :language: json
   :caption: Source: schemas/config-latin1.json
   :encoding: latin-1

.. code-block:: rst

   .. jsonschema:: schemas/config-latin1.json
      :encoding: latin-1

.. jsonschema:: schemas/config-latin1.json
   :encoding: latin-1

Part 3: Schema elements
-----------------------

Every schema below is rendered with the default configuration (no options).
The schemas use JSON Schema Draft 4, plus the parts of Draft 6 and 7 that the plugin already supports.

Types and formats
~~~~~~~~~~~~~~~~~

.. literalinclude:: schemas/types.json
   :language: json
   :caption: Source: schemas/types.json

.. jsonschema:: schemas/types.json

Constraints
~~~~~~~~~~~

.. literalinclude:: schemas/constraints.json
   :language: json
   :caption: Source: schemas/constraints.json

.. jsonschema:: schemas/constraints.json

Enum, const and examples
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: schemas/enum-const-examples.json
   :language: json
   :caption: Source: schemas/enum-const-examples.json

.. jsonschema:: schemas/enum-const-examples.json

Arrays
~~~~~~

.. literalinclude:: schemas/arrays.json
   :language: json
   :caption: Source: schemas/arrays.json

.. jsonschema:: schemas/arrays.json

Objects
~~~~~~~

.. literalinclude:: schemas/objects.json
   :language: json
   :caption: Source: schemas/objects.json

.. jsonschema:: schemas/objects.json

Combinators
~~~~~~~~~~~

.. literalinclude:: schemas/combinators.json
   :language: json
   :caption: Source: schemas/combinators.json

.. jsonschema:: schemas/combinators.json

Conditionals
~~~~~~~~~~~~

.. literalinclude:: schemas/conditional.json
   :language: json
   :caption: Source: schemas/conditional.json

.. jsonschema:: schemas/conditional.json

References
~~~~~~~~~~

.. literalinclude:: schemas/references.json
   :language: json
   :caption: Source: schemas/references.json

.. jsonschema:: schemas/references.json

Plugin extensions
~~~~~~~~~~~~~~~~~

The target defined with ``$$target`` can be referenced like this: :ref:`demo-extensions-alias`.

.. literalinclude:: schemas/extensions.json
   :language: json
   :caption: Source: schemas/extensions.json

.. jsonschema:: schemas/extensions.json
