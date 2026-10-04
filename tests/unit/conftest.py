"""Shared fixtures for the unit tests.

Unit tests look at one function at a time. Collaborators that would require a
running Sphinx (the application, the docutils parser state) are replaced by
mocks that provide just what the code under test touches. Behaviour that depends
on the real Sphinx is covered by the integration tests instead.
"""
import pytest
from unittest.mock import Mock

from docutils import nodes
from docutils.parsers.rst.states import RSTStateMachine, Body

# The package directory contains a hyphen, so it cannot be imported with a normal import statement.
ext = __import__('sphinx-jsonschema')
wide_format = __import__('sphinx-jsonschema.wide_format')


@pytest.fixture
def app():
    """Stand-in for the Sphinx application: config options, label registries and doc name."""
    app = Mock()
    app.config.jsonschema_options = {}  # the ``jsonschema_options`` setting from conf.py
    app.env.domaindata = {'std': {'labels': {}, 'anonlabels': {}}}  # filled by $$target/auto_target
    app.env.docname = 'doc'
    return app


@pytest.fixture
def state():
    """A real docutils ``Body`` state with the document and table builder replaced by mocks."""
    state = Body(RSTStateMachine([], None))
    state.document = Mock()
    state.document.current_source = '/docs/index.rst'
    # WideFormat only collects rows; docutils' real table builder is replaced so tests
    # can inspect what would have been handed to it.
    state.build_table = Mock(return_value=nodes.table())
    return state


@pytest.fixture
def make_wideformat(state, app):
    """Factory for ``WideFormat`` objects, for tests that need non-default options."""
    def make(options=None, source=''):
        return wide_format.WideFormat(state, 1, source, options or {}, app)
    return make


@pytest.fixture
def wideformat(make_wideformat):
    """A ``WideFormat`` with default options."""
    return make_wideformat()


@pytest.fixture
def directive(state):
    """A ``JsonSchema`` directive instance for testing its helper methods (not ``run``)."""
    return ext.JsonSchema('jsonschema', [], {}, [], 1, 0, '', state, Mock())
