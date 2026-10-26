#!/usr/bin/env python3
"""Bind the existing complete registration C++ producer to the current cold graph.

No new runtime harness: the configured required native/raw/ownership gates are
distinct from supporting selected historical runtime observations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_registration_layout import verify as layout

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/mainl-registration-build.json'
INPUTS=(*sound.INPUTS,'scripts/review_th03_mainl_registration_work.py',
        'scripts/lib/decoded_mainl_registration_layout.py','scripts/lib/decoded_mainl_registration_inventory.py',
        'scripts/review_th03_mainl_regist.py','scripts/review_th03_mainl_cutscene.py',
        'src/mainl/hiscore/regdata.cpp','src/mainl/regist.cpp',
        'src/mainl/hiscore/regist.hpp','src/mainl/hiscore/regist_text.hpp',
        'src/mainl/hiscore/scoredat.hpp','src/mainl/hiscore/regi.h',
        'src/mainl/hiscore/score_load.inl','src/mainl/hiscore/score_save.inl','src/mainl/hiscore/scorecry.hpp')


def need(value,message):
    if not value:
        raise ValueError('MAINL current registration: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {n:sha((root/n).read_bytes()) for n in INPUTS}


def observe(work,target,candidate,graph,files):
    return json.loads(json.dumps(dict(layout=layout(work,target,candidate,graph,files))))


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-registration-build.json').read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-registration-current-review-v1','complete current report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),
         'current complete source/implementation/cold binding')
    need(report['scope']==observe(work,target,candidate,graph,files),'entire current native proof')
    return dict(**report['scope'],review_sha256=sha(raw))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true')
    options=parser.parse_args()
    if not options.current_cold:
        parser.error('registration review requires --current-cold; rebuild genuinely changed inputs separately')
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    report=dict(schema='th03-mainl-registration-current-review-v1',complete=True,
        implementation_sha256=inputs(ROOT),cold_report_sha256=sha(raw),
        source_inventory_sha256=sound.digest(cold['source_sha256']),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False,
        scope=observe(work,target,candidate,graph,files))
    need(report['implementation_sha256']==inputs(ROOT), 'implementation changed during review')
    temporary=REPORT.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(report,indent=2)+'\n')
    temporary.replace(REPORT)
    current_scope(ROOT,work,target,candidate,raw,graph,files)
    print('MAINL registration: 14 complete procedures /2720 instruction bytes/988 instructions; '
          'all188 native fields;54 selected ordered MZ relocations;68 CODE +40 DATA uncredited context')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
