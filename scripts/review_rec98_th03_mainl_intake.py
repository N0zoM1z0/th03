#!/usr/bin/env python3
"""Index frozen MAINL direct-source CODE diagnostics without accepting source."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from inventory_rec98_th03 import frozen_files, link_roots
from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import REVISION
from review_th03_mainl_coverage import coverage

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'config/rec98_th03_candidate_reviews.csv'
PROOF = '.analysis/sol-mainl-linked-tail-review-20261006.json'
PROOF_SHA = '0a7d3bc422baa9cab175ff55f5b4e73d70382c58ccfb9f785bb823a661f67b4b'
FIELDS = ['artifact', 'path', 'frozen_revision', 'frozen_sha256', 'scope', 'state',
          'unit_ids', 'evidence_ids', 'failed_evidence_ids', 'carrier_bytes', 'covered_bytes', 'gap_bytes',
          'raw_equal', 'ordered_relocations_equal', 'source_accepted', 'exact_accepted',
          'receipt', 'notes']
SCOPE = 'decoded-linked-CODE-only'
OPEN = ('Candidate diagnostics only. Whole-file review, headers, DATA/BSS, dependency '
        'ownership, physical devices, canonical storage and the complete Oracle set remain open.')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def csv_rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


# This source checkpoint is not a cold-integrated library owner. Keep its
# admission exact and separate; every other maintained source uses the cold gate.
RETAINED_HEAP_UNIT = 'th03-mainl-decoded-heap-manager'
RETAINED_HEAP_SOURCE = 'src/mainl/memory/heap.inl'
RETAINED_HEAP_SHA = '3960b8f2ff1821475f86d947b82380957a35ce4c7169a518689e857560774432'
RETAINED_HEAP_REVIEW = 'python3 scripts/review_th03_mainl_heap.py --output .analysis/NEW_HEAP_REVIEW.json'
RETAINED_HEAP_EVIDENCE = {
    'ev-th03-mainl-heap-maintained-source': (
        'upstream', 'pass', RETAINED_HEAP_SOURCE, RETAINED_HEAP_SHA),
    'ev-th03-mainl-heap-native-attempt-failed': (
        'control-plane', 'fail',
        '.analysis/th03-mainl-heap-native/mainl-heap-feasibility-20261020-v01/receipt.json',
        '476c40fc05d320075cc0a627aefcbe38eeb489060323f7f66a151110e71f1329'),
    'ev-th03-mainl-heap-retained-structural': (
        'binary', 'pass', '.analysis/mainl-heap-retained-validation-20261020-v01/structural.json',
        'cb3379b976fd189e5e419c1d0aa6cec8d8e5821f49268b411f28050645680eb3'),
    'ev-th03-mainl-heap-retained-runtime': (
        'runtime', 'pass', '.analysis/mainl-heap-retained-validation-20261020-v01/behavior.json',
        'c9d3ead4db8db4b311e658350c0c33ad28e027de07802508f94048ce0c89c003'),
    'ev-th03-mainl-heap-retained-completion': (
        'control-plane', 'pass', '.analysis/mainl-heap-retained-validation-20261020-v01/completion.json',
        '61e83cf52a067e02cf743856ee029b6835d1fd5787b063b1b005fa807ca83c51'),
}
RETAINED_HEAP_LEGACY = {
    'ev-th03-mainl-heap-complete-analysis', 'ev-th03-mainl-heap-cached-producers',
    'ev-th03-mainl-heap-cached-raw', 'ev-th03-mainl-heap-cpu-contracts',
    'ev-th03-mainl-heap-controls',
}


def retained_heap_source_checkpoint(row, unit, evidence):
    """Admit only pinned source presence; this cannot satisfy a cold/accepted gate."""
    expected_unit = {
        'id': RETAINED_HEAP_UNIT, 'artifact': 'th03-mainl',
        'kind': 'module-candidate', 'segment': 'decoded:0000', 'offset': '0x210a',
        'file_offset': '', 'size': '628', 'compare_size': '628',
        'boundary_state': 'reviewed', 'origin': 'library', 'state': 'source-present',
        'source': RETAINED_HEAP_SOURCE, 'replay_command': RETAINED_HEAP_REVIEW,
    }
    if any(unit.get(key) != value for key, value in expected_unit.items()):
        raise ValueError('retained heap checkpoint identity/source/scope differs')
    if (row.get('artifact'), row.get('path'), row.get('frozen_revision'),
            row.get('frozen_sha256'), row.get('scope'), row.get('receipt'),
            row.get('source_accepted'), row.get('exact_accepted')) != (
            'th03-mainl', 'th03_mainl.asm', REVISION,
            '0144b4c14d948a993d5da4f9591ea39c0f17772cba9cd47a6eda1e8e52a283d6',
            SCOPE, PROOF, 'false', 'false'):
        raise ValueError('retained heap checkpoint diagnostic provenance/acceptance differs')
    refs = unit['evidence_ids'].split(';')
    if (len(refs) != len(set(refs))
            or set(refs) != RETAINED_HEAP_LEGACY | set(RETAINED_HEAP_EVIDENCE)):
        raise ValueError('retained heap checkpoint evidence IDs differ')
    if any(evidence.get(name, {}).get('evidence_class') == 'reproducibility' for name in refs):
        raise ValueError('retained heap checkpoint cannot claim cold reproducibility')
    for name, (kind, result, location, digest) in RETAINED_HEAP_EVIDENCE.items():
        item = evidence.get(name, {})
        expected = {
            'id': name, 'oracle': 'analysis-bundle', 'artifact': 'th03-mainl',
            'unit_id': RETAINED_HEAP_UNIT, 'extent_start': '0x210a', 'extent_size': '628',
            'evidence_class': kind, 'result': result, 'location': location,
            'input_sha256': RETAINED_HEAP_SHA, 'output_sha256': digest,
        }
        if any(item.get(key) != value for key, value in expected.items()):
            raise ValueError('retained heap checkpoint evidence binding differs: ' + name)
    source = Path(RETAINED_HEAP_SOURCE)
    if any((ROOT / Path(*source.parts[:i])).is_symlink()
           for i in range(1, len(source.parts) + 1)):
        raise ValueError('retained heap checkpoint source cannot traverse a symlink')
    try:
        source_bytes = (ROOT / source).read_bytes()
    except OSError as error:
        raise ValueError('retained heap checkpoint source missing') from error
    if sha(source_bytes) != RETAINED_HEAP_SHA:
        raise ValueError('retained heap checkpoint source SHA-256 differs')


def references(row, units, evidence):
    names = row['unit_ids'].split(';') if row['unit_ids'] else []
    refs = row['evidence_ids'].split(';') if row['evidence_ids'] else []
    if not names or not refs or len(names) != len(set(names)) or len(refs) != len(set(refs)):
        raise ValueError('candidate diagnostic references empty or duplicated')
    expected = set()
    for name in names:
        unit = units.get(name)
        if (not unit or unit['artifact'] != 'th03-mainl' or not unit['segment'].startswith('decoded:')
                or unit['boundary_state'] != 'reviewed' or unit['state'] not in ('boundary-reviewed', 'source-present')
                or bool(unit['source']) != (unit['state'] == 'source-present') or unit['file_offset']):
            raise ValueError('candidate unit namespace/state/source differs')
        if unit['state'] == 'source-present':
            source = Path(unit['source'])
            if (source.is_absolute() or '..' in source.parts or source.suffix not in ('.cpp', '.c', '.asm', '.inl')
                    or source.parts[:2] not in (('src', 'shared'), ('src', 'mainl'))):
                raise ValueError('candidate maintained source ownership differs')
            if (name == RETAINED_HEAP_UNIT
                    and unit.get('replay_command') == RETAINED_HEAP_REVIEW):
                retained_heap_source_checkpoint(row, unit, evidence)
            else:
                passes = {evidence[n].get('evidence_class') for n in unit['evidence_ids'].split(';')
                          if n in evidence and evidence[n]['result'] == 'pass'}
                if not {'compiler', 'runtime', 'reproducibility'} <= passes or not unit.get('replay_command', '').startswith('python3 scripts/replay_'):
                    raise ValueError('candidate maintained source lacks independent cold/runtime/reproducibility evidence')
        expected.update(unit['evidence_ids'].split(';'))
    if set(refs) != expected:
        raise ValueError('candidate evidence reference union differs')
    failed = set()
    for name in refs:
        item = evidence.get(name)
        if (not item or item['artifact'] != 'th03-mainl' or item['oracle'] not in ('analysis-bundle', 'raw-bytes', 'runtime-trace')
                or item['result'] not in ('pass', 'fail') or not item['output_sha256']):
            raise ValueError('candidate evidence missing or accepted through another Oracle')
        if item['result'] == 'fail':
            failed.add(name)
    recorded = row['failed_evidence_ids'].split(';') if row['failed_evidence_ids'] else []
    if set(recorded) != failed or len(recorded) != len(set(recorded)):
        raise ValueError('candidate failed evidence must be retained explicitly')
    for name in names:
        if not any(evidence[n]['result'] == 'pass' and evidence[n]['oracle'] == 'analysis-bundle'
                   for n in units[name]['evidence_ids'].split(';')):
            raise ValueError('candidate unit lacks passing diagnostic bundle')


def validate(rows, expected_hashes, units, evidence):
    """Keep this CODE index diagnostic even after independent source migration."""
    paths = [r['path'] for r in rows]
    if len(paths) != len(set(paths)) or set(paths) != set(expected_hashes):
        raise ValueError('candidate direct-source membership differs')
    for row in rows:
        if (row['artifact'] != 'th03-mainl' or row['frozen_revision'] != REVISION
                or row['frozen_sha256'] != expected_hashes[row['path']] or row['scope'] != SCOPE
                or row['source_accepted'] != 'false' or row['exact_accepted'] != 'false'
                or row['receipt'] != PROOF):
            raise ValueError('candidate provenance/scope/acceptance differs')
        size, owned, gaps = (int(row[k]) for k in ('carrier_bytes', 'covered_bytes', 'gap_bytes'))
        if not 0 <= owned <= size or size <= 0 or gaps != size-owned:
            raise ValueError('candidate coverage accounting differs')
        state = 'code-covered-candidate' if not gaps else 'code-gap-candidate'
        if row['state'] != state or row['raw_equal'] not in ('true', 'false') or row['ordered_relocations_equal'] not in ('true', 'false'):
            raise ValueError('candidate coverage/state/equality differs')
        if row['notes'] != OPEN:
            raise ValueError('candidate open scope differs')
        references(row, units, evidence)


def summarize(direct, observed, comparisons, hashes, units, evidence):
    """Tie file rows to disjoint decoded intervals; retain raw failures and gaps."""
    rows = []
    for path in direct:
        carriers = [o for o in observed if o['carrier']['module'] == path]
        if not carriers or any(o['overlapping_unit_bytes'] for o in carriers):
            raise ValueError('candidate CODE carrier missing or ownership overlaps')
        names = sorted({i['unit'] for o in carriers for i in o['unit_intersections']})
        refs = sorted({e for n in names for e in units[n]['evidence_ids'].split(';')})
        size = sum(o['carrier']['size'] for o in carriers)
        owned = sum(o['independent_unit_bytes'] for o in carriers)
        matches = [comparisons[(o['carrier']['segment'], o['carrier']['offset'])] for o in carriers]
        rows.append(dict(artifact='th03-mainl', path=path, frozen_revision=REVISION,
                         frozen_sha256=hashes[path], scope=SCOPE,
                         state='code-covered-candidate' if owned == size else 'code-gap-candidate',
                         unit_ids=';'.join(names), evidence_ids=';'.join(refs),
                         failed_evidence_ids=';'.join(n for n in refs if evidence[n]['result']=='fail'),
                         carrier_bytes=str(size), covered_bytes=str(owned), gap_bytes=str(size-owned),
                         raw_equal=str(all(c['raw_slice_equal'] for m in matches for c in m)).lower(),
                         ordered_relocations_equal=str(all(c['ordered_relocations_equal'] for m in matches for c in m)).lower(),
                         source_accepted='false', exact_accepted='false', receipt=PROOF, notes=OPEN))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Portable policy and tracking reference check')
    parser.add_argument('--write', action='store_true', help='Refresh the separate diagnostic candidate CSV')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    inventory = csv_rows(ROOT/'config/rec98_th03_inventory.csv')
    units = {r['id']: r for r in csv_rows(ROOT/'config/units.csv')}
    evidence = {r['id']: r for r in csv_rows(ROOT/'config/evidence.csv')}
    hashes = {r['path']: r['sha256'] for r in inventory if 'th03-mainl' in r['direct_link_artifacts'].split(';')}
    if args.check:
        validate(csv_rows(ROOT/INDEX), hashes, units, evidence)
        print('PASS MAINL candidate index policy:', len(hashes), 'direct sources; source/exact false')
        return
    if not args.output:
        parser.error('--output required for private carrier replay')
    raw = (ROOT/PROOF).read_bytes()
    if sha(raw) != PROOF_SHA:
        raise ValueError('candidate pinned tail proof differs')
    proof = json.loads(raw)
    if not proof['diagnostic_checks_pass'] or proof['source_acceptance'] or proof['exact_acceptance']:
        raise ValueError('candidate tail proof acceptance differs')
    frozen = frozen_files(REVISION)
    direct = sorted(link_roots(frozen)['th03-mainl'])
    if {p: sha(frozen[p]) for p in direct} != hashes:
        raise ValueError('candidate inventory/frozen direct providers differ')
    inputs = {**proof['inputs'], PROOF: sha(raw),
              'scripts/review_rec98_th03_mainl_intake.py': sha(Path(__file__).read_bytes()),
              'tests/test_mainl_candidate_intake.py': sha((ROOT/'tests/test_mainl_candidate_intake.py').read_bytes()),
              'config/rec98_th03_inventory.csv': sha((ROOT/'config/rec98_th03_inventory.csv').read_bytes()),
              'config/units.csv': sha((ROOT/'config/units.csv').read_bytes())}
    target = parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    if not target.valid:
        raise ValueError('candidate invalid target MZ')
    observed = None
    comparisons = {}
    for item in proof['observations'][1:]:
        path = item['path']
        mz = parse_mz((ROOT/path).read_bytes())
        if not mz.valid:
            raise ValueError('candidate invalid cold MZ')
        mp = str(Path(path).parents[2]/'obj/th03/mainl.map')
        inputs[mp] = sha((ROOT/mp).read_bytes())
        carriers = code_rows((ROOT/mp).read_text(), len(mz.program_image))
        current = coverage(list(units.values()), carriers, len(target.program_image))
        if observed is not None and observed != current:
            raise ValueError('candidate two-round carrier ownership differs')
        observed = current
        for carrier in carriers:
            if carrier['module'] not in direct or not carrier['size']:
                continue
            key = (carrier['segment'], carrier['offset'])
            comparisons.setdefault(key, []).append(extent_observation(target, mz, carrier))
        lineage = item['source_lineage']
        if any(lineage[p]['frozen_sha256'] != hashes[p] for p in direct):
            raise ValueError('candidate frozen lineage differs')
    rows = summarize(direct, observed, comparisons, hashes, units, evidence)
    validate(rows, hashes, units, evidence)
    if args.write:
        with (ROOT/INDEX).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, FIELDS, lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
    if csv_rows(ROOT/INDEX) != rows:
        raise ValueError('candidate CSV differs from current diagnostic replay')
    inputs[INDEX] = sha((ROOT/INDEX).read_bytes())
    selected = {n: evidence[n] for row in rows for n in row['evidence_ids'].split(';')}
    # Pin selected rows, rather than an append-only journal's unrelated future rows.
    selected_sha = sha(json.dumps(selected, sort_keys=True, separators=(',', ':')).encode())
    for item in selected.values():
        path = item['location']
        digest = sha((ROOT/path).read_bytes())
        if digest != item['output_sha256']:
            raise ValueError('candidate diagnostic evidence output changed: '+path)
        inputs[path] = digest
    for p, digest in inputs.items():
        if sha((ROOT/p).read_bytes()) != digest:
            raise ValueError('candidate input changed: '+p)
    live = {r['id']: r for r in csv_rows(ROOT/'config/evidence.csv')}
    if {n: live[n] for n in selected} != selected:
        raise ValueError('candidate selected evidence rows changed')
    final_frozen = frozen_files(REVISION)
    if {p: sha(final_frozen[p]) for p in direct} != hashes:
        raise ValueError('candidate frozen source changed')
    result = dict(kind='th03-mainl-frozen-direct-source-CODE-candidate-index',
                  observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  rows=rows, carrier_coverage=observed, comparisons={f'{s:04x}:{o:04x}': v for (s,o),v in comparisons.items()},
                  selected_evidence=selected, selected_evidence_sha256=selected_sha,
                  diagnostic_checks_pass=True, source_acceptance=False, exact_acceptance=False,
                  whole_file_review_complete=False, notes=OPEN)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS MAINL CODE candidate index:', len(rows), 'sources;',
          sum(r['state']=='code-covered-candidate' for r in rows), 'covered;',
          sum(int(r['gap_bytes']) for r in rows), 'gap bytes; source/exact false')


if __name__ == '__main__':
    main()
