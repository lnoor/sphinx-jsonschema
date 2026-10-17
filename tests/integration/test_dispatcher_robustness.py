"""Schemas that stress the dispatcher: boolean schemas in every place and ``type`` lists.

A boolean schema (``true`` accepts everything, ``false`` accepts nothing) may stand wherever a
schema is expected, and ``type`` may list several types, so that the keywords of each apply.
"""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


class TestBooleanSchemas:
    @pytest.mark.parametrize('schema, expected', [
        ({'not': False}, ['not', 'false']),
        ({'allOf': [True, {'type': 'string'}]}, ['allOf', 'true']),
        ({'anyOf': [False, {'type': 'string'}]}, ['anyOf', 'false']),
        ({'if': True, 'then': {'type': 'string'}}, ['if', 'true']),
        ({'if': {'type': 'string'}, 'else': False}, ['else', 'false']),
        ({'dependencies': {'a': False}}, ['a', 'false']),
        ({'patternProperties': {'^x': True}}, ['^x', 'true']),
        ({'type': 'object', 'additionalProperties': False}, ['additionalProperties', 'false']),
        ({'type': 'array', 'items': [True, False]}, ['', 'false']),
    ], ids=['not', 'allOf', 'anyOf', 'if', 'else', 'dependencies', 'patternProperties',
            'additionalProperties', 'items-list'])
    def test_boolean_schema_is_rendered_where_a_schema_is_expected(self, render, schema, expected):
        """The boolean is shown as ``true`` / ``false`` in the row of the keyword that holds it."""
        out = render(doc(schema))
        assert out.warnings == ''
        assert expected in [row[-len(expected):] for row in out.rows]

    @pytest.mark.parametrize('value', [True, False])
    def test_boolean_schema_as_document_root(self, render, value):
        """A schema that is just ``true`` or ``false`` renders as a single row."""
        out = render(doc(value))
        assert out.warnings == ''
        assert out.rows == [[json.dumps(value)]]

    def test_boolean_definition_with_lift_definitions(self, render):
        """Definitions that are objects become sections; boolean ones stay in the definitions list."""
        schema = {
            'type': 'object',
            'definitions': {'yes': True, 'text': {'type': 'string'}},
        }
        out = render(doc(schema, lift_definitions=''))
        assert out.warnings == ''
        assert 'text' in out.section_titles
        assert ['yes', 'true'] in out.rows

    def test_boolean_definition_without_lift_definitions(self, render):
        """Without lifting, a boolean definition is listed like any other definition."""
        out = render(doc({'definitions': {'no': False}}))
        assert out.warnings == ''
        assert ['no', 'false'] in out.rows


class TestTypeLists:
    def test_object_and_array_keywords_are_both_rendered(self, render):
        """``type: [object, array]`` shows the properties as well as the items."""
        out = render(doc({
            'type': ['object', 'array'],
            'properties': {'name': {'type': 'string'}},
            'items': {'type': 'integer'},
        }))
        assert out.rows[0] == ['type', 'object / array']
        assert 'properties' in out.flat
        assert 'name' in out.flat
        assert 'items' in out.flat
        assert out.flat.count('type') == 3, 'one type row for each of the schema, name and items'

    def test_type_row_is_shown_once(self, render):
        """The type of a multi-type schema is not repeated for each type."""
        out = render(doc({'type': ['object', 'array'], 'items': {'type': 'integer'}}))
        assert out.rows.count(['type', 'object / array']) == 1

    @pytest.mark.parametrize('types, expected', [
        (['object', 'null'], ['properties', 'name']),
        (['array', 'null'], ['items']),
        (['string', 'array'], ['items']),
    ])
    def test_single_structured_type_in_a_list(self, render, types, expected):
        """Only the keywords of the listed structured type are rendered, as before."""
        out = render(doc({
            'type': types,
            'properties': {'name': {'type': 'string'}},
            'items': {'type': 'integer'},
        }))
        assert out.warnings == ''
        assert set(expected) <= set(out.flat)
        assert ('items' in out.flat) == ('array' in types)
