#!/usr/bin/env python3
"""Verify two consumed-source root_tail builds and retained full-image model identity."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from lib import mainl_root_tail_source as composer
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE="config/th03_mainl_root_tail_link.json"
RECIPE_SHA="473d655bc3282559122fe5e4d1702928297d5f3557cf8c8c97a4497a6e19c96c"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,text):
    if not ok:raise ValueError(text)
def validate_partition(units):
    expected=[('th03-mainl-decoded-root-tail-align-bfnt', 0, 1221, 1), ('th03-mainl-decoded-root-tail-align-bread', 0, 1547, 1), ('th03-mainl-decoded-root-tail-align-bseek', 0, 1661, 1), ('th03-mainl-decoded-root-tail-align-filesize', 0, 1709, 1), ('th03-mainl-decoded-root-tail-keyclear', 0, 1790, 6), ('th03-mainl-decoded-root-tail-grcg', 0, 3126, 48), ('th03-mainl-decoded-root-tail-root-zero-font', 0, 3185, 1), ('th03-mainl-decoded-root-tail-atan-end', 0, 5982, 114), ('th03-mainl-decoded-root-tail-align-pfgetc', 0, 6403, 1), ('th03-mainl-decoded-root-tail-pfgetc-zero', 0, 6563, 1), ('th03-mainl-decoded-root-tail-align-pfread', 0, 6669, 1), ('th03-mainl-decoded-root-tail-rand', 0, 6718, 42), ('th03-mainl-decoded-root-tail-sound-text', 0, 7926, 116), ('th03-mainl-decoded-root-tail-resident', 0, 10094, 226), ('th03-mainl-decoded-root-tail-joystick', 0, 10925, 105), ('th03-mainl-decoded-root-tail-compare-align', 0, 11311, 57)]
    groups=[['src/mainl/archive_io/bfill.asm'], ['src/mainl/archive_io/bopenr.asm'], ['src/mainl/archive_io/bseek.asm'], ['src/mainl/archive_io/bseek_.asm'], ['src/mainl/root_tail/dos_keyclear.asm'], ['src/mainl/root_tail/grcg_setcolor.asm'], ['src/mainl/root_tail/root_zero_font.asm'], ['src/mainl/root_tail/iatan2.asm', 'src/mainl/root_tail/js_end.asm'], ['src/mainl/archive_io/pfgetc.asm'], ['src/mainl/archive_io/pfgetc.asm'], ['src/mainl/archive_io/pfrewind.asm'], ['src/mainl/root_tail/random.asm'], ['src/mainl/root_tail/soundio.asm', 'src/mainl/root_tail/text_clear.asm', 'src/mainl/root_tail/text_fillca.asm'], ['src/mainl/root_tail/respal_exist.asm', 'src/mainl/root_tail/respal_set_palettes.asm'], ['src/mainl/root_tail/joystick_prefix.asm', 'src/mainl/root_tail/js_start.asm', 'src/mainl/root_tail/js_sense.asm', 'src/mainl/root_tail/joystick_suffix.asm'], ['src/mainl/root_tail/pf_str_ieq.asm', 'src/mainl/archive_io/pfopen.asm']]
    need([(u['unit_id'],u['segment'],u['offset'],u['bytes']) for u in units]==expected,'root-tail existing-unit partition differs')
    need([u['source_paths'] for u in units]==groups,'root-tail actual producer ownership differs')

def comparable(rows,name):
    need(name in ('tail',),'unknown model comparison contract')
    excluded=('memory_before_sha256','memory_after_sha256','data_before_sha256','data_after_sha256')
    return [{k:v for k,v in row.items() if k not in excluded} for row in rows]

def replay(root=ROOT):
    raw=(root/RECIPE).read_bytes()
    need(sha(raw)==RECIPE_SHA,"recipe identity differs")
    recipe=json.loads(raw)
    for path,digest in recipe["proof_inputs_sha256"].items():
        need(sha((root/path).read_bytes())==digest,"retained input differs: "+path)
    validate_partition(recipe['units'])
    source_recipe=json.loads((root/'config/th03_mainl_root_tail_source.json').read_text())
    def load(row):
        raw=(root/row['path']).read_bytes()
        need(sha(raw)==row['sha256'],'source recipe identity differs: '+row['path'])
        return raw
    providers={};maintained={}
    for u in source_recipe['units']:
        for row in u['providers']:
            provider=load(row['provider'])
            if 'root_anchor' in row:
                marker=row['root_anchor'].encode()+b'\n'
                normalized=provider.replace(b'\r\n',b'\n')
                need(normalized.count(marker)==1,'root declaration anchor differs')
                provider=normalized.split(marker,1)[1].split(b'\n',1)[0]+b'\n'
            providers[row['name']]=provider;maintained[row['name']]=load(row['source'])
        if 'existing_producer' in u:load(u['existing_producer']['source'])
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
        need(done["complete"] and done["native_invocations"]==2 and done["owned_lock_released"] and not done["errors"],"fresh root_tail root/link incomplete")
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
    pair=[]
    for kind in ('target','candidate'):
        m=json.loads((root/recipe['model_phases']['tail'][kind]).read_text())
        need(m['success'] and (m['scenario_count'],m['prefix_count'],m['context_count'])==(3895,24,106),'model counts/results differ')
        need((len(m['cpu']),len(m['prefixes']),len(m['pf_context']))==(3895,24,106),'actual model row counts differ')
        need(sum(r['top_level_calls'] for r in m['cpu'])==8445,'top-level call count differs')
        need(sum(bool(s['fault']) for r in m['cpu'] for s in r['steps'])==10,'actual DIV stop count differs')
        need(m['exe_sha256']==sha(target_raw if kind=='target' else candidate_raw),'model full image differs')
        for dep,h in m['inputs'].items():need(sha((root/dep).read_bytes())==h,'actual model dependency differs: '+dep)
        pair.append(m)
    a,b=pair
    need(a['analysis']==b['analysis'],'root-tail model analysis differs')
    for key in ('cpu','prefixes','pf_context'):
        need(comparable(a[key],'tail')==comparable(b[key],'tail'),'model observations differ: '+key)
    trace=json.loads((root/recipe['producer_trace']).read_text())
    need(trace['producer_count']==len(trace['producers'])==21,'actual producer count differs')
    for row in trace['producers']:
        need(sha((root/row['source']).read_bytes())==row['sha256'],'actual source producer changed')
    need(sha((root/trace['macro']['path']).read_bytes())==trace['macro']['sha256'],'original func/endfunc macro differs')
    target,candidate=parse_mz(target_raw),parse_mz(candidate_raw)
    need(target.valid and candidate.valid,'invalid MZ')
    relocs=lambda m:[(r.segment,r.offset) for r in m.relocations]
    ta,ca=relocs(target),relocs(candidate)
    for unit in recipe['units']:
        start=unit['segment']*16+unit['offset'];end=start+unit['bytes']
        need(target.program_image[start:end]==candidate.program_image[start:end],'root_tail raw bytes differ: '+unit['unit_id'])
        scoped=lambda rows:[r for r in rows if start<=r[0]*16+r[1]<end]
        need(scoped(ta)==scoped(ca)==[],'root-tail relocation sites differ: '+unit['unit_id'])
    return dict(kind='mainl-root-tail-consumed-source-replay',recipe_sha256=sha(raw),
        source_owned_bytes_eligible=722,existing_source_units=recipe['units'],
        native_fragment_consumption_proven=True,fresh_root_link_builds=2,
        raw_repeat_obj_exe_map_equal=True,whole_carrier_exe_map_equal=True,
        ordered_root_tail_relocations_equal=True,root_tail_relocations=0,
        global_relocation_membership_equal=Counter(ta)==Counter(ca),
        global_ordered_difference_count=sum(x!=y for x,y in zip(ta,ca)),
        target_decoded_difference_count=sum(x!=y for x,y in zip(target.program_image,candidate.program_image))+abs(len(target.program_image)-len(candidate.program_image)),
        runtime_observations_equal=True,models_rerun=False,fresh_model_phase_records_retained=2,root_tail_scenarios_per_image=3895,root_tail_calls_per_image=8445,semantic_prefixes_per_image=24,pfopen_context_cases_per_image=106,model_reuse='pinned complete EXE identity; independent full scalar/native comparisons retained',
        prior_scoped_bytes_preserved_by_complete_exe_identity=21565,total_scoped_target_equal_bytes=22287,
        native_invocations_in_this_replay=0,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    text=json.dumps(replay(),indent=2)+"\n"
    if a.output:
        with a.output.open("x") as out:out.write(text)
    else:print(text,end="")
if __name__=="__main__":main()
