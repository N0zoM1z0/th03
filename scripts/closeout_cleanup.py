#!/usr/bin/env python3
"""Audit and prune disposable output while keeping proof and documented references."""
import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
from unittest.mock import patch

import clean_generated as cleanup

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    if path.is_symlink():
        return hashlib.sha256(str(path.readlink()).encode()).hexdigest()
    if not path.is_file():
        return None
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1048576), b''):
            result.update(block)
    return result.hexdigest()


def documented_paths():
    """Keep literal private paths in tracked documents, commands and ledgers."""
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    preserved, corpus = set(), {}
    for name in tracked:
        path = ROOT/name
        if not name or not path.is_file() or path.is_symlink():
            continue
        raw = path.read_bytes()
        try:
            value = raw.decode('utf-8')
        except UnicodeDecodeError:
            continue
        corpus[name] = hashlib.sha256(raw).hexdigest()
        for raw_path in re.findall(r'\.analysis/[A-Za-z0-9_./-]+', value):
            lexical = Path(raw_path)
            if '..' in lexical.parts:
                continue
            preserved.add(ROOT/lexical)
            resolved = cleanup.normalized_local_path(raw_path)
            if resolved is not None:
                preserved.add(resolved)
    return preserved, corpus


def entries(path):
    if path.is_symlink() or path.is_file():
        return [path]
    return sorted(p for p in path.rglob('*') if p.is_file() or p.is_symlink())


def input_states(paths):
    return {str(p.relative_to(ROOT)): dict(exists=p.exists() or p.is_symlink(), sha256=digest(p))
            for p in sorted(paths) if cleanup.is_under(p, ROOT)}


def retired_proofs(names, documented):
    selected = []
    records = {}
    for name in names:
        lexical = Path(name)
        if not re.fullmatch(r'\.analysis/[A-Za-z0-9_.-]+\.json', name) or \
                lexical.parts[:1] != ('.analysis',) or len(lexical.parts) != 2 or \
                lexical.suffix != '.json' or lexical.name == 'receipt.json':
            raise ValueError('retirement requires a top-level diagnostic JSON')
        path = ROOT/lexical
        if path in cleanup.PRESERVED_ANALYSIS_FILES or path.is_symlink() or not path.is_file():
            raise ValueError('protected or unsafe retired proof: '+name)
        if any(cleanup.is_under(path, ref) for ref in documented | cleanup.ledger_preserved_paths()):
            raise ValueError('retired proof is documented or ledger-referenced: '+name)
        proof = json.loads(path.read_bytes())
        if not isinstance(proof, dict) or not isinstance(proof.get('inputs'), dict) or \
                proof.get('exact_acceptance') is not False or proof.get('source_acceptance') is not False:
            raise ValueError('only unaccepted diagnostic proofs can retire: '+name)
        selected.append(path)
        records[name] = dict(kind=proof.get('kind'), sha256=digest(path), bytes=path.stat().st_size,
                             reason='Superseded diagnostic; no tracked, ledger or retained-proof dependency.')
    if not selected:
        return selected, records
    needles = [str(path.relative_to(ROOT)).encode() for path in selected]
    for path in (ROOT/'.analysis').rglob('*.json'):
        if path in selected or path.is_symlink():
            continue
        # Stream the large diagnostic matrices; parse only matching files.
        matched = False
        with path.open('rb') as handle:
            tail = b''
            while block := handle.read(65536):
                data = tail + block
                if any(needle in data for needle in needles) or b'\\u' in data or b'\\/' in data:
                    matched = True
                    break
                tail = data[-max(map(len, needles)):]
        if not matched:
            continue
        proof = json.loads(path.read_bytes())
        if isinstance(proof, dict) and proof.get('kind') == 'th03-abandoned-build-output-cleanup':
            # A historical corpus fingerprint records past existence, not a read dependency.
            fingerprints = proof.get('reference_corpus')
            if isinstance(fingerprints, dict) and all(isinstance(h, str) and re.fullmatch(r'[0-9a-f]{64}', h)
                                                     for h in fingerprints.values()):
                proof = {k: v for k, v in proof.items() if k != 'reference_corpus'}
        value = json.dumps(proof).encode()
        if any(needle in value for needle in needles):
            raise ValueError('retired proof has a retained JSON reference: '+str(path.relative_to(ROOT)))
    return selected, records


