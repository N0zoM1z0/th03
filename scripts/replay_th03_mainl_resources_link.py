#!/usr/bin/env python3
"""Verify two consumed-source resource builds and retained full-image model identity."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from lib import mainl_resources_source as composer
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE="config/th03_mainl_resources_link.json"
RECIPE_SHA="ee875ef769dd9fe113f8ece261378f7b646d1ecc6c824c38f02d0009114a2463"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,text):
    if not ok:raise ValueError(text)
def validate_partition(units):
    expected=[('draw-gaiji',0xf58,148),('draw-pack',0x162c,212),('draw-scroll',0x1700,88),('draw-show',0x1758,6),('draw-noclip',0x2c68,202),('draw-table',0x1aaa,1024),('bfnt-library',0x272,512),('super-library',0x237e,1008),('dos-close',0xa98,22),('gdc-outpw',0xc66,11),('pi-decoder-free',0xfec,76),('stack-memory',0x1eaa,76),('palette-bfnt',0x4c6,64),('buffer-dos-open',0xaae,26)]
    need([(u['unit_id'],u['segment'],u['offset'],u['bytes']) for u in units]==[('th03-mainl-decoded-'+n,0,o,z) for n,o,z in expected], 'resource existing-unit partition differs')
    groups=[['graph_gaiji_putc'],['graph_pack_put_8'],['graph_scrollup'],['graph_show'],['graph_pack_put_8_noclip'],['rottbl'],['bfnt_entry_pat','bfnt_extend_header_skip','bfnt_header_read','bfnt_header_analysis'],['super_free','super_entry_pat','super_entry_at','super_entry_bfnt','super_cancel_pat','super_put'],['dos_close'],['gdc_outpw'],['graph_pi_free'],['smem_release','smem_wget'],['bfnt_palette_set'],['dos_ropen']]
    need([u['source_paths'] for u in units]==[['src/mainl/resources/'+n+'.asm' for n in group] for group in groups],'resource source partition differs')


def replay(root=ROOT):
    raw=(root/RECIPE).read_bytes()
    need(sha(raw)==RECIPE_SHA,"recipe identity differs")
    recipe=json.loads(raw)
    for path,digest in recipe["proof_inputs_sha256"].items():
        need(sha((root/path).read_bytes())==digest,"retained input differs: "+path)
    validate_partition(recipe['units'])
    source_recipe=json.loads((root/'config/th03_mainl_resources_source.json').read_text())
    def load(row):
        raw=(root/row['path']).read_bytes()
        need(sha(raw)==row['sha256'],'source recipe identity differs: '+row['path'])
        return raw
    providers={};maintained={}
    for u in source_recipe['units']:
        for row in u['providers']:
            providers[row['name']]=load(row['provider']);maintained[row['name']]=load(row['source'])
    generated=composer.compose(load(source_recipe['previous_generated_root']),providers,maintained)
    products=[]
    for build in recipe["builds"]:
        work=root/build["work"];output=root/build["output"]
        manifest=json.loads((root/build["proposal"]/"manifest.json").read_text())
        for row in manifest["inputs"]:
            need(sha((root/row["path"]).read_bytes())==row["sha256"],"guarded native input differs: "+row["path"])
        for name in ("obj/th03/mainl.obj","bin/th03/mainl.exe","obj/th03/mainl.map"):
            need(name not in manifest["repeat_inputs"],"native output copied as input: "+name)
        if build.get("repeat"):
            mtimes=json.loads((output/"source-mtimes.json").read_text())
            for name,row in manifest["repeat_inputs"].items():
                first,second=root/row["path"],work/name
                need(first.read_bytes()==second.read_bytes(),"repeat input differs: "+name)
                need(first.stat().st_mtime_ns==second.stat().st_mtime_ns==row["mtime_ns"]==mtimes[name],"declared repeat source mtime differs: "+name)
        done=json.loads((output/"completion.json").read_text())
        need(done["complete"] and done["native_invocations"]==2 and done["owned_lock_released"] and not done["errors"],"fresh resource root/link incomplete")
        for path,content in generated.items():need((work/path).read_bytes()==content,"consumed source differs: "+path)
        for phase in ("root","link"):
            start=json.loads((output/(phase+"-started.json")).read_text())
            end=json.loads((output/(phase+"-finished.json")).read_text())
            transition=json.loads((output/(phase+"-registry-transition.json")).read_text())
            need(start["argv"]==manifest["native_argv"][phase] and start["wait_seconds"]==90 and start["cleanup_seconds"]==15,"native command/budget differs")
            need(end["exit_code"]==0 and not end["timeout"] and not end["cleanup_uncertain"] and not end["poison"] and not end["survivors"] and not end["errors"] and transition["ok"],"native cleanup/result differs")
        products.append({name:(work/name).read_bytes() for name in ("obj/th03/mainl.obj","bin/th03/mainl.exe","obj/th03/mainl.map")})
    need(len(products)==2 and products[0]==products[1],"repeat raw OBJ/EXE/MAP differs")
    candidate_raw=products[0]["bin/th03/mainl.exe"]
    need(candidate_raw==(root/recipe["previous_exe"]).read_bytes(),"full carrier EXE differs")
    need(products[0]["obj/th03/mainl.map"]==(root/recipe["previous_map"]).read_bytes(),"full carrier MAP differs")
    models=json.loads((root/recipe['model_proof']).read_text())
    need(models['candidate_exe_sha256']==sha(candidate_raw) and models['runtime_equal'],'resource model image identity differs')
    def comparable(rows,name):
        excluded=('data_before_sha256','data_after_sha256') if name=='buffer' else ('memory_before_sha256','memory_after_sha256')
        return [{k:v for k,v in row.items() if k not in excluded} for row in rows]
    expected={'draw':(7196,16),'super':(949,10),'smem':(488,0),'palette':(2498,8),'buffer':(1754,0)}
    for name,(terminal,prefix) in expected.items():
        pair=[]
        for kind in ('target','candidate'):
            p=models['fresh_models'][name][kind];m=json.loads((root/p).read_text())
            need(m['success'] and m['terminal_count']==terminal and m['prefix_count']==prefix,'model count/result differs: '+name)
            need(m['exe_sha256']==sha((root/m['path']).read_bytes()),'model full image differs')
            for dep,h in m['inputs'].items():need(sha((root/dep).read_bytes())==h,'actual model dependency differs: '+dep)
            pair.append(m)
        a,b=pair
        need(a['analysis']==b['analysis'],'model analysis differs: '+name)
        for key in ('cpu','nonterminal'):need(comparable(a[key],name)==comparable(b[key],name),'model observations differ: '+name)
    pi=json.loads((root/recipe['pi_model_proof']).read_text())
    need(pi['runtime_equal'] and pi['candidate_exe_sha256']==sha(candidate_raw),'PI_FREE retained full-image proof differs')
    target_raw=(root/recipe['decoded_target']).read_bytes()
    need(models['target_exe_sha256']==pi['target_exe_sha256']==sha(target_raw),'model target identity differs')
    target,candidate=parse_mz(target_raw),parse_mz(candidate_raw)
    need(target.valid and candidate.valid,'invalid MZ')
    relocs=lambda m:[(r.segment,r.offset) for r in m.relocations]
    ta,ca=relocs(target),relocs(candidate)
    for unit in recipe['units']:
        start=unit['segment']*16+unit['offset'];end=start+unit['bytes']
        need(target.program_image[start:end]==candidate.program_image[start:end],'resource raw bytes differ: '+unit['unit_id'])
        scoped=lambda rows:[r for r in rows if start<=r[0]*16+r[1]<end]
        need(scoped(ta)==scoped(ca)==[],'resource relocation sites differ: '+unit['unit_id'])
    return dict(kind='mainl-resources-consumed-source-replay',recipe_sha256=sha(raw),
        source_owned_bytes_eligible=3475,existing_source_units=recipe['units'],
        native_fragment_consumption_proven=True,fresh_root_link_builds=2,
        raw_repeat_obj_exe_map_equal=True,whole_carrier_exe_map_equal=True,
        ordered_resource_relocations_equal=True,resource_relocations=0,
        global_relocation_membership_equal=Counter(ta)==Counter(ca),
        global_ordered_difference_count=sum(x!=y for x,y in zip(ta,ca)),
        target_decoded_difference_count=sum(x!=y for x,y in zip(target.program_image,candidate.program_image))+abs(len(target.program_image)-len(candidate.program_image)),
        runtime_observations_equal=True,models_rerun=False,model_reuse='pinned complete EXE identity; independent full scalar/native comparisons retained',
        prior_scoped_bytes_preserved_by_complete_exe_identity=13495,total_scoped_target_equal_bytes=16970,
        native_invocations_in_this_replay=0,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    text=json.dumps(replay(),indent=2)+"\n"
    if a.output:
        with a.output.open("x") as out:out.write(text)
    else:print(text,end="")
if __name__=="__main__":main()
