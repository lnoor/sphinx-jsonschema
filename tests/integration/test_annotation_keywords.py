"""Annotation keywords of Drafts 7 and 2019-09, rendered through the real directive.

They do not constrain the instance; they describe it. Each one is shown as a row of its own,
below the type of the schema it belongs to.
"""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


@pytest.mark.parametrize('keyword, value, shown', [
    ('deprecated', True, 'true'),
    ('deprecated', False, 'false'),
    ('readOnly', True, 'true'),
    ('writeOnly', True, 'true'),
    ('contentMediaType', 'image/png', 'image/png'),
    ('contentEncoding', 'base64', 'base64'),
])
def test_annotation_is_rendered_as_row(render, keyword, value, shown):
    """The keyword and its value appear as a row below the type."""
    out = render(doc({'type': 'string', keyword: value}))
    assert out.warnings == ''
    assert out.rows == [['type', 'string'], [keyword, shown]]


def test_annotations_of_a_property_are_rendered(render):
    """Annotations inside ``properties`` are shown with the property, as for any other keyword."""
    out = render(doc({
        'type': 'object',
        'properties': {'id': {'type': 'integer', 'readOnly': True}},
    }))
    assert ['id', 'type', 'integer'] in out.rows
    assert ['readOnly', 'true'] in out.rows


def test_annotations_of_an_object_do_not_hide_its_properties(render):
    """``deprecated`` on an object is shown in addition to the properties."""
    out = render(doc({
        'type': 'object',
        'deprecated': True,
        'properties': {'a': {'type': 'string'}},
    }))
    assert ['deprecated', 'true'] in out.rows
    assert 'a' in out.flat


def test_content_schema_is_rendered_as_subschema(render):
    """``contentSchema`` describes the decoded content and is rendered like a nested schema."""
    out = render(doc({
        'type': 'string',
        'contentMediaType': 'application/json',
        'contentSchema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
    }))
    assert out.warnings == ''
    assert ['contentMediaType', 'application/json'] in out.rows
    assert ['contentSchema', 'type', 'object'] in out.rows
    assert 'id' in out.flat


def test_boolean_content_schema(render):
    """A boolean ``contentSchema`` is shown as ``true`` / ``false``."""
    out = render(doc({'type': 'string', 'contentSchema': False}))
    assert out.rows == [['type', 'string'], ['contentSchema', 'false']]