def plan_cleanup(mutable_paths=(), retire=()):
    documented, corpus = documented_paths()
    proof_corpus = {str(p.relative_to(ROOT)): digest(p) for p in (ROOT/'.analysis').rglob('*.json')
                    if p.is_file() and not p.is_symlink() and p not in mutable_paths}
    retired, retirement = retired_proofs(retire, documented)
    files, roots = cleanup.proof_preserved_paths()
    ledger = cleanup.ledger_preserved_paths()
    guarded = files | ledger | documented
    selected = list(retired)

    def collect(path, dry_run):
        selected.append(path)
        return 0

    with patch.object(cleanup, 'proof_preserved_paths', return_value=(files, roots)), \
            patch.object(cleanup, 'ledger_preserved_paths', return_value=ledger | documented), \
            patch.object(cleanup, 'remove_path', side_effect=collect), redirect_stdout(io.StringIO()):
        cleanup.clean_analysis(True)
        cleanup.clean_caches(True)
    removed = {str(p.relative_to(ROOT)): dict(bytes=p.lstat().st_size, sha256=digest(p))
               for path in selected for p in entries(path)}
    return dict(selected=[str(p.relative_to(ROOT)) for p in selected], removed=removed,
                tracked_reference_corpus=corpus, proof_reference_corpus=proof_corpus,
                mutable_receipts=[str(p.relative_to(ROOT)) for p in mutable_paths], retained_input_states=input_states(guarded - set(mutable_paths) - set(retired)),
                retired_proofs=retirement,
                retained_receipt_roots=[str(p.relative_to(ROOT)) for p in sorted(roots)],
                documented_paths=len(documented))


def verify_plan(plan):
    """Finish all reference and candidate checks before the first deletion."""
    mutable = set(plan['mutable_receipts'])
    current = {str(p.relative_to(ROOT)): digest(p) for p in (ROOT/'.analysis').rglob('*.json')
               if p.is_file() and not p.is_symlink() and str(p.relative_to(ROOT)) not in mutable}
    if current != plan['proof_reference_corpus']:
        raise ValueError('proof reference corpus changed')
    for name, expected in plan['tracked_reference_corpus'].items():
        if digest(ROOT/name) != expected:
            raise ValueError('tracked reference changed: '+name)
    states = input_states({ROOT/name for name in plan['retained_input_states']})
    if states != plan['retained_input_states']:
        raise ValueError('retained input state changed')
    for name in plan['selected']:
        path = ROOT/name
        current = {str(p.relative_to(ROOT)) for p in entries(path)}
        expected = {p for p in plan['removed'] if p == name or p.startswith(name+'/')}
        if current != expected:
            raise ValueError('selected tree changed: '+name)
    for name, expected in plan['removed'].items():
        if digest(ROOT/name) != expected['sha256']:
            raise ValueError('cleanup candidate changed: '+name)


def apply_plan(plan):
    verify_plan(plan)
    with redirect_stdout(io.StringIO()):
        for name in plan['selected']:
            cleanup.remove_path(ROOT/name, False)
    states = input_states({ROOT/name for name in plan['retained_input_states']})
    if states != plan['retained_input_states']:
        raise ValueError('retained input state changed after deletion')


def output_path(value):
    path = Path(value)
    if path.is_absolute() or '..' in path.parts or len(path.parts) < 4 or \
            path.parts[:2] != ('.analysis', 'closeout') or path.name != 'receipt.json':
        raise ValueError('output must be a fresh .analysis/closeout/RUN/receipt.json')
    candidate = ROOT/path
    for parent in [candidate, *candidate.parents]:
        if parent == ROOT:
            break
        if parent.is_symlink():
            raise ValueError('output has a symlink component')
    if candidate.exists():
        raise ValueError('output receipt already exists')
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--retire-proof', action='append', default=[],
                        help='explicit superseded top-level unaccepted diagnostic; reject all live references')
    args = parser.parse_args()
    output = output_path(args.output)
    inputs = {p: digest(ROOT/p) for p in ['scripts/closeout_cleanup.py', 'scripts/clean_generated.py', 'tests/test_closeout_cleanup.py']}
    report = dict(kind='th03-closeout-disposable-output-cleanup', observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, applied=False, complete=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    # The receipt directory protects the receipt itself and its verification logs.
    output.write_text(json.dumps(report, indent=2)+'\n')
    plan = plan_cleanup(mutable_paths={output}, retire=args.retire_proof)
    verify_plan(plan)
    report.update(plan, removed_files=len(plan['removed']),
                  removed_bytes=sum(r['bytes'] for r in plan['removed'].values()))
    if args.apply:
        apply_plan(plan)
    report.update(applied=args.apply, complete=True, retained_input_states_unchanged=True,
                  notes='Proof inputs, complete receipt directories, ledger and literal tracked references retained. '
                        'Explicit retired unaccepted diagnostics have no tracked/ledger/retained JSON dependency; historical corpus fingerprints remain. '
                        'Historical missing/stale inputs are recorded as found, without repair. Product code and accepted claims unchanged.')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print('APPLIED' if args.apply else 'DRY RUN', report['removed_files'], 'files;', report['removed_bytes'], 'bytes;',
          len(plan['retained_input_states']), 'retained states unchanged')
    print('Receipt:', output.relative_to(ROOT))


if __name__ == '__main__':
    main()
