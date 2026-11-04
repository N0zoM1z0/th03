#!/usr/bin/env python3
"""Recover NEC PC-98 BIOS video initialization and CRT screen-line routines
on source-bound 261-source Japanese MAINL without historical cold replay.

This validates *all* CODE/DATA bytes, fixup sites and targets, unchanged CRT
membership and the complete native linked EXE/MAP. It explicitly does not
normalize or claim original literal OMF FIXUPP order/frame equality.
"""
import argparse,fcntl,json,os,shutil,subprocess,tomllib
from pathlib import Path

import build_th03_mainl_after261_work as parent
from review_th03_mainl_after261_work import review as review_parent
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
DRIVER='scripts/build_th03_mainl_after263_work.py'
PREFIX='.analysis/work/mainl-after263-'
LAST='nec-video-core'
MODES={'pc98-dos-small-leaves':('movedata','dosext','segread','lrotr','lrotl','swab','getswit','getverf','pc98crt','biosprin','bios_prn','pc98sfky','pc98mem','pc98gfky','dosvgadr','bioscom','bios_com','bdos','dosvuscr','cnecwhxy'),}
NATIVE={
    'movedata':dict(index=265,code=34,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',34),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_movedata')],imports=[],group='08ff03ff02'),
    'dosext':dict(index=215,code=34,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',34),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_dosexterr')],imports=[],group='08ff03ff02'),
    'segread':dict(index=111,code=34,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',34),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_segread')],imports=[],group='08ff03ff02'),
    'lrotr':dict(index=86,code=33,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',33),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__lrotr')],imports=[],group='08ff03ff02'),
    'lrotl':dict(index=85,code=32,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',32),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__lrotl')],imports=[],group='08ff03ff02'),
    'swab':dict(index=317,code=31,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',31),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_swab')],imports=[],group='08ff03ff02'),
    'getswit':dict(index=63,code=31,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',31),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__getswitchar'), (14, '__setswitchar')],imports=[],group='08ff02ff03'),
    'getverf':dict(index=65,code=28,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',28),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_getverify'), (12, '_setverify')],imports=[],group='08ff03ff02'),
    'pc98crt':dict(index=496,code=27,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',27),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_pc98crt')],imports=[],group='08ff03ff02'),
    'biosprin':dict(index=481,code=24,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',24),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__ibmpc_biosprint')],imports=[],group='08ff03ff02'),
    'bios_prn':dict(index=476,code=24,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',24),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__ibmpc_bios_printer')],imports=[],group='08ff03ff02'),
    'pc98sfky':dict(index=507,code=21,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',21),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_pc98setfkey')],imports=[],group='08ff03ff02'),
    'pc98mem':dict(index=503,code=21,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',21),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_pc98mem')],imports=[],group='08ff03ff02'),
    'pc98gfky':dict(index=500,code=21,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',21),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_pc98getfkey')],imports=[],group='08ff03ff02'),
    'dosvgadr':dict(index=482,code=21,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',21),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_dosvgetvideoaddr')],imports=[],group='08ff03ff02'),
    'bioscom':dict(index=477,code=20,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',20),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__ibmpc_bioscom')],imports=[],group='08ff03ff02'),
    'bios_com':dict(index=472,code=20,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',20),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__ibmpc_bios_serialcom')],imports=[],group='08ff03ff02'),
    'bdos':dict(index=197,code=20,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',20),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_bdos')],imports=[],group='08ff03ff02'),
    'dosvuscr':dict(index=492,code=19,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',19),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '_dosvupdatescreen')],imports=[],group='08ff03ff02'),
    'cnecwhxy':dict(index=549,code=18,data=0,bss=0,fields=0,
      segments=[('_TEXT','CODE',18),('_DATA','DATA',0),('_BSS','BSS',0)],
      publics=[(0, '__NEC_WHEREXY')],imports=[],group='08ff03ff02'),
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
    """Validate the complete 62→263 receipt DAG once, in topological order.

    A naive `parent.retained(); review_parent(...)` duplicates ancestor
    validation exponentially at depth 7 and eventually times out. Reuse
    source-bound raw receipts, comparing every intermediate member program
    and original linked EXE/MAP, without rerunning a historical cold build.
    """
    import importlib
    first=importlib.import_module('build_th03_mainl_after62_work')
    base,files,accepted,members,original62,parent_hash=first.retained()
    need(len(original62)==2 and len(original62[0][0])==62 and
         original62[0][0]==original62[1][0],
         'source-bound 62-source original Japanese parent')
    carry=[(dict(src),None) for src,_ in original62]
    layers=(
        ('after62','sprintf-calloc-puts-ctime'),
        ('after66','strerror-bsearch-strdup-abort-atexit-strcpy-strcat'),
        ('after73','vprinter-collate-strxfrm-locale'),
        ('after77','strings-ctype-math'),
        ('after86','lstrftim'),
        ('after87','signal-fheapchk'),
        ('after89','utime-console'),
        ('after97','lsetlocl-wild-vappv'),
        ('after100','system-scanners'),
        ('after103','cputn'),
        ('after104','constrea'),
        ('after105','ioststd'),
        ('after106','scan-vectors-time'),
        ('after112','vector-family'),
        ('after116','istelng'),
        ('after117','pc98com'),
        ('after118','ostint'),
        ('after119','far-memory-leaves'),
        ('after128','pc98comx'),
        ('after129','ostoutst'),
        ('after130','cibmscrn'),
        ('after131','video-chain'),
        ('after133','cibmgptx'),
        ('after134','strstream-bosses'),
        ('after136','ostischr'),
        ('after137','streambuf-ios-leaves'),
        ('after149','constructors'),
        ('after151','strstream-constructors'),
        ('after153','strstream-destructors'),
        ('after155','far-string-algorithms'),
        ('after168','stsync'),
        ('after169','fstream-constructors'),
        ('after173','fstream-destructor'),
        ('after174','strstream-family'),
        ('after177','file-stream-methods'),
        ('after185','hardware-io-leaves'),
        ('after201','istrstream-more-constructors'),
        ('after202','filebuf-constructors'),
        ('after204','ifstream-lifecycle'),
        ('after209','ofstream-lifecycle'),
        ('after214','jis-multibyte-leaves'),
        ('after232','bios-dos-core-leaves'),
        ('after252','fstreambase-constructors'),
        ('after256','strstreambase-constructors'),
        ('after258','ostrstream-constructor'),
        ('after259','nec-screen-text'),
        ('after260','nec-textmode'),
        ('after261','nec-video-core'),
    )
    target_exe=(WORK/'bin/th03/mainl.target.exe').read_bytes()
    target_map=(WORK/'obj/th03/mainl.map').read_bytes()
    for layer,mode in layers:
        module=importlib.import_module('build_th03_mainl_'+layer+'_work')
        receipt_raw=(ROOT/(module.PREFIX+mode+'-build.json')).read_bytes()
        receipt=json.loads(receipt_raw)
        names=module.MODES[mode]
        source_paths={n:'src/mainl/crt/'+n+'.asm' for n in names}
        source_hashes={n:sha((ROOT/source_paths[n]).read_bytes()) for n in names}
        need(receipt['complete'] and not receipt['source_acceptance'] and
             not receipt['original_cold_rebuilt'] and
             receipt['added_accepted_bytes']==0 and
             receipt['parent_receipt_sha256']==parent_hash and
             receipt['accepted_library_sha256']==sha(accepted) and
             receipt['driver_sha256']==sha((ROOT/module.DRIVER).read_bytes()) and
             receipt['mode']==mode and tuple(receipt['names'])==names and
             receipt['source_paths']==source_paths and
             receipt['source_sha256']==source_hashes and
             receipt['assembler_flags']==module.TASM_FLAGS and
             len(receipt['rounds'])==2,
             'hash-bound actual '+layer+' source/parent/driver ABI receipt')
        need(all(x['returncode']==0 and
                 sha((ROOT/x['log_path']).read_bytes())==x['log_sha256']
                 for x in receipt['phases']),
             'actual native TASM/TLIB/TLINK writer phase logs '+layer)
        target_obj={n:(WORK/'vendor'/(n+'.obj')).read_bytes() for n in names}
        expected={n:module.scope(n,target_obj[n]) for n in names}
        need(receipt['original_profiles']==json.loads(json.dumps(expected)),
             'selected original native CRT member profiles '+layer)
        next_carrier=[]
        raw_outputs=[]
        for i,row in enumerate(receipt['rounds']):
            need(row['round']==i+1 and set(row['outputs'])==
                 set(names)|{'lib','exe','map'},
                 'complete original two-round OBJ/LIB/EXE/MAP vector '+layer)
            out={}
            for kind,meta in row['outputs'].items():
                blob=(ROOT/meta['path']).read_bytes()
                need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                     'unmodified original native '+layer+' '+kind+' vector')
                out[kind]=blob
            need(all(module.scope(n,out[n])==expected[n] for n in names),
                 'original CODE/DATA/ABI/FIXUPP targets '+layer)
            if 'literal_omf_fixupp_equal_by_member' in row:
                need(row['literal_omf_fixupp_equal_by_member']=={
                    n:literal_fields(out[n])==literal_fields(target_obj[n])
                    for n in names},
                    'unmodified original literal OMF FIXUPP assertions '+layer)
            sources=dict(carry[i][0],**{n:out[n] for n in names})
            comp=compare_members(members,library_members(out['lib']),sources)
            need(comp==row['library_comparison'] and
                 comp['contextual_members_unchanged']==893-len(sources) and
                 comp['replaced_members']==sorted(sources) and
                 out['exe']==target_exe and out['map']==target_map,
                 'original CRT membership and full Japanese EXE/MAP '+layer)
            next_carrier.append((sources,out['lib']))
            raw_outputs.append(out)
        need(raw_outputs[0]==raw_outputs[1] and
             next_carrier[0][0]==next_carrier[1][0],
             'independent identical source-native output rounds '+layer)
        carry=next_carrier
        parent_hash=sha(receipt_raw)
    need(len(carry[0][0])==263 and len(members)==893 and
         carry[0][0]==carry[1][0],
         'complete 263-source Japanese original native CRT carrier')
    return base,files,accepted,members,carry,parent_hash


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
    scratch=WORK/'probe/after263'
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
        dest=f'.analysis/work/after263-{mode}-{label}.log'
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
            response=build.response(r'probe\after263\newcrt.lib /E',
                ['+probe\\after263\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\after263\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\after263\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\after263\\newcrt.lib')):
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
                run(player+['tlib',r'@probe\after263\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\after263\link.lnk'],WORK,
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
                    path=f'.analysis/work/after263-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                    literal_omf_fixupp_equal_by_member=literal_omf,
                    library_comparison=comparison))
                save()
                print(f'after263 {mode}: {len(all_sources)} source CRT members, '
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
