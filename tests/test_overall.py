#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest

from unittest.mock import Mock

from docutils.parsers.rst.states import RSTStateMachine, Body

wide_format = __import__('sphinx-jsonschema.wide_format')

@pytest.fixture
def wideformat():
    state = Body(RSTStateMachine(None, None))
    #state = Mock()
    lineno = 1
    app = None

    return wide_format.WideFormat(state, lineno, app)

def test_create(wideformat):
    wf = wideformat
    assert isinstance(wf, wide_format.WideFormat)

def test_string(wideformat):
    schema = {
        '$id': 'somewhere',
        'title': 'Just a String',
        'description': 'just another boring string',
        'type': 'string'
    }
    result = wideformat.transform(schema)
    #wideformat.state.build_table.assert_called()
