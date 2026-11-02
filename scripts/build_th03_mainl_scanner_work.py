#!/usr/bin/env python3
"""Full source TASM DOS scanner: 1282 CODE + 128 true ASCII-class DATA bytes.

Reuse the 22-source exact Japanese MAINL native working library. Assemble
only scanner with real TASM twice, replacing its original member at109,
then use genuine original TLIB/TLINK twice. No full cold or DIET replay.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_native_extension_work as parent
import build_th03_mainl_xx_work as xx
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
SOURCE='src/mainl/crt/scanner.asm'
DRIVER='scripts/build_th03_mainl_scanner_work.py'
REPORT='.analysis/work/mainl-scanner-native-build.json'
SCRATCH=WORK/'probe/scnfsrc'
ORIGINAL=WORK/'vendor/scanner.obj'
PRIOR_MODE='scantol-strspn-strcspn-strpbrk'
TASM_FLAGS=['/m','/mx','/kh32768','/t','scanner.asm','scanner.obj']


def original_scope(blob):
    need(describe_omf(blob)['valid'],'complete valid native original Borland scanner OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(blob)]==
         [('_TEXT','CODE',1282),('_DATA','DATA',128),('_BSS','BSS',0)],
         'actual 1282 CODE and genuine128-byte initialized ASCII format class DATA')
    need(code_publics(blob,1)==[(0,'__scanner')] and
         externs(blob)==['__scantod','__scantol','__scanpop','__scanrslt'],
         'original one private near scanner entry and four near runtime imports')
    need([rec.data.hex() for rec in parse_omf(blob) if rec.name=='GRPDEF']==
         ['08ff03ff02'],'original sixteenth-bit BSS-before-DATA segment group')
    fields=literal_fields(blob)
    need(len(fields)==33 and len([f for f in fields if 1238<=f['site']<1282])==22 and
         [q['site'] for q in fields[:4]]==[96,108,204,221] and
         fields[3]['frame_method']==5 and fields[3]['addend']==1238 and
         all(f['frame_method']==5 and f['target_method']==0 and
             f['target']==1 and f['width']==2 for f in fields[-22:]),
         'literal BCC chronological DATA references and22 real target-frame CODE switch words')
    p=payload(blob)
    native_CODE=bytes(p[1,i] for i in range(1282))
    native_DATA=bytes(p[2,i] for i in range(128))
    return dict(CODE_bytes=1282,CODE_sha256=sha(native_CODE),
                initialized_DATA_bytes=128,initialized_DATA_sha256=sha(native_DATA),
                literal_fields=fields,public=code_publics(blob,1),
                externals=externs(blob),group='08ff03ff02',
                jump_table_start=1238,jump_table_entries=22)


def retained():
    base,files,accepted,members,earlier,parenthash=parent.retained()
    report_file=ROOT/(parent.PREFIX+PRIOR_MODE+'-build.json')
    raw=report_file.read_bytes()
    r=json.loads(raw)
    names=parent.MODES[PRIOR_MODE]
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_eighteen_source_receipt_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes())
                              for n in names} and
         len(r['rounds'])==2,
         'complete original22-source exact native CRT and unchanged source input')
    all_source=[]
    for idx,row in enumerate(r['rounds']):
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete retained original22-source '+kind+' raw vector')
            outputs[kind]=data
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'original22-source native EXE/MAP exact and unchanged')
        objects=dict(earlier[idx],**{n:outputs[n] for n in names})
        compared=compare_members(members,library_members(outputs['lib']),objects)
        need(compared['replaced_members']==sorted(objects) and
             compared['contextual_members_unchanged']==871,
             '22 genuine original CRT source slots and871 other native programs')
        all_source.append(objects)
    need(all_source[0]==all_source[1] and len(all_source[0])==22 and
         len(members)==893 and members[109].name=='scanner',
         'two identical existing source pairs and actual scanner library slot109')
    return base,files,accepted,members,all_source,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[109].program_records,
         'unchanged genuine original scanner native program records')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=base,
                accepted_library_sha256=sha(accepted),
                prior_twenty_two_source_build_sha256=parenthash,
                original_sha256=sha(original),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(args,cwd,label):
        cp=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=130)
        where=f'.analysis/work/scanner-full-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=args,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as writer:
        fcntl.flock(writer,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated scanner native source tree')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={x.stem.lower():x for x in SCRATCH.iterdir()
                       if x.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 fixed original CRT members extracted')
            for m in members:
                found=extracted[m.name.lower()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'original actual member record '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            (SCRATCH/'scanner.asm').write_bytes(source)
            os.utime(SCRATCH/'scanner.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\scnfsrc\newcrt.lib /E',
                ['+probe\\scnfsrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\scnfsrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\scnfsrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\scnfsrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one true original native MAINL linker destination')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/scanner-full-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/scanner-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('scanner.obj','newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'scanner.obj').read_bytes()
                need(original_scope(obj)==goal,
                     'all original1282 CODE,128 literal DATA and33 ordered OMF fields')
                sources=dict(prior[i-1],scanner=obj)
                for name,data in prior[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(data)
                run(dos+['tlib',r'@probe\scnfsrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==870,
                     '23 exact original source modules and870 unchanged CRT programs')
                run(dos+['tlink',r'@probe\scnfsrc\link.lnk'],
                    WORK,f'round{i}-link')
                outs={}
                for kind,name in (('obj','scanner.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/scanner-full-round{i}-{name}'
                    (ROOT/where).write_bytes(blob)
                    outs[kind]=dict(path=where,bytes=len(blob),sha256=sha(blob))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'actual entire Japanese decoded MAINL EXE/MAP exact with23 natural sources')
                report['rounds'].append(dict(round=i,outputs=outs,
                                             library_comparison=compared))
                save()
                print('23 original CRT sources incl. scanner+scantol EXE/MAP exact round',i,
                      flush=True)
            need({k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two complete same raw TASM/TLIB/TLINK output vectors')
        finally:shutil.rmtree(SCRATCH)
    b,_,lib,_,_,newhash=retained()
    need(b==base and lib==accepted and newhash==parenthash and
         source==(ROOT/SOURCE).read_bytes(),
         'all original accepted and source evidence unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
