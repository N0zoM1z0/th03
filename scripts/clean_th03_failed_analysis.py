#!/usr/bin/env python3
"""Remove unreferenced files from explicitly selected abandoned cold build runs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
FAILED=[
 '.analysis/th03-main-exact/sol-main-bounded-probe-20261006',
 '.analysis/th03-main-exact/sol-main-shared-probe-20261006-b',
 '.analysis/th03-main-exact/sol-main-shared-probe-20261006-c',
 '.analysis/th03-main-exact/sol-player-move-shots-probe-20261005',
 '.analysis/th03-op-score/sol-op-score-source-20261006',
 '.analysis/th03-op-score/sol-op-score-source-20261006-b',
 '.analysis/th03-op-score/sol-op-score-source-20261006-c',
]


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    paths=set(p for p in tracked if p and (ROOT/p).is_file())
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'.analysis').rglob('*.json') if p.is_file() and not p.is_symlink())
    texts=[];corpus={};guards={}
    def visit(value):
        if isinstance(value,dict):
            for key,v in value.items():
                if key=='inputs' and isinstance(v,dict):
                    for p,h in v.items():
                        if p.startswith('.analysis/') and isinstance(h,str) and len(h)==64:guards.setdefault(p,set()).add(h)
                visit(v)
        elif isinstance(value,list):
            for v in value:visit(v)
    for p in sorted(paths):
        raw=(ROOT/p).read_bytes()
        try:text=raw.decode()
        except UnicodeDecodeError:continue
        corpus[p]=sha(raw)
        if p.endswith('.json'):
            try:
                if json.loads(text).get('kind')=='th03-abandoned-build-output-cleanup':continue
            except (json.JSONDecodeError,AttributeError):pass
        texts.append(text)
        if p.endswith('.json'):
            try:visit(json.loads(text))
            except json.JSONDecodeError:pass
    corpus_text='\n'.join(texts)
    references=set(re.findall(r'\.analysis/[A-Za-z0-9_./-]+',corpus_text))
    def status():
        return {p:dict(exists=(ROOT/p).is_file(),sha256=sha((ROOT/p).read_bytes()) if (ROOT/p).is_file() else None) for p in guards}
    before=status();removed=[];kept=[]
    for prefix in FAILED:
        run=ROOT/prefix
        if not run.exists():continue
        if not run.is_dir() or run.is_symlink() or (run/'receipt.json').exists():raise ValueError('selected run has a receipt or unsafe path: '+prefix)
        for p in sorted(run.rglob('*')):
            if not p.is_file() or p.is_symlink():continue
            relative=p.relative_to(ROOT).as_posix()
            # Preserve failure transcripts, review helpers and every literal path
            # referenced by tracked documentation/scripts or retained JSON proofs.
            if p.suffix.lower() in ('.log','.json','.txt','.py') or relative in references or relative in guards or (' ' in relative and relative in corpus_text):
                kept.append(relative);continue
            removed.append(dict(path=relative,bytes=p.stat().st_size,sha256=sha(p.read_bytes())))
    if any(r['path'] in guards for r in removed):raise ValueError('cleanup intersects receipt inputs')
    # Freeze and validate both corpus and selected outputs immediately before mutation.
    for p,h in corpus.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('cleanup reference corpus changed: '+p)
    for r in removed:
        if sha((ROOT/r['path']).read_bytes())!=r['sha256']:raise ValueError('cleanup candidate changed')
    if args.apply:
        for r in removed:(ROOT/r['path']).unlink()
        for prefix in FAILED:
            run=ROOT/prefix
            if run.exists():
                for p in sorted((p for p in run.rglob('*') if p.is_dir() and not p.is_symlink()),key=lambda p:len(p.parts),reverse=True):
                    if not any(p.iterdir()):p.rmdir()
                if not any(run.iterdir()):run.rmdir()
    after=status()
    if before!=after:raise ValueError('retained private receipt input state changed')
    report=dict(kind='th03-abandoned-build-output-cleanup',observed_utc=datetime.now(timezone.utc).isoformat(),applied=args.apply,
                selected_runs=FAILED,reference_corpus=corpus,retained_guarded_inputs=len(guards),guarded_input_state_unchanged=True,
                removed=removed,removed_files=len(removed),removed_bytes=sum(r['bytes'] for r in removed),retained=kept,
                notes='Only explicit failed cold runs without receipt.json selected. All retained JSON input paths and tracked literal references protected; failure logs/helpers retained. Canonical targets, toolchain/Wine prefix, accepted builds and source-present proof inputs excluded. Historical pre-existing missing or stale guards are unchanged; no claim to repair old proof lineage.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('APPLIED' if args.apply else 'DRY RUN',len(removed),'files',report['removed_bytes'],'bytes; retained private input states unchanged')


if __name__=='__main__':main()
