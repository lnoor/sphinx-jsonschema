"""WideFormat building blocks: cells, spans, escaping and reference helpers.

WideFormat turns a schema into rows of "cells", which docutils' table builder then
turns into a table. A cell is a list ``[rowspan, colspan, lineno, StringList]``
(a tuple once spans are final). How whole schemas render is tested in the
integration tests; here the individual building blocks are checked.
"""
import pytest

wide_format = __import__('sphinx-jsonschema.wide_format')
NOESC = wide_format.NOESC


def text(cell):
    """The text of a cell (its content lines joined), for readable assertions."""
    return '\n'.join(cell[3].data)


def test_options_are_merged_defaults_then_config_then_directive(make_wideformat, app):
    """Precedence of settings: built-in defaults < conf.py ``jsonschema_options`` < directive options."""
    app.config.jsonschema_options = {'lift_title': False, 'lift_description': True}
    wf = make_wideformat({'lift_description': False, 'auto_target': True})
    assert wf.options['lift_title'] is False          # from conf.py, overrides the default (True)
    assert wf.options['lift_description'] is False    # directive option beats conf.py
    assert wf.options['auto_target'] is True          # from the directive
    assert wf.options['lift_definitions'] is False    # untouched default


def test_transform_hands_rows_to_build_table(wideformat):
    """transform() builds the rows and passes (column widths, header, body) to the table builder."""
    table, definitions = wideformat.transform({'type': 'string', 'minLength': 3})
    (cols, head, body), lineno = wideformat.state.build_table.call_args.args
    assert cols == [1, 1]          # two equally wide columns: label and value
    assert head == []              # these tables have no header row
    assert [[text(c) for c in row] for row in body] == [['type', '*string*'], ['minLength', '3']]
    assert table is wideformat.state.build_table.return_value
    assert definitions == []


def test_transform_of_empty_schema_builds_no_table(wideformat):
    """Nothing to show means no table (and no empty table node in the output)."""
    table, definitions = wideformat.transform({})
    assert table is None
    wideformat.state.build_table.assert_not_called()


@pytest.mark.parametrize('raw, escaped', [
    ('plain', 'plain'),
    ('a_b', r'a\_b'),                 # underscore could start a reference/emphasis
    ('*x*', r'\*x\*'),                # asterisks could start emphasis
    ('c:\\dir', 'c:\\\\dir'),         # a backslash is itself the escape character
    (NOESC + '_a_*b*', '_a_*b*'),     # the NOESC marker disables escaping and is removed
])
def test_escape(wideformat, raw, escaped):
    assert wideformat._escape(raw) == escaped


@pytest.mark.parametrize('typ, expected', [
    ('string', '*string*'),
    (['string', 'null'], '*string* / *null*'),   # types are emphasised, alternatives joined by " / "
])
def test_decodetype(wideformat, typ, expected):
    assert text(wideformat._decodetype(typ)) == expected


def test_cell_has_table_builder_layout(wideformat):
    """A fresh cell has no spans yet, the source line number, and one entry per text line."""
    cell = wideformat._cell('line1\nline2')
    assert cell[:3] == [0, 0, 1]
    assert cell[3].data == ['line1', 'line2']


@pytest.mark.parametrize('path, with_pointer, expected', [
    ('', False, ''),
    ('user.json', False, 'user.json'),
    ('dir/user.json', False, 'user.json'),                  # directories are dropped
    ('http://host/dir/user.json', False, 'user.json'),      # ... also for URLs
    ('dir/user.json#/definitions/User', False, 'user.json'),  # the pointer is cut off ...
    ('dir/user.json#/definitions/User', True, 'user.json#/definitions/User'),  # ... or kept on request
])
def test_get_filename(wideformat, path, with_pointer, expected):
    """File name used for auto_target labels and ``$ref`` links."""
    assert wideformat._get_filename(path, with_pointer) == expected


@pytest.mark.parametrize('ref, key, expected', [
    # result: (nesting depth of the definition, name of the definition)
    ('#/definitions/User', 'definitions', (1, 'User')),
    ('#/definitions/A/definitions/B', 'definitions', (2, 'B')),
    ('#/$defs/User', '$defs', (1, 'User')),
    ('#/$defs/User', 'definitions', None),                       # other keyword than asked for
    ('other.json#/definitions/User', 'definitions', None),       # not a reference into this schema
])
def test_get_defined_reference(wideformat, ref, key, expected):
    assert wideformat._get_defined_reference({'$ref': ref}, key) == expected


def test_prepend_spans_label_over_all_rows(wideformat):
    """A label put in front of N rows sits in the first row and spans all N (rowspan N-1 extra)."""
    rows = [[wideformat._cell('a')], [wideformat._cell('b')], [wideformat._cell('c')]]
    label = wideformat._cell('L')
    result = wideformat._prepend(label, rows)
    assert label[0] == 2                                  # rowspan: two more rows below the first
    assert result[0][0] is label
    assert result[1][0] is None and result[2][0] is None  # covered by the span, hence empty


def test_prepend_to_no_rows_yields_label_only(wideformat):
    label = wideformat._cell('L')
    assert wideformat._prepend(label, []) == [[label]]


def test_square_pads_short_rows_with_none(wideformat):
    """All rows are padded to the widest row; None marks a column the previous cell spans."""
    rows = [[1], [1, 2, 3], [1, 2]]
    assert wideformat._square(rows) == 3
    assert rows == [[1, None, None], [1, 2, 3], [1, 2, None]]


def test_calc_spans_extends_cell_over_following_empty_columns(wideformat):
    """Each None after a cell widens that cell's colspan; finished cells become tuples."""
    rows = [[wideformat._cell('wide'), None, None], [wideformat._cell('a'), wideformat._cell('b'), None]]
    wideformat._calc_spans(rows, 3)
    assert rows[0][0][:3] == (0, 2, 1) and rows[0][1:] == [None, None]
    assert rows[1][0][1] == 0 and rows[1][1][1] == 1
    # the table builder requires tuples, not the mutable lists used while calculating
    assert all(isinstance(c, tuple) for row in rows for c in row if c is not None)


@pytest.mark.parametrize('key', ['id', '$id'])
def test_cover_puts_schema_id_first_and_removes_it(wideformat, key):
    """The outermost schema id (draft 4 "id" or later "$id") becomes the first row, then is dropped."""
    schema = {key: 'http://example.com/s.json'}
    body = [[wideformat._cell('type'), wideformat._cell('x')]]
    cols, head, body = wideformat._cover(schema, body)
    assert cols == [1, 1] and head == []
    assert key not in schema
    assert text(body[0][0]) == 'http://example.com/s.json'
    assert body[0][0][1] == 1 and body[0][1] is None   # the id cell spans both columns


@pytest.mark.parametrize('value, expected', [
    ([], ['']),                # empty containers still produce an (empty) row
    ({}, ['']),
    (None, ['null']),          # JSON null is shown as the word "null"
    (5, ['5']),
    ('a_b', [r'a\_b']),        # strings are escaped
    ([1, 'x'], ['1', 'x']),    # list items become one row each
])
def test_render_any_value_flat_values(wideformat, value, expected):
    rows = wideformat._render_any_value(value)
    assert [text(row[0]) for row in rows] == expected


def test_render_any_value_labels_dict_entries(wideformat):
    """Dict keys become labels; the label is only in the first row of its (multi-row) value."""
    rows = wideformat._render_any_value({'k': ['v1', 'v2']})
    assert [[text(c) if c else None for c in row] for row in rows] == [['k', 'v1'], [None, 'v2']]
