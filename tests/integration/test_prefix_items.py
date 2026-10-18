"""``prefixItems`` (Draft 2020-12) next to the older tuple form, rendered through the real directive.

Up to Draft 2019-09 a list in ``items`` describes the positions of a tuple and ``additionalItems`` the
rest. Draft 2020-12 moves the positions to ``prefixItems``; ``items`` then holds the schema for the rest.
"""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def test_prefix_items_are_rendered_as_positions(render):
    """One row for the keyword, then one row per position."""
    out = render(doc({'type': 'array', 'prefixItems': [{'type': 'string'}, {'type': 'integer'}]}))
    assert out.warnings == ''
    assert out.rows == [
        ['type', 'array'],
        ['prefixItems'],
        ['', 'type', 'string'],
        ['', 'type', 'integer'],
    ]


def test_items_after_prefix_items_describes_the_remaining_items(render):
    """``items`` as a schema keeps its label and follows the positions."""
    out = render(doc({'type': 'array', 'prefixItems': [{'type': 'string'}], 'items': {'type': 'number'}}))
    assert out.rows == [
        ['type', 'array'],
        ['prefixItems'],
        ['', 'type', 'string'],
        ['items', 'type', 'number'],
    ]


def test_items_false_closes_the_tuple(render):
    """``items: false`` after ``prefixItems`` forbids further items and is shown as such."""
    out = render(doc({'type': 'array', 'prefixItems': [{'type': 'string'}], 'items': False}))
    assert out.rows[-1] == ['items', 'false']


def test_boolean_schema_as_position(render):
    """A position may be a boolean schema."""
    out = render(doc({'type': 'array', 'prefixItems': [True, False]}))
    assert out.rows == [['type', 'array'], ['prefixItems'], ['', 'true'], ['', 'false']]


def test_prefix_items_of_a_property(render):
    """Inside ``properties`` the property name is prepended, as for every other array keyword."""
    out = render(doc({
        'type': 'object',
        'properties': {'entry': {'type': 'array', 'prefixItems': [{'type': 'string', 'description': 'name'}]}},
    }))
    assert ['entry', 'type', 'array'] in out.rows
    assert 'prefixItems' in out.flat
    assert 'name' in out.flat


@pytest.mark.parametrize('extra, expected_last', [
    ({'additionalItems': False}, ['additionalItems', 'false']),
    ({'additionalItems': {'type': 'number'}}, ['additionalItems', 'type', 'number']),
])
def test_tuple_form_with_items_list_is_unchanged(render, extra, expected_last):
    """Draft 4 to 2019-09: a list in ``items`` is still rendered as the positions, with ``additionalItems``."""
    out = render(doc({'type': 'array', 'items': [{'type': 'string'}], **extra}))
    assert out.rows == [
        ['type', 'array'],
        ['items'],
        ['', 'type', 'string'],
        expected_last,
    ]
