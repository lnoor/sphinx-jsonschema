"""Keywords next to ``$ref``, rendered through the real directive.

Up to Draft 7 a validator ignores everything next to a ``$ref``. From Draft 2019-09 on, those keywords
apply as well. The plugin renders them in either case: the keywords first, then the reference.
"""
import json


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def test_description_next_to_ref(render):
    """The example from the demo: a description of the property that refers to a definition."""
    out = render(doc({
        'type': 'object',
        'properties': {'shipping': {'$ref': '#/$defs/address', 'description': 'Where to ship to.'}},
        '$defs': {'address': {'type': 'string'}},
    }))
    assert out.warnings == ''
    assert ['shipping', 'Where to ship to.'] in out.rows
    assert ['#/$defs/address'] in out.rows


def test_type_and_constraints_next_to_ref(render):
    """Simple keywords are shown ahead of the reference."""
    out = render(doc({'$ref': '#/$defs/a', 'type': 'string', 'minLength': 2}))
    assert out.rows == [['type', 'string'], ['minLength', '2'], ['#/$defs/a']]


def test_object_keywords_next_to_ref(render):
    """Properties next to the reference are rendered, followed by the reference."""
    out = render(doc({'$ref': '#/$defs/a', 'properties': {'extra': {'type': 'string'}}}))
    assert out.rows == [['properties'], ['extra', 'type', 'string'], ['#/$defs/a']]


def test_combinator_next_to_ref(render):
    """A combinator next to the reference keeps its rows as well."""
    out = render(doc({'$ref': '#/$defs/a', 'allOf': [{'type': 'string'}]}))
    assert out.rows == [['#/$defs/a'], ['allOf', 'type', 'string']]


def test_ref_with_siblings_inside_a_list(render):
    """The keywords next to a ``$ref`` in ``items`` are rendered below ``items``."""
    out = render(doc({
        'type': 'array',
        'items': {'$ref': '#/$defs/a', 'description': 'One entry.'},
    }))
    assert out.rows == [['type', 'array'], ['items', 'One entry.'], ['#/$defs/a']]


def test_siblings_with_linked_reference(render):
    """With lifted definitions and ``auto_reference`` the reference becomes a link and the siblings stay."""
    schema = {
        'title': 'Order',
        'type': 'object',
        'properties': {'shipping': {'$ref': '#/$defs/address', 'description': 'Where to ship to.'}},
        '$defs': {'address': {'title': 'Address', 'type': 'string'}},
    }
    out = render(doc(schema, lift_definitions='', auto_reference=''))
    assert out.warnings == ''
    assert 'Address' in out.section_titles
    assert ['shipping', 'Where to ship to.'] in out.rows
    assert ['Address'] in out.rows
    assert list(out.root.iter('reference')), 'the reference is a link'
