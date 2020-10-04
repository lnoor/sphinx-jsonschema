Extending jsonschema
====================

I didn't create jsonschema with extensibility in mind.
But I also never thought so many people would find it useful.

Render custom keywords
----------------------

That being said `ankostis <https://github.com/ankostis>`_ needed a way to render his own custom keywords.
This is his solution, you need to append this code to your `conf.py` file.

.. code-block:: python

    ## PATCH `sphinx-jsonschema`
    #  to render the extra `units`` and ``tags`` schema properties
    #
    def _patched_sphinx_jsonschema_simpletype(self, schema):
        """Render the *extra* ``units`` and ``tags`` schema properties for every object."""
        rows = _original_sphinx_jsonschema_simpletype(self, schema)

        if "units" in schema:
            units = schema["units"]
            units = f"``{units}``"
            rows.append(self._line(self._cell("units"), self._cell(units)))
            del schema["units"]

        if "tags" in schema:
            tags = ", ".join(f"``{tag}``" for tag in schema["tags"])
            rows.append(self._line(self._cell("tags"), self._cell(tags)))
            del schema["tags"]

        return rows

    sjs_wide_format = importlib.import_module("sphinx-jsonschema.wide_format")
    _original_sphinx_jsonschema_simpletype = sjs_wide_format.WideFormat._simpletype  # type: ignore
    sjs_wide_format.WideFormat._simpletype = _patched_sphinx_jsonschema_simpletype  # type: ignore

