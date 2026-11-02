#!/usr/bin/env python3
"""Recover real DOS CRT memory/string members with isolated cumulative native links.

Use the unchanged MAINL cold pair and accepted 28-source library, extract
all 893 native members, replace only the selected source CRT members, then
link the actual Japanese MAINL twice. No full cold or DIET replay.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
import build_th03_mainl_xx_work as baseline_provider
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import describe_omf, parse_omf
from lib.borland_library import library_members, compare_members, object_program_records
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT = Path(__file__).resolve().parents[1]
WORK = build.WORK
DRIVER = 'scripts/build_th03_mainl_crt_growth_work.py'
CORE = ('memcmp', 'memcpy', 'strcmp')
# Available original member slots and complete actual code lengths. Do not
# assume a library's alphabetic layout or change its original program order.
KNOWN = {'memchr': (259, 37), 'memcmp': (260, 40),
         'memcpy': (261, 36), 'memset': (263, 72),
         'strchr': (291, 63), 'strcmp': (292, 48),
         'strlen': (300, 33)}
MODES = {'memchr': ('memchr',),
         'memchr-memset': ('memchr', 'memset'),
         'memchr-memset-strlen': ('memchr', 'memset', 'strlen'),
         'memchr-memset-strlen-strchr': ('memchr', 'memset', 'strlen', 'strchr')}
PREFIX = '.analysis/work/mainl-crt-growth-'


def source_names(mode):
    need(mode in MODES, 'supported exact source-only variant')
    return tuple(sorted(set(CORE + MODES[mode]), key=lambda n: KNOWN[n][0]))


def original_scope(name, raw):
    """Exact emitted code and OMF geometry, not module-name/header comments."""
    index, size = KNOWN[name]
    need(describe_omf(raw)['valid'], 'valid native OMF '+name)
    segs = segment_definitions(raw)
    need([(q['name'], q['class'], q['size']) for q in segs] ==
         [('_TEXT', 'CODE', size), ('_DATA', 'DATA', 0),
          ('_BSS', 'BSS', 0)], 'original native CRT geometry '+name)
    refs = literal_fields(raw)
    need(not externs(raw) and refs == [], 'no original source import/relocation '+name)
    group = [rec.data.hex() for rec in parse_omf(raw) if rec.name == 'GRPDEF']
    need(group == ['08ff03ff02'], 'literal BSS-before-DATA group '+name)
    pub = code_publics(raw, 1)
    expect = [(0, '_setmem'), (38, '_memset')] if name == 'memset' else [(0, '_'+name)]
    need(pub == expect, 'exact original public entry/offset and near/far ABI '+name)
    p = payload(raw)
    code = bytes(p[1, pos] for pos in range(size))
    return dict(name=name, member_index=index, CODE_bytes=size,
                CODE_sha256=sha(code), CODE_hex=code.hex(),
                group_record=group, public_entries=pub, external_imports=[],
                literal_fields=[])


def link_response(files):
    raw = baseline_provider.link_response(files)
    for old, new in (
        (b'probe\\xxwhole\\xxfull.exe', b'probe\\crtinc\\linked.exe'),
        (b'probe\\xxwhole\\xxfull.map', b'probe\\crtinc\\linked.map'),
        (b'probe\\xxwhole\\xxcrt.lib', b'probe\\crtinc\\newcrt.lib'),
    ):
        need(raw.count(old) == 1, 'single normal MAINL link position')
        raw = raw.replace(old, new)
    return raw


def run_native(mode):
    names=source_names(mode)
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base, files, library, members, _=baseline_provider.baseline(ROOT)
    need(len(members)==893 and all(members[KNOWN[n][0]].name==n for n in names),
         'complete original 893-member native CRT order')
    vendor={n:(WORK/'vendor'/f'{n}.obj').read_bytes() for n in names}
    profiles={n:original_scope(n,vendor[n]) for n in names}
    need(all(object_program_records(vendor[n])==
             members[KNOWN[n][0]].program_records for n in names),
         'original member program record identity')
    sources={n:(ROOT/f'src/mainl/crt/{n}.asm').read_bytes() for n in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
             WINEPREFIX=str(prefix), MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC', LANG='C', LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    scratch=WORK/'probe/crtinc'
    report_path=ROOT/(PREFIX+mode+'-build.json')
    r=dict(complete=False, original_cold_rebuilt=False, source_acceptance=False,
           added_accepted_bytes=0, mode=mode, names=names,
           accepted_baseline=base, accepted_library_sha256=sha(library),
           source_sha256={n:sha(raw) for n,raw in sources.items()},
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           original_native_scope=profiles, phases=[], rounds=[])
    save=lambda:report_path.write_text(json.dumps(r,indent=2)+'\n')
    def execute(args,cwd,label):
        cp=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/crt-growth-{mode}-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=args,returncode=cp.returncode,
                                log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not scratch.exists(),'fresh isolated native CRT source scratch')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(library)
            (scratch/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            execute(dos+['tlib','@extract.rsp'],scratch,'extract')
            extracted={p.stem.casefold():p for p in scratch.iterdir()
                       if p.suffix.casefold()=='.obj'}
            need(set(extracted)=={m.name.casefold() for m in members},
                 'all893 original TLIB members extracted')
            for m in members:
                found=extracted[m.name.casefold()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'actual untouched member '+m.name)
                dest=scratch/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            for n,raw in sources.items():
                (scratch/(n+'.asm')).write_bytes(raw)
                os.utime(scratch/(n+'.asm'),(946684800,946684800))
            rsp=build.response(r'probe\crtinc\newcrt.lib /E',
                 ['+probe\\crtinc\\'+m.name+'.obj' for m in members])
            (scratch/'library.rsp').write_bytes(rsp)
            (scratch/'link.lnk').write_bytes(link_response(files))
            (ROOT/f'.analysis/work/crt-growth-{mode}-library.rsp').write_bytes(rsp)
            (ROOT/f'.analysis/work/crt-growth-{mode}-link.lnk').write_bytes(link_response(files))
            for round_no in (1,2):
                for fname in [*(n+'.obj' for n in names),'newcrt.lib',
                              'newcrt.bak','linked.exe','linked.map']:
                    (scratch/fname).unlink(missing_ok=True)
                source_objs={}
                for n in names:
                    execute(tasm+['/m','/mx','/kh32768','/t',n+'.asm',n+'.obj'],
                            scratch,f'round{round_no}-assemble-{n}')
                    raw=(scratch/(n+'.obj')).read_bytes()
                    need(original_scope(n,raw)==profiles[n],
                         'whole source code/public/group/fixup equality '+n)
                    source_objs[n]=raw
                execute(dos+['tlib',r'@probe\crtinc\library.rsp'],
                        WORK,f'round{round_no}-library')
                result_lib=(scratch/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(result_lib),source_objs)
                expected=sorted(names,key=lambda n:KNOWN[n][0])
                need(compared['replaced_members']==expected and
                     compared['contextual_members_unchanged']==893-len(names),
                     'original slot replacement and every other program unchanged')
                execute(dos+['tlink',r'@probe\crtinc\link.lnk'],
                        WORK,f'round{round_no}-link')
                outputs={}
                for k,filename in ([(n,n+'.obj') for n in names]+[
                    ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]):
                    raw=(scratch/filename).read_bytes()
                    out=f'.analysis/work/crt-growth-{mode}-round{round_no}-{filename}'
                    (ROOT/out).write_bytes(raw)
                    outputs[k]=dict(path=out,bytes=len(raw),sha256=sha(raw))
                need((scratch/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'actual full decoded Japanese EXE and MAP remain raw equal')
                r['rounds'].append(dict(round=round_no,outputs=outputs,
                                        library_comparison=compared))
                save()
                print('Native CRT',','.join(names),'EXE/MAP exact round',round_no,flush=True)
            need(len(r['rounds'])==2 and
                 {k:q['sha256'] for k,q in r['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in r['rounds'][1]['outputs'].items()},
                 'two complete deterministic native raw output vectors')
        finally:
            shutil.rmtree(scratch)
    later,_,new_library,new_members,_=baseline_provider.baseline(ROOT)
    need(later==base and new_library==library and
         [m.program_records for m in members]==[m.program_records for m in new_members] and
         {n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes()) for n in names}==
         r['source_sha256'],'accepted baseline/source unchanged')
    r['complete']=True
    save()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=tuple(MODES))
    run_native(parser.parse_args().mode)
