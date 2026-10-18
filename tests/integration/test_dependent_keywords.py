"""``dependentRequired`` and ``dependentSchemas`` (Draft 2019-09) next to ``dependencies`` (Drafts 4 to 7).

Draft 2019-09 split ``dependencies`` in two: a list of property names became ``dependentRequired``, a
schema became ``dependentSchemas``. Both are rendered like ``dependencies``, one row for each property.
"""
import json


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


class TestDependentRequired:
    def test_required_properties_are_listed(self, render):
        """The property that triggers the requirement is shown with the names it requires."""
        out = render(doc({'type': 'object', 'dependentRequired': {'credit_card': ['billing_address']}}))
        assert out.warnings == ''
        assert out.rows == [
            ['type', 'object'],
            ['dependentRequired'],
            ['credit_card', 'billing_address'],
        ]

    def test_several_names_and_properties(self, render):
        """Several required names are joined; every property gets a row of its own."""
        out = render(doc({
            'type': 'object',
            'dependentRequired': {'a': ['b', 'c'], 'd': ['e']},
        }))
        assert out.rows[1:] == [['dependentRequired'], ['a', 'b, c'], ['d', 'e']]

    def test_without_type(self, render):
        """An object schema without ``type`` is rendered like one with it."""
        out = render(doc({'dependentRequired': {'a': ['b']}}))
        assert out.rows == [['dependentRequired'], ['a', 'b']]


class TestDependentSchemas:
    def test_schema_is_rendered_below_the_property(self, render):
        """The schema that applies if the property is present is rendered as nested rows."""
        out = render(doc({
            'type': 'object',
            'dependentSchemas': {'credit_card': {'properties': {'billing_address': {'type': 'string'}}}},
        }))
        assert out.warnings == ''
        assert out.rows[:3] == [['type', 'object'], ['dependentSchemas'], ['credit_card', 'properties']]
        assert ['billing_address', 'type', 'string'] in out.rows

    def test_boolean_schema(self, render):
        """A boolean schema is shown as ``true`` / ``false``."""
        out = render(doc({'type': 'object', 'dependentSchemas': {'a': False}}))
        assert out.rows == [['type', 'object'], ['dependentSchemas'], ['a', 'false']]

    def test_without_type(self, render):
        """An object schema without ``type`` is rendered like one with it."""
        out = render(doc({'dependentSchemas': {'a': {'minProperties': 2}}}))
        assert ['dependentSchemas'] in out.rows
        assert ['a', 'minProperties', '2'] in out.rows


class TestDependencies:
    def test_older_keyword_is_unchanged(self, render):
        """Drafts 4 to 7: both forms of ``dependencies`` are rendered as before."""
        out = render(doc({
            'type': 'object',
            'dependencies': {'a': ['b'], 'c': {'minProperties': 2}},
        }))
        assert out.rows == [
            ['type', 'object'],
            ['dependencies'],
            ['a', 'b'],
            ['c', 'minProperties', '2'],
        ]
