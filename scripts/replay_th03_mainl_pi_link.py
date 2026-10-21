#!/usr/bin/env python3
"""Verify two consumed-source PI builds and retained full-image model identity."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from lib import mainl_pi_source as composer
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE="config/th03_mainl_pi_link.json"
RECIPE_SHA="c63859bdd646bbc2460453e092ceef856affbde3e199b1f11cf7eb7c2644f7cc"
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,text):
    if not ok:raise ValueError(text)
def validate_partition(unit):
    need(unit==dict(unit_id="th03-mainl-decoded-pi-decoder-load",segment=0,offset=0x1038,bytes=1524,source_paths=["src/mainl/formats/pi_decode.asm"]),"PI existing-unit partition differs")
def replay(root=ROOT):
    raw=(root/RECIPE).read_bytes()
    need(sha(raw)==RECIPE_SHA,"recipe identity differs")
    recipe=json.loads(raw)
    for path,digest in recipe["proof_inputs_sha256"].items():
        need(sha((root/path).read_bytes())==digest,"retained input differs: "+path)
    validate_partition(recipe["unit"])
    source_recipe=json.loads((root/"config/th03_mainl_pi_source.json").read_text())
    values={}
    for key in ("previous_generated_root","provider","source","composer"):
        row=source_recipe[key];values[key]=(root/row["path"]).read_bytes()
        need(sha(values[key])==row["sha256"],"source recipe identity differs: "+key)
    generated=composer.compose(values["previous_generated_root"],values["provider"],values["source"])
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
        need(done["complete"] and done["native_invocations"]==2 and done["owned_lock_released"] and not done["errors"],"fresh PI root/link incomplete")
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
    models=json.loads((root/recipe["model_proof"]).read_text())
    need(models["candidate_exe_sha256"]==sha(candidate_raw) and models["runtime_equal"] and models["models_rerun"],"retained model full EXE identity differs")
    need(models["scope_bytes"]==1524 and len(models["observations"])==2,"model scope differs")
    normalize=lambda rows:[{k:v for k,v in row.items() if k not in ("memory_before_sha256","memory_after_sha256")} for row in rows]
    a,b=models["observations"]
    for key,count in (("terminal",985),("prefixes",20),("borrower",7)):
        need(len(a[key])==len(b[key])==count and normalize(a[key])==normalize(b[key]),"retained semantic observations differ: "+key)
    target_raw=(root/recipe["decoded_target"]).read_bytes()
    need(models["target_exe_sha256"]==sha(target_raw),"model target identity differs")
    target,candidate=parse_mz(target_raw),parse_mz(candidate_raw)
    need(target.valid and candidate.valid,"invalid MZ")
    need(target.program_image[0x1038:0x162c]==candidate.program_image[0x1038:0x162c],"PI raw bytes differ")
    relocs=lambda m:[(r.segment,r.offset) for r in m.relocations]
    ta,ca=relocs(target),relocs(candidate)
    scoped=lambda rows:[r for r in rows if 0x1038<=r[0]*16+r[1]<0x162c]
    need(scoped(ta)==scoped(ca)==[(0,0x103c),(0,0x1120),(0,0x1179),(0,0x14ec)],"four ordered PI relocations differ")
    return dict(kind="mainl-pi-consumed-source-replay",recipe_sha256=sha(raw),
        source_owned_bytes_eligible=1524,existing_source_units=[recipe["unit"]],
        native_fragment_consumption_proven=True,fresh_root_link_builds=2,
        raw_repeat_obj_exe_map_equal=True,whole_carrier_exe_map_equal=True,
        ordered_pi_relocations_equal=True,pi_relocations=4,
        global_relocation_membership_equal=Counter(ta)==Counter(ca),
        global_ordered_difference_count=sum(x!=y for x,y in zip(ta,ca)),
        target_decoded_difference_count=sum(x!=y for x,y in zip(target.program_image,candidate.program_image))+abs(len(target.program_image)-len(candidate.program_image)),
        runtime_observations_equal=True,models_rerun=False,model_reuse="pinned complete EXE identity",
        prior_scoped_bytes_preserved_by_complete_exe_identity=11971,total_scoped_target_equal_bytes=13495,
        native_invocations_in_this_replay=0,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args()
    text=json.dumps(replay(),indent=2)+"\n"
    if a.output:
        with a.output.open("x") as out:out.write(text)
    else:print(text,end="")
if __name__=="__main__":main()
