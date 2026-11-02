#!/usr/bin/env python3
"""Original DOS stream input sources atop complete 36-source stat CRT.

Compile only requested native 8086 source objects and their actual
normal MAINL TLIB/TLINK outputs. Reuse pinned original cold and original
893-member library; never hide existing fopen/fclose native OMF gaps.
"""
import argparse,fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_tzset_work as previous
import build_th03_mainl_strset_work as bcc
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
DRIVER='scripts/build_th03_mainl_posttzset_work.py'
PREFIX='.analysis/work/mainl-posttzset-'
MODES={
    'lsearch':('lsearch',),
    'lsearch-getenv':('lsearch','getenv'),
}
NATIVE={
    'lsearch':dict(index=247,size=202,data=0,
                   publics=[(117,'_lsearch'),(160,'_lfind')],
                   exts=['_movmem'],group='08ff02ff03',fields=1,kind='asm'),
    'getenv':dict(index=240,size=112,data=0,
                  publics=[(0,'_getenv')],exts=['__environ'],
                  group='08ff03ff02',fields=1,kind='asm'),
}

TASM_FLAGS=['/m','/mx','/kh32768','/t']
BCC_FLAGS=bcc.BCC_FLAGS
def source_path(name):
    return 'src/mainl/crt/'+name+'.'+NATIVE[name]['kind']



def scope(name,raw):
    q=NATIVE[name]
    need(describe_omf(raw)['valid'],'actual original OMF object '+name)
    need([(x['name'],x['class'],x['size']) for x in segment_definitions(raw)]==
         [('_TEXT','CODE',q['size']),('_DATA','DATA',q['data']),('_BSS','BSS',0)],
         'whole original CODE and genuine initialized DATA extent '+name)
    need(code_publics(raw,1)==q['publics'] and externs(raw)==q['exts'],
         'original public/EXTDEF and proper ABI '+name)
    need([x.data.hex() for x in parse_omf(raw) if x.name=='GRPDEF']==[q['group']],
         'original literal Borland GRPDEF '+name)
    f=literal_fields(raw)
    need(len(f)==q['fields'],'full literal ordered OMF fields '+name)
    a=payload(raw)
    code=bytes(a[1,i] for i in range(q['size']))
    data=bytes(a[2,i] for i in range(q['data']))
    if name=='perror':
        need(data==bytes.fromhex('556e6b6e6f776e206572726f72003a20000a00'),
             'original unknown error/prefix/newline initialized DATA')
    return dict(CODE_bytes=q['size'],CODE_sha256=sha(code),
                DATA_bytes=q['data'],DATA_sha256=sha(data),
                ordered_fields=f,public=code_publics(raw,1),
                imports=externs(raw),group=q['group'])


