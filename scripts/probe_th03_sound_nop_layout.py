#!/usr/bin/env python3
"""Bounded sound NOP/layout diagnosis; never publishes source or exact credit.

Compile disposable copies without active trailing codestrings, compare supported TC4 options,
assemble untouched compiler output, and isolate CODE alignment through annotated
assembly controls. Product sources, installed tools and current builds are inputs.
"""
import argparse,fcntl,hashlib,json,os,re,subprocess,sys,tempfile,tomllib
from pathlib import Path
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.toolchain import attest_surface
from probe_th03_main_boss_marisa_cpp import code_bytes
from build_th03_op_work import compare_mz
import review_th03_op_cfg_work as op_review
import review_th03_mainl_sound_work as ml_review
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/sound-nop-layout-probe.json'
PROFILES={
 'op':(('mode','src/op/snd/determine_mode.c','th02/snd_mode.obj',2,'O',1),
       ('pmd','src/op/snd/pmd_resident.c','th02/snd_pmdr.obj',2,'O',1),
       ('load','src/shared/sound/load.cpp','th02/snd_load.obj',2,'O',0)),
 'mainl':(('mode','src/mainl/linked_game/sound_mode.c','th02/snd_mode.obj',2,'O',1),
          ('pmd','src/mainl/linked_game/sound_pmd.c','th02/snd_pmdr.obj',2,'O',1),
          ('volume','src/mainl/linked_game/sound_volume.c','th02/snd_dlyv.obj',2,'M',1),
          ('load','src/shared/sound/load.cpp','th02/snd_load.obj',2,'O',0),
          ('reset','src/mainl/linked_game/sound_reset.cpp','th02/snd_se_r.obj',2,'O',1),
          ('se','src/mainl/linked_game/sound_se.cpp','th03/snd_se.obj',3,'M',0))}
FLAGS=('source_acceptance','product_exact','canonical_unit_credit_changed','authored_byte_credit_changed')
INPUTS=('scripts/probe_th03_sound_nop_layout.py','scripts/build_th03_op_work.py','scripts/build_th03_mainl_work.py',
 'scripts/review_th03_op_cfg_work.py','scripts/review_th03_mainl_sound_work.py','scripts/lib/omf.py','scripts/lib/pc98.py','scripts/lib/toolchain.py',
 'scripts/probe_th03_main_bomb_rikako_cpp.py','scripts/probe_th03_main_boss_marisa_cpp.py','config/toolchain.toml','config/targets.toml','config/th03_diet.toml',
 *sorted({row[1] for rows in PROFILES.values() for row in rows}))
