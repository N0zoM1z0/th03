#!/usr/bin/env python3
"""Measure OP/MAINL reviewed intervals against a pinned current cold MAP pair."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows
from review_th03_mainl_cutscene import sha
from review_th03_mainl_coverage import coverage as mainl_coverage
from review_th03_op_coverage import coverage as op_coverage

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler-receipt', required=True)
    parser.add_argument('--receipt-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    path = Path(args.compiler_receipt)
    if path.is_absolute() or '..' in path.parts or path.parts[0] != '.analysis' or path.name != 'receipt.json':
        raise ValueError('current coverage receipt path differs')
    raw = (ROOT/path).read_bytes()
    if sha(raw) != args.receipt_sha256:
        raise ValueError('current coverage pinned compiler receipt differs')
    proof = json.loads(raw)
    if proof['kind'] not in ('th03-shared-cdg-loading-maintained-cold-probes', 'th03-shared-cdg-drawing-maintained-cold-probes', 'th03-shared-text-maintained-cold-probes') or not proof['diagnostic_checks_pass'] or proof['exact_acceptance'] or len(proof['rounds']) != 2:
        raise ValueError('current coverage compiler scope differs')
    inputs = {**proof['inputs'], str(path): sha(raw)}
    for p in ('config/units.csv', 'scripts/review_th03_current_decoded_coverage.py',
              'scripts/review_th03_mainl_coverage.py', 'scripts/review_th03_op_coverage.py',
              'tests/test_mainl_coverage_review.py', 'tests/test_op_coverage_review.py'):
        inputs[p] = sha((ROOT/p).read_bytes())
    units = list(csv.DictReader((ROOT/'config/units.csv').read_text().splitlines()))
    observations = {}
    for art, compare in [('op', op_coverage), ('mainl', mainl_coverage)]:
        current = []
        for r in proof['rounds']:
            tree = path.parent/f'round{r["number"]}/source'
            ip, mp = str(tree/f'bin/th03/{art}.exe'), str(tree/f'obj/th03/{art}.map')
            inputs[ip], inputs[mp] = sha((ROOT/ip).read_bytes()), sha((ROOT/mp).read_bytes())
            if inputs[ip] != r['products'][f'bin/th03/{art}.exe'] or inputs[mp] != r['observations'][art]['map_sha256']:
                raise ValueError('current coverage cold image/MAP changed')
            mz = parse_mz((ROOT/ip).read_bytes())
            if not mz.valid:
                raise ValueError('current coverage invalid MZ')
            rows = compare(units, code_rows((ROOT/mp).read_text(), len(mz.program_image)), len(mz.program_image))
            if any(o['overlapping_unit_bytes'] for o in rows):
                raise ValueError('current coverage decoded ownership overlaps')
            current.append(rows)
        if current[0] != current[1]:
            raise ValueError('current coverage cold MAP pair differs')
        observations[art] = current[0]
    for p, h in inputs.items():
        if sha((ROOT/p).read_bytes()) != h:
            raise ValueError('current coverage input changed: '+p)
    report = dict(kind='th03-current-OP-MAINL-decoded-interval-vs-cold-MAP', observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, observations=observations, source_acceptance=False, exact_acceptance=False,
                  notes='Union of current reviewed/source-present decoded intervals, using both pinned current shared source cold MAPs. No source/exact/whole-file/semantic-gap credit. Historical shifted OP MAP coverage remains separate; source migration must not erase MAINL interval credit or duplicate existing function/producer rows.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    for art, rows in observations.items():
        print('PASS current coverage', art, len(rows), 'carriers', sum(o['independent_unit_bytes'] for o in rows), 'covered',
              sum(sum(g['size'] for g in o['independent_unit_gaps']) for o in rows), 'gap bytes')


if __name__ == '__main__':
    main()
