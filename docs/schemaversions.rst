
Supported JSON Schema versions
==============================

**sphinx-jsonschema** was initially written for `JSON Schema Draft 4 <http://json-schema.org/specification-links.html#draft-4>`_.
It renders the keywords of the later drafts up to Draft 2020-12 as well.

The plugin does not need to know which draft a schema is written for.
The names of the keywords hardly overlap between the drafts, so every keyword is rendered when it is present and ignored otherwise.
Where two drafts use the same keyword differently, the value tells them apart.
A list in ``items`` is the tuple form of Draft 4 to 2019-09, a schema in ``items`` next to ``prefixItems`` is the form of Draft 2020-12.
The ``$schema`` keyword therefore does not influence the output.
The option ``show_schema`` displays it, see :doc:`directive`.

Supported keywords
------------------

The tables list the draft that introduced each keyword.
A keyword stays available in the later drafts unless the notes say it was replaced.

Core
^^^^

.. list-table::
    :header-rows: 1
    :widths: 25 15 60

    * - Keyword
      - Since
      - Rendering
    * - ``$schema``
      - Draft 4
      - Hidden; the option ``show_schema`` adds a first row with the value (root of the schema only).
    * - ``id``, ``$id``
      - Draft 4, Draft 6
      - First row of the table; only the outermost value is shown.
        ``$id`` replaced ``id`` in Draft 6.
    * - ``$comment``
      - Draft 7
      - Hidden; the option ``show_comments`` adds a row.
    * - ``$ref``
      - Draft 4
      - A link or plain text, see :doc:`directive`.
        Keywords next to ``$ref`` are rendered, ahead of the reference.
    * - ``definitions``, ``$defs``
      - Draft 4, Draft 2019-09
      - A list of the definitions, or separate sections with ``lift_definitions``.
        ``$defs`` replaced ``definitions``.
    * - ``$anchor``, ``$dynamicAnchor``, ``$recursiveAnchor``
      - Draft 2019-09, 2020-12
      - A row of the schema it belongs to.
        The anchor is not a link target.
    * - ``$dynamicRef``, ``$recursiveRef``
      - Draft 2020-12, 2019-09
      - Rendered like ``$ref``, with the keyword as label.
        ``$dynamicRef`` replaced ``$recursiveRef``.
    * - ``$vocabulary``
      - Draft 2019-09
      - Not rendered, because it only occurs in meta-schemas.

Types and values
^^^^^^^^^^^^^^^^

.. list-table::
    :header-rows: 1
    :widths: 25 15 60

    * - Keyword
      - Since
      - Rendering
    * - ``title``, ``description``
      - Draft 4
      - Section heading and text; reStructuredText is allowed.
    * - ``type``
      - Draft 4
      - A list of types is shown as ``a / b``; the keywords of every listed structured type are rendered.
    * - ``enum``, ``default``
      - Draft 4
      - A row each.
    * - ``const``
      - Draft 6
      - A row.
    * - ``examples``
      - Draft 6
      - A row group.
    * - ``format``, ``pattern``, ``multipleOf``, ``minimum``, ``maximum``, ``minLength``, ``maxLength``
      - Draft 4
      - A row each.
    * - ``exclusiveMinimum``, ``exclusiveMaximum``
      - Draft 4, Draft 6
      - A row each.
        Boolean in Draft 4, a number from Draft 6 on.
    * - ``deprecated``
      - Draft 2019-09
      - A row.
    * - ``readOnly``, ``writeOnly``
      - Draft 7
      - A row each.
    * - ``contentMediaType``, ``contentEncoding``
      - Draft 7
      - A row each.
    * - ``contentSchema``
      - Draft 2019-09
      - A nested schema.

Arrays
^^^^^^

.. list-table::
    :header-rows: 1
    :widths: 25 15 60

    * - Keyword
      - Since
      - Rendering
    * - ``items``
      - Draft 4
      - A schema, or a list of schemas for the tuple form (Draft 4 to 2019-09).
    * - ``additionalItems``
      - Draft 4
      - A schema or a boolean.
        Replaced by ``items`` in Draft 2020-12.
    * - ``prefixItems``
      - Draft 2020-12
      - Rendered like the list form of ``items``.
    * - ``contains``
      - Draft 6
      - A nested schema.
    * - ``minContains``, ``maxContains``
      - Draft 2019-09
      - A row each, below ``contains``.
    * - ``minItems``, ``maxItems``, ``uniqueItems``
      - Draft 4
      - A row each.
    * - ``unevaluatedItems``
      - Draft 2019-09
      - A schema or a boolean.

Objects
^^^^^^^

.. list-table::
    :header-rows: 1
    :widths: 25 15 60

    * - Keyword
      - Since
      - Rendering
    * - ``properties``, ``patternProperties``, ``required``
      - Draft 4
      - A list of the properties; required ones are shown in bold.
    * - ``additionalProperties``
      - Draft 4
      - A schema or a boolean.
    * - ``propertyNames``
      - Draft 6
      - A nested schema.
    * - ``minProperties``, ``maxProperties``
      - Draft 4
      - A row each.
    * - ``dependencies``
      - Draft 4
      - A list; the values are property names or schemas.
        Replaced in Draft 2019-09.
    * - ``dependentRequired``, ``dependentSchemas``
      - Draft 2019-09
      - Rendered like ``dependencies``.
    * - ``unevaluatedProperties``
      - Draft 2019-09
      - A schema or a boolean.

Combining schemas
^^^^^^^^^^^^^^^^^

.. list-table::
    :header-rows: 1
    :widths: 25 15 60

    * - Keyword
      - Since
      - Rendering
    * - ``allOf``, ``anyOf``, ``oneOf``, ``not``
      - Draft 4
      - Nested schemas.
    * - ``if``, ``then``, ``else``
      - Draft 7
      - Nested schemas; shown when at least two of the three have content.
    * - Boolean schemas
      - Draft 6
      - ``true`` and ``false`` are shown wherever a schema is expected.

Known limitations
-----------------

* Array keywords (``items``, ``prefixItems``, ``contains``, ``unevaluatedItems`` and so on) are only rendered for schemas with ``type: array``.
  A schema without ``type`` is rendered as an object, so a subschema such as ``{"items": [...]}`` in an ``allOf`` needs ``"type": "array"``.
* Anchors are shown, but ``$ref: "#name"`` does not link to them.
* ``$vocabulary`` is ignored, so meta-schemas are only shown without their vocabularies.
