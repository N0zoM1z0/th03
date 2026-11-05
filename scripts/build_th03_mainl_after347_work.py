#!/usr/bin/env python3
"""Reconstruct original Japanese Borland operator new / handler C++ boss:
754 CODE, 24 DATA (first 6 genuinely uninitialized), both native 6-byte
_INIT_/_EXIT_ records, 49 OMF fixups, and 389-source inherited CRT.
No full native cold replay."""
import argparse,fcntl,json,os,shutil,subprocess,tomllib
from pathlib import Path

import build_th03_mainl_after346_work as parent
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
DRIVER='scripts/build_th03_mainl_after347_work.py'
PREFIX='.analysis/work/mainl-after347-'
MODES={'new-operator-exception-boss':('new',)}
NATIVE={
    'new':dict(index=90,code=754,data=24,bss=0,fields=49,
        init_size=6,exit_size=6,implicit_data_sites=list(range(6)),
        segments=[('_TEXT','CODE',754),('_DATA','DATA',24),
                  ('_BSS','BSS',0),('_INIT_','INITDATA',6),('_EXIT_','EXITDATA',6)],
        publics=[(28,'@xnew_handler$qv'),
                 (135,'@set_new_handler$qnqv$v'),
                 (181,'@$bnew$qui')],
        data_publics=[(0,'___xalloc'),(6,'__new_handler')],
        imports=['@$bdele$qnv','@__RefDestructorCount$qv',
                 '@_ThrowException$qnvt1t1t1uiuiuinuc',
                 '___InitExceptBlocks','___ExitExceptBlocks','_malloc',
                 '@xmsg@$bctr$qmx4xmsg','@xmsg@$bdtr$qv',
                 '@xalloc@$bctr$qmx6stringui','@string@$bctr$qnxc',
                 '@string@$bdtr$qv'],
        group='0cff02ff03'),
}
TASM_FLAGS=['/m','/mx','/kh32768','/t']


def original_library_member(member):
    """Read the original CL.LIB member as OMF without rewriting its program.

    A valid empty THEADR is only a parser envelope: library members have no
    standalone THEADR and object_program_records deliberately excludes it.
    The original record sequence, including its non-semantic COMENTs, is
    borrowed unchanged from the pinned original library.
    """
    return b'\x80\x02\x00\x00\x7e' + member.program_records


