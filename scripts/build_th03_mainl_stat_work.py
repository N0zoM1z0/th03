#!/usr/bin/env python3
"""Build the complete original 556-CODE/4-DATA DOS stat through native TASM.

Use the verified 35-source fclose product-only CRT as immutable parent;
preserve its explicitly tracked fopen/fclose raw OMF metadata gaps.
Rebuild ONLY the new stat producer and its 36-member normal MAINL link.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_fclose_work as previous
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
SOURCE='src/mainl/crt/stat.asm'
DRIVER='scripts/build_th03_mainl_stat_work.py'
REPORT='.analysis/work/mainl-stat-native-build.json'
ORIGINAL=WORK/'vendor/stat.obj'
SCRATCH=WORK/'probe/stat36'
TASM_FLAGS=['/m','/mx','/kh32768','/t','stat.asm','stat.obj']
EXTERNS=['__IOERROR','__DOSTIMETOU','_free','__fullpath','___path_isdbcsleadbyte']
FIXUP_SITES=[30,175,210,256,334,347,376,432,486]


def original_scope(blob):
    need(describe_omf(blob)['valid'],'valid original Borland 556-byte stat OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(blob)]==
         [('_TEXT','CODE',556),('_DATA','DATA',4),('_BSS','BSS',0)],
         'full 556 original CODE and four initialized pathname-class DATA')
    need(code_publics(blob,1)==[(132,'_stat')] and
         externs(blob)==EXTERNS,
         'original private far pathname helper, public stat and five runtime imports')
    need([q.data.hex() for q in parse_omf(blob) if q.name=='GRPDEF']==
         ['08ff03ff02'],'original BSS-before-DATA group record')
    fs=literal_fields(blob)
    need([f['site'] for f in fs]==FIXUP_SITES and len(fs)==9,
         'all nine literal ordered original __IOERROR/datetime/path FIXUPPs')
    p=payload(blob)
    code=bytes(p[1,i] for i in range(556))
    data=bytes(p[2,i] for i in range(4))
    need(data==bytes([0x5c,0x2f,0x2e,0]),
         'original four initialized DOS path separator/period bytes')
    return dict(CODE_bytes=556,CODE_sha256=sha(code),
                DATA_bytes=4,DATA_sha256=sha(data),
                literal_fields=fs,imports=externs(blob),
                original_pub_offset=132,original_group='08ff03ff02')


def retained():
    base,files,accepted,members,old34,parenthash=previous.retained()
    report_raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(report_raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['partial_parent_fopen_OMF_order_open'] is True and
         r['native_fclose_MKNAME_TARGET_frame_open'] is True and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_four_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'verified 35-source native fopen/fclose product link with real OMF gaps still open')
    out=[]
    for index,row in enumerate(r['rounds']):
        objects={}
        for kind,q in row['outputs'].items():
            raw=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete unchanged 35-source native '+kind+' file')
            objects[kind]=raw
        need(objects['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             objects['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'prior 35 original-source linker full Japanese EXE/MAP')
        old=dict(old34[index],fclose=objects['obj'])
        c=compare_members(members,library_members(objects['lib']),old)
        need(c['replaced_members']==sorted(old) and
             c['contextual_members_unchanged']==858,
             '35 native source modules and 858 untouched original programs')
        out.append(old)
    need(len(out)==2 and out[0]==out[1] and len(out[0])==35 and
         len(members)==893 and members[289].name=='stat',
         'identical 35 source vectors and genuine original stat member289')
    return base,files,accepted,members,out,sha(report_raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[289].program_records,
         'original complete stat library member identity')
    target=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    rec=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
             original_cold_rebuilt=False,prior_fopen_FIXUPP_order_open=True,
             prior_fclose_MKNAME_frame_open=True,
             accepted_baseline=base,accepted_library_sha256=sha(accepted),
             previous_thirty_five_source_build_sha256=parenthash,
             original_sha256=sha(original),source_sha256=sha(source),
             driver_sha256=sha((ROOT/DRIVER).read_bytes()),
             native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(rec,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/stat-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        rec['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                  log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'new isolated native stat original CRT scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all 893 vendor native CRT object programs extracted')
            for member in members:
                f=extracted[member.name.lower()]
                need(object_program_records(f.read_bytes())==member.program_records,
                     'unchanged original member program '+member.name)
                targetfile=SCRATCH/(member.name+'.obj')
                if f!=targetfile:f.rename(targetfile)
            (SCRATCH/'stat.asm').write_bytes(source)
            os.utime(SCRATCH/'stat.asm',(946684800,946684800))
            response=build.response(r'probe\stat36\newcrt.lib /E',
                ['+probe\\stat36\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stat36\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stat36\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stat36\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one actual normal-link Japanese MAINL output')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(response)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/stat-library.rsp').write_bytes(response)
            (ROOT/'.analysis/work/stat-link.lnk').write_bytes(link)
            for i in (1,2):
                for file in ('stat.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/file).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                object_bytes=(SCRATCH/'stat.obj').read_bytes()
                need(original_scope(object_bytes)==target and
                     literal_fields(object_bytes)==literal_fields(original),
                     'original 556 native CODE +4 DATA and nine ordered OMF fields')
                sources=dict(prior[i-1],stat=object_bytes)
                for name,b in prior[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(b)
                run(dos+['tlib',r'@probe\stat36\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==857,
                     '36 original source module positions and 857 other vendor programs unchanged')
                run(dos+['tlink',r'@probe\stat36\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,file in (('obj','stat.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/file).read_bytes()
                    location=f'.analysis/work/stat-round{i}-{file}'
                    (ROOT/location).write_bytes(blob)
                    output[kind]=dict(path=location,bytes=len(blob),sha256=sha(blob))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete Japanese decoded MAINL original EXE and MAP raw equal')
                rec['rounds'].append(dict(round=i,outputs=output,library_comparison=comparison))
                save()
                print('Original 36-source stat Japanese MAINL EXE and MAP exact round',i,flush=True)
            need({k:v['sha256'] for k,v in rec['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in rec['rounds'][1]['outputs'].items()},
                 'two exact full byte-identical native source output vectors')
        finally:shutil.rmtree(SCRATCH)
    b,_,lib,_,_,afterhash=retained()
    need(b==base and lib==accepted and afterhash==parenthash and
         (ROOT/SOURCE).read_bytes()==source,
         'all native parent sources and accepted original library frozen')
    rec['complete']=True
    save()


if __name__=='__main__':
    main()
