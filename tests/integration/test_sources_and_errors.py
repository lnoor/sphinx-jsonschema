"""Where a schema can come from (inline, file, JSON pointer, URL) and how failures are reported.

Errors in a directive do not abort the Sphinx build; they appear as warnings/errors
in Sphinx's output and the directive renders nothing. The error tests therefore
check ``out.warnings`` for the message and ``out.rows`` for an empty result.
"""
import json
from unittest.mock import Mock, patch

import pytest

SCHEMA = {'type': 'object', 'properties': {'name': {'type': 'string'}}}


def page(argument='', content=''):
    """Page with one jsonschema directive using an optional argument and/or inline content."""
    body = ''.join(f'    {line}\n' for line in content.splitlines())
    return f"Doc\n===\n\n.. jsonschema:: {argument}\n\n{body}"


def test_inline_yaml_content(render):
    """Inline content may be YAML as well as JSON."""
    out = render(page(content='type: string\nminLength: 2'))
    assert out.rows == [['type', 'string'], ['minLength', '2']]


def test_schema_from_json_file_relative_to_document(render):
    """A file argument is resolved relative to the document that contains the directive."""
    out = render(page('schemas/user.json'), files={'schemas/user.json': json.dumps(SCHEMA)})
    assert 'name' in out.flat
    assert out.warnings == ''


def test_schema_from_yaml_file(render):
    """Schema files may be YAML."""
    out = render(page('user.yaml'), files={'user.yaml': 'type: integer\nminimum: 1\n'})
    assert out.rows == [['type', 'integer'], ['minimum', '1']]


def test_json_pointer_selects_subschema(render):
    """``file#/pointer`` renders only the part of the file the pointer selects."""
    schema = {'definitions': {'Age': {'type': 'integer', 'minimum': 0}}}
    out = render(page('defs.json#/definitions/Age'), files={'defs.json': json.dumps(schema)})
    assert out.rows == [['type', 'integer'], ['minimum', '0']]


def test_schema_from_url(render):
    """An http(s) argument is downloaded with ``requests`` (mocked here; default timeout 30 s)."""
    response = Mock(status_code=200, content=json.dumps({'type': 'boolean'}).encode())
    with patch('requests.get', return_value=response) as get:
        out = render(page('http://example.invalid/schema.json'))
    assert out.rows == [['type', 'boolean']]
    assert get.call_args.kwargs['timeout'] == 30


def test_url_http_error_is_reported(render):
    """A non-200 response is reported with the server's reason phrase."""
    with patch('requests.get', return_value=Mock(status_code=404, reason='Not Found')):
        out = render(page('http://example.invalid/missing.json'))
    assert 'Not Found' in out.warnings
    assert not out.rows


def test_invalid_json_is_reported_with_source_text(render):
    """Unparsable content gives a parse error (the offending text is attached to the message)."""
    out = render(page(content='{"type": '))
    assert 'encountered a the following error while parsing' in out.warnings
    assert not out.rows


def test_unknown_pointer_is_reported(render):
    """A pointer that does not exist in the schema leads to an error and no output."""
    out = render(page('defs.json#/nope'), files={'defs.json': json.dumps(SCHEMA)})
    assert 'nope' in out.warnings
    assert not out.rows


@pytest.mark.xfail(
    strict=True,
    reason="jsonpointer raises JsonPointerException, but only KeyError is caught (symptom seen in lnoor/sphinx-jsonschema#36)",
)
def test_unknown_pointer_gives_friendly_message(render):
    """Known defect, kept as strict xfail: the intended message is unreachable.

    The code handles ``KeyError`` ("... encountered a KeyError when trying to resolve
    the pointer"), but ``jsonpointer`` raises ``JsonPointerException``. When that is
    fixed this test starts to pass, strict mode fails the run, and the xfail marker
    should then be removed.

    The traceback in lnoor/sphinx-jsonschema#36 ends in exactly this exception
    ("member 'definitions' not found in {}"), although that issue was closed for a
    different root cause (quotes in a title combined with ``$$target``).
    """
    out = render(page('defs.json#/nope'), files={'defs.json': json.dumps(SCHEMA)})
    assert 'KeyError when trying to resolve the pointer' in out.warnings


def test_file_and_content_together_are_rejected(render):
    """An external file and inline content are mutually exclusive."""
    out = render(page('user.json', content='type: string'), files={'user.json': '{}'})
    assert 'may not both specify an external file and have content' in out.warnings


def test_missing_content_and_argument_is_rejected(render):
    """A directive with neither argument nor content reports an error and renders nothing."""
    out = render("Doc\n===\n\n.. jsonschema::\n")
    assert out.warnings
    assert not out.rows


@pytest.mark.xfail(
    strict=True,
    reason="_convert_filename(None) raises TypeError before the intended error (no matching upstream issue; cf. #76)",
)
def test_missing_content_and_argument_gives_friendly_message(render):
    """Known defect, kept as strict xfail: the intended message is unreachable.

    ``get_json_data`` calls ``_convert_filename(None)``, which fails with a
    ``TypeError`` before the "has no content or a reference to an external file"
    error can be raised.

    No upstream issue describes this. The closest is lnoor/sphinx-jsonschema#76, a
    different ``TypeError`` caused by the 1.19 change in how ``filename`` is handled
    (the very code path involved here).
    """
    out = render("Doc\n===\n\n.. jsonschema::\n")
    assert 'has no content or a reference to an external file' in out.warnings


def test_invalid_hide_key_path_is_reported(render):
    """``/*/*`` is not allowed (consecutive wildcards); the user gets a clear message."""
    out = render(f"Doc\n===\n\n.. jsonschema::\n    :hide_key: /*/*\n\n    {json.dumps(SCHEMA)}\n")
    assert 'Supplied JSON path is invalid' in out.warnings
