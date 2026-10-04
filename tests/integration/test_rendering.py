"""How individual schema keywords are rendered into the table.

Each test feeds a small inline schema to the real directive and compares the
resulting table rows. A row is a list of cell texts: the first cell is the
keyword or property label, the following cells hold its value or nested rows.
"""
import json

import pytest


def directive(schema, options=''):
    """Wrap `schema` (a dict) into a minimal page containing one jsonschema directive."""
    body = json.dumps(schema, indent=2).replace('\n', '\n    ')
    return f"Doc\n===\n\n.. jsonschema::\n{options}\n    {body}\n"


@pytest.mark.parametrize('schema, expected', [
    # keyword constraints are listed after the type, one row each
    ({'type': 'string', 'minLength': 3},
     [['type', 'string'], ['minLength', '3']]),
    # a list of types is joined with " / "
    ({'type': ['string', 'null']},
     [['type', 'string / null']]),
    # enum values are rendered comma separated on a single row
    ({'type': 'integer', 'enum': [1, 2, 3]},
     [['type', 'integer'], ['enum', '1, 2, 3']]),
    # The extension escapes "_" and "*" in patterns so reStructuredText does not
    # treat them as markup. After Sphinx has parsed the cell the characters appear
    # literally, i.e. the pattern is shown unchanged and no emphasis is created.
    ({'type': 'string', 'pattern': '^a_b*$'},
     [['type', 'string'], ['pattern', '^a_b*$']]),
    # The description comes first, then the type, then constraints in the fixed
    # order of WideFormat.KV_SIMPLE (maximum is listed before minimum).
    ({'type': 'number', 'description': 'A number', 'minimum': 0, 'maximum': 10},
     [['A number'], ['type', 'number'], ['maximum', '10'], ['minimum', '0']]),
], ids=['string-constraint', 'type-list', 'enum', 'pattern-literal', 'description-first'])
def test_simple_types(render, schema, expected):
    """Scalar types render as plain key/value rows and produce no Sphinx warnings."""
    out = render(directive(schema))
    assert out.rows == expected
    assert out.warnings == ''


def test_object_properties_and_required(render):
    """Properties are listed under a "properties" row; required ones are bold."""
    out = render(directive({
        'type': 'object',
        'properties': {'name': {'type': 'string'}, 'age': {'type': 'integer'}},
        'required': ['name'],
    }))
    # The "- " the extension puts in front of each property name is bullet-list
    # syntax and does not show up in the cell text.
    assert out.rows == [
        ['type', 'object'],
        ['properties'],
        ['name', 'type', 'string'],
        ['age', 'type', 'integer'],
    ]
    # "required" is expressed as bold text (<strong>) on the property label only.
    required = [s.text for s in out.root.iter('strong')]
    assert required == ['name']


def test_array_items(render):
    """The schema of the array items is nested under an "items" row."""
    out = render(directive({'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}))
    assert out.rows == [['type', 'array'], ['items', 'type', 'string'], ['minItems', '1']]


@pytest.mark.parametrize('keyword', ['allOf', 'anyOf', 'oneOf'])
def test_combinators(render, keyword):
    """Combinators are labelled with their keyword and list every alternative."""
    out = render(directive({keyword: [{'type': 'string'}, {'type': 'integer'}]}))
    assert out.flat[0] == keyword
    assert 'string' in out.flat and 'integer' in out.flat


def test_additional_properties_false(render):
    """A boolean additionalProperties is shown as a simple key/value row."""
    out = render(directive({'type': 'object', 'additionalProperties': False}))
    assert ['additionalProperties', 'False'] in out.rows


def test_default_and_examples(render):
    """default and examples are rendered as rows; each example gets its own line."""
    out = render(directive({'type': 'string', 'default': 'x', 'examples': ['a', 'b']}))
    assert out.rows[0] == ['type', 'string']
    assert ['default', 'x'] in out.rows
    assert 'a' in out.flat and 'b' in out.flat
