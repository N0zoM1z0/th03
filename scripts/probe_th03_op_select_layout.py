#!/usr/bin/env python3
"""Observe whether the Select candidate's explicit padding has a compiler effect."""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tomllib
from lib.omf import describe_omf,normalize_dependency_timestamps,parse_omf
from review_th03_mainl_cutscene import sha
from replay_th03_main_exact_units import execute
from inventory_rec98_th03 import frozen_files
from review_th03_mainl_cutscene import REVISION

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run-id',required=True);a=ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',a.run_id):raise ValueError('invalid run id')
    out=ROOT/'.analysis/th03-op-select-layout'/a.run_id;out.mkdir(parents=True,exist_ok=False)
    cfg=dict(reference_revision=REVISION,source='th03/op/m_select.cpp',wrapper='th03/op_sel.cpp',object='obj/th03/op_sel.obj')
    inputs={p:sha((ROOT/p).read_bytes()) for p in ['scripts/probe_th03_op_select_layout.py','config/toolchain.toml','scripts/lib/omf.py','scripts/inventory_rec98_th03.py','scripts/replay_th03_main_exact_units.py']}
    archive=out/'reference.tar';subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());env=os.environ.copy()
    env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    frozen=frozen_files(REVISION);source=frozen[cfg['source']].decode();rows=[];objects=[]
    for label in ('candidate_padding','compiler_alignment'):
        work=out/label/'source';work.mkdir(parents=True)
        subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        text=source
        if label=='compiler_alignment':
            for line in ('static int8_t padding_1; // ZUN bloat\n','static int8_t padding_2; // ZUN bloat\n'):
                if text.count(line)!=1:raise ValueError('candidate padding anchor differs')
                text=text.replace(line,'')
        (work/cfg['source']).write_text(text);(work/cfg['wrapper']).write_text(f'#include "{cfg["source"]}"\n')
        (work/'obj/th03').mkdir(parents=True,exist_ok=True)
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r"&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='O' -nobj/th03/ th03/op_sel.cpp"]
        result=execute(command,work,env,out/label/'compiler.log');raw=(work/cfg['object']).read_bytes();obj=describe_omf(raw)
        if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:raise ValueError('wrong Select compiler')
        record_types=('LNAMES','SEGDEF','GRPDEF','EXTDEF','PUBDEF','LPUBDEF','LEDATA','LIDATA','FIXUPP')
        records=[dict(name=r.name,payload=r.data.hex()) for r in parse_omf(raw) if r.name in record_types]
        objects.append(normalize_dependency_timestamps(raw))
        rows.append(dict(case=label,source_sha256=sha(text.encode()),build=result,object_sha256=sha(raw),normalized_sha256=sha(objects[-1]),records=records))
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('Select layout input changed: '+p)
    if frozen_files(REVISION)[cfg['source']]!=frozen[cfg['source']]:raise ValueError('frozen Select changed')
    report=dict(kind='th03-op-select-unused-padding-vs-compiler-alignment',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                reference_archive_sha256=sha(archive.read_bytes()),frozen_source_sha256=sha(frozen[cfg['source']]),reference_revision=REVISION,observations=rows,normalized_objects_equal=objects[0]==objects[1],
                producer_records_equal=rows[0]['records']==rows[1]['records'],source_acceptance=False,exact_acceptance=False,
                notes='Two fresh frozen private trees; one Select object each with identical target compiler flags. Removing the two unreferenced candidate int8 padding declarations tests natural compiler alignment. No target/link/fullproduct/exact result inferred from object equality.')
    (out/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('Select compiler layout:',report['normalized_objects_equal'],report['producer_records_equal'])


if __name__=='__main__':main()
