"""The release version is written down in three places that have to be raised together.

The files are read as text instead of being imported, because ``setup.py`` would run the packaging code
and ``docs/conf.py`` expects to be loaded by Sphinx.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def find_version(relative_path, pattern):
    """Return the single value captured by ``pattern`` in the given file of the repository."""
    text = (ROOT / relative_path).read_text(encoding='utf-8')
    matches = re.findall(pattern, text, re.MULTILINE)
    assert len(matches) == 1, f'expected exactly one match of {pattern!r} in {relative_path}, found {len(matches)}'
    return matches[0]


def test_versions_match():
    """setup.py, the value reported by the extension and the documentation agree on the full version."""
    setup_py = find_version('setup.py', r"^\s*version='([^']+)'")
    extension = find_version('sphinx-jsonschema/__init__.py', r"'version':\s*'([^']+)'")
    release = find_version('docs/conf.py', r"^release\s*=\s*u?'([^']+)'")
    assert setup_py == extension == release


def test_documentation_short_version_is_major_minor():
    """The short ``version`` of the documentation is the full version without the patch level."""
    release = find_version('docs/conf.py', r"^release\s*=\s*u?'([^']+)'")
    short = find_version('docs/conf.py', r"^version\s*=\s*u?'([^']+)'")
    assert short == '.'.join(release.split('.')[:2])
