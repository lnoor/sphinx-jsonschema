#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest

from unittest.mock import Mock

from docutils.parsers.rst.states import RSTStateMachine, Body

wide_format = __import__('sphinx-jsonschema.wide_format')

@pytest.fixture
def wideformat():
    state = Body(RSTStateMachine([], None))
    state.build_table = Mock()
    lineno = 1
    source = ''
    options = {}
    app = None

    return wide_format.WideFormat(state, lineno, source, options, app)

def test_create(wideformat):
    wf = wideformat
    assert isinstance(wf, wide_format.WideFormat)

def test_string(wideformat):
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
    result = wideformat.transform(schema)
    wideformat.state.build_table.assert_called()