def fixed_fields(blob):
    # No frame coercion: genuine frame details remain visible as an open gap.
    # For link-equivalent near externs TASM uses CODE frame while the original
    # BCC object uses target frame. Only the site/target comparison ignores it.
    keys=('segment','site','location_type','width','segment_relative',
          'frame_method','frame','target_method','target','addend')
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
    """Revalidate unchanged 62→389 native source-bound evidence, then extend it.

    Reads actual parent OBJ/LIB/EXE/MAP rounds; never launches cold replay.
    """
    base,files,accepted,members,previous,parent_hash=parent.retained()
    mode='mbcs-classification-leaves'
    raw=(ROOT/(parent.PREFIX+mode+'-build.json')).read_bytes()
    record=json.loads(raw)
    names=parent.MODES[mode]
    source_paths={n:'src/mainl/crt/'+n+'.asm' for n in names}
    need(record['complete'] and not record['source_acceptance'] and
         not record['original_cold_rebuilt'] and
         record['added_accepted_bytes']==0 and
         record['parent_receipt_sha256']==parent_hash and
         record['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         record['accepted_library_sha256']==sha(accepted) and
         record['source_paths']==source_paths and
         record['source_sha256']=={n:sha((ROOT/path).read_bytes())
                                  for n,path in source_paths.items()} and
         record['assembler_flags']==parent.TASM_FLAGS and
         tuple(record['names'])==names and record['mode']==mode and
         len(record['rounds'])==2,
         'native parent 389-source build bound to unchanged source')
    expected={n:parent.scope(n,parent.original_library_member(
        members[parent.NATIVE[n]['index']])) for n in names}
    need(record['original_profiles']==json.loads(json.dumps(expected)),
         'complete inherited original member scope')
    carry=[]
    vectors=[]
    for i,row in enumerate(record['rounds']):
        need(row['round']==i+1 and
             set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete round vector with all new native member programs')
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'original retained OBJ/LIB/EXE/MAP bytes '+kind)
            out[kind]=blob
        need(all(parent.scope(n,out[n])==expected[n] for n in names),
             'selected original inherited CODE/DATA/FIXUPP sites and targets')
        src=dict(previous[i][0],**{n:out[n] for n in names})
        comparison=compare_members(members,library_members(out['lib']),src)
        need(comparison==row['library_comparison'] and len(src)==389 and
             comparison['contextual_members_unchanged']==504 and
             out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             '389 original-source members and complete Japanese link parity')
        carry.append((src,out['lib']))
        vectors.append(out)
    need(vectors[0]==vectors[1] and carry[0][0]==carry[1][0],
         'unchanged byte-identical two-round 389-source carrier')
    return base,files,accepted,members,carry,sha(raw)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,carry,parent_hash=retained()
    need(not set(names)&set(carry[0][0]), 'newly selected native CRT slots only')
    need(all(members[NATIVE[n]['index']].name==n for n in names),
         'correct original member indices')
    originals={n:original_library_member(members[NATIVE[n]['index']]) for n in names}
    need(all(object_program_records(originals[n])==
             members[NATIVE[n]['index']].program_records for n in names),
         'original Japanese library program records, not alternate OBJ')
    # Verify the standalone Japanese vendor OBJs against the actual pinned
    # CL.LIB members on all literal CODE/data/public/import/fixup fields.
    # Unlike the preceding fbrk slot, this MBCS family does not have the
    # independent EXTDEF/GROUP/frame discrepancy.
    need(all(scope(n,(WORK/'vendor'/(n+'.obj')).read_bytes())==
             scope(n,originals[n]) for n in names),
         'MBCS vendor programs agree with original CL.LIB full frame semantics')
    expected={n:scope(n,originals[n]) for n in names}
    inputs={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    player=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    scratch=WORK/'probe/after347'
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
        dest=f'.analysis/work/after347-{mode}-{label}.log'
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
            response=build.response(r'probe\after347\newcrt.lib /E',
                ['+probe\\after347\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\after347\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\after347\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\after347\\newcrt.lib')):
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
                original_programs={}
                for n in names:
                    run(dos+TASM_FLAGS+[n+'.asm',n+'.obj'],scratch,
                        f'round{idx}-assemble-{n}')
                    obj=(scratch/(n+'.obj')).read_bytes()
                    need(scope(n,obj)==expected[n],
                         'all original CODE/DATA bytes, public interface, targets '+n)
                    literal_omf[n]=(literal_fields(obj)==literal_fields(originals[n]))
                    original_programs[n]=(object_program_records(obj)==
                        members[NATIVE[n]['index']].program_records)
                    compiled[n]=obj
                all_sources=dict(carry[idx-1][0],**compiled)
                for n,b in carry[idx-1][0].items():
                    (scratch/(n+'.obj')).write_bytes(b)
                run(player+['tlib',r'@probe\after347\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\after347\link.lnk'],WORK,
                    f'round{idx}-link')
                need((scratch/'linked.exe').read_bytes()==
                       (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                       (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete original Japanese MAINL EXE and MAP raw identical')
                out={}
                for kind,file in [(n,n+'.obj') for n in names]+[
                        ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]:
                    blob=(scratch/file).read_bytes()
                    path=f'.analysis/work/after347-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                    literal_omf_fixupp_equal_by_member=literal_omf,
                    original_program_equal_by_member=original_programs,
                    library_comparison=comparison))
                save()
                print(f'after347 {mode}: {len(all_sources)} source CRT members, '
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
