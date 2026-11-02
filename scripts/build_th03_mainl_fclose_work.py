#!/usr/bin/env python3
"""Scoped 192-byte DOS fclose with a 35-source normal MAINL product link.

Original fclose CODE and 5 logical fields match; existing fopen
remains marked product-exact but original OMF order open. No cold replay.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_closeall_work as previous
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
SOURCE='src/mainl/crt/fclose.asm'
DRIVER='scripts/build_th03_mainl_fclose_work.py'
REPORT='.analysis/work/mainl-fclose-native-build.json'
ORIGINAL=WORK/'vendor/fclose.obj'
SCRATCH=WORK/'probe/fcls35'
TASM_FLAGS=['/m','/mx','/kh32768','/t','fclose.asm','fclose.obj']


def original_scope(blob):
    need(describe_omf(blob)['valid'],'valid original DOS fclose OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(blob)]==
         [('_TEXT','CODE',192),('_DATA','DATA',0),('_BSS','BSS',0)],
         'complete 192 original CODE bytes, real empty DATA/BSS')
    need(code_publics(blob,1)==[(0,'_fclose')] and
         externs(blob)==['_fflush','_unlink','_free','_close','__MKNAME'],
         'one far fclose public and five real DOS runtime imports')
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA-before-BSS group')
    fields=literal_fields(blob)
    need([f['site'] for f in fields]==[168,163,112,89,60],
         'original five chronological descending native FIXUPP fields')
    need(all(f['frame_method']==5 for f in fields if f['site']!=163) and
         fields[1]['target_method']==2 and fields[1]['target']==5 and
         fields[1]['frame_method'] in (0,5),
         'four exact far TARGET frames, one genuine near __MKNAME frame variation')
    normalized=[dict(f,frame_method=5,frame=None) if f['site']==163 else f
                for f in fields]
    p=payload(blob)
    return dict(CODE_bytes=192,CODE_sha256=sha(bytes(p[1,i] for i in range(192))),
                logical_fields=normalized,imports=externs(blob),
                publics=code_publics(blob,1))


def retained():
    base,files,accepted,members,old33,parenthash=previous.retained()
    report_raw=(ROOT/previous.REPORT).read_bytes()
    report=json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and
         report['partial_parent_fopen_OMF_order_open'] is True and
         not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['previous_thirty_three_source_build_sha256']==parenthash and
         report['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         report['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(report['rounds'])==2,
         '34-source source-only fcloseall parent, fopen OMF remains open')
    pair=[]
    for index,row in enumerate(report['rounds']):
        output={}
        for kind,q in row['outputs'].items():
            raw=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete previous 34-source file '+kind)
            output[kind]=raw
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'actual whole original 34-source Japanese EXE/MAP')
        originals=dict(old33[index],closeall=output['obj'])
        cmp=compare_members(members,library_members(output['lib']),originals)
        need(cmp['replaced_members']==sorted(originals) and
             cmp['contextual_members_unchanged']==859,
             '34 original source library slots,859 untouched original members')
        pair.append(originals)
    need(pair[0]==pair[1] and len(pair[0])==34 and
         len(members)==893 and members[217].name=='fclose',
         'two whole original source pairs and original fclose index217')
    return base,files,accepted,members,pair,sha(report_raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,old,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[217].program_records,
         'original fclose CRT native member program identity')
    goal=original_scope(original)
    src=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,partial_parent_fopen_OMF_order_open=True,
                native_fclose_MKNAME_TARGET_frame_open=True,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_thirty_four_source_build_sha256=parenthash,
                original_sha256=sha(original),source_sha256=sha(src),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        r=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/fclose-{label}.log'
        (ROOT/where).write_bytes(r.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=r.returncode,
                                     log_path=where,log_sha256=sha(r.stdout)))
        save()
        need(r.returncode==0,label+': '+r.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated fclose original native scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all 893 original native CRT member files')
            for m in members:
                p=extracted[m.name.lower()]
                need(object_program_records(p.read_bytes())==m.program_records,
                     'unmodified original CRT member '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if p!=dest:p.rename(dest)
            (SCRATCH/'fclose.asm').write_bytes(src)
            os.utime(SCRATCH/'fclose.asm',(946684800,946684800))
            rsp=build.response(r'probe\fcls35\newcrt.lib /E',
                ['+probe\\fcls35\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for a,b in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fcls35\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fcls35\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fcls35\\newcrt.lib'),
            ):
                need(link.count(a)==1,'one real original MAINL linker output')
                link=link.replace(a,b)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fclose-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/fclose-link.lnk').write_bytes(link)
            for i in (1,2):
                for filename in ('fclose.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/filename).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'fclose.obj').read_bytes()
                need(original_scope(obj)==goal and
                     literal_fields(obj)!=literal_fields(original) and
                     literal_fields(obj)[1]['frame_method']==0 and
                     literal_fields(original)[1]['frame_method']==5,
                     'entire original192 CODE; one genuine near frame discrepancy remains open')
                owners=dict(old[i-1],fclose=obj)
                for n,blob in old[i-1].items():
                    (SCRATCH/(n+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\fcls35\library.rsp'],WORK,
                    f'round{i}-library')
                c=compare_members(members,library_members((SCRATCH/'newcrt.lib').read_bytes()),owners)
                need(c['replaced_members']==sorted(owners) and
                     c['contextual_members_unchanged']==858,
                     '35 real source modules and858 other vendor programs unchanged')
                run(dos+['tlink',r'@probe\fcls35\link.lnk'],WORK,
                    f'round{i}-link')
                out={}
                for kind,name in (('obj','fclose.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/fclose-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    out[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese MAINL EXE/MAP raw-exact with35 source owners')
                report['rounds'].append(dict(round=i,outputs=out,library_comparison=c))
                save()
                print('35-source original fclose Japanese MAINL product exact round',i,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two identical full native OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    after,_,originallib,_,_,afterhash=retained()
    need(after==base and originallib==accepted and afterhash==parenthash and
         src==(ROOT/SOURCE).read_bytes(),
         'original accepted source library and modified scope unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
