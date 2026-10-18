"""``contains`` (Draft 6) and ``minContains`` / ``maxContains`` (Draft 2019-09), rendered through the real directive."""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def test_contains_is_rendered_as_subschema(render):
    """``contains`` is shown like ``items``: a row labelled with the keyword, holding the subschema."""
    out = render(doc({'type': 'array', 'contains': {'type': 'string'}}))
    assert out.warnings == ''
    assert out.rows == [['type', 'array'], ['contains', 'type', 'string']]


def test_contains_with_const(render):
    """The example from the demo: at least one item equals a constant."""
    out = render(doc({'type': 'array', 'items': {'type': 'string'}, 'contains': {'const': 'admin'}}))
    assert out.rows == [
        ['type', 'array'],
        ['items', 'type', 'string'],
        ['contains', 'const', 'admin'],
    ]


@pytest.mark.parametrize('value', [True, False])
def test_contains_boolean_schema(render, value):
    """A boolean subschema is shown as ``true`` / ``false``."""
    out = render(doc({'type': 'array', 'contains': value}))
    assert out.rows == [['type', 'array'], ['contains', json.dumps(value)]]


def test_min_and_max_contains_follow_contains(render):
    """The limits are shown directly below the ``contains`` they refer to."""
    out = render(doc({
        'type': 'array',
        'contains': {'const': 'admin'},
        'minContains': 2,
        'maxContains': 3,
        'maxItems': 10,
    }))
    assert out.rows == [
        ['type', 'array'],
        ['contains', 'const', 'admin'],
        ['minContains', '2'],
        ['maxContains', '3'],
        ['maxItems', '10'],
    ]


def test_min_contains_zero_is_shown(render):
    """``minContains: 0`` makes ``contains`` optional; the zero must not be swallowed."""
    out = render(doc({'type': 'array', 'contains': {'type': 'integer'}, 'minContains': 0}))
    assert ['minContains', '0'] in out.rows


def test_contains_of_a_property(render):
    """Inside ``properties`` the property name is prepended, as for every other array keyword."""
    out = render(doc({
        'type': 'object',
        'properties': {'roles': {'type': 'array', 'contains': {'const': 'admin'}}},
    }))
    assert ['roles', 'type', 'array'] in out.rows
    assert ['contains', 'const', 'admin'] in out.rows
