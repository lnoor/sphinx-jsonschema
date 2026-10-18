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

The directive options ``lift_title``, ``lift_description``, ``lift_definitions``, ``auto_target``, ``auto_reference``, ``warn_unresolved_refs`` and ``show_comments`` are also available as the global configuration value ``jsonschema_options`` in ``conf.py``.
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

Unresolved references
~~~~~~~~~~~~~~~~~~~~~

Without ``auto_reference`` a ``$ref`` such as ``#/definitions/address`` is shown as plain text unless a label of that name exists;
the *Default* example above shows this.
Sphinx reports no ``undefined label`` warning for it, so this document builds with ``-W``.
The option ``warn_unresolved_refs`` brings the warnings back; it is not demonstrated here for exactly that reason.

.. code-block:: rst

   .. jsonschema:: schemas/config-base.json
      :warn_unresolved_refs:

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

Comments
~~~~~~~~

The keyword ``$comment`` holds notes for the maintainers of a schema and is hidden by default.
The option ``show_comments`` adds a row for every comment.

.. literalinclude:: schemas/feature-comment.json
   :language: json
   :caption: Source: schemas/feature-comment.json

.. code-block:: rst

   .. jsonschema:: schemas/feature-comment.json
      :show_comments:

.. jsonschema:: schemas/feature-comment.json
   :show_comments:

Part 3: Schema elements
-----------------------

Every schema below is rendered with the default configuration (no options).
The schemas use JSON Schema Draft 4, plus the parts of Draft 6 and 7 that the plugin already supports.
Keywords introduced by later drafts are shown in Part 4.

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

Part 4: Keywords by schema version
----------------------------------

This part shows one small schema per keyword, ordered by the draft that introduced the keyword.
Each example states since which draft the keyword is part of JSON Schema.
Keywords that are not rendered yet are marked accordingly.
Their examples show the current output, which will change as support is added.

Draft 4
~~~~~~~

Exclusive limits as booleans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``exclusiveMinimum`` and ``exclusiveMaximum`` are booleans that modify ``minimum`` and ``maximum``.
This feature of JSON Schema is supported since Draft 4 and was replaced in Draft 6 by numeric limits.

.. literalinclude:: schemas/feature-exclusive-minmax-bool.json
   :language: json
   :caption: Source: schemas/feature-exclusive-minmax-bool.json

.. jsonschema:: schemas/feature-exclusive-minmax-bool.json

Tuple validation with ``items`` as a list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An ``items`` list describes the array positions one by one, ``additionalItems`` the remaining ones.
This feature of JSON Schema is supported since Draft 4 and was replaced in Draft 2020-12 by ``prefixItems``.

.. literalinclude:: schemas/feature-tuple-items.json
   :language: json
   :caption: Source: schemas/feature-tuple-items.json

.. jsonschema:: schemas/feature-tuple-items.json

Dependencies
^^^^^^^^^^^^

``dependencies`` makes a property require other properties or a further schema.
This feature of JSON Schema is supported since Draft 4 and was split in Draft 2019-09 into ``dependentRequired`` and ``dependentSchemas``.

.. literalinclude:: schemas/feature-dependencies.json
   :language: json
   :caption: Source: schemas/feature-dependencies.json

.. jsonschema:: schemas/feature-dependencies.json

Multiple types
^^^^^^^^^^^^^^

A schema can allow several types, so that the keywords of each of them apply.
This feature of JSON Schema is supported since Draft 4.

.. literalinclude:: schemas/feature-type-list-mixed.json
   :language: json
   :caption: Source: schemas/feature-type-list-mixed.json

.. jsonschema:: schemas/feature-type-list-mixed.json

The ``$schema`` keyword
^^^^^^^^^^^^^^^^^^^^^^^

``$schema`` names the dialect a schema is written for.
This feature of JSON Schema is supported since Draft 4.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-schema-keyword.json
   :language: json
   :caption: Source: schemas/feature-schema-keyword.json

.. jsonschema:: schemas/feature-schema-keyword.json

