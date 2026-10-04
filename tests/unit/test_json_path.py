"""Pure helper functions: JSON path handling (``:hide_key:`` & co.) and option validators.

None of these functions touches Sphinx or docutils state, so no mocks are needed.
"""
import copy

import pytest

ext = __import__('sphinx-jsonschema')


def test_pairwise():
    """pairwise yields neighbouring elements; a single element has no pairs."""
    assert list(ext.pairwise([1, 2, 3])) == [(1, 2), (2, 3)]
    assert list(ext.pairwise([1])) == []


@pytest.mark.parametrize('value, expected', [
    ('42', 42), ('0', 0), ('-10', -10), (7, 7),
    # anything that is not an integer is passed through untouched
    ('hello', 'hello'), ('3.14', '3.14'),
])
def test_maybe_int(value, expected):
    """Path segments that look like integers become ints, so they can index lists."""
    assert ext.maybe_int(value) == expected


@pytest.mark.parametrize('path, valid', [
    (['properties', 'name'], True),
    (['items', 0, 'type'], True),
    (['**', 'properties'], True),
    (['a', '*', 'b', '**', 'c'], True),   # wildcards are fine if something separates them
    # two wildcards in a row are ambiguous and therefore rejected, in any combination
    (['*', '*'], False),
    (['**', '**'], False),
    (['*', '**'], False),
    (['**', '*'], False),
    (['a', '*', '*'], False),
])
def test_json_path_validate(path, valid):
    assert ext.json_path_validate(path) is valid


# Document used for the path tests. "val" occurs at six places, at different depths:
# top level, a, a/x, b, items[0], items[1].
DOC = {
    'val': 0,
    'a': {'val': 1, 'x': {'val': 2}},
    'b': {'val': 3},
    'items': [{'val': 4}, {'val': 5}],
}


def hits(path, doc=DOC):
    """Run json_path_transform on a copy of `doc` and return the keys it invoked the transformer on."""
    seen = []
    ext.json_path_transform(copy.deepcopy(doc), path, lambda obj, key: seen.append(key))
    return seen


@pytest.mark.parametrize('path, expected', [
    # explicit paths, including a list index (digits are converted to int)
    ('/val', ['val']),
    ('/a/val', ['val']),
    ('/a/x/val', ['val']),
    ('/items/1/val', ['val']),
    # "**" matches at any depth: all six "val" keys; below "a" only the two inside a
    ('/**/val', ['val'] * 6),
    ('/a/**/val', ['val'] * 2),
    # a trailing "*" matches every element of a list
    ('/items/*', [0, 1]),
    # paths that do not exist are silently ignored rather than raising
    ('/missing', []),
    ('/missing/deeper/val', []),
    ('/items/9/val', []),
    ('/', []),
])
def test_json_path_transform_visits_matching_keys(path, expected):
    assert hits(path) == expected


@pytest.mark.xfail(
    strict=True,
    reason="'*' followed by more path segments does not descend one level (intended semantics: lnoor/sphinx-jsonschema#54)",
)
@pytest.mark.parametrize('path, expected', [
    ('/*/val', ['val', 'val']),
    ('/items/*/val', ['val', 'val']),
])
def test_single_level_wildcard_descends_into_children(path, expected):
    """Known defect, kept as strict xfail.

    The documentation says "*" matches a single level. In practice ``/*/val``
    matches only the "val" at the top level and ``/items/*/val`` matches nothing,
    instead of the "val" in each child. "**" and a trailing "*" work.

    The intended semantics are stated by the author of the wildcard syntax in
    lnoor/sphinx-jsonschema#54 ("``*`` passes through one level of keys and ``**``
    through multiple levels"). No issue describes this defect yet.
    """
    assert hits(path) == expected


@pytest.mark.parametrize('path', ['', '/*/*', '/**/**', '/a/*/**'])
def test_json_path_transform_rejects_invalid_paths(path):
    """An empty path or consecutive wildcards raise a ValueError with a clear message."""
    with pytest.raises(ValueError, match='Supplied JSON path is invalid'):
        hits(path)


def test_json_path_transform_mutates_in_place():
    """The transformer receives the parent object and the key and may modify the document."""
    doc = {'a': {'b': 'x'}}
    ext.json_path_transform(doc, '/a/b', lambda obj, key: obj.__setitem__(key, obj[key].upper()))
    assert doc == {'a': {'b': 'X'}}


def test_remove():
    doc = {'a': 1, 'b': 2}
    ext.remove(doc, 'a')
    assert doc == {'b': 2}


@pytest.mark.parametrize('func', [ext.remove, ext.remove_empty])
@pytest.mark.parametrize('key', ['*', '**'])
def test_removers_reject_wildcards(func, key):
    """Wildcards must have been expanded before a transformer sees the key; a raw one is a bug."""
    with pytest.raises(ValueError):
        func({'a': 1}, key)


@pytest.mark.parametrize('value, removed', [
    # "empty" means falsy: this includes 0 and False, not just '' and []
    ('', True), ([], True), ({}, True), (None, True), (0, True), (False, True),
    ('x', False), ([1], False), ({'k': 1}, False), (1, False), (True, False),
])
def test_remove_empty_removes_falsy_values(value, removed):
    doc = {'key': value}
    ext.remove_empty(doc, 'key')
    assert ('key' not in doc) is removed


def test_tag_noescape_prefixes_strings_only():
    """``:pass_unmodified:`` marks a string with the NOESC prefix; other types are an error."""
    doc = {'text': 'a *b*', 'num': 1}
    ext.tag_noescape(doc, 'text')
    assert doc['text'] == ext.NOESC + 'a *b*'
    with pytest.raises(ValueError, match='does not refer to a string'):
        ext.tag_noescape(doc, 'num')


@pytest.mark.parametrize('argument, expected', [
    (None, True),                          # a flag option without a value means "on"
    ('on', True), ('ON', True), (' True ', True),   # case and surrounding spaces do not matter
    ('off', False), ('FALSE', False),
])
def test_flag(argument, expected):
    assert ext.flag(argument) is expected


@pytest.mark.parametrize('argument', ['', 'yes', 'maybe'])
def test_flag_rejects_unknown_values(argument):
    """Only on/true/off/false are accepted; anything else is reported to the user."""
    with pytest.raises(ValueError):
        ext.flag(argument)


@pytest.mark.parametrize('argument, expected', [
    ('/a', ['/a']),
    ('/a,/b', ['/a', '/b']),
    # CSV quoting lets a single path contain a comma (example taken from the documentation)
    ('/**/examples,"/**/with, comma"', ['/**/examples', '/**/with, comma']),
])
def test_jsonpath_list(argument, expected):
    assert ext.jsonpath_list(argument) == expected


def test_jsonpath_list_rejects_empty():
    with pytest.raises(ValueError):
        ext.jsonpath_list('')
