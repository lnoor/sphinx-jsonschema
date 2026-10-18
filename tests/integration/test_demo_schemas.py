"""Regression baseline for the demo schemas.

Each schema in ``BASELINE`` is rendered through the ``jsonschema`` directive and compared with a
stored snapshot (``snapshots/<name>.json``). The snapshots pin the current output so that extending
the keyword support cannot silently change how existing schemas are rendered.

To accept an intended change, run the tests with ``UPDATE_SNAPSHOTS=1`` and review the diff.
"""
import json
import os
from pathlib import Path

import pytest

SCHEMAS = Path(__file__).parents[2] / 'demo' / 'schemas'
SNAPSHOTS = Path(__file__).parent / 'snapshots'

# Demo schemas that existed before the newer drafts were addressed.
BASELINE = [
    'arrays', 'combinators', 'conditional', 'constraints', 'enum-const-examples', 'extensions',
    'minimal', 'objects', 'other', 'references', 'types',
]
# Feature demos for keywords that are already rendered today.
BASELINE += [
    'feature-boolean-schemas', 'feature-const', 'feature-defs', 'feature-dependencies',
    'feature-exclusive-minmax-bool', 'feature-exclusive-minmax-number', 'feature-ref-siblings',
    'feature-tuple-items', 'feature-type-list-mixed',
]
# Feature demos for keywords the plugin gained support for later; each support PR adds its demos here.
BASELINE += [
    'feature-comment', 'feature-contains', 'feature-contains-min-max', 'feature-content',
    'feature-content-schema', 'feature-dependent-required', 'feature-dependent-schemas',
    'feature-deprecated', 'feature-prefix-items', 'feature-property-names', 'feature-read-write-only',
    'feature-schema-keyword', 'feature-unevaluated-items', 'feature-unevaluated-properties',
]


def render_schema(render, name):
    source = (SCHEMAS / f'{name}.json').read_text(encoding='utf-8')
    return render('Doc\n===\n\n.. jsonschema:: schema.json\n', files={'schema.json': source})


@pytest.mark.parametrize('name', BASELINE)
def test_baseline_snapshot(render, name):
    """Rendering of the demo schema is unchanged compared to its snapshot."""
    out = render_schema(render, name)
    actual = {'rows': out.rows, 'warnings': out.warnings}
    snapshot = SNAPSHOTS / f'{name}.json'
    if os.environ.get('UPDATE_SNAPSHOTS'):
        SNAPSHOTS.mkdir(exist_ok=True)
        snapshot.write_text(json.dumps(actual, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    assert actual == json.loads(snapshot.read_text(encoding='utf-8'))