def need(v,m):
    if not v:raise ValueError('sound layout diagnosis: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def inputs():return {p:sha((ROOT/p).read_bytes()) for p in INPUTS}
def unchanged_source_credit():return {k:False for k in FLAGS}
def comparison(candidate,target,*,annotated):
    result=compare_mz(candidate,target);sites=result.pop('differing_program_sites');a,b=map(parse_mz,(candidate,target))
    return dict(**result,different_loaded_bytes=len(sites),shown_loaded_differences=[dict(site=p,candidate=a.program_image[p],target=b.program_image[p]) for p in sites[:20]],
        difference_list_truncated=len(sites)>20,candidate_sha256=sha(candidate),target_sha256=sha(target),
        assembly_alignment_annotation_control=annotated,**unchanged_source_credit())
def case_file(work,name):
    matches=[p for p in work.iterdir() if p.name.lower()==name.lower()]
    need(len(matches)==1,'single native output: '+name);return matches[0]
def object_info(path):
    raw=path.read_bytes();code,_=code_bytes(raw,1)
    return code,dict(bytes=len(raw),sha256=sha(raw),code_bytes=len(code),code_sha256=sha(code),
        segment_attributes=[r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF'])
def images(profile):
    values=op_review.images(ROOT) if profile=='op' else ml_review.images(ROOT)
    return values[0],values[1],values[2],values[3],values[4]
def surfaces(config):
    rows=[attest_surface(ROOT,s) for s in config['surfaces'] if not s.get('bootstrap_only')]
    need(all(r['pass'] or not r['required'] for r in rows),'pinned installed tool identities');return rows

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=REPORT);o=p.parse_args()
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix'];bound={k:images(k) for k in PROFILES}
    r=dict(schema='th03-sound-nop-layout-diagnostic-v1',complete=False,provenance='candidate-local-attested',fresh_whole_product_build=False,only_selected_sound_objects_recompiled=True,implementation_sha256=inputs(),
        toolchain_before=surfaces(config),native_phases=[],profiles={},**unchanged_source_credit())
    o.output.parent.mkdir(parents=True,exist_ok=True)
    save=lambda:o.output.write_text(json.dumps(r,indent=2)+'\n');save()
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        # An eight-character random basename remains representable by DOS 8.3.
        with tempfile.TemporaryDirectory(prefix='',dir=prefix/'drive_c') as temp:
            scratch=Path(temp);need(len(scratch.name)==8,'DOS scratch basename')
            def win(name):return 'C:\\'+scratch.name+'\\'+name
            def execute(argv,cwd,label):
                run=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
                r['native_phases'].append(dict(label=label,returncode=run.returncode,output_sha256=sha(run.stdout)))
                save();need(run.returncode==0,label+': '+run.stdout.decode(errors='replace')[-800:]);print(label,flush=True)
            for profile,rows in PROFILES.items():
                work,target,candidate,cold,cold_raw=bound[profile];objects=[];asm_objects={};word_objects={}
                for index,(kind,source,old_obj,game,binary,nops) in enumerate(rows):
                    stem=('O' if profile=='op' else 'M')+str(index);ext=Path(source).suffix
                    body=(ROOT/source).read_text();marker='#pragma codestring "\\x90"\n';need(not nops or body.count(marker)==nops,'explicit codestring count: '+source)
                    stripped=body.replace(marker,'') if nops else body;(scratch/(stem+ext)).write_text(stripped)
                    current_code,current=object_info(work/('obj/'+old_obj));flags=['-c','-I'+str('C:\\'+work.name),'-O','-b-','-3','-Z','-d','-DGAME='+str(game),'-ml',"-DBINARY='"+binary+"'"]
                    def compile_variant(tag,extra,assembly=False):
                        name=stem+tag+('.ASM' if assembly else '.OBJ');execute(dos+['tcc',*flags,*extra,'-o'+name,stem+ext],scratch,profile+':'+kind+':'+tag)
                        return case_file(scratch,name)
                    direct=compile_variant('D',[]);dc,di=object_info(direct)
                    asm=compile_variant('S',['-S'],True);generated=asm.read_text();assembler_name=stem+'A.OBJ'
                    execute(tasm+['/m','/mx','/kh32768','/t',asm.name+','+assembler_name+',,;'],scratch,profile+':'+kind+':assemble')
                    ap=case_file(scratch,assembler_name);ac,ai=object_info(ap);asm_objects[old_obj]=ap
                    byte_decl="SHARED\tsegment byte public use16 'CODE'";word_decl="SHARED\tsegment word public use16 'CODE'"
                    need(byte_decl in generated or word_decl in generated,'native compiler SHARED declaration')
                    annotated=generated.replace(byte_decl,word_decl);wp=scratch/(stem+'W.ASM');wp.write_text(annotated);word_name=stem+'W.OBJ'
                    execute(tasm+['/m','/mx','/kh32768','/t',wp.name+','+word_name+',,;'],scratch,profile+':'+kind+':word-control')
                    wp=case_file(scratch,word_name);wc,wi=object_info(wp);word_objects[old_obj]=wp
                    need(wc==ac,'alignment-only annotation must preserve complete unresolved CODE')
                    obj=dict(kind=kind,source=source,first_use_game=game,first_use_binary=binary,original_object=old_obj,removed_codestring_bytes=nops,preserved_conditional_codestrings=body.count(marker)-nops,current_object=current,
                        direct=di,compiler_assembly=ai,annotated_word_control=wi,direct_matches_current_prefix=dc==current_code[:-nops] if nops else dc==current_code,
                        assembly_matches_direct_code=ac==dc,annotated_word_preserves_code=wc==ac,annotated_segment_declarations=generated.count(byte_decl),options=[])
                    if profile=='op':
                        for tag,opts in (('G',['-G']),('NO',['-O-']),('A2',['-a2'])):
                            pc=compile_variant(tag,opts);vc,vi=object_info(pc);obj['options'].append(dict(flags=opts,object=vi,same_code_as_direct=vc==dc))
                        if kind in ('pmd','load'):
                            pc=compile_variant('WX',['-WX']);vc,vi=object_info(pc);obj['options'].append(dict(flags=['-WX'],object=vi,same_code_as_direct=vc==dc))
                    objects.append(obj);save()
                results={}
                for label,selected in (('compiler_assembly',asm_objects),('word_alignment_control',word_objects)):
                    response=(work/f'obj/th03/{profile}.@l').read_text()
                    for original,replacement in selected.items():
                        old=('obj/'+original).replace('/','\\');need(response.count(old)==1,'original response slot: '+original);response=response.replace(old,win(replacement.name))
                    output=profile+('A' if label=='compiler_assembly' else 'W');response=response.replace('bin\\th03\\'+profile+'.exe',win(output+'.EXE')).replace('obj\\th03\\'+profile+'.map',win(output+'.MAP'))
                    rsp=scratch/(output+'.RSP');rsp.write_text(response);execute(dos+['tlink','@'+win(rsp.name)],work,profile+':link:'+label)
                    results[label]=comparison(case_file(scratch,output+'.EXE').read_bytes(),(work/f'bin/th03/{profile}.target.exe').read_bytes(),annotated=label=='word_alignment_control')
                r['profiles'][profile]=dict(cold_report_sha256=sha(cold_raw),source_inventory_sha256=sha(json.dumps(cold['source_sha256'],sort_keys=True).encode()),objects=objects,comparisons=results);save()
    r['toolchain_after']=surfaces(config);need(r['toolchain_before']==r['toolchain_after'],'tool installation changed')
    for profile,old in bound.items():need(images(profile)[4]==old[4],'current cold pair changed during diagnostics')
    need(r['implementation_sha256']==inputs(),'diagnostic inputs changed');r.update(complete=True,scratch_removed=True,current_product_pairs_unchanged=True);save()
    for profile,row in r['profiles'].items():
        for label,c in row['comparisons'].items():print(profile,label,'loaded differences',c['different_loaded_bytes'],'ordered relocations',c['ordered_relocations_equal'],flush=True)
    print('Diagnostic only; source, authored bytes and whole-product acceptance unchanged',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
