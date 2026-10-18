"""``propertyNames`` (Draft 6), rendered through the real directive."""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


@pytest.mark.parametrize('names, expected', [
    ({'pattern': '^[a-z]+$'}, ['propertyNames', 'pattern', '^[a-z]+$']),
    ({'maxLength': 8}, ['propertyNames', 'maxLength', '8']),
    ({'enum': ['a', 'b']}, ['propertyNames', 'enum', 'a, b']),
    (True, ['propertyNames', 'true']),
    (False, ['propertyNames', 'false']),
], ids=['pattern', 'maxLength', 'enum', 'true', 'false'])
def test_property_names_is_rendered_as_subschema(render, names, expected):
    """The constraint on the names is shown like any other subschema, or as ``true`` / ``false``."""
    out = render(doc({'type': 'object', 'propertyNames': names}))
    assert out.warnings == ''
    assert out.rows == [['type', 'object'], expected]


def test_property_names_without_type(render):
    """An object schema without ``type`` is rendered like one with it."""
    out = render(doc({'propertyNames': {'minLength': 1}}))
    assert out.rows == [['propertyNames', 'minLength', '1']]


def test_property_names_follows_the_properties(render):
    """The keyword is shown after the properties and the additional properties it complements."""
    out = render(doc({
        'type': 'object',
        'properties': {'a': {'type': 'string'}},
        'additionalProperties': False,
        'propertyNames': {'maxLength': 1},
    }))
    assert out.rows == [
        ['type', 'object'],
        ['properties'],
        ['a', 'type', 'string'],
        ['additionalProperties', 'false'],
        ['propertyNames', 'maxLength', '1'],
    ]


def test_property_names_of_a_property(render):
    """Inside ``properties`` the property name is prepended."""
    out = render(doc({
        'type': 'object',
        'properties': {'labels': {'type': 'object', 'propertyNames': {'pattern': '^x-'}}},
    }))
    assert ['labels', 'type', 'object'] in out.rows
    assert ['propertyNames', 'pattern', '^x-'] in out.rows
