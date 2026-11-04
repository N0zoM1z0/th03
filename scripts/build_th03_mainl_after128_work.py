#!/usr/bin/env python3
"""Recover complete PC-98 extended serial driver with ten hardware APIs
on the proven 128-source Japanese MAINL CRT, without full cold replay.

This validates *all* CODE/DATA bytes, fixup sites and targets, unchanged CRT
membership and the complete native linked EXE/MAP. It explicitly does not
normalize or claim original literal OMF FIXUPP order/frame equality.
"""
import argparse,fcntl,json,os,shutil,subprocess,tomllib
from pathlib import Path

import build_th03_mainl_after119_work as parent
from review_th03_mainl_after119_work import review as review_parent
import build_th03_mainl_work as build
import build_th03_mainl_xx_work as xx
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_after128_work.py'
PREFIX='.analysis/work/mainl-after128-'
LAST='far-memory-leaves'
MODES={
    'pc98comx':('pc98comx',),
}
NATIVE={
    'pc98comx':dict(index=495,code=1383,data=35,bss=70,fields=58,
        publics=[(672,'_pc98cominitx'),(951,'_pc98comtermx'),
                 (1021,'_pc98comsendx'),(1043,'_pc98comrecvx'),
                 (1068,'_pc98comgetstatx'),(1104,'_pc98comsetstatx'),
                 (1126,'_pc98comchkbufx'),(1165,'_pc98comsendbreakx'),
                 (1202,'_pc98comresetx'),(1268,'_pc98comcheckbaudx')],
        imports=['_getvect','_setvect','___nec_delay','N_SCOPY@'],
        group='08ff03ff02'),
}
TASM_FLAGS=['/m','/mx','/kh32768','/t']

def fixed_fields(blob):
    # No frame coercion: genuine frame details remain visible as an open gap.
    # For link-equivalent near externs TASM uses CODE frame while the original
    # BCC object uses target frame. Only the site/target comparison ignores it.
    keys=('segment','site','location_type','width','segment_relative',
          'target_method','target','addend')
    return sorted(tuple(f[k] for k in keys) for f in literal_fields(blob))


def scope(name,blob):
    q=NATIVE[name]
    need(describe_omf(blob)['valid'],'actual native OMF '+name)
    expected_segments=q.get('segments',[('_TEXT','CODE',q['code']),
        ('_DATA','DATA',q['data']),
        (q.get('third_name','_BSS'),q.get('third_class','BSS'),q['bss'])])
    if 'segments' not in q:
        if q.get('init_size') is not None:
            expected_segments.append(('_INIT_','INITDATA',q['init_size']))
        if q.get('exit_size') is not None:
            expected_segments.append(('_EXIT_','EXITDATA',q['exit_size']))
    need([(r['name'],r['class'],r['size']) for r in segment_definitions(blob)]==
         expected_segments,
         'complete original segment sizes '+name)
    need(code_publics(blob,1)==q['publics'] and externs(blob)==q['imports'],
         'complete native public/extern interface '+name)
    need([x.data.hex() for x in parse_omf(blob) if x.name=='GRPDEF']==
         [q.get('group','08ff02ff03')], 'original group layout '+name)
    need(code_publics(blob,2)==q.get('data_publics',[]) and
         code_publics(blob,3)==q.get('bss_publics',[]),
         'complete selected native DATA/BSS public ABI '+name)
    need(len(literal_fields(blob))==q['fields'],
         'entire source relocation field population '+name)
    p=payload(blob)
    missing_code=[i for i in range(q['code']) if (1,i) not in p]
    missing_data=[i for i in range(q['data']) if (2,i) not in p]
    need(missing_code==q.get('implicit_code_sites',[]) and
         missing_data==q.get('implicit_data_sites',[]),
         'actual original materialized CODE/DATA coverage '+name)
    c=bytes(p.get((1,i),0) for i in range(q['code']))
    d=bytes(p.get((2,i),0) for i in range(q['data']))
    initdata=bytes(p[4,i] for i in range(q.get('init_size',0)))
    exit_index=5 if q.get('init_size') is not None else 4
    exitdata=bytes(p[exit_index,i] for i in range(q.get('exit_size',0)))
    return dict(CODE_sha256=sha(c),CODE_bytes=len(c),
                CODE_implicit_sites=missing_code,DATA_implicit_sites=missing_data,
                DATA_sha256=sha(d),
                DATA_bytes=len(d),BSS_bytes=q['bss'],
                INITDATA_bytes=len(initdata),INITDATA_sha256=sha(initdata),
                EXITDATA_bytes=len(exitdata),EXITDATA_sha256=sha(exitdata),
                publics=code_publics(blob,1),
                data_publics=code_publics(blob,2),
                bss_publics=code_publics(blob,3),imports=externs(blob),
                relocation_sites_targets=fixed_fields(blob))


