#!/usr/bin/env python3
"""Verify two consumed-source display_hardware builds and retained full-image model identity."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from lib import mainl_display_hardware_source as composer
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE="config/th03_mainl_display_hardware_link.json"
RECIPE_SHA="37adff2f46383f2d51174b3c9488c477ef016eba0b77ef7778a07a09f170e28c"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,text):
    if not ok:raise ValueError(text)
def validate_partition(units):
    expected=[('palette-black-fades', 1334, 130), ('palette-show', 6096, 266), ('palette-rgb', 6760, 66), ('palette-wait-white-fades', 8292, 166), ('vsync-library', 8042, 250), ('dos-setvect', 1796, 32), ('graph-extmode', 3842, 86), ('egc-library', 1828, 98), ('grcg-box-library', 2760, 366), ('gaiji-backup', 3186, 64), ('gaiji-load', 3250, 150), ('gaiji-read', 3400, 108), ('gaiji-write', 3508, 112), ('screen-mode', 3620, 78), ('screen-clear', 3698, 36), ('screen-copy', 3734, 108)]
    groups=[['palette_black_in', 'palette_black_out'], ['palette_show'], ['palette_entry_rgb'], ['vsync_wait', 'palette_white_in', 'palette_white_out'], ['vsync'], ['dos_setvect'], ['graph_extmode'], ['egc'], ['grcg_boxfill', 'grcg_byteboxfill_x'], ['gaiji_backup'], ['gaiji_entry_bfnt'], ['gaiji_read'], ['gaiji_write'], ['graph_400line'], ['graph_clear'], ['graph_copy_page']]
    need([(u['unit_id'],u['segment'],u['offset'],u['bytes']) for u in units]==[('th03-mainl-decoded-'+n,0,o,z) for n,o,z in expected],'display/hardware existing-unit partition differs')
    need([u['source_paths'] for u in units]==[['src/mainl/display_hardware/'+n+'.asm' for n in group] for group in groups],'display/hardware source partition differs')

def comparable(rows,name):
    need(name in ('vsync','graphics','gaiji','screen','palette'),'unknown model comparison contract')
    excluded=('memory_before_sha256','memory_after_sha256')
    return [{k:v for k,v in row.items() if k not in excluded} for row in rows]

def replay(root=ROOT):
    raw=(root/RECIPE).read_bytes()
    need(sha(raw)==RECIPE_SHA,"recipe identity differs")
    recipe=json.loads(raw)
    for path,digest in recipe["proof_inputs_sha256"].items():
        need(sha((root/path).read_bytes())==digest,"retained input differs: "+path)
    validate_partition(recipe['units'])
    source_recipe=json.loads((root/'config/th03_mainl_display_hardware_source.json').read_text())
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
        need(done["complete"] and done["native_invocations"]==2 and done["owned_lock_released"] and not done["errors"],"fresh display_hardware root/link incomplete")
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
    target_raw=(root/recipe['decoded_target']).read_bytes()
    expected={'vsync':(9664,20),'graphics':(3220,4),'gaiji':(2302,4),'screen':(1188,4),'palette':(2498,8)}
    for name,(terminal,prefixes) in expected.items():
        pair=[]
        for kind in ('target','candidate'):
            p=recipe['palette_models'][kind] if name=='palette' else recipe['model_phases'][name][kind]
            m=json.loads((root/p).read_text())
            need(m['success'] and (m['terminal_count'],m['prefix_count'])==(terminal,prefixes),'model counts/results differ: '+name)
            need((len(m['cpu']),len(m['nonterminal']))==(terminal,prefixes),'actual model row counts differ: '+name)
            need(m['exe_sha256']==sha(target_raw if kind=='target' else candidate_raw),'model full image differs: '+name)
            for dep,h in m['inputs'].items():need(sha((root/dep).read_bytes())==h,'actual model dependency differs: '+dep)
            pair.append(m)
        a,b=pair
        need(a['analysis']==b['analysis'],'model analysis differs: '+name)
        for key in ('cpu','nonterminal'):need(comparable(a[key],name)==comparable(b[key],name),'model observations differ: '+name+' '+key)
    target,candidate=parse_mz(target_raw),parse_mz(candidate_raw)
    need(target.valid and candidate.valid,'invalid MZ')
    relocs=lambda m:[(r.segment,r.offset) for r in m.relocations]
    ta,ca=relocs(target),relocs(candidate)
    for unit in recipe['units']:
        start=unit['segment']*16+unit['offset'];end=start+unit['bytes']
        need(target.program_image[start:end]==candidate.program_image[start:end],'display_hardware raw bytes differ: '+unit['unit_id'])
        scoped=lambda rows:[r for r in rows if start<=r[0]*16+r[1]<end]
        need(scoped(ta)==scoped(ca)==([(0,0x1fe5)] if unit['unit_id']=='th03-mainl-decoded-vsync-library' else []),'display/hardware relocation sites differ: '+unit['unit_id'])
    return dict(kind='mainl-display-hardware-consumed-source-replay',recipe_sha256=sha(raw),
        source_owned_bytes_eligible=2116,existing_source_units=recipe['units'],
        native_fragment_consumption_proven=True,fresh_root_link_builds=2,
        raw_repeat_obj_exe_map_equal=True,whole_carrier_exe_map_equal=True,
        ordered_display_hardware_relocations_equal=True,display_hardware_relocations=1,
        global_relocation_membership_equal=Counter(ta)==Counter(ca),
        global_ordered_difference_count=sum(x!=y for x,y in zip(ta,ca)),
        target_decoded_difference_count=sum(x!=y for x,y in zip(target.program_image,candidate.program_image))+abs(len(target.program_image)-len(candidate.program_image)),
        runtime_observations_equal=True,models_rerun=False,fresh_model_phase_records_retained=8,palette_models_reused_by_complete_exe_identity=True,model_transport_note=recipe['model_transport_note'],model_reuse='pinned complete EXE identity; independent full scalar/native comparisons retained',
        prior_scoped_bytes_preserved_by_complete_exe_identity=19449,total_scoped_target_equal_bytes=21565,
        native_invocations_in_this_replay=0,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    text=json.dumps(replay(),indent=2)+"\n"
    if a.output:
        with a.output.open("x") as out:out.write(text)
    else:print(text,end="")
if __name__=="__main__":main()
