"""Less common schema keywords and cross-references, rendered through the real directive."""
import json
import textwrap

import pytest


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def first_cells(out):
    """First cell of every non-empty row, i.e. the row labels."""
    return [row[0] for row in out.rows if row]


def test_conditional_renders_if_then_else(render):
    """if/then/else produce three labelled blocks; each branch's content is rendered."""
    out = render(doc({
        'if': {'properties': {'a': {'const': 1}}},
        'then': {'properties': {'b': {'type': 'string'}}},
        'else': {'properties': {'c': {'type': 'integer'}}},
    }))
    assert {'if', 'then', 'else'} <= set(first_cells(out))
    assert {'b', 'c'} <= set(out.flat)


def test_description_list_is_joined_into_lines(render):
    """The extension keyword ``$$description`` may be a list; its items become lines of one text."""
    out = render(doc({'type': 'string', '$$description': ['first line', 'second line']}))
    assert out.rows[0] == ['first line second line']


def test_hide_key_with_deep_wildcard_removes_all_matches(render):
    """``/**/examples`` hides ``examples`` at every depth (the example from the documentation)."""
    schema = {
        'type': 'object',
        'examples': ['top'],
        'properties': {'a': {'type': 'string', 'examples': ['nested']}},
    }
    out = render(doc(schema, hide_key='/**/examples'))
    assert 'examples' not in out.flat
    assert 'a' in out.flat


def test_hide_key_accepts_quoted_path_containing_comma(render):
    """The option value is a comma separated list; quoting allows a comma inside a path."""
    schema = {'type': 'object', 'properties': {'keep': {'type': 'string'}, 'a, b': {'type': 'string'}}}
    out = render(doc(schema, hide_key='"/properties/a, b"'))
    assert 'keep' in out.flat
    assert 'a, b' not in out.flat


