"""The ``$schema`` keyword and the ``show_schema`` option.

``$schema`` names the dialect (draft) a schema is written for. It does not change how the schema is
rendered, but it can be displayed so that readers know which draft the documentation refers to.
"""
import json

DRAFT_2020_12 = 'https://json-schema.org/draft/2020-12/schema'
DRAFT_4 = 'http://json-schema.org/draft-04/schema#'


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def test_schema_is_hidden_by_default(render):
    """Without the option the keyword does not appear in the output."""
    out = render(doc({'$schema': DRAFT_2020_12, 'type': 'string'}))
    assert out.warnings == ''
    assert out.rows == [['type', 'string']]


def test_schema_is_shown_with_show_schema(render):
    """With ``:show_schema:`` the first row names the schema dialect."""
    out = render(doc({'$schema': DRAFT_2020_12, 'type': 'string'}, show_schema=''))
    assert out.warnings == ''
    assert out.rows == [['$schema', DRAFT_2020_12], ['type', 'string']]


def test_schema_with_trailing_hash_is_shown_unchanged(render):
    """The Draft 4 spelling, with a trailing ``#``, is shown as written."""
    out = render(doc({'$schema': DRAFT_4, 'type': 'string'}, show_schema=''))
    assert out.rows[0] == ['$schema', DRAFT_4]


def test_schema_row_precedes_the_id_row(render):
    """``$schema`` comes first, followed by the id of the schema."""
    out = render(doc({'$schema': DRAFT_2020_12, '$id': 'http://example.com/s', 'type': 'string'}, show_schema=''))
    assert out.rows[:2] == [['$schema', DRAFT_2020_12], ['http://example.com/s']]


def test_schema_is_shown_with_a_lifted_title(render):
    """The title becomes a section heading; the table still starts with the ``$schema`` row."""
    out = render(doc({'$schema': DRAFT_2020_12, 'title': 'Named', 'type': 'string'}, show_schema=''))
    assert 'Named' in out.section_titles
    assert out.rows[0] == ['$schema', DRAFT_2020_12]


def test_schema_of_a_nested_schema_is_not_shown(render):
    """Only the root of the schema document names its dialect; the keyword is ignored elsewhere."""
    schema = {'type': 'object', 'properties': {'a': {'$schema': DRAFT_2020_12, 'type': 'string'}}}
    out = render(doc(schema, show_schema=''))
    assert '$schema' not in out.flat


def test_show_schema_without_schema_keyword(render):
    """The option has no effect on a schema that does not name its dialect."""
    out = render(doc({'type': 'string'}, show_schema=''))
    assert out.warnings == ''
    assert out.rows == [['type', 'string']]


def test_show_schema_can_be_set_in_conf(render):
    """``jsonschema_options`` sets the default for all directives; the directive option overrides it."""
    conf = "jsonschema_options = {'show_schema': True}\n"
    source = doc({'$schema': DRAFT_2020_12, 'type': 'string'})
    assert render(source, conf=conf).rows[0] == ['$schema', DRAFT_2020_12]
    off = doc({'$schema': DRAFT_2020_12, 'type': 'string'}, show_schema='false')
    assert '$schema' not in render(off, conf=conf).flat