Draft 6
~~~~~~~

Const
^^^^^

``const`` restricts a value to exactly one value.
This feature of JSON Schema is supported since Draft 6.

.. literalinclude:: schemas/feature-const.json
   :language: json
   :caption: Source: schemas/feature-const.json

.. jsonschema:: schemas/feature-const.json

Exclusive limits as numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``exclusiveMinimum`` and ``exclusiveMaximum`` are the limits themselves.
This feature of JSON Schema is supported since Draft 6.

.. literalinclude:: schemas/feature-exclusive-minmax-number.json
   :language: json
   :caption: Source: schemas/feature-exclusive-minmax-number.json

.. jsonschema:: schemas/feature-exclusive-minmax-number.json

Boolean schemas
^^^^^^^^^^^^^^^

``true`` accepts everything and ``false`` accepts nothing wherever a schema is expected.
This feature of JSON Schema is supported since Draft 6.

.. literalinclude:: schemas/feature-boolean-schemas.json
   :language: json
   :caption: Source: schemas/feature-boolean-schemas.json

.. jsonschema:: schemas/feature-boolean-schemas.json

Contains
^^^^^^^^

``contains`` requires at least one array item to match a schema.
This feature of JSON Schema is supported since Draft 6.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-contains.json
   :language: json
   :caption: Source: schemas/feature-contains.json

.. jsonschema:: schemas/feature-contains.json

Property names
^^^^^^^^^^^^^^

``propertyNames`` constrains the names of all properties of an object.
This feature of JSON Schema is supported since Draft 6.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-property-names.json
   :language: json
   :caption: Source: schemas/feature-property-names.json

.. jsonschema:: schemas/feature-property-names.json

Draft 7
~~~~~~~

Comment
^^^^^^^

``$comment`` holds notes for the maintainers of a schema.
This feature of JSON Schema is supported since Draft 7.

The specification asks implementations not to show comments to end users, so the keyword is hidden by default.
The option ``show_comments`` displays it, as shown in the section "Comments" of part 2.

.. literalinclude:: schemas/feature-comment.json
   :language: json
   :caption: Source: schemas/feature-comment.json

.. jsonschema:: schemas/feature-comment.json

Read-only and write-only
^^^^^^^^^^^^^^^^^^^^^^^^

``readOnly`` and ``writeOnly`` mark values that must not be sent or are never returned.
This feature of JSON Schema is supported since Draft 7.

.. literalinclude:: schemas/feature-read-write-only.json
   :language: json
   :caption: Source: schemas/feature-read-write-only.json

.. jsonschema:: schemas/feature-read-write-only.json

Content encoding and media type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``contentMediaType`` and ``contentEncoding`` describe the content of a string.
This feature of JSON Schema is supported since Draft 7.

.. literalinclude:: schemas/feature-content.json
   :language: json
   :caption: Source: schemas/feature-content.json

.. jsonschema:: schemas/feature-content.json

Draft 2019-09
~~~~~~~~~~~~~

Definitions with ``$defs``
^^^^^^^^^^^^^^^^^^^^^^^^^^

``$defs`` replaces ``definitions`` as the place for reusable schemas.
This feature of JSON Schema is supported since Draft 2019-09.

.. literalinclude:: schemas/feature-defs.json
   :language: json
   :caption: Source: schemas/feature-defs.json

.. jsonschema:: schemas/feature-defs.json

Keywords next to ``$ref``
^^^^^^^^^^^^^^^^^^^^^^^^^

A schema with ``$ref`` may carry further keywords.
This feature of JSON Schema is supported since Draft 2019-09.

.. literalinclude:: schemas/feature-ref-siblings.json
   :language: json
   :caption: Source: schemas/feature-ref-siblings.json

.. jsonschema:: schemas/feature-ref-siblings.json

Anchors
^^^^^^^

``$anchor`` names a location inside a schema so that it can be referenced as ``#name``.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The anchor itself is not shown.

.. literalinclude:: schemas/feature-anchor.json
   :language: json
   :caption: Source: schemas/feature-anchor.json

