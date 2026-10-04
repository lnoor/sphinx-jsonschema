"""Harness for the integration tests: render reStructuredText with a real Sphinx build.

The integration tests exercise the extension through its public interface, the
``jsonschema`` directive, exactly as a user's documentation build would. Nothing
inside the extension is mocked. A test supplies reStructuredText (plus optional
side files such as schema files) and asserts on what Sphinx produced.

The Sphinx *xml* builder is used because its output is a structured doctree
that can be parsed and inspected, which is far more robust than comparing HTML.
"""
import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from sphinx.application import Sphinx


class Rendered:
    """Result of one Sphinx build, with a few helpers to inspect the doctree."""

    def __init__(self, root, warnings):
        self.root = root          # parsed doctree (xml.etree element of <document>)
        self.warnings = warnings  # everything Sphinx reported as warning/error, as plain text

    @property
    def rows(self):
        """Text of every table cell, one list per table row.

        Whitespace is normalised, so multi-line cells compare easily. Markup is
        reduced to its text: ``*string*`` (emphasis) becomes ``string``, and a
        ``- name`` bullet becomes ``name``.
        """
        return [
            [re.sub(r'\s+', ' ', ''.join(e.itertext())).strip() for e in row.iter('entry')]
            for row in self.root.iter('row')
        ]

    @property
    def flat(self):
        """All cell texts of all rows in one flat list; use when column layout is irrelevant."""
        return [cell for row in self.rows for cell in row]

    @property
    def section_titles(self):
        """Titles of all sections, e.g. the page title and any lifted schema titles."""
        return [''.join(s.find('title').itertext()) for s in self.root.iter('section')]


@pytest.fixture
def render(tmp_path):
    """Return a function that builds ``source`` as ``index.rst`` and returns a `Rendered`.

    ``files`` maps relative paths to contents and is written next to ``index.rst``
    (for schema files, ``.yaml`` files and so on). ``conf`` is appended to the
    generated ``conf.py``. The function may be called several times in one test;
    every call builds in its own directory.
    """
    builds = []

    def _render(source, files=None, conf=''):
        builds.append(None)
        base = tmp_path / f'build{len(builds)}'
        src = base / 'src'
        src.mkdir(parents=True)
        (src / 'conf.py').write_text(
            "extensions = ['sphinx-jsonschema']\n" + conf, encoding='utf-8')
        (src / 'index.rst').write_text(source, encoding='utf-8')
        for name, content in (files or {}).items():
            target = src / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')

        out, doctrees = base / 'out', base / 'doctrees'
        warnings = io.StringIO()
        app = Sphinx(str(src), str(src), str(out), str(doctrees), 'xml',
                     status=None, warning=warnings, freshenv=True)
        app.build()
        root = ET.parse(Path(out) / 'index.xml').getroot()

        # Sphinx colours its warnings with ANSI codes; strip them so tests can match plain text.
        lines = [re.sub(r'\x1b\[[0-9;]*m', '', line) for line in warnings.getvalue().splitlines()]
        # Building several Sphinx apps in one process makes Sphinx complain about re-registering
        # its own node classes. That is a test-harness artefact, not something the extension did.
        lines = [line for line in lines if 'is already registered' not in line]
        return Rendered(root, '\n'.join(lines))
    return _render
