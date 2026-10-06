#!/usr/bin/env python3
"""Retain whole decoded OP scaffold inequalities outside the owned score cohort."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path

from lib.pc98 import parse_mz
from review_th03_mainl_cutscene import sha

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.proof.read_bytes()
    proof = json.loads(raw)
    if proof['kind'] != 'th03-op-maintained-score-cold-compiler-probes' or not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:
        raise ValueError('maintained score compiler prerequisite differs')
    inputs = {args.proof.as_posix(): sha(raw)}
    for p,h in proof['inputs'].items():
        if sha((ROOT / p).read_bytes()) != h:
            raise ValueError('compiler prerequisite input changed: ' + p)
    for p in ('scripts/review_th03_op_score_scaffold.py', 'scripts/lib/pc98.py', 'scripts/review_th03_mainl_cutscene.py'):
        inputs[p] = sha((ROOT / p).read_bytes())
    diagnostic = json.loads((ROOT / '.analysis/sol-op-score-review-20261006.json').read_bytes())
    target_path = diagnostic['observations'][0]['path']
    inputs[target_path] = diagnostic['inputs'][target_path]
    data = (ROOT / target_path).read_bytes()
    if sha(data) != inputs[target_path]:
        raise ValueError('original decoded work image differs')
    target = parse_mz(data)
    if not target.valid:
        raise ValueError('invalid decoded target')
    observations = []
    for round in proof['rounds']:
        p = args.proof.parent / f'round{round["number"]}' / 'source/bin/th03/op.exe'
        data = p.read_bytes()
        digest = sha(data)
        if digest != round['products']['bin/th03/op.exe']:
            raise ValueError('fresh OP product differs')
        inputs[p.as_posix()] = digest
        candidate = parse_mz(data)
        if not candidate.valid or len(candidate.program_image) != len(target.program_image):
            raise ValueError('decoded program size differs')
        changes = [dict(decoded_linear=i, target=x, candidate=y)
                   for i,(x,y) in enumerate(zip(target.program_image, candidate.program_image)) if x!=y]
        observations.append(dict(round=round['number'], path=p.as_posix(),
                                 decoded_program_size=len(candidate.program_image),
                                 raw_equal=not changes, changed_bytes=len(changes), changes=changes,
                                 ordered_relocations_equal=target.relocations==candidate.relocations,
                                 original_ordered_relocations=[asdict(r) for r in target.relocations],
                                 candidate_ordered_relocations=[asdict(r) for r in candidate.relocations]))
    if observations[0]['changes'] != observations[1]['changes']:
        raise ValueError('cold decoded inequality changed between rounds')
    for p,h in inputs.items():
        if sha((ROOT / p).read_bytes()) != h:
            raise ValueError('scaffold comparison input changed: ' + p)
    report = dict(kind='th03-op-score-scaffold-whole-decoded-inequality',
                  observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  observations=observations, source_acceptance=False, exact_acceptance=False,
                  notes='Whole decoded program comparison is a retained inequality diagnostic. The fresh OP scaffold omits four MAIN aggregate owner wrappers; the older4867-byte inequality remains historical evidence. No shift/sort/padding/target-array compensation. Other scaffold code/data, original relocation ownership and canonical DIET storage remain unreviewed; no reconstructed whole OP claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('Recorded whole decoded OP inequalities:', observations[0]['changed_bytes'],
          'changed bytes; ordered relocations equal:', observations[0]['ordered_relocations_equal'])


if __name__ == '__main__':
    main()
