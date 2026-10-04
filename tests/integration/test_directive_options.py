"""Directive options (``:lift_title:``, ``:hide_key:`` and friends) and their effect on the output."""
import json


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    body = json.dumps(schema).replace('\n', '\n    ')
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {body}\n"


TITLED = {'title': 'My Schema', 'description': 'About it', 'type': 'string'}


def test_title_is_lifted_into_section_by_default(render):
    """Default: the schema title becomes a section heading (and TOC entry), not a table row."""
    out = render(doc(TITLED))
    assert 'My Schema' in out.section_titles
    assert ['type', 'string'] in out.rows
    assert 'My Schema' not in out.flat


def test_title_stays_in_table_when_not_lifted(render):
    """With ``:lift_title: false`` the title is just another row in the table."""
    out = render(doc(TITLED, lift_title='false'))
    assert 'My Schema' not in out.section_titles
    assert 'My Schema' in out.flat


def test_lift_description_moves_description_out_of_table(render):
    """``:lift_description:`` places the description between title and table, not inside it."""
    lifted = render(doc(TITLED, lift_description='true'))
    assert 'About it' not in lifted.flat
    assert 'About it' in ''.join(lifted.root.itertext())


def test_hide_key_removes_property(render):
    """``:hide_key:`` takes a JSON pointer and removes that part of the schema from the output."""
    schema = {'type': 'object', 'properties': {'keep': {'type': 'string'}, 'secret': {'type': 'string'}}}
    out = render(doc(schema, hide_key='/properties/secret'))
    assert 'keep' in out.flat
    assert 'secret' not in out.flat


def test_hide_key_if_empty_only_removes_empty_values(render):
    """``:hide_key_if_empty:`` hides the key only while its value is empty."""
    schema = {'type': 'object', 'properties': {'a': {'type': 'string'}}, 'required': []}
    out = render(doc(schema, hide_key_if_empty='/required'))
    assert 'required' not in out.flat

    # Same option, non-empty value: the build must still succeed without complaints.
    schema['required'] = ['a']
    out = render(doc(schema, hide_key_if_empty='/required'))
    assert out.warnings == ''


def test_descriptions_are_rendered_as_rst(render):
    """Descriptions are deliberately not escaped: reStructuredText in them is interpreted."""
    out = render(doc({'type': 'string', 'description': 'has *emphasis*'}))
    assert 'emphasis' in [e.text for e in out.root.iter('emphasis')]


def test_pass_unmodified_keeps_markup_in_default_value(render):
    """Values such as ``default`` are escaped, so markup stays literal ...

    ... unless ``:pass_unmodified:`` names their path, which suppresses the escaping.
    (The type "string" is itself rendered as emphasis, hence the check for "b" specifically.)
    """
    schema = {'type': 'string', 'default': 'a *b*'}
    emphasised = lambda out: [e.text for e in out.root.iter('emphasis')]

    assert 'b' not in emphasised(render(doc(schema)))
    assert 'b' in emphasised(render(doc(schema, pass_unmodified='/default')))


def test_lift_definitions_renders_each_definition_as_section(render):
    """``:lift_definitions:`` renders every entry of ``definitions`` as its own titled section."""
    schema = {
        'title': 'Root',
        'type': 'object',
        'properties': {'user': {'$ref': '#/definitions/User'}},
        'definitions': {'User': {'type': 'object', 'properties': {'name': {'type': 'string'}}}},
    }
    out = render(doc(schema, lift_definitions='true'))
    assert out.section_titles[:1] == ['Doc']
    assert 'Root' in out.section_titles
    assert 'User' in out.section_titles


def test_auto_target_makes_schema_referenceable(render):
    """``:auto_target:`` registers a label named after the file, so ``:ref:`` can point at it.

    For an inline schema the "file" is the document itself (index.rst). An unresolved
    reference would show up in the warnings.
    """
    schema = {'title': 'Target Me', 'type': 'string'}
    source = doc(schema, auto_target='true') + "\nSee :ref:`index.rst`.\n"
    out = render(source)
    assert out.warnings == ''
    assert list(out.root.iter('target'))