.. jsonschema:: schemas/feature-anchor.json

Recursive references
^^^^^^^^^^^^^^^^^^^^

``$recursiveRef`` and ``$recursiveAnchor`` allow extensible recursive schemas.
This feature of JSON Schema is supported since Draft 2019-09 and was replaced in Draft 2020-12 by ``$dynamicRef``.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The reference is not shown.

.. literalinclude:: schemas/feature-recursive-ref.json
   :language: json
   :caption: Source: schemas/feature-recursive-ref.json

.. jsonschema:: schemas/feature-recursive-ref.json

Dependent required
^^^^^^^^^^^^^^^^^^

``dependentRequired`` makes a property require other properties.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-dependent-required.json
   :language: json
   :caption: Source: schemas/feature-dependent-required.json

.. jsonschema:: schemas/feature-dependent-required.json

Dependent schemas
^^^^^^^^^^^^^^^^^

``dependentSchemas`` applies a further schema if a property is present.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-dependent-schemas.json
   :language: json
   :caption: Source: schemas/feature-dependent-schemas.json

.. jsonschema:: schemas/feature-dependent-schemas.json

Contains with limits
^^^^^^^^^^^^^^^^^^^^

``minContains`` and ``maxContains`` limit how many items must match ``contains``.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keywords are ignored.

.. literalinclude:: schemas/feature-contains-min-max.json
   :language: json
   :caption: Source: schemas/feature-contains-min-max.json

.. jsonschema:: schemas/feature-contains-min-max.json

Unevaluated properties
^^^^^^^^^^^^^^^^^^^^^^

``unevaluatedProperties`` applies to properties that no other keyword has evaluated, even across ``allOf``.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-unevaluated-properties.json
   :language: json
   :caption: Source: schemas/feature-unevaluated-properties.json

.. jsonschema:: schemas/feature-unevaluated-properties.json

Unevaluated items
^^^^^^^^^^^^^^^^^

``unevaluatedItems`` applies to array items that no other keyword has evaluated.
This feature of JSON Schema is supported since Draft 2019-09.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword is ignored.

.. literalinclude:: schemas/feature-unevaluated-items.json
   :language: json
   :caption: Source: schemas/feature-unevaluated-items.json

.. jsonschema:: schemas/feature-unevaluated-items.json

Deprecated
^^^^^^^^^^

``deprecated`` marks a value that should no longer be used.
This feature of JSON Schema is supported since Draft 2019-09.

.. literalinclude:: schemas/feature-deprecated.json
   :language: json
   :caption: Source: schemas/feature-deprecated.json

.. jsonschema:: schemas/feature-deprecated.json

Content schema
^^^^^^^^^^^^^^

``contentSchema`` describes the structure of the decoded content of a string.
This feature of JSON Schema is supported since Draft 2019-09.

.. literalinclude:: schemas/feature-content-schema.json
   :language: json
   :caption: Source: schemas/feature-content-schema.json

.. jsonschema:: schemas/feature-content-schema.json

Draft 2020-12
~~~~~~~~~~~~~

Prefix items
^^^^^^^^^^^^

``prefixItems`` describes the array positions one by one; ``items`` now applies to all remaining items.
This feature of JSON Schema is supported since Draft 2020-12.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The keyword ``prefixItems`` is ignored.

.. literalinclude:: schemas/feature-prefix-items.json
   :language: json
   :caption: Source: schemas/feature-prefix-items.json

.. jsonschema:: schemas/feature-prefix-items.json

Dynamic references
^^^^^^^^^^^^^^^^^^

``$dynamicRef`` and ``$dynamicAnchor`` allow extensible recursive schemas.
This feature of JSON Schema is supported since Draft 2020-12.

.. note:: This feature is not rendered yet by this version of sphinx-jsonschema. The reference is not shown.

.. literalinclude:: schemas/feature-dynamic-ref.json
   :language: json
   :caption: Source: schemas/feature-dynamic-ref.json

.. jsonschema:: schemas/feature-dynamic-ref.json
