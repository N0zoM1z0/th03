#!/usr/bin/env python3
"""Scoped original-TC4 source/object/full-MAIN check for Extra Attacks and major BOSSes.

The after596 parent is a *frozen* historical source proof. Never overwrite its
source snapshots or claim that its stored source hash describes later edits.
This probe overlays ONLY selected current C++ TUs and the live entity header,
builds two fresh native objects/links, and compares all original CODE fields,
PUBLIC offsets, segment definitions, whole loaded image and ordered MZ vector.
It does not run a full cold build or promote canonical Factory credit.

Usage: PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
          --stage af598u --units ex_yume,ex_mima
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import build_th03_main_yumemi_cpu_after596_work as parent
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.omf import parse_omf

ROOT = parent.ROOT
WORK = parent.WORK
SOURCES = {
    'ex_yume': 'src/main/player/exatt_yumemi.cpp',
    'ex_mima': 'src/main/player/exatt_mima.cpp',
    'ex_rika': 'src/main/player/exatt_rikako.cpp',
    'ex_kana': 'src/main/player/exatt_kana.cpp',
    'ex_ellen': 'src/main/player/exatt_ellen.cpp',
    'ex_maris': 'src/main/player/exatt_marisa.cpp',
    'ex_chyu': 'src/main/player/exatt_chiyuri.cpp',
    'ex_koto': 'src/main/player/exatt_kotohime.cpp',
    'ex_rfly': 'src/main/player/exatt_flight_reimu.cpp',
    'ex_reup': 'src/main/player/exatt_reimu.cpp',
    'ba_chiyu': 'src/main/boss/chiyuri.cpp',
    'ba_kana': 'src/main/boss/kana.cpp',
    'ba_koto': 'src/main/boss/kotohime.cpp',
    'ba_ellen': 'src/main/boss/ellen.cpp',
    'ba_rikak': 'src/main/boss/rikako.cpp',
    'ba_yumem': 'src/main/boss/yumemi.cpp',
    'ba_mima': 'src/main/boss/mima.cpp',
    'ba_reimu': 'src/main/boss/reimu.cpp',
    'ba_maris': 'src/main/boss/marisa.cpp',
    'ba_sring': 'src/main/boss/shared.cpp',
    'ba_srest': 'src/main/boss/shared.cpp',
    'e_fireb': 'src/main/enemy/fireball.cpp',
    'e_expl': 'src/main/enemy/expl.cpp',
    'bullet': 'src/main/bullet/bullet.cpp',
    'eforna': 'src/main/enemy/enemy.cpp',
    'efornb': 'src/main/enemy/enemy.cpp',
    'eupda': 'src/main/enemy/enemy.cpp',
    'eupdb': 'src/main/enemy/enemy.cpp',
}
BOSS_SHARED_UNITS = ('ba_sring', 'ba_srest')
ENTITY = 'src/main/player/exatt_entity.hpp'
BOSS_TEMPLATE = 'src/main/boss/template_state.hpp'
BOSS_TEMPLATE_NEEDLE = f'#include "{BOSS_TEMPLATE}"'.encode()
PRODUCER_WRAPPERS = {
    'e_fireb': 'src/main/enemy/producers/fireball_native.cpp',
    'e_expl': 'src/main/enemy/producers/explosion_native.cpp',
    'bullet': 'src/main/bullet/producers/bullet_native.cpp',
    'eforna': 'src/main/enemy/producers/eforna.cpp',
    'efornb': 'src/main/enemy/producers/efornb.cpp',
    'eupda': 'src/main/enemy/producers/eupda.cpp',
    'eupdb': 'src/main/enemy/producers/eupdb.cpp',
}
ORIGINAL_STAGES = {
    'e_fireb': 'af589f', 'e_expl': 'af589f',
    'bullet': 'af588b',
    'eforna': 'af572e', 'efornb': 'af572e',
    'eupda': 'af572e', 'eupdb': 'af572e',
}
# The original native MAP has CODE/DATA/BSS/empty segment rows, and
# the enemy's compiler flags also instantiate additional empty sections.
MAP_ROWS = {
    'ba_sring':5, 'ba_srest':5,
    'e_fireb':3, 'e_expl':3, 'bullet':4,
    'eforna':8, 'efornb':8, 'eupda':8, 'eupdb':9,
}

def wrapper_source(unit):
    if unit in BOSS_SHARED_UNITS:
        partition=('TH03_BOSS_SHARED_RING_ONLY' if unit=='ba_sring'
                   else 'TH03_BOSS_SHARED_REST_ONLY')
        return f'#define {partition} 1\n#include "{SOURCES[unit]}"\n'.encode()
    if unit in PRODUCER_WRAPPERS:
        return (ROOT/PRODUCER_WRAPPERS[unit]).read_bytes()
    return (('#define TH03_EXATT_REIMU_UPDATE_ONLY\n' if unit=='ex_reup' else '') +
            f'#include "{SOURCES[unit]}"\n').encode()


# Explicit include paths are mandatory: with the original literal
# #include "src/..." the TC4 search order can silently choose the old
# WORK/src/... first. A copied overlay is NOT proof of compilation.
SOURCE_HEADER_NEEDLE = b'#include "src/main/player/exatt_entity.hpp"'
BINDING_MODE = 'explicit-native-include-with-omf-dependency-check-v2'

def rooted_source(unit, stage, n, raw):
    for header, needle in ((ENTITY, SOURCE_HEADER_NEEDLE),
                           (BOSS_TEMPLATE, BOSS_TEMPLATE_NEEDLE)):
        if needle in raw:
            raw = raw.replace(
                needle, f'#include "probe/{stage}/r{n}/{header}"'.encode()
            )
    return raw

def rooted_wrapper(unit, stage, n, raw):
    literal=f'#include "{SOURCES[unit]}"'.encode()
    need(raw.count(literal)==1, 'one real source include '+unit)
    return raw.replace(
        literal, f'#include "probe/{stage}/r{n}/{SOURCES[unit]}"'.encode(),
    )

def check_native_dependencies(obj, unit, stage, n, source_has_entity,
                              source_has_boss_template=False):
    records=[r.data for r in parse_omf(obj) if r.record_type==0x88 and
             r.data.startswith(b'\x00\xe9')]
    low=[v.lower() for v in records]
    name=f'probe/{stage}/r{n}/{SOURCES[unit]}'.encode().lower()
    need(any(name in v for v in low),
         'actual native OMF dependency binds forced overlay source '+unit)
    for header, used in ((ENTITY,source_has_entity),
                         (BOSS_TEMPLATE,source_has_boss_template)):
        if used:
            expected=f'probe/{stage}/r{n}/{header}'.encode().lower()
            need(any(expected in v for v in low),
                 'actual native OMF dependency binds forced header '+unit+' '+header)
    return {'source':name.decode(), 'entity_header_bound':source_has_entity,
            'boss_template_header_bound':source_has_boss_template}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def need(cond, desc):
    if not cond:
        raise ValueError(desc)

def pins(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    need(not path.exists(), 'refusing to replace native evidence: ' + str(path))
    path.write_bytes(raw)
    return {'path': path.relative_to(ROOT).as_posix(),
            'bytes': len(raw), 'sha256': sha(raw)}

def run(argv, env, label, stage_path, rounds):
    p = subprocess.run(argv, cwd=WORK, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=110)
    log = pins(stage_path / (label + '.log'), p.stdout)
    rounds.append({'label':label, 'argv':argv, 'exit_code':p.returncode, 'log':log})
    need(p.returncode == 0,
         label + ': ' + p.stdout.decode(errors='replace')[-2000:])

def scope(actual, original, stem):
    need(payload(actual) == payload(original), stem + ' entire CODE payload differs')
    need(literal_fields(actual) == literal_fields(original),
         stem + ' ordered native fields differ')
    need(public_offsets(actual) == public_offsets(original),
         stem + ' PUBLIC offsets differ')
    need(segment_definitions(actual) == segment_definitions(original),
         stem + ' segment definitions differ')
    initialized = payload(original)
    segs = segment_definitions(original)
    classes = {row['index']:row['class'] for row in segs}
    code_bytes = sum(classes[index]=='CODE' for index, offset in initialized)
    data_bytes = sum(classes[index]=='DATA' for index, offset in initialized)
    need(code_bytes + data_bytes == len(initialized),
         stem + ' original initialized bytes have known CODE/DATA owners')
    result = {'CODE_bytes':code_bytes, 'ordered_native_fields':len(literal_fields(original)),
              'PUBLICs':len(public_offsets(original)), 'all_original_CODE_and_fields_exact':True,
              'raw_OMF_packet_identical':actual == original}
    if stem in ORIGINAL_STAGES:
        result['DATA_bytes']=data_bytes
        result['BSS_bytes']=sum(row['size'] for row in segs if row['class']=='BSS')
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage', required=True)
    ap.add_argument('--units', required=True, help='comma-separated original OBJ names')
    args=ap.parse_args()
    need(re.fullmatch(r'af[0-9]+[a-z][0-9]*', args.stage), 'unique DOS-safe stage')
    units=args.units.split(',')
    need(len(units)==len(set(units)) and 1 <= len(units) <= len(SOURCES)
         and all(u in SOURCES for u in units), 'known, distinct native units')
    stage=WORK/'probe'/args.stage
    logroot=ROOT/'.analysis/work'/('exatt-layout-' + args.stage)
    report_path=logroot/'report.json'
    need(not stage.exists() and not logroot.exists(), 'fresh proof stage')
    parent.inputs()  # Validates the after595 ancestor and the after596 recipe.
    prior=json.loads((ROOT/parent.REPORT).read_text())
    need(len(prior['rounds'])==2 and prior['complete'], 'historical after596 native full-MAIN parent')
    old=(WORK/'obj/th03')
    originals={u:(old/(u+'.obj')).read_bytes() for u in units}
    ref=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    target=parse_mz(ref)
    need(len(ref)==130882 and len(target.relocations)==1553,'pinned original Japanese MAIN')
    source_data={name:(ROOT/SOURCES[name]).read_bytes() for name in units}
    header_data=(ROOT/ENTITY).read_bytes()
    template_data=(ROOT/BOSS_TEMPLATE).read_bytes()
    wrapper_data={u:wrapper_source(u) for u in units}
    need(all(w.count(f'#include "{SOURCES[u]}"'.encode())==1 for u,w in wrapper_data.items())
         and all(b'\r' not in w for w in wrapper_data.values()),
         'per-producer original C++ wrapper with exactly one source include')
    # The original source-only project still contains the full old graph.
    # Only these per-round overlays alter what the compiler sees.
    need(all(b'\r' not in s for s in (*source_data.values(),header_data)),
         'maintained sources must use LF')
    rows=[]
    result={'schema':'th03-main-source-rooted-overlay-v2', 'stage':args.stage,
            'parent_report':parent.REPORT,
            'parent_report_sha256':sha((ROOT/parent.REPORT).read_bytes()),
            'units':units, 'source_sha256':{u:sha(s) for u,s in source_data.items()},
            'entity_header_sha256':sha(header_data),
            'boss_template_header_sha256':sha(template_data),
            'wrapper_sha256':{u:sha(w) for u,w in wrapper_data.items()},
            'whole_original_image_and_relocations_equal':False,
            'canonical_Factory_credit':False, 'rounds':[],
            'compiler_source_binding': BINDING_MODE}
    cpu=min(os.sched_getaffinity(0))
    env=dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
             WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
             MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    # No stale or live proof source file is edited: only new ignored probe data.
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        stage.mkdir(parents=True)
        logroot.mkdir(parents=True)
        all_rounds=[]
        for n in (1,2):
            rd=stage/f'r{n}'
            rd.mkdir()
            for u in units:
                file=rd/SOURCES[u]
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(rooted_source(u,args.stage,n,source_data[u]).replace(b'\n',b'\r\n'))
            entity=rd/ENTITY
            entity.parent.mkdir(parents=True, exist_ok=True)
            entity.write_bytes(header_data.replace(b'\n',b'\r\n'))
            template=rd/BOSS_TEMPLATE
            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_bytes(template_data.replace(b'\n',b'\r\n'))
            wrapper=wrapper_data
            for u in units:
                (rd/(u+'.cpp')).write_bytes(
                    rooted_wrapper(u,args.stage,n,wrapper[u]).replace(b'\n',b'\r\n'))
            phases=[];scopes={};outputs={}
            def exec_cmd(argv,label):
                prefix=['taskset','-c',str(cpu),'nice','-n','10']
                run(prefix+argv,env,label,logroot,phases)
            for u in units:
                exec_cmd(dos+['tcc','-c',f'-Iprobe/{args.stage}/r{n}','-I.','-O','-b-',
                              '-3','-Z','-d','-DGAME=3','-ml',"-DBINARY='M'",
                              f'-nprobe/{args.stage}/r{n}/',
                              f'probe/{args.stage}/r{n}/{u}.cpp'],
                          f'round{n}-{u}-TC4')
                raw=(rd/(u+'.obj')).read_bytes()
                check_native_dependencies(raw,u,args.stage,n,
                    SOURCE_HEADER_NEEDLE in source_data[u],
                    BOSS_TEMPLATE_NEEDLE in source_data[u])
                scopes[u]=scope(raw,originals[u],u)
                outputs[u+'_obj']=pins(logroot/(f'round{n}-{u}.obj'),raw)
            response=parent.response(n)
            for u in units:
                oldpath=(f'probe\\{parent.STAGE}\\r{n}\\{u}.obj' if u in parent.ORDER
                         else f'probe\\af567c\\r{n}-{u}.obj' if u.startswith('ba_') and u not in BOSS_SHARED_UNITS
                         else f'probe\\{ORIGINAL_STAGES[u]}\\r{n}\\{u}.obj' if u in ORIGINAL_STAGES
                         else f'obj\\th03\\{u}.obj').encode()
                newpath=f'probe\\{args.stage}\\r{n}\\{u}.obj'.encode()
                need(response.count(oldpath)==1,'unique original link slot '+u)
                response=response.replace(oldpath,newpath)
            for ext in ('exe','map'):
                oldname=f'probe\\{parent.STAGE}\\r{n}.{ext}'.encode()
                newname=f'probe\\{args.stage}\\r{n}.{ext}'.encode()
                need(response.count(oldname)==1,'unique output '+ext)
                response=response.replace(oldname,newname)
            (stage/f'r{n}.@l').write_bytes(response)
            exec_cmd(dos+['tlink',f'@probe\\{args.stage}\\r{n}.@l'],
                     f'round{n}-TLINK')
            exe=(stage/f'r{n}.exe').read_bytes()
            newmap=(stage/f'r{n}.map').read_bytes()
            prev=prior['rounds'][n-1]['outputs']
            prevexe=parent.read_pin(prev['exe'])
            prevmap=parent.read_pin(prev['map'])
            need(exe==prevexe,'full native TLINK output changed at round '+str(n))
            mz=parse_mz(exe)
            need(mz.program_image==target.program_image
                 and mz.relocations==target.relocations
                 and compact_mz(exe)==ref,'entire original Japanese image, MZ and relocations')
            # Path spelling alone differs between the overlay and parent.
            for u in units:
                a=f'M=probe/{args.stage}/r{n}/{u}.cpp'.encode()
                b=(f'M=probe/{parent.STAGE}/r{n}/{u}.cpp' if u in parent.ORDER
                   else f'M=th03/{u}.cpp' if u.startswith('ba_')
                   else f'M=probe/{ORIGINAL_STAGES[u]}/r{n}/{u}.cpp' if u in ORIGINAL_STAGES
                   else f'M=th03/{u}.cpp').encode()
                need(newmap.count(a)==MAP_ROWS.get(u,4), 'all original MAP rows '+u)
                newmap=newmap.replace(a,b)
            need(newmap==prevmap,'complete original MAP layout/ownership differs')
            outputs['exe']=pins(logroot/(f'round{n}.exe'),exe)
            outputs['map']=pins(logroot/(f'round{n}.map'),(stage/f'r{n}.map').read_bytes())
            outputs['compact_mz']=pins(logroot/(f'round{n}-compact.exe'),compact_mz(exe))
            all_rounds.append({'number':n,'scopes':scopes,'phases':phases,
                               'response_sha256':sha(response),'outputs':outputs})
            print('native TC4 round',n,','.join(units),'CODE',
                  sum(x['CODE_bytes'] for x in scopes.values()),
                  'original MAIN image and relocations exact',flush=True)
        result['rounds']=all_rounds
        result['whole_original_image_and_relocations_equal']=True
        report_path.write_text(json.dumps(result,indent=2)+'\n')
        print('PROOF',report_path.relative_to(ROOT),'SHA256',sha(report_path.read_bytes()))
if __name__=='__main__':
    main()