class TestCrossReferences:
    """Targets and references between schemas.

    Sphinx reports a dangling ``:ref:`` as "undefined label". The tests below use
    that warning as the signal for "reference did not resolve".
    """

    def test_dollar_target_creates_referenceable_label(self, render):
        """``$$target`` in a schema defines a label other pages can ``:ref:``."""
        source = doc({'type': 'string', '$$target': 'my-label'}) + "\nSee :ref:`my-label`.\n"
        out = render(source)
        assert out.warnings == ''
        assert list(out.root.iter('target'))

    def test_reference_to_unknown_label_is_warned_about(self, render):
        """Control: proves this harness would notice a broken reference at all."""
        out = render(doc({'type': 'string'}) + "\nSee :ref:`nowhere`.\n")
        assert 'undefined label' in out.warnings

    def test_unresolved_ref_is_plain_text_by_default(self, render):
        """A ``$ref`` without a matching label is shown as text and does not warn.

        This is the minimal example from lnoor/sphinx-jsonschema#88 (pydantic style
        ``#/$defs/...`` pointer, no ``:auto_reference:``) and the "other file" part of #99.
        """
        schema = {'properties': {'item': {'$ref': '#/$defs/Item'}, 'file': {'$ref': 'other.json'}},
                  '$defs': {'Item': {'type': 'string'}}}
        out = render(doc(schema))
        assert out.warnings == ''
        assert '#/$defs/Item' in out.flat
        assert 'other.json' in out.flat

    def test_unresolved_ref_warns_with_warn_unresolved_refs(self, render):
        """``:warn_unresolved_refs:`` restores Sphinx's "undefined label" warning for a dangling ``$ref``."""
        out = render(doc({'properties': {'u': {'$ref': '#/definitions/User'}}}, warn_unresolved_refs='true'))
        assert "undefined label: '#/definitions/user'" in out.warnings

    def test_warn_unresolved_refs_can_be_set_in_conf(self, render):
        """The option is also available through ``jsonschema_options`` in ``conf.py``."""
        out = render(doc({'properties': {'u': {'$ref': '#/definitions/User'}}}),
                     conf="jsonschema_options = {'warn_unresolved_refs': True}\n")
        assert 'undefined label' in out.warnings

    @pytest.mark.parametrize('options', [{}, {'warn_unresolved_refs': 'true'}], ids=['quiet', 'warning'])
    def test_ref_to_existing_label_is_linked(self, render, options):
        """A ``$ref`` that matches a ``$$target`` label becomes a link, whatever the warning setting."""
        schema = {'$$target': 'my-label', 'properties': {'p': {'$ref': 'my-label'}}}
        out = render(doc(schema, **options))
        assert out.warnings == ''
        assert 'my-label' in [r.get('refid') for r in out.root.iter('reference')]

    @pytest.mark.parametrize('options', [
        {},
        {'auto_reference': 'true'},
        {'auto_reference': 'true', 'lift_title': 'false'},
    ], ids=['default', 'auto_reference', 'auto_reference-no-lift_title'])
    @pytest.mark.parametrize('target', [
        'http://example.com/schema.json',
        'https://example.com/schema.json#/definitions/User',
        '#',
    ], ids=['url', 'url-with-pointer', 'root'])
    def test_ref_that_cannot_be_a_label_is_plain_text(self, render, options, target):
        """URLs and the root ``#`` can never be Sphinx labels, so they must not be ``:ref:`` (#99)."""
        out = render(doc({'properties': {'p': {'$ref': target}}}, **options))
        assert out.warnings == ''
        assert target in out.flat

    def test_auto_reference_links_definition_title(self, render):
        """With ``:auto_reference:`` and ``:lift_definitions:`` a local ``$ref`` links to the section."""
        schema = {
            'title': 'Root',
            'properties': {'user': {'$ref': '#/definitions/User'}},
            'definitions': {'User': {'type': 'object', 'properties': {'name': {'type': 'string'}}}},
        }
        out = render(doc(schema, lift_definitions='true', auto_reference='true'))
        assert out.warnings == ''
        assert 'User' in [r.text for r in out.root.iter('reference')]

    def test_auto_reference_to_other_schema_file_uses_auto_target(self, render):
        """A ``$ref`` to another schema file resolves via the label ``:auto_target:`` created for it."""
        source = textwrap.dedent('''\
            Doc
            ===

            .. jsonschema:: other.json
                :auto_target: true

            .. jsonschema::
                :auto_reference: true
                :auto_target: true

                {"properties": {"o": {"$ref": "other.json"}}}
            ''')
        out = render(source, files={'other.json': json.dumps({'type': 'string'})})
        assert out.warnings == ''
        # The label "other.json" produces the anchor id "other-json" (Sphinx normalises the name).
        assert 'other-json' in [r.get('refid') for r in out.root.iter('reference')]


class TestPythonObjectSource:
    """Schema taken from a Python object: ``.. jsonschema:: package.module.NAME``."""

    def test_schema_from_python_module_attribute(self, render, tmp_path, monkeypatch):
        """The attribute is imported and its string form is parsed as the schema."""
        (tmp_path / 'schema_mod_ok.py').write_text("SCHEMA = {'type': 'integer', 'minimum': 5}\n")
        monkeypatch.syspath_prepend(str(tmp_path))
        out = render("Doc\n===\n\n.. jsonschema:: schema_mod_ok.SCHEMA\n")
        assert out.rows == [['type', 'integer'], ['minimum', '5']]

    def test_unimportable_module_is_reported(self, render):
        """A module that cannot be imported yields a descriptive error, not a crash."""
        out = render("Doc\n===\n\n.. jsonschema:: no_such_module_xyz.SCHEMA\n")
        assert "error while importing python module 'no_such_module_xyz'" in out.warnings

    def test_reference_without_module_part_is_reported(self, render):
        """A bare name (no dotted module path) is neither a file nor a valid Python reference."""
        out = render("Doc\n===\n\n.. jsonschema:: justaname\n")
        assert "requires a Python reference to a schema object" in out.warnings
