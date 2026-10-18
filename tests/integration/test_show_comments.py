"""The ``$comment`` keyword (Draft 7) and the ``show_comments`` option.

``$comment`` is meant for the maintainers of a schema; the specification asks implementations not to
show it to end users. It is therefore hidden unless ``show_comments`` is set.
"""
import json

SCHEMA = {
    '$comment': 'root note',
    'type': 'object',
    'description': 'About it',
    'properties': {'id': {'$comment': 'property note', 'type': 'integer'}},
}


def doc(schema, **options):
    """Page with one jsonschema directive; keyword arguments become ``:option: value`` lines."""
    opts = ''.join(f'    :{k}: {v}\n' for k, v in options.items())
    return f"Doc\n===\n\n.. jsonschema::\n{opts}\n    {json.dumps(schema)}\n"


def test_comment_is_hidden_by_default(render):
    """Without the option no comment appears anywhere in the output."""
    out = render(doc(SCHEMA))
    assert out.warnings == ''
    assert '$comment' not in out.flat
    assert 'root note' not in out.flat
    assert 'property note' not in out.flat


def test_comment_is_shown_with_show_comments(render):
    """With ``:show_comments:`` every ``$comment`` becomes a row, on the root and on nested schemas."""
    out = render(doc(SCHEMA, show_comments=''))
    assert out.warnings == ''
    assert ['$comment', 'root note'] in out.rows
    assert ['id', '$comment', 'property note'] in out.rows


def test_comment_row_follows_the_description(render):
    """The comment is shown right below the description."""
    out = render(doc(SCHEMA, show_comments=''))
    assert out.rows[:3] == [['About it'], ['$comment', 'root note'], ['type', 'object']]


def test_comment_without_other_keywords(render):
    """A schema that consists of a comment only still renders it."""
    out = render(doc({'properties': {'a': {'$comment': 'only a note'}}}, show_comments=''))
    assert ['a', '$comment', 'only a note'] in out.rows


def test_comment_is_not_interpreted_as_markup(render):
    """Comments are plain text: emphasis and underscores are shown literally."""
    out = render(doc({'$comment': 'use *this* or snake_case'}, show_comments=''))
    assert ['$comment', 'use *this* or snake_case'] in out.rows


def test_show_comments_can_be_set_in_conf(render):
    """``jsonschema_options`` sets the default for all directives; the directive option overrides it."""
    conf = "jsonschema_options = {'show_comments': True}\n"
    assert ['$comment', 'root note'] in render(doc(SCHEMA), conf=conf).rows
    assert '$comment' not in render(doc(SCHEMA, show_comments='false'), conf=conf).flat
