"""``unevaluatedProperties`` and ``unevaluatedItems`` (Draft 2019-09), rendered through the real directive.

They work like ``additionalProperties`` and ``additionalItems``, but also see the properties and items
that were evaluated by subschemas, for example in ``allOf``. They are rendered like their counterparts.
"""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


class TestUnevaluatedProperties:
    @pytest.mark.parametrize('value, expected', [
        (False, ['unevaluatedProperties', 'false']),
        (True, ['unevaluatedProperties', 'true']),
        ({'type': 'string'}, ['unevaluatedProperties', 'type', 'string']),
    ], ids=['false', 'true', 'schema'])
    def test_value_is_rendered(self, render, value, expected):
        """A boolean is shown as such, a schema as nested rows."""
        out = render(doc({'type': 'object', 'unevaluatedProperties': value}))
        assert out.warnings == ''
        assert out.rows == [['type', 'object'], expected]

    def test_without_type(self, render):
        """An object schema without ``type`` is rendered like one with it."""
        out = render(doc({'unevaluatedProperties': False}))
        assert out.rows == [['unevaluatedProperties', 'false']]

    def test_combined_with_all_of(self, render):
        """The keyword is shown with the object keywords, ahead of the combinators it looks into."""
        out = render(doc({
            'type': 'object',
            'allOf': [{'properties': {'name': {'type': 'string'}}}],
            'unevaluatedProperties': False,
        }))
        assert out.rows == [
            ['type', 'object'],
            ['unevaluatedProperties', 'false'],
            ['allOf', 'properties'],
            ['name', 'type', 'string'],
        ]

    def test_of_a_property(self, render):
        """Inside ``properties`` the property name is prepended."""
        out = render(doc({
            'type': 'object',
            'properties': {'address': {'type': 'object', 'unevaluatedProperties': False}},
        }))
        assert ['address', 'type', 'object'] in out.rows
        assert ['unevaluatedProperties', 'false'] in out.rows


class TestUnevaluatedItems:
    @pytest.mark.parametrize('value, expected', [
        (False, ['unevaluatedItems', 'false']),
        (True, ['unevaluatedItems', 'true']),
        ({'type': 'integer'}, ['unevaluatedItems', 'type', 'integer']),
    ], ids=['false', 'true', 'schema'])
    def test_value_is_rendered(self, render, value, expected):
        """A boolean is shown as such, a schema as nested rows."""
        out = render(doc({'type': 'array', 'unevaluatedItems': value}))
        assert out.warnings == ''
        assert out.rows == [['type', 'array'], expected]

    def test_combined_with_all_of(self, render):
        """The keyword is shown with the array keywords, ahead of the combinators it looks into."""
        out = render(doc({
            'type': 'array',
            'allOf': [{'type': 'array', 'items': [{'type': 'string'}]}],
            'unevaluatedItems': False,
        }))
        assert out.rows[:2] == [['type', 'array'], ['unevaluatedItems', 'false']]
        assert out.rows[2][0] == 'allOf'

    def test_follows_items(self, render):
        """The keyword is shown after the items it complements."""
        out = render(doc({'type': 'array', 'items': {'type': 'string'}, 'unevaluatedItems': False}))
        assert out.rows == [['type', 'array'], ['items', 'type', 'string'], ['unevaluatedItems', 'false']]
