#!/usr/bin/env python3
"""Source-bound TASM/TLINK proof for TH03 MAIN's three shared sound leaves.

Only these three physical objects are assembled. The unchanged, pinned
99-object MAIN response supplies every other input; no cold replay.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess

from build_th03_main_yumemi_cpu_after596_work import ROOT, WORK
import build_th03_main_yumemi_cpu_after596_work as parent
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from probe_th03_main_exatt_layout import need, scope, sha

SOURCES = {
    'snd_mode_main': 'mode',
    'snd_pmdr_main': 'pmd',
    'snd_se_r_main': 'reset',
}
ORDER = tuple(SOURCES)
SOURCE_FILES = {owner: f'src/main/sound/{leaf}.asm'
                for owner,leaf in SOURCES.items()}
ORIGINAL_OBJECT_FILES = {owner: f'obj/th03/{owner}.obj' for owner in SOURCES}
ORIGINAL_LINK_SLOTS = {owner: 'obj\\th03\\'+owner+'.obj' for owner in SOURCES}
SOURCE_INCLUDES = ()
MAP_ORIGINAL = {owner: 'th03\\'+owner+'.asm' for owner in SOURCES}
MAP_ROWS = {owner: 3 for owner in SOURCES}
# Only exact-value aliases of identical original public data may be
# reordered for a different native TASM version. No relocation, symbol
# value, CODE, DATA, BSS, segment or MAP module row is relaxed.
MAP_TIED_PUBLIC_ORDER_PAIRS = ()
# Zero-byte segment carriers need byte-level ACBP/LNAMES/SEGDEF/GRPDEF
# equality. Other proven owners retain their existing strict physical scope.
STRICT_OMF_SEGMENT_LAYOUT = False


def strict_segment_encoding(actual, original, owner):
    """Compare ordered raw OMF segment metadata, including ACBP alignment."""
    types = (0x96, 0x98, 0x99, 0x9A)
    def entries(raw):
        return tuple((r.record_type, r.data) for r in parse_omf(raw)
                     if r.record_type in types)
    candidate, reference = entries(actual), entries(original)
    need(candidate == reference,
         owner + ' raw ordered OMF LNAMES/SEGDEF/GRPDEF differs')
    return sha(b''.join(bytes([kind]) + len(data).to_bytes(2, 'little') + data
                        for kind, data in candidate))
REPORT_SCHEMA = 'th03-main-three-sound-asm-v1'
REPORT_FOLDER = 'main-sound-asm-'



def original_paths():
    return {owner: WORK/ORIGINAL_OBJECT_FILES[owner] for owner in ORDER}


def checked_includes():
    pinned = {}
    for name in SOURCE_INCLUDES:
        current = (ROOT/name).read_bytes()
        need(current==(WORK/name).read_bytes(),
             'native assembler actually consumed matching maintained include '+name)
        pinned[name] = sha(current)
    return pinned


def response(stage, n):
    data = parent.response(n)
    for owner, leaf in SOURCES.items():
        old = ORIGINAL_LINK_SLOTS[owner].format(n=n).encode()
        new = (f'probe\\{stage}\\r{n}\\{leaf}.obj').encode()
        need(data.count(old)==1, 'one original physical sound slot: '+owner)
        data = data.replace(old, new)
    for ext in ('exe','map'):
        old = (f'probe\\{parent.STAGE}\\r{n}.{ext}').encode()
        new = (f'probe\\{stage}\\r{n}.{ext}').encode()
        need(data.count(old)==1, 'one MAIN '+ext+' path')
        data = data.replace(old, new)
    return data


def expected_sources():
    return {owner: (ROOT/SOURCE_FILES[owner]).read_bytes()
            for owner in SOURCES}


def check_round(stage, n, originals, sources, expected_target):
    stage_dir = WORK/'probe'/stage
    rd = stage_dir/f'r{n}'
    need((stage_dir/f'r{n}.@l').read_bytes()==response(stage,n),
         'original 99-object MAIN link response')
    native = {}
    strict_layout = {}
    for owner,leaf in SOURCES.items():
        source_file = rd/(leaf+'.asm')
        need(source_file.read_bytes()==sources[owner].replace(b'\n', b'\r\n'),
             'original TASM consumed maintained '+owner)
        obj=(rd/(leaf+'.obj')).read_bytes()
        desc=describe_omf(obj)
        module=desc['module_name'].replace('\\','/').lower()
        need(desc['valid'] and module==f'probe/{stage}/r{n}/{leaf}.asm',
             'native object THEADR binds staged maintained source '+owner)
        native[owner] = scope(obj, originals[owner], owner)
        if STRICT_OMF_SEGMENT_LAYOUT:
            strict_layout[owner] = strict_segment_encoding(
                obj, originals[owner], owner)
    exe=(stage_dir/f'r{n}.exe').read_bytes()
    prior=json.loads((ROOT/parent.REPORT).read_text())
    parent_exe=parent.read_pin(prior['rounds'][n-1]['outputs']['exe'])
    need(exe==parent_exe and compact_mz(exe)==expected_target,
         'complete original Japanese MAIN image and header serialization')
    mz=parse_mz(exe); target=parse_mz(expected_target)
    need(mz.program_image==target.program_image and mz.relocations==target.relocations,
         'complete original Japanese MAIN and ordered MZ relocations')
    map_bytes=(stage_dir/f'r{n}.map').read_bytes()
    for owner,leaf in SOURCES.items():
        current=(f'M=probe\\{stage}\\r{n}\\{leaf}.asm').encode()
        original=('M='+MAP_ORIGINAL[owner].format(n=n)).encode()
        need(map_bytes.count(current)==MAP_ROWS[owner],
             'complete original CODE/DATA/BSS MAP rows '+owner)
        map_bytes=map_bytes.replace(current,original)
    parent_map=parent.read_pin(prior['rounds'][n-1]['outputs']['map'])
    for candidate_pair, original_pair in MAP_TIED_PUBLIC_ORDER_PAIRS:
        need(map_bytes.count(candidate_pair)==1 and
             parent_map.count(original_pair)==1,
             'unique tied same-address PUBLIC alias order in MAP')
        map_bytes=map_bytes.replace(candidate_pair,original_pair)
    need(map_bytes==parent_map,'complete normalized native MAIN MAP geometry')
    result = {'number':n,'original_scopes':native,
            'original_objects_sha256':{k:sha(originals[k]) for k in ORDER},
            'objects_sha256':{owner:sha((rd/(leaf+'.obj')).read_bytes())
                              for owner,leaf in SOURCES.items()},
            'normal_exe_sha256':sha(exe),
            'normal_map_sha256':sha((stage_dir/f'r{n}.map').read_bytes()),
            'response_sha256':sha(response(stage,n))}
    if STRICT_OMF_SEGMENT_LAYOUT:
        result['raw_OMF_segment_layout_sha256'] = strict_layout
    return result


def summary(stage, rows):
    counts={'CODE_bytes':0,'ordered_native_fields':0,'PUBLICs':0}
    for item in rows[0]['original_scopes'].values():
        for name in counts: counts[name]+=item[name]
    return {'stage':stage,'complete_original_units':len(ORDER),
            'full_Japanese_MAIN_equal':True,'native_rounds':len(rows),
            'original_scope':counts,'canonical_Factory_credit':False}


def check(stage):
    path=ROOT/'.analysis/work'/(REPORT_FOLDER+stage)/'report.json'
    need(path.is_file() and not path.is_symlink(), 'retained sound source proof')
    report=json.loads(path.read_text())
    sources=expected_sources()
    includes=checked_includes()
    originals={k:v.read_bytes() for k,v in original_paths().items()}
    target=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    need(report['schema']==REPORT_SCHEMA and report['stage']==stage and
         report['source_sha256']=={k:sha(v) for k,v in sources.items()} and
         report.get('include_sha256',{})==includes and
         report['target_sha256']==sha(target) and
         report['original_objects_sha256']=={k:sha(v) for k,v in originals.items()} and
         len(report['rounds'])==2,'current sound source and target identities')
    rows=[check_round(stage,n,originals,sources,target) for n in (1,2)]
    need(rows==report['rounds'],'actual two-round pinned sound outputs')
    return summary(stage,rows)


def build(stage):
    parent.inputs()
    stage_dir=WORK/'probe'/stage
    logs=ROOT/'.analysis/work'/(REPORT_FOLDER+stage)
    need(not stage_dir.exists() and not logs.exists(), 'fresh native sound stage')
    sources=expected_sources()
    includes=checked_includes()
    originals={k:v.read_bytes() for k,v in original_paths().items()}
    need(all(b'\r' not in v for v in sources.values()),'maintained LF ASM sources')
    target=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    env=dict(os.environ, DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    cpu=str(min(os.sched_getaffinity(0)))
    command=['taskset','-c',cpu,'nice','-n','10','/usr/bin/wine-stable']
    tasm=str(prefix/'drive_c/TASM50/bin/TASM32.EXE')
    dos=str(ROOT/'_reference/ReC98/bin/msdos.exe')
    rows=[]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        stage_dir.mkdir(parents=True)
        logs.mkdir(parents=True)
        for n in (1,2):
            rd=stage_dir/f'r{n}'
            rd.mkdir()
            for owner,leaf in SOURCES.items():
                (rd/(leaf+'.asm')).write_bytes(sources[owner].replace(b'\n',b'\r\n'))
                rel=f'probe/{stage}/r{n}/{leaf}'
                argv=command+[tasm,'/m','/mx','/kh32768','/t','/dGAME=3',
                              (rel+'.asm').replace('/','\\'),
                              (rel+'.obj').replace('/','\\')]
                completed=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,timeout=120)
                (logs/f'r{n}-{owner}-TASM.log').write_bytes(completed.stdout)
                need(completed.returncode==0,'native original TASM failure '+owner)
            (stage_dir/f'r{n}.@l').write_bytes(response(stage,n))
            argv=command+[dos,'-e','-x','tlink',f'@probe\\{stage}\\r{n}.@l']
            completed=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,timeout=120)
            (logs/f'r{n}-TLINK.log').write_bytes(completed.stdout)
            need(completed.returncode==0,'native original TLINK failure')
            row=check_round(stage,n,originals,sources,target)
            rows.append(row)
            print('round',n,'native TASM source-owner CODE',
                  sum(x['CODE_bytes'] for x in row['original_scopes'].values()),
                  'whole Japanese MAIN link exact',flush=True)
        need(expected_sources()==sources,'source did not change during native rounds')
    report={'schema':REPORT_SCHEMA,'stage':stage,
            'source_sha256':{k:sha(v) for k,v in sources.items()},
            'include_sha256':includes,
            'original_objects_sha256':{k:sha(v) for k,v in originals.items()},
            'target_sha256':sha(target),'rounds':rows}
    (logs/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PROOF',str((logs/'report.json').relative_to(ROOT)),
          'SHA256',sha((logs/'report.json').read_bytes()))
    return summary(stage,rows)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
         'DOS-safe unique stage name')
    print(json.dumps(check(args.stage) if args.check else build(args.stage),sort_keys=True))
