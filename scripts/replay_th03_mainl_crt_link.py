#!/usr/bin/env python3
"""Read-only replay of semantic CRT producers, normal library links and CPU receipts."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE='config/th03_mainl_crt_link.json'
RECIPE_SHA='f50cd013f9cbb84e5cb44a4f9ce98c456b61ba080c0db5441aed73e9cfbfa17f'
UNITS=[('h_llsh',0x315e,33),('h_padd',0x317f,96),('ioerror',0x31df,82),('n_pcmp',0x357c,33),('fbrk',0x3e70,352),('setblock',0x8e5a,32)]
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok: raise ValueError(message)
def replay(root=ROOT):
    def raw(p): return (root/p).read_bytes()
    def load(p): return json.loads(raw(p))
    data=raw(RECIPE);need(sha(data)==RECIPE_SHA,'CRT recipe identity differs');r=json.loads(data)
    for p,h in r['proof_inputs_sha256'].items():need(sha(raw(p))==h,'CRT proof input differs: '+p)
    need([(u['unit_id'],u['segment'],u['offset'],u['bytes']) for u in r['units']]==[('th03-mainl-decoded-crt-'+n,0,o,z) for n,o,z in UNITS],'CRT unit partition differs')
    for u,(name,_,_) in zip(r['units'],UNITS):
        expected=['src/mainl/crt/'+name+'.asm']
        if name=='ioerror':expected+=['src/mainl/crt/crt_errno.inc','src/mainl/crt/dos_error_map.inc']
        need(u['source_paths']==expected,'CRT source partition differs')
    for b in r['native_builds']:
        m=load(b['manifest']);out=Path(m['output'])
        for basename,binding in m.get('source_timestamp_bindings',{}).items():
            maintained=binding['maintained']; consumed=root/m['work']/basename
            need(sha(raw(maintained['path']))==maintained['sha256'] and consumed.read_bytes()==raw(maintained['path']),'CRT maintained/consumed source binding differs')
            observed=load(binding['first_observation']['path'])
            need(observed[basename]==binding['first_observed_timestamp_ns']==consumed.stat().st_mtime_ns,'CRT repeat source timestamp differs')
        for phase in b['accepted_phases']:
            if phase in {x[0] for x in UNITS}:
                need(m['native_outputs'][phase] not in m.get('repeat_inputs',{}),'CRT assembler output copied as input')
            start=load(str(out/(phase+'-started.json')));end=load(str(out/(phase+'-finished.json')));transition=load(str(out/(phase+'-registry-transition.json')))
            need(start['argv']==m['native_argv'][phase] and start['wait_seconds']==90 and start['cleanup_seconds']==15,'CRT command/budget differs')
            need(end['exit_code']==0 and end['inventory_complete'] and end['initial_inventory_complete'] and not any(end[k] for k in ('timeout','cleanup_uncertain','poison','survivors','errors')) and transition['ok'],'CRT native phase failed/uncertain')
            product=root/m['work']/m['native_outputs'][phase]
            if phase=='extract':
                matches=[x for x in product.parent.iterdir() if x.name.lower()==product.name.lower()]
                need(len(matches)==1,'ambiguous extracted filename');product=matches[0]
            produced=product.read_bytes();receipt=load(str(out/(phase+'-output.json')))
            need(sha(produced)==receipt['sha256'] and len(produced)==receipt['bytes'],'CRT native output receipt differs')
        if not b['require_complete']:
            failed=load(str(out/'completion.json'));need(not failed['complete'] and failed['owned_lock_released'],'historical failed C batch incorrectly represented')
        if b['require_complete']:
            done=load(str(out/'completion.json'));need(done['complete'] and done['owned_lock_released'] and not done['errors'],'CRT build completion differs')
    for p in r['producers']:
        source=raw(p['source'])
        for consumed in p['consumed_sources']:need(raw(consumed)==source,'actual consumed CRT source differs')
        name=Path(p['source']).stem
        need(raw(p['first_object'])==raw(str(Path(r['links'][0]['work'])/'crtobjs'/(name+'.obj'))),'first producer not consumed by first library')
        need(raw(p['repeat_object'])==raw(str(Path(r['links'][1]['work'])/'crtobjs'/(name+'.obj'))),'repeat producer not consumed by repeat library')
        a,b=(raw(p[k]) for k in ('first_object','repeat_object'));need(a==b,'CRT raw object repeat differs')
        for companion in p['companions']:
            need(all(raw(x)==raw(companion['source']) for x in companion['consumed_sources']),'CRT consumed include differs')
    spec=importlib.util.spec_from_file_location('crt_library_reader',root/r['library_inspector']);lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
    original=lib.inventory(root/r['original_library'])
    products=[]
    for b in r['links']:
        work=root/b['work'];objects={n:work/'crtobjs'/f'{n}.obj' for n,_,_ in UNITS}
        report=lib.compare(original,lib.inventory(work/'crt.lib'),objects)
        need(report['member_count']==893 and report['contextual_members_unchanged']==887 and report['all_member_order_equal'],'CRT library extraction/order differs')
        need(len(report['fresh_producer_comparisons'])==6 and all(x['library_program_records_equal'] for x in report['fresh_producer_comparisons']),'CRT fresh producer not consumed')
        products.append({p:(work/p).read_bytes() for p in ('crt.lib','bin/th03/mainl.exe','obj/th03/mainl.map')})
    need(len(products)==2 and products[0]==products[1],'CRT raw LIB/EXE/MAP repeat differs')
    candidate_raw=products[-1]['bin/th03/mainl.exe'];need(candidate_raw==raw(r['previous_exe']),'CRT full prior carrier bridge differs')
    target_raw=raw(r['decoded_target']);target=parse_mz(target_raw);candidate=parse_mz(candidate_raw)
    need(target.valid and candidate.valid,'CRT invalid actual image')
    need(len(target.program_image)==len(candidate.program_image),'CRT image length differs')
    differences=[{'linear':i,'target':a,'candidate':b} for i,(a,b) in enumerate(zip(target.program_image,candidate.program_image)) if a!=b]
    need(differences==[{'linear':60473,'target':144,'candidate':0}],'CRT outside-scope target difference changed')
    reloc=lambda m:[(x.segment,x.offset) for x in m.relocations]
    ar,br=reloc(target),reloc(candidate)
    need(len(ar)==len(br)==677 and Counter(ar)==Counter(br) and sum(a!=b for a,b in zip(ar,br))==461,'CRT global relocation observation differs')
    for _,offset,size in UNITS:need(target.program_image[offset:offset+size]==candidate.program_image[offset:offset+size],'CRT linked code differs')
    for offset,size in ((0xe3f0+0xe8e,91),(0xe3f0+0x1130,2)):need(target.program_image[offset:offset+size]==candidate.program_image[offset:offset+size],'CRT owned data differs')
    models=[load(r['models'][k]) for k in ('target','candidate')]
    for m,actual in zip(models,(target_raw,candidate_raw)):
        need(m['model_pass'] and m['scenarios']==len(m['cpu'])==7858 and m['instruction_coverage']=={'instructions':277,'visited':277,'unvisited':[]},'CRT runtime incomplete')
        need(m['image_sha256']==sha(actual)==sha(raw(m['image'])),'CRT runtime actual image differs')
        for p,h in m['source_inputs'].items():need(sha(raw(p))==h,'CRT consumed model source differs')
    a,b=models;need(a['source_inputs']==b['source_inputs'] and a['tools']==b['tools'] and a['analysis']==b['analysis'],'CRT runtime analysis/dependencies differ')
    clean=lambda rows:[{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in rows]
    need(clean(a['cpu'])==clean(b['cpu']),'CRT actual CPU state/events/stores differ')
    return {'existing_source_units':6,'source_owned_bytes_eligible':628,'source_present_eligible':True,'native_source_consumption':True,'raw_object_repeat_equal':True,'raw_library_exe_map_repeat_equal':True,'first_repeat_full_image_bridge':True,'runtime_equal':True,'scenarios_per_image':7858,'instruction_positions':277,'owned_data_bytes':93,'models_rerun':False,'models_rerun_scope':'This fast replay only reads two fresh actual-image runtime receipts; those original runs executed the models.','exact_acceptance':False,'canonical_packed_acceptance':False,'known_target_differences':differences,'global_ordered_relocation_differences':461}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();result=replay();text=json.dumps(result,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
