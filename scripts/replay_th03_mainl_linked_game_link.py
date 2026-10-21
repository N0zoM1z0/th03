"""Replay retained MAINL linked-game source/build/model evidence; no native invocation."""
import argparse,json,hashlib
from pathlib import Path
from collections import Counter
from lib import mainl_linked_game_source as composer
from lib.pc98 import parse_mz
ROOT=Path(__file__).resolve().parents[1]
RECIPE="config/th03_mainl_linked_game_link.json"
RECIPE_SHA="61b21570918fa0d1cae88b0d652fe90d356ba346e1af3da56a5c4166ddedfae7"
COUNTS={"lifecycle":51,"input":254,"sound":1560,"linked_tail":493,"staff":649,"cfg_windows":489}
EXCLUDED={"input":("before_sha256","after_sha256"),"sound":("before_sha256","after_sha256"),"linked_tail":("memory_before_sha256","memory_after_sha256")}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def validate_partition(units):
    expected=[('th03-mainl-decoded-linked-tail-planes', 3198, 2, 41), ('th03-mainl-decoded-sound-mode', 3198, 44, 29), ('th03-mainl-decoded-linked-tail-producer-0049', 3198, 73, 1), ('th03-mainl-decoded-sound-pmd', 3198, 74, 57), ('th03-mainl-decoded-linked-tail-producer-0083', 3198, 131, 1), ('th03-mainl-decoded-sound-volume', 3198, 132, 27), ('th03-mainl-decoded-linked-tail-producer-009f', 3198, 159, 1), ('th03-mainl-decoded-sound-reset', 3198, 1630, 11), ('th03-mainl-decoded-linked-tail-producer-0669', 3198, 1641, 1), ('th03-mainl-decoded-lifecycle-exit', 3198, 432, 67), ('th03-mainl-decoded-input-sense', 3198, 904, 417), ('th03-mainl-decoded-sound-kaja', 3198, 1762, 30), ('th03-mainl-decoded-cfg-resident', 2399, 3, 49), ('th03-mainl-decoded-lifecycle-init', 3198, 1792, 62), ('th03-mainl-decoded-sound-play', 3198, 1642, 60), ('th03-mainl-decoded-sound-update', 3198, 1702, 60), ('th03-mainl-decoded-win-load', 2399, 52, 282), ('th03-mainl-decoded-win-text', 2399, 334, 56), ('th03-mainl-decoded-staff-flake', 2399, 9370, 76), ('th03-mainl-decoded-lifecycle-exit-to-main', 3198, 2447, 40), ('th03-mainl-decoded-sound-measure', 3198, 3100, 49), ('th03-mainl-decoded-staff-music', 2399, 9022, 68), ('th03-mainl-decoded-staff-ending', 2399, 9090, 280)]
    sources=[['src/mainl/linked_game/planes.cpp'], ['src/mainl/linked_game/sound_mode.c'], ['src/mainl/linked_game/sound_mode.c'], ['src/mainl/linked_game/sound_pmd.c'], ['src/mainl/linked_game/sound_pmd.c'], ['src/mainl/linked_game/sound_volume.c'], ['src/mainl/linked_game/sound_volume.c'], ['src/mainl/linked_game/sound_reset.cpp'], ['src/mainl/linked_game/sound_reset.cpp'], ['src/mainl/linked_game/exit.cpp'], ['src/mainl/linked_game/input_sense.cpp'], ['src/mainl/linked_game/sound_kaja.cpp'], ['src/mainl/linked_game/cfg_resident.cpp'], ['src/mainl/linked_game/init.cpp'], ['src/mainl/linked_game/sound_se.cpp'], ['src/mainl/linked_game/sound_se.cpp'], ['src/mainl/linked_game/win.cpp'], ['src/mainl/linked_game/win.cpp'], ['src/mainl/linked_game/flake.cpp'], ['src/mainl/linked_game/exit_to_main.cpp'], ['src/mainl/linked_game/sound_measure.cpp'], ['src/mainl/linked_game/staff_flow.asm'], ['src/mainl/linked_game/staff_flow.asm']]
    need([(u["unit_id"],u["segment"],u["offset"],u["bytes"]) for u in units]==expected,"linked-game existing-unit partition differs")
    need([u["source_paths"] for u in units]==sources,"linked-game actual source ownership differs")
def comparable(rows,name):
    need(name in COUNTS,"unknown model comparison contract")
    if name not in EXCLUDED:return rows
    return [{k:v for k,v in row.items() if k not in EXCLUDED[name]} for row in rows]
