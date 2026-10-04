#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest

from unittest.mock import Mock, MagicMock

from docutils.parsers.rst.states import RSTStateMachine, Body
from docutils import nodes

wide_format = __import__('sphinx-jsonschema.wide_format')


@pytest.fixture
def mock_app():
    """Create a mock Sphinx app with required config."""
    app = Mock()
    app.config = Mock()
    app.config.jsonschema_options = {}
    app.env = Mock()
    app.env.domaindata = {'std': {'labels': {}, 'anonlabels': {}}}
    app.env.docname = 'test_doc'
    return app


@pytest.fixture
def mock_state():
    """Create a mock RST state with required methods."""
    state = Body(RSTStateMachine([], None))

    # Mock document
    state.document = Mock()
    state.document.current_source = '/path/to/source.rst'
    state.document.settings = Mock()
    state.document.settings.record_dependencies = set()
    state.document.note_implicit_target = Mock()

    # Mock build_table to return a mock table node
    state.build_table = Mock(return_value=nodes.table())

    # Mock nested_parse for description parsing
    state.nested_parse = Mock()

    # Mock inline_text for title parsing
    state.inline_text = Mock(return_value=([], []))

    return state


@pytest.fixture
def wideformat(mock_app, mock_state):
    """Create a WideFormat instance with properly mocked dependencies."""
    lineno = 1
    source = ''
    options = {}

    return wide_format.WideFormat(mock_state, lineno, source, options, mock_app)


def test_create(wideformat):
    """Test that WideFormat instance can be created."""
    assert isinstance(wideformat, wide_format.WideFormat)


def test_wideformat_options_initialization(mock_app, mock_state):
    """Test that WideFormat initializes options correctly."""
    mock_app.config.jsonschema_options = {'lift_title': False}
    options = {'lift_description': True}

    wf = wide_format.WideFormat(mock_state, 1, '', options, mock_app)

    assert wf.options['lift_title'] is False
    assert wf.options['lift_description'] is True


def test_string(wideformat):
    """Test transform with a simple string schema."""
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "An example",
        "id": "http://example.com/schemas/example.json",
        "description": "This is just a tiny example of a schema rendered by `sphinx-jsonschema <http://github.com/lnoor/sphinx-jsonschema>`_.\n\nYes that's right you can use *reStructuredText* in a description.",
        "type": "string",
        "minLength": 10,
        "maxLength": 100,
        "pattern": "^[A-Z]+$"
    }
    table, definitions = wideformat.transform(schema)

    # build_table should have been called with (cols, head, body), lineno
    wideformat.state.build_table.assert_called()

    # Should return a table
    assert table is not None or definitions is not None