def retained():
    # Inherit and review the two unchanged source-bound 128-source Japanese
    # member vectors. No prior source or original cold product is rebuilt.
    base,files,accepted,members,original119,_=parent.retained()
    checked=review_parent(LAST)
    need(checked['complete'] and checked['native_source_members']==128 and
         checked['complete_native_link_EXE_MAP_equal'],
         'source-bound original Japanese 128-source parent review')
    raw=(ROOT/(parent.PREFIX+LAST+'-build.json')).read_bytes()
    receipt=json.loads(raw)
    names=parent.MODES[LAST]
    need(receipt['complete'] and not receipt['source_acceptance'] and
         not receipt['original_cold_rebuilt'] and
         receipt['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         receipt['accepted_library_sha256']==sha(accepted) and
         tuple(receipt['names'])==names and len(receipt['rounds'])==2,
         'current source-bound original 128-source parent receipt')
    carrier=[]
    for i,row in enumerate(receipt['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'unaltered original 128-source '+kind+' vector')
            out[kind]=blob
        source=dict(original119[i][0],**{n:out[n] for n in names})
        need(len(source)==128 and
             compare_members(members,library_members(out['lib']),source)
                ['contextual_members_unchanged']==765 and
             out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese 128-source selected CRT and EXE/MAP')
        carrier.append((source,out['lib']))
    need(carrier[0][0]==carrier[1][0],
         'two identical independent 128-source original native objects')
    return base,files,accepted,members,carrier,sha(raw)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,carry,parent_hash=retained()
    need(not set(names)&set(carry[0][0]), 'newly selected native CRT slots only')
    need(all(members[NATIVE[n]['index']].name==n for n in names),
         'correct original member indices')
    originals={n:(WORK/'vendor'/(n+'.obj')).read_bytes() for n in names}
    need(all(object_program_records(originals[n])==
             members[NATIVE[n]['index']].program_records for n in names),
         'selected original vendor members, not alternate unused OBJ')
    expected={n:scope(n,originals[n]) for n in names}
    inputs={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    player=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    scratch=WORK/'probe/after128'
    report=dict(complete=False,mode=mode,names=list(names),
                source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,parent_receipt_sha256=parent_hash,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                source_sha256={n:sha(x) for n,x in inputs.items()},
                source_paths={n:'src/mainl/crt/'+n+'.asm' for n in names},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                assembler_flags=TASM_FLAGS,original_profiles=expected,
                literal_OMF_FIXUPP_equal=False,phases=[],rounds=[])
    save=lambda:(ROOT/(PREFIX+mode+'-build.json')).write_text(json.dumps(report,indent=2)+'\n')
    def run(argv,cwd,label):
        cp=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        dest=f'.analysis/work/after128-{mode}-{label}.log'
        (ROOT/dest).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,returncode=cp.returncode,
               command=argv,log_path=dest,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-2400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not scratch.exists(), 'fresh incremental scoped native workdir')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(carry[0][1])
            (scratch/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(player+['tlib','@extract.rsp'],scratch,'extract')
            extracted={f.stem.lower():f for f in scratch.iterdir()
                       if f.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all 893 inherited native CRT member programs extracted')
            old=library_members(carry[0][1])
            for m in old:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'native inherited member intact '+m.name)
                dest=scratch/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            for n,b in inputs.items():
                (scratch/(n+'.asm')).write_bytes(b)
                os.utime(scratch/(n+'.asm'),(946684800,946684800))
            (scratch/'stdio_layout.inc').write_bytes(
                (ROOT/'src/mainl/crt/stdio_layout.inc').read_bytes())
            response=build.response(r'probe\after128\newcrt.lib /E',
                ['+probe\\after128\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\after128\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\after128\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\after128\\newcrt.lib')):
                need(link.count(old)==1,'native MAINL link response binding')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(response)
            (scratch/'link.lnk').write_bytes(link)
            for idx in (1,2):
                for name in [*(n+'.obj' for n in names),'newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map']:
                    (scratch/name).unlink(missing_ok=True)
                compiled={}
                literal_omf={}
                for n in names:
                    run(dos+TASM_FLAGS+[n+'.asm',n+'.obj'],scratch,
                        f'round{idx}-assemble-{n}')
                    obj=(scratch/(n+'.obj')).read_bytes()
                    need(scope(n,obj)==expected[n],
                         'all original CODE/DATA bytes, public interface, targets '+n)
                    literal_omf[n]=(literal_fields(obj)==literal_fields(originals[n]))
                    compiled[n]=obj
                all_sources=dict(carry[idx-1][0],**compiled)
                for n,b in carry[idx-1][0].items():
                    (scratch/(n+'.obj')).write_bytes(b)
                run(player+['tlib',r'@probe\after128\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\after128\link.lnk'],WORK,
                    f'round{idx}-link')
                need((scratch/'linked.exe').read_bytes()==
                       (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                       (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete decoded Japanese MAINL EXE/MAP raw identical')
                out={}
                for kind,file in [(n,n+'.obj') for n in names]+[
                        ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]:
                    blob=(scratch/file).read_bytes()
                    path=f'.analysis/work/after128-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                    literal_omf_fixupp_equal_by_member=literal_omf,
                    library_comparison=comparison))
                save()
                print(f'after128 {mode}: {len(all_sources)} source CRT members, '
                      f'Japanese EXE/MAP exact round {idx}',flush=True)
            need(len(report['rounds'])==2 and
                 {n:q['sha256'] for n,q in report['rounds'][0]['outputs'].items()}==
                 {n:q['sha256'] for n,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical independent native output rounds')
        finally:
            shutil.rmtree(scratch)
    need(inputs=={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names},
         'source unchanged during producer rounds')
    report['literal_OMF_FIXUPP_equal']=all(
        report['rounds'][0]['literal_omf_fixupp_equal_by_member'].values())
    report['complete']=True
    save()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(MODES))
    main(ap.parse_args().mode)