def retained():
    base,files,accepted,members,original57,parenthash=previous.retained()
    original_report=(ROOT/previous.REPORT).read_bytes()
    rec=json.loads(original_report)
    need(rec['complete'] and not rec['source_acceptance'] and
         rec['added_accepted_bytes']==0 and not rec['original_cold_rebuilt'] and
         rec['original_tzset_literal_OMF_exact'] and
         rec['accepted_baseline']==base and
         rec['accepted_library_sha256']==sha(accepted) and
         rec['previous_fifty_seven_source_build_sha256']==parenthash and
         rec['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         rec['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         len(rec['rounds'])==2,
         'current 58-source original native tzset with four real segments/48 fields')
    objpairs=[]
    for index,row in enumerate(rec['rounds']):
        out={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'previous real complete 58-source tzset '+kind+' bytes')
            out[kind]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded 58-source EXE/MAP identity')
        sources=dict(original57[index],tzset=out['obj'])
        compared=compare_members(members,library_members(out['lib']),sources)
        need(compared['replaced_members']==sorted(sources) and
             compared['contextual_members_unchanged']==835,
             '58 actual source CRT member positions,835 original vendor programs')
        objpairs.append(sources)
    need(len(objpairs)==2 and objpairs[0]==objpairs[1] and
         len(objpairs[0])==58 and len(members)==893,
         'two real source-bound 58-CRT original object vectors')
    return base,files,accepted,members,objpairs,sha(original_report)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,previous_sources,parenthash=retained()
    need(not set(names)&set(previous_sources[0]),
         'refuse to overwrite a previously reconstructed native source member')
    need(all(members[NATIVE[name]['index']].name==name for name in names),
         'original named member slots for scoped source extension')
    originals={name:(WORK/'vendor'/(name+'.obj')).read_bytes() for name in names}
    expected={name:scope(name,blob) for name,blob in originals.items()}
    need(all(object_program_records(originals[name])==
             members[NATIVE[name]['index']].program_records for name in names),
         'entire original vendor CRT member program identities')
    inputs={name:(ROOT/source_path(name)).read_bytes() for name in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    scratch=WORK/'probe/posttzset'
    report=dict(complete=False,mode=mode,names=names,
                source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                parent_fopen_OMF_order_open=True,parent_fclose_near_frame_open=True,
                parent_timecvt_near_frame_open=True,
                parent_strftime_near_frame_open=True,
                parent_tempnam_near_frame_open=True,
                parent_tzset_full_OMF_exact=True,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_fifty_eight_source_build_sha256=parenthash,
                original_profiles=expected,
                source_sha256={name:sha(blob) for name,blob in inputs.items()},
                original_source_paths={name:source_path(name) for name in names},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,bcc_compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    report_path=ROOT/(PREFIX+mode+'-build.json')
    save=lambda:report_path.write_text(json.dumps(report,indent=2)+'\n')
    def run(command,cwd,label):
        c=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/posttzset-{mode}-{label}.log'
        (ROOT/path).write_bytes(c.stdout)
        report['phases'].append(dict(label=label,command=command,
                                     returncode=c.returncode,log_path=path,
                                     log_sha256=sha(c.stdout)))
        save()
        need(c.returncode==0,label+': '+c.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not scratch.exists(),'fresh isolated native CRT post-tzset source scratch')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(accepted)
            (scratch/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],scratch,'extract')
            extracted={f.stem.lower():f for f in scratch.iterdir() if f.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original native CRT objects extracted')
            for member in members:
                f=extracted[member.name.lower()]
                need(object_program_records(f.read_bytes())==member.program_records,
                     'unchanged original CRT member '+member.name)
                dest=scratch/(member.name+'.obj')
                if f!=dest:f.rename(dest)
            for name,src in inputs.items():
                file=scratch/(name+'.'+NATIVE[name]['kind'])
                file.write_bytes(src)
                os.utime(file,(946684800,946684800))
            library_rsp=build.response(r'probe\posttzset\newcrt.lib /E',
                ['+probe\\posttzset\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\posttzset\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\posttzset\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\posttzset\\newcrt.lib'),
            ):
                need(link.count(old)==1,'real normal Japanese MAINL TLINK target')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(library_rsp)
            (scratch/'link.lnk').write_bytes(link)
            (ROOT/f'.analysis/work/posttzset-{mode}-library.rsp').write_bytes(library_rsp)
            (ROOT/f'.analysis/work/posttzset-{mode}-link.lnk').write_bytes(link)
            for idx in (1,2):
                for file in [*(n+'.obj' for n in names),'newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map']:
                    (scratch/file).unlink(missing_ok=True)
                compiled={}
                for name in names:
                    if NATIVE[name]['kind']=='asm':
                        run(tasm+TASM_FLAGS+[name+'.asm',name+'.obj'],
                            scratch,f'round{idx}-assemble-{name}')
                    else:
                        run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,name+'.cpp'],
                            scratch,f'round{idx}-compile-{name}')
                    obj=(scratch/(name+'.obj')).read_bytes()
                    need(scope(name,obj)==expected[name] and
                         literal_fields(obj)==literal_fields(originals[name]),
                         'source-assembled original CODE, PUB, GROUP and literal ordered FIXUPPs '+name)
                    compiled[name]=obj
                sources=dict(previous_sources[idx-1],**compiled)
                for name,blob in previous_sources[idx-1].items():
                    (scratch/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\posttzset\library.rsp'],
                    WORK,f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==893-len(sources),
                     'all genuine source object positions, others unchanged')
                run(dos+['tlink',r'@probe\posttzset\link.lnk'],
                    WORK,f'round{idx}-link')
                out={}
                for kind,file in ([(name,name+'.obj') for name in names]+[
                    ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]):
                    data=(scratch/file).read_bytes()
                    path=f'.analysis/work/posttzset-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(data)
                    out[kind]=dict(path=path,bytes=len(data),sha256=sha(data))
                need((scratch/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese decoded MAINL EXE/MAP raw-equal')
                report['rounds'].append(dict(round=idx,outputs=out,library_comparison=comparison))
                save()
                print('Post-tzset native CRT',mode,'source members',len(sources),
                      'whole Japanese MAINL EXE/MAP exact round',idx,flush=True)
            need(len(report['rounds'])==2 and
                 {k:x['sha256'] for k,x in report['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in report['rounds'][1]['outputs'].items()},
                 'two whole deterministic TASM/TLIB/TLINK output vectors')
        finally:shutil.rmtree(scratch)
    again,_,origlib,_,_,afterhash=retained()
    need(again==base and origlib==accepted and afterhash==parenthash and
         inputs=={name:(ROOT/source_path(name)).read_bytes()
                   for name in names},
         'current source, retained original fixed CRT and cold pair unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(MODES))
    main(ap.parse_args().mode)
