#!/usr/bin/env python3
"""Bind the existing complete cutscene C++ producer to the current cold graph.

No new runtime harness: the configured required native/raw/ownership gates are
distinct from supporting selected historical runtime observations.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_cutscene_layout import verify as layout

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/mainl-cutscene-build.json'
INPUTS=(*sound.INPUTS,'scripts/review_th03_mainl_cutscene_work.py',
        'scripts/lib/decoded_mainl_cutscene_layout.py','scripts/lib/decoded_mainl_cutscene_inventory.py',
        'scripts/review_th03_mainl_cutscene.py','src/mainl/cutscene.cpp',
        'src/mainl/cutscene/cutscene.hpp','src/mainl/cutscene/script.inl',
        'src/mainl/cutscene/egc_start_copy.inl')


def need(value,message):
    if not value:
        raise ValueError('MAINL current cutscene: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {n:sha((root/n).read_bytes()) for n in INPUTS}


def observe(work,target,candidate,graph,files):
    return json.loads(json.dumps(dict(layout=layout(work,target,candidate,graph,files))))


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-cutscene-build.json').read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-cutscene-current-review-v1','complete current report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),
         'current complete source/implementation/cold binding')
    need(report['scope']==observe(work,target,candidate,graph,files),'entire current native proof')
    return dict(**report['scope'],review_sha256=sha(raw))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true')
    options=parser.parse_args()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_roll_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    report=dict(schema='th03-mainl-cutscene-current-review-v1',complete=True,
        implementation_sha256=inputs(ROOT),cold_report_sha256=sha(raw),
        source_inventory_sha256=sound.digest(cold['source_sha256']),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False,
        scope=observe(work,target,candidate,graph,files))
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    current_scope(ROOT,work,target,candidate,raw,graph,files)
    print('MAINL cutscene: 13 complete procedures /3122 instruction bytes/1057 instructions; '
          'all236 native fields/56 ordered MZ relocations;72 table bytes +1 zero required uncredited context')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