def replay(root=ROOT):
    raw=(root/RECIPE).read_bytes();need(sha(raw)==RECIPE_SHA,"recipe identity differs");r=json.loads(raw)
    for path,h in r["proof_inputs_sha256"].items():need(sha((root/path).read_bytes())==h,"retained input differs: "+path)
    def read(path):return (root/path).read_bytes()
    def doc(path):return json.loads(read(path))
    source=doc("config/th03_mainl_linked_game_source.json");validate_partition(r["units"])
    def source_read(row):
        raw=read(row["path"]);need(sha(raw)==row["sha256"],"source input differs: "+row["path"]);return raw
    providers={p["name"]:source_read(p["provider"]) for p in source["providers"]}
    wrappers={p["name"]:source_read(p["wrapper"]) for p in source["providers"]}
    maintained={p["name"]:source_read(p["source"]) for p in source["providers"]}
    for p in source["compatibility_inputs"]:need(source_read(p)==p["text"].encode(),"compatibility forwarder differs")
    generated=composer.compose(source_read(source["previous_generated_root"]),providers,wrappers,maintained,source_read(source["staff_source"]),source)
    need(len(generated)==56,"consumed source output count differs")
    expected_phases=[p["name"] for p in source["providers"]]+["root","link"]
    expected_products=[p["object"] for p in source["providers"]]+["obj/th03/mainl.obj","bin/th03/mainl.exe","obj/th03/mainl.map"]
    need(len(expected_products)==18,"rebuilt output count differs")
    products=[];all_phases=0
    for build in r["builds"]:
        work=root/build["work"];previous=None;seen=[];initial_inputs=None;initial_mtimes=None
        need(len(build["groups"])==4,"four bounded groups required")
        for index,group in enumerate(build["groups"]):
            output=group["output"];m=doc(group["proposal"]+"/manifest.json");done=doc(output+"/completion.json")
            phases=expected_phases[index*5:index*5+5] if index<3 else ["root","link"]
            need(m["phases"]==phases and done["phases"]==phases,"native group phase partition differs")
            need(done["complete"] and done["owned_lock_released"] and not done["errors"] and done["native_invocations"]==len(phases),"native group did not finish cleanly")
            need(done["round"]==build["round"] and done["group"]=="ABCD"[index],"group identity differs")
            need(m["all_native_outputs"]==expected_products,"actual rebuilt product list differs")
            need(not set(expected_products)&set(m["repeat_inputs"]),"rebuilt output copied as input")
            if previous:
                need(m["predecessor"]["path"]==previous+"/completion.json" and m["predecessor"]["sha256"]==sha(read(previous+"/completion.json")),"predecessor chain differs")
                need(m["registry_baseline"]==doc(previous+"/next-registry-baseline.json"),"registry continuation differs")
                need(m["accumulated_objects"]==doc(previous+"/accumulated-objects.json"),"prior object continuation differs")
                need(m["materialized_inputs"]==initial_inputs and m["source_mtimes"]==initial_mtimes,"source continuation differs")
            for phase in phases:
                start=doc(output+"/"+phase+"-started.json");end=doc(output+"/"+phase+"-finished.json");transition=doc(output+"/"+phase+"-registry-transition.json")
                need(start["argv"]==m["native_argv"][phase] and start["wait_seconds"]==90 and start["cleanup_seconds"]==15,"actual command/budget differs")
                need(end["exit_code"]==0 and not any(end[k] for k in ("timeout","cleanup_uncertain","poison","survivors","errors")) and transition["ok"],"native exit/owned cleanup differs")
                if phase not in ("root","link"):
                    row=next(p for p in source["providers"] if p["name"]==phase)
                    need(start["argv"][4]=="tcc" and start["argv"][5:]==row["compiler_flags"]+[row["wrapper_relative"]],"actual first-use TCC flags differ")
                    need(m["native_outputs"][phase]==row["object"],"TCC object ownership differs")
                seen.append(phase)
            materialized=doc(output+"/materialized-inputs.json");mtimes=doc(output+"/source-mtimes.json")
            if initial_inputs is None:initial_inputs,initial_mtimes=materialized,mtimes
            need(materialized==initial_inputs and mtimes==initial_mtimes,"captured materialized source changed between groups")
            accumulated=doc(output+"/accumulated-objects.json")
            for name,pin in accumulated.items():need(sha((work/name).read_bytes())==pin["sha256"],"actual compiled product changed")
            previous=output
        need(seen==expected_phases,"all fifteen TUs plus root/link must execute")
        all_phases+=len(seen)
        for path,content in generated.items():need((work/path).read_bytes()==content,"consumed maintained source differs: "+path)
        for path,pin in initial_inputs.items():need(sha((work/path).read_bytes())==pin["sha256"],"materialized contextual input differs: "+path)
        for path,t in initial_mtimes.items():need((work/path).stat().st_mtime_ns==t,"materialized source mtime differs: "+path)
        if build["round"]==2:
            first=root/r["builds"][0]["work"]
            for path in initial_inputs:need((first/path).read_bytes()==(work/path).read_bytes() and (first/path).stat().st_mtime_ns==initial_mtimes[path],"repeat observed-input identity/mtime differs")
        products.append({p:(work/p).read_bytes() for p in expected_products})
    need(len(products)==2 and products[0]==products[1] and all_phases==34,"two rounds/18 raw products differ")
    candidate_raw=products[0]["bin/th03/mainl.exe"];target_raw=read(r["decoded_target"])
    need(candidate_raw==read(r["previous_exe"]) and products[0]["obj/th03/mainl.map"]==read(r["previous_map"]),"whole carrier EXE/MAP differs")
    need(set(r["model_phases"])==set(COUNTS),"complete model set required")
    for name,paths in r["model_phases"].items():
        pair=[]
        for kind in ("target","candidate"):
            model=doc(paths[kind]);need(model["success"] and model["module"]==name and model["scenario_count"]==COUNTS[name],"model count/status differs")
            need(model["exe_sha256"]==sha(target_raw if kind=="target" else candidate_raw),"model full EXE identity differs")
            for dep,h in model["inputs"].items():need(sha(read(dep))==h,"actual model dependency differs: "+dep)
            if name=="staff":
                cpu=model["cpu"];need([len(cpu[k]) for k in ("ending_cases","failed_interface_cases","flake_cases")]==[512,4,132] and "music_case" in cpu,"STAFF scenario partition differs")
            else:need(len(model["cpu"])==COUNTS[name],"actual model row count differs")
            if name=="cfg_windows":need(sum(len(row["events"]) for row in model["cpu"])==4723,"CFG/window foreign call count differs")
            pair.append(model)
        need(pair[0]["analysis"]==pair[1]["analysis"] and comparable(pair[0]["cpu"],name)==comparable(pair[1]["cpu"],name),"independent model observations differ: "+name)
    controls=doc(r["cfg_tests"])
    need(controls["success"] and controls["tests"]==2 and controls["cpu_mutations_rejected"]==9 and controls["exe_sha256"]==sha(candidate_raw),"CFG/window real mutation controls differ")
    target,candidate=parse_mz(target_raw),parse_mz(candidate_raw);need(target.valid and candidate.valid,"invalid MZ")
    ta=[(x.segment,x.offset) for x in target.relocations];ca=[(x.segment,x.offset) for x in candidate.relocations];scopes=[]
    for u in r["units"]:
        start=u["segment"]*16+u["offset"];end=start+u["bytes"]
        need(target.program_image[start:end]==candidate.program_image[start:end],"linked-game raw scope differs: "+u["unit_id"])
        a=[x for x in ta if start<=x[0]*16+x[1]<end];b=[x for x in ca if start<=x[0]*16+x[1]<end]
        need(Counter(a)==Counter(b),"scoped relocation membership differs")
        scopes.append({"unit_id":u["unit_id"],"bytes":u["bytes"],"raw_equal":True,"relocation_membership_equal":True,"ordered_relocations_equal":a==b,"relocation_sites":len(a),"ordered_difference_count":sum(x!=y for x,y in zip(a,b))})
    diffs=[{"linear":i,"target":a,"candidate":b} for i,(a,b) in enumerate(zip(target.program_image,candidate.program_image)) if a!=b]
    need(len(target.program_image)==len(candidate.program_image) and diffs==[{"linear":60473,"target":144,"candidate":0}],"whole decoded outside differences changed")
    need(Counter(ta)==Counter(ca) and len(ta)==677 and sum(x!=y for x,y in zip(ta,ca))==461,"global relocation context changed")
    return dict(kind="mainl-linked-game-consumed-source-replay",recipe_sha256=sha(raw),source_owned_bytes_eligible=1765,existing_source_units=r["units"],
        native_fragment_consumption_proven=True,fresh_producer_link_builds=2,successful_native_invocations=34,rebuilt_objects_per_round=16,
        raw_repeat_obj_exe_map_equal=True,raw_repeat_products=18,whole_carrier_exe_map_equal=True,scoped_comparisons=scopes,
        ordered_linked_game_relocations_equal=all(s["ordered_relocations_equal"] for s in scopes),global_relocation_membership_equal=True,global_ordered_difference_count=461,target_decoded_difference_count=1,target_decoded_differences=diffs,
        runtime_observations_equal=True,models_rerun=False,fresh_model_phase_records_retained=12,scenarios_per_image=3496,cfg_window_cpu_negative_controls=9,
        model_reuse="Pinned full EXE identity and actual imported model dependencies; explicit per-module diagnostic comparison contracts retained.",
        prior_scoped_bytes_preserved_by_complete_exe_identity=22287,total_scoped_target_equal_bytes=24052,
        native_invocations_in_this_replay=0,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args();text=json.dumps(replay(),indent=2)+"\n"
    if a.output:
        with a.output.open("x") as out:out.write(text)
    else:print(text,end="")
if __name__=="__main__":main()
