"""JsonSchema directive helpers that do not need a running Sphinx.

Reading schemas from files/URLs/Python objects and the directive's ``run`` method
are covered by the integration tests; here only the small self-contained helpers
are tested.
"""
import os
from unittest.mock import Mock

import pytest

ext = __import__('sphinx-jsonschema')


@pytest.mark.parametrize('argument, expected', [
    ('schema.json', ['schema.json', '']),                       # no pointer
    ('schema.json#/definitions/User', ['schema.json', '/definitions/User']),
    # only the *last* "#" separates the pointer, so a "#" inside the file name survives
    ('dir/a#b.json#/p', ['dir/a#b.json', '/p']),
    ('http://host/s.json#/x', ['http://host/s.json', '/x']),    # URLs work the same way
])
def test_splitpointer(directive, argument, expected):
    """The directive argument ``file#/pointer`` is split into file name and JSON pointer."""
    assert directive._splitpointer(argument) == expected


def test_ordered_load_json_and_yaml_give_the_same_result(directive):
    """JSON is a subset of YAML, so one loader handles both syntaxes."""
    from_json = directive.ordered_load('{"type": "object", "required": ["a"]}')
    from_yaml = directive.ordered_load('type: object\nrequired:\n  - a\n')
    assert from_json == from_yaml == {'type': 'object', 'required': ['a']}


def test_ordered_load_preserves_key_order(directive):
    """Keys keep their order from the file, which determines the row order in the table."""
    assert list(directive.ordered_load('{"z": 1, "a": 2, "m": 3}')) == ['z', 'a', 'm']


def test_ordered_load_falls_back_to_json_when_yaml_scanner_fails(directive):
    """Some valid JSON trips the YAML scanner; the loader then retries with the json module."""
    # a tab inside a flow mapping is a YAML scanner error but valid JSON
    assert directive.ordered_load('{"a":\t1}') == {'a': 1}


def test_ordered_load_rejects_garbage(directive):
    """Text that is neither YAML nor JSON raises, so the caller can report it."""
    with pytest.raises(Exception):
        directive.ordered_load('{unclosed: [')


def test_convert_filename_keeps_absolute_paths(directive):
    absolute = os.path.abspath(os.path.join(os.sep, 'abs', 'schema.json'))
    assert directive._convert_filename(absolute) == absolute


def test_convert_filename_is_relative_to_current_document(directive):
    """Relative file names are resolved against the directory of the .rst file, not the cwd."""
    directive.state.document.current_source = os.path.join('docs', 'index.rst')
    assert directive._convert_filename('s/u.json') == os.path.join('docs', 's/u.json')


def test_setup_registers_directive_and_config():
    """Sphinx entry point: registers the directive and the conf.py setting, declares parallel safety."""
    app = Mock()
    meta = ext.setup(app)
    app.add_directive.assert_called_once_with('jsonschema', ext.JsonSchema)
    app.add_config_value.assert_called_once_with('jsonschema_options', {}, 'env')
    assert meta['parallel_read_safe'] is True
    assert meta['version']
