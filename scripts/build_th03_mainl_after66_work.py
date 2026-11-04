#!/usr/bin/env python3
"""Incremental native reconstruction on the proven 66-source original Japanese
MAINL library, without rebuilding the original cold pair.

This validates *all* CODE/DATA bytes, fixup sites and targets, unchanged CRT
membership and the complete native linked EXE/MAP. It explicitly does not
normalize or claim original literal OMF FIXUPP order/frame equality.
"""
import argparse,fcntl,json,os,shutil,subprocess,tomllib
from pathlib import Path

import build_th03_mainl_after62_work as parent
from review_th03_mainl_after62_work import review as review_parent
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
DRIVER='scripts/build_th03_mainl_after66_work.py'
PREFIX='.analysis/work/mainl-after66-'
LAST='sprintf-calloc-puts-ctime'
MODES={
    'strerror':('strerror',),
    'strerror-bsearch-strdup-abort':('strerror','bsearch','strdup','abort'),
}
NATIVE={
    'strerror':dict(index=297,code=176,data=26,bss=161,
        publics=[(135,'__strerror'),(157,'_strerror')],
        imports=['_sprintf','_errno','__sys_nerr','__sys_errlist'],fields=12),
    'bsearch':dict(index=198,code=125,data=0,bss=0,
        publics=[(0,'_bsearch')],imports=[],fields=0),
    'strdup':dict(index=296,code=75,data=0,bss=0,
        publics=[(0,'_strdup')],imports=['_memcpy','_strlen','_malloc'],fields=3),
    'abort':dict(index=2,code=20,data=0,bss=0,
        publics=[(0,'_abort')],imports=['_raise','__abort'],fields=2),
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
    need([(r['name'],r['class'],r['size']) for r in segment_definitions(blob)]==
         [('_TEXT','CODE',q['code']),('_DATA','DATA',q['data']),('_BSS','BSS',q['bss'])],
         'complete original segment sizes '+name)
    need(code_publics(blob,1)==q['publics'] and externs(blob)==q['imports'],
         'complete native public/extern interface '+name)
    need([x.data.hex() for x in parse_omf(blob) if x.name=='GRPDEF']==
         ['08ff02ff03'], 'original group layout '+name)
    need(len(literal_fields(blob))==q['fields'],
         'entire source relocation field population '+name)
    p=payload(blob)
    c=bytes(p[1,i] for i in range(q['code']))
    d=bytes(p[2,i] for i in range(q['data']))
    return dict(CODE_sha256=sha(c),CODE_bytes=len(c),DATA_sha256=sha(d),
                DATA_bytes=len(d),BSS_bytes=q['bss'],
                publics=code_publics(blob,1),imports=externs(blob),
                relocation_sites_targets=fixed_fields(blob))


def retained():
    # The previous working carrier has four newly assembled native CRT modules,
    # which must remain compiled from source at the original member positions.
    base,files,accepted,members,original62,_=parent.retained()
    need(review_parent(LAST)['complete'] and
         review_parent(LAST)['native_source_members']==66,
         'complete source-bound 66-member original Japanese link review')
    raw=(ROOT/(parent.PREFIX+LAST+'-build.json')).read_bytes()
    record=json.loads(raw)
    names=parent.MODES[LAST]
    need(record['complete'] and not record['source_acceptance'] and
         record['original_cold_rebuilt'] is False and
         record['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         record['accepted_library_sha256']==sha(accepted) and
         tuple(record['names'])==names and len(record['rounds'])==2,
         'unchanged original 66-source native carrier receipt')
    carry=[]
    for i,row in enumerate(record['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'retained original 66-source '+kind+' byte vector')
            out[kind]=blob
        src=dict(original62[i][0],**{name:out[name] for name in names})
        need(len(src)==66 and
             compare_members(members,library_members(out['lib']),src)
                ['contextual_members_unchanged']==827 and
             out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'entire Japanese 66-member EXE/MAP and contextual vendor program identity')
        carry.append((src,out['lib']))
    need(carry[0][0]==carry[1][0],
         'independent identical inherited 66-source real native object vectors')
    return base,files,accepted,members,carry,sha(raw)


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
    scratch=WORK/'probe/after66'
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
        dest=f'.analysis/work/after66-{mode}-{label}.log'
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
            response=build.response(r'probe\after66\newcrt.lib /E',
                ['+probe\\after66\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in ((b'probe\\xxwhole\\xxfull.exe',b'probe\\after66\\linked.exe'),
                            (b'probe\\xxwhole\\xxfull.map',b'probe\\after66\\linked.map'),
                            (b'probe\\xxwhole\\xxcrt.lib',b'probe\\after66\\newcrt.lib')):
                need(link.count(old)==1,'native MAINL link response binding')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(response)
            (scratch/'link.lnk').write_bytes(link)
            for idx in (1,2):
                for name in [*(n+'.obj' for n in names),'newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map']:
                    (scratch/name).unlink(missing_ok=True)
                compiled={}
                for n in names:
                    run(dos+TASM_FLAGS+[n+'.asm',n+'.obj'],scratch,
                        f'round{idx}-assemble-{n}')
                    obj=(scratch/(n+'.obj')).read_bytes()
                    need(scope(n,obj)==expected[n],
                         'all original CODE/DATA bytes, public interface, targets '+n)
                    compiled[n]=obj
                all_sources=dict(carry[idx-1][0],**compiled)
                for n,b in carry[idx-1][0].items():
                    (scratch/(n+'.obj')).write_bytes(b)
                run(player+['tlib',r'@probe\after66\library.rsp'],WORK,
                    f'round{idx}-library')
                comparison=compare_members(members,
                    library_members((scratch/'newcrt.lib').read_bytes()),all_sources)
                need(comparison['contextual_members_unchanged']==893-len(all_sources)
                     and comparison['replaced_members']==sorted(all_sources),
                     'all inherited source members and original remainder unchanged')
                run(player+['tlink',r'@probe\after66\link.lnk'],WORK,
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
                    path=f'.analysis/work/after66-{mode}-round{idx}-{file}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                report['rounds'].append(dict(round=idx,outputs=out,
                                               library_comparison=comparison))
                save()
                print(f'after66 {mode}: {len(all_sources)} source CRT members, '
                      f'Japanese EXE/MAP exact round {idx}',flush=True)
            need(len(report['rounds'])==2 and
                 {n:q['sha256'] for n,q in report['rounds'][0]['outputs'].items()}==
                 {n:q['sha256'] for n,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical independent native output rounds')
        finally:
            shutil.rmtree(scratch)
    need(inputs=={n:(ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes() for n in names},
         'source unchanged during producer rounds')
    report['complete']=True
    save()

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(MODES))
    main(ap.parse_args().mode)
