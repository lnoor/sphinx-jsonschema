"""Anchors (Draft 2019-09 and 2020-12) and the references that use them, rendered through the real directive.

``$anchor`` names a location of a schema so that ``$ref: "#name"`` can point at it. ``$dynamicAnchor`` and
``$dynamicRef`` (2020-12) and their predecessors ``$recursiveAnchor`` and ``$recursiveRef`` (2019-09) let a
reference be resolved at validation time. All of them are shown as a row with the keyword as label.
"""
import json

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


class TestAnchors:
    @pytest.mark.parametrize('keyword, value, shown', [
        ('$anchor', 'name', 'name'),
        ('$dynamicAnchor', 'node', 'node'),
        ('$recursiveAnchor', True, 'true'),
    ])
    def test_anchor_is_rendered_as_row(self, render, keyword, value, shown):
        """The keyword and its value come first, above the type."""
        out = render(doc({'type': 'string', keyword: value}))
        assert out.warnings == ''
        assert out.rows == [[keyword, shown], ['type', 'string']]

    def test_anchor_name_is_shown_literally(self, render):
        """Underscores of an anchor name are not taken for markup."""
        out = render(doc({'type': 'string', '$anchor': 'my_anchor_'}))
        assert out.rows[0] == ['$anchor', 'my_anchor_']

    def test_anchor_in_definitions(self, render):
        """An anchor inside ``$defs`` is shown with the definition it belongs to."""
        out = render(doc({'$defs': {'name': {'$anchor': 'name', 'type': 'string'}}}))
        assert ['name', '$anchor', 'name'] in out.rows


class TestDynamicReferences:
    @pytest.mark.parametrize('keyword, target', [
        ('$dynamicRef', '#node'),
        ('$recursiveRef', '#'),
    ])
    def test_reference_is_rendered_as_row(self, render, keyword, target):
        """The reference is shown with its keyword, so it can be told from a plain ``$ref``."""
        out = render(doc({'type': 'array', 'items': {keyword: target}}))
        assert out.warnings == ''
        assert out.rows == [['type', 'array'], ['items', keyword, target]]

    def test_reference_with_sibling_keywords(self, render):
        """Other keywords next to the reference are rendered as well."""
        out = render(doc({'$dynamicRef': '#node', 'description': 'A child.'}))
        assert out.rows == [['A child.'], ['$dynamicRef', '#node']]

    def test_recursive_reference_to_root_links_to_the_title(self, render):
        """``$recursiveRef: "#"`` points at the schema itself, exactly as ``$ref: "#"`` does."""
        schema = {
            'title': 'Tree',
            'type': 'object',
            'properties': {'children': {'type': 'array', 'items': {'$recursiveRef': '#'}}},
        }
        out = render(doc(schema, auto_reference='true'))
        assert out.warnings == ''
        assert ['items', '$recursiveRef', 'Tree'] in out.rows

    def test_reference_next_to_ref_keeps_both(self, render):
        """A schema may hold ``$ref`` and a dynamic reference; neither hides the other."""
        out = render(doc({'$ref': '#/$defs/a', '$dynamicRef': '#node'}))
        assert ['#/$defs/a'] in out.rows
        assert ['$dynamicRef', '#node'] in out.rows
