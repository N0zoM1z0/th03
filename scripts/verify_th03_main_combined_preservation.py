#!/usr/bin/env python3
"""Four-output preservation proof; never expands original exact scope."""
import argparse, hashlib, importlib.util, json, re, sys, tomllib
from datetime import datetime
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
HELPER_PINS={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
             for p in [Path(__file__).resolve(),HERE/"lib/th03_combined_preservation_layout.py",ROOT/"scripts/lib/pc98.py",ROOT/"scripts/lib/th03_preservation_layout.py"]}
sys.path.insert(0,str(ROOT/"scripts"))
spec=importlib.util.spec_from_file_location("layout_supplement",HERE/"lib/th03_combined_preservation_layout.py")
layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
require=layout.require;parse_mz=layout.parse_mz
LO,HI=0x142D0,0x158F5
REM_END=0x159FF
REIMU="th03-main-reimu-shared-gameplay"
NEW="th03-main-mima-gameplay"
MARISA="th03-main-marisa-gameplay"
TARGET_SHA=layout.TARGET_SHA
def sha(b):return hashlib.sha256(b).hexdigest()
outside_relocs=layout.outside_relocs
def receipt_shape(r,candidate,not_before):
    require(r.get("kind")=="th03-main-owned-extent-cold-replay","wrong receipt kind")
    require(r.get("pass") is True,"original aggregate gates did not pass")
    require(r.get("target_sha256")==TARGET_SHA,"wrong target")
    stamp=datetime.fromisoformat(r["observed_utc"])
    require(stamp.tzinfo is not None and stamp>=not_before,"receipt is not fresh")
    require(bool(r.get("candidate_manifest"))==candidate,"default/candidate role mismatch")
    require(sorted(r["selected_units"])==sorted(r["aggregate_units"]),"partial selection forbidden")
    require(r.get("owned_extent_bytes")== (59624 if candidate else 53122),"unexpected aggregate byte scope")
    require(len(r["rounds"])==2 and [x["round"] for x in r["rounds"]]==[1,2],"missing two independent rounds")
    for key in ("objects_metadata_normalized_equal","candidate_equal","all_products_equal","game_objects_metadata_normalized_equal"):
        require(r.get(key) is True,"failed original gate: "+key)
    for rd in r["rounds"]:
        require(rd.get("fresh_owned_objects") is True and rd.get("behavior_pass") is True,"round not fresh/passing")
        require(len(rd["units"])==(78 if candidate else 74),"missing owner extents")
        require(len(rd["functions"])==(371 if candidate else 334),"missing function gates")
        for field in ("functions","units","producer_ranges"):
            for item in rd[field]:
                require(item["raw_equal"] is True and item["relocations_equal"] is True and item.get("ordered_relocations_equal") is True,"original raw/order gate failure")
        for item in rd["auxiliary_map_contributions"]:
            require(not item["raw_compare"] or(item["raw_equal"] and item["relocations_equal"]),"original DATA gate failed")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--default-receipt",type=Path,required=True)
    p.add_argument("--candidate-receipt",type=Path,required=True)
    p.add_argument("--default-completion",type=Path,required=True)
    p.add_argument("--candidate-completion",type=Path,required=True)
    p.add_argument("--launch-plan",type=Path,required=True)
    p.add_argument("--launch-plan-sha256",required=True)
    p.add_argument("--not-before",required=True,help="Explicit UTC start bound for these newly scheduled runs")
    p.add_argument("--report",type=Path,required=True)
    a=p.parse_args(); out=a.report.resolve()
    require(out.is_relative_to((ROOT/".analysis").resolve()) and out.parent.is_dir() and not out.exists(),"new report path under existing .analysis directory required")
    inputs={}
    def read(path):
        path=path.resolve()
        require(path.is_relative_to(ROOT),"outside repository")
        b=path.read_bytes();inputs[str(path.relative_to(ROOT))]={"sha256":sha(b),"size":len(b)};return b
    result={"kind":"four-output-baseline-preservation","authored_byte_credit":0,
            "exact_acceptance":False,"factory_acceptance":False,
            "baseline_preservation_proved":False,"target_hitbox_tail_exact":False,"target_comparison_scope":{"name":"retained_hitbox_tail","payload_start":0x158F5,"payload_end_exclusive":0x159FF}}
    try:
        cutoff=datetime.fromisoformat(a.not_before);require(cutoff.tzinfo is not None,"timezone required")
        require(a.default_receipt.resolve()!=a.candidate_receipt.resolve(),"distinct fresh runs required")
        plan_raw=read(a.launch_plan);require(sha(plan_raw)==a.launch_plan_sha256,"technical launch plan pin mismatch")
        plan=json.loads(plan_raw)
        layout.check_launch(plan,ROOT,read)
        require(datetime.fromisoformat(plan["scheduled_not_before_utc"])==cutoff,"cutoff differs from launch plan")
        require(plan["run_ids"]==[a.default_receipt.resolve().parent.name,a.candidate_receipt.resolve().parent.name],"run pair differs from launch plan")
        require(plan["verifier_sha256"]==HELPER_PINS[str(Path(__file__).resolve().relative_to(ROOT))],"verifier differs from launch plan")
        require(plan["layout_helper_sha256"]==HELPER_PINS[str((HERE/"lib/th03_combined_preservation_layout.py").relative_to(ROOT))],"layout helper differs from launch plan")
        for name,pin in HELPER_PINS.items():
            require(sha(read(ROOT/name))==pin,"helper changed before use: "+name)
        receipts=[];sets=[];attestations=[];completions=[]
        for path,completion_path,is_candidate in [(a.default_receipt,a.default_completion,False),(a.candidate_receipt,a.candidate_completion,True)]:
            raw_receipt=read(path);r=json.loads(raw_receipt);receipt_shape(r,is_candidate,cutoff)
            require(r["source_inputs"]==plan["expected_source_inputs"]["candidate" if is_candidate else "default"],"frozen source inventory differs from launch pins")
            require(path.resolve()==ROOT/".analysis/th03-main-exact"/r["run_id"]/"receipt.json","unexpected receipt namespace")
            completion=json.loads(read(completion_path))
            for key in ("supervisor_script_sha256","schedule_adapter_sha256","original_replay_sha256"):
                require(completion[key]==plan[key],"execution tooling differs from launch plan: "+key)
            require(completion["source_inputs_unchanged"] is True,"supervisor source guards failed")
            frozen_guard=[]
            for stem in ("before","after"):
                data=read(ROOT/completion[f"inputs_{stem}_path"])
                require(sha(data)==completion[f"inputs_{stem}_sha256"],"supervisor input manifest drift")
                frozen_guard.append(json.loads(data))
            require(frozen_guard[0]==frozen_guard[1],"supervisor before/after source differs")
            require(completion["run_id"]==r["run_id"] and completion["receipt_path"]==str(path.resolve().relative_to(ROOT)),"completion identity mismatch")
            require(completion["receipt_sha256"]==sha(raw_receipt) and completion["receipt_pass"] is True and completion["replay_exit_code"]==0,"completion receipt not passing")
            times=[datetime.fromisoformat(completion[k]) for k in ("scheduled_at_utc","supervisor_started_at_utc","replay_started_at_utc")]
            require(all(t.tzinfo is not None for t in times) and cutoff<=times[0]<=times[1]<=times[2]<=datetime.fromisoformat(r["observed_utc"]),"fresh schedule/start evidence missing")
            att=completion["tool_attestation"];att_raw=read(ROOT/att["path"])
            require(sha(att_raw)==att["sha256"]==r["toolchain_receipt_sha256"],"archived tool attestation drift")
            tool=json.loads(att_raw)
            require(all(tool.get(k) is True for k in ("ready","identity_pass","execution_pass")),"tool attestation failed")
            require(all(x["pass"] is True for x in tool["surfaces"] if x["required"]),"required tool surface failed")
            attestations.append({k:tool[k] for k in ("schema_version","manifest_sha256","selected_surface_ids","surfaces")})
            completions.append(completion)
            run=path.resolve().parent
            require(r["run_id"]==run.name,"run identity mismatch")
            for name,pin in completion["schedule_sidecars"].items():
                # Runner's explicitly documented keys are relative to replay output.
                require(sha(read(run/name))==pin,"schedule sidecar drift")
            require(completion["original_replay_sha256"]==r["source_inputs"]["scripts/replay_th03_main_exact_units.py"],"scheduled original replay differs")
            require(r["source_inputs"]["scripts/lib/pc98.py"]==HELPER_PINS["scripts/lib/pc98.py"],"parser differs from frozen replay inputs")
            for name,pin in r["source_inputs"].items():
                require(sha(read(run/"repository-inputs"/name))==pin,"frozen source guard mismatch: "+name)
            require(sha(read(run/"reference.tar"))==r["reference_archive_sha256"],"reference archive drift")
            images=[]
            for rd in r["rounds"]:
                work=run/f"round{rd['round']}"/"source"
                b=read(work/"bin/th03/main.exe")
                require(sha(b)==rd["candidate_sha256"],"output differs from original receipt")
                require(b==read(run/f"round{rd['round']}"/"main.exe"),"retained output copies disagree")
                mapb=read(work/"obj/th03/main.map")
                require(sha(mapb)==completion["maps"][f"round{rd['round']}/source/obj/th03/main.map"],"completion MAP pin differs")
                lines=mapb.decode("ascii").splitlines()
                for item in rd["map_contributions"]+rd["auxiliary_map_contributions"]:
                    require(sum(line.strip()==item["map"].strip() for line in lines)==1,"receipt MAP row absent/duplicated")
                require(mapb==read(run/f"round{rd['round']}"/"main.map"),"retained MAP copies disagree")
                im=parse_mz(b);require(im.valid,"invalid MZ")
                rows=layout.contributions(mapb.decode("ascii"));require(rows,"missing detailed MAP")
                images.append((im,rows,mapb.decode("ascii"),work))
            require(images[0][0].raw==images[1][0].raw,"round image determinism failed")
            receipts.append(r);sets.append(images)
        default,candidate=receipts
        require(attestations[0]==attestations[1],"normalized tool surface identities differ")
        require(completions[0]["execution_limits"]==completions[1]["execution_limits"],"execution scheduling limits differ")
        require(set(candidate["aggregate_units"])==set(default["aggregate_units"])|{MARISA,REIMU,NEW},"aggregate owner change exceeds combined proposal")
        require(NEW not in default["aggregate_units"],"default already includes candidate")
        for k in ("target_sha256","reference_revision","reference_archive_sha256","compiler_flags","accepted_units_at_start","environment","determinism_object_roots"):
            require(default[k]==candidate[k],"baseline/candidate configuration differs: "+k)
        for k in set(default["source_inputs"])&set(candidate["source_inputs"]):
            require(default["source_inputs"][k]==candidate["source_inputs"][k],"shared source differs: "+k)
        manifest_path=a.candidate_receipt.resolve().parent/"repository-inputs"/candidate["candidate_manifest"]
        manifest=tomllib.loads(read(manifest_path).decode())
        units=manifest["units"]
        require([u["id"] for u in units]==[MARISA,REIMU,NEW],"candidate must contain retained Marisa then Reimu then Mima")
        old=tomllib.loads(read(ROOT/"config/th03_main_reimu_shared_candidate.toml").decode())
        require(units[:2]==old["units"] and manifest["functions"][:24]==old["functions"],"retained Marisa declaration changed")
        require(candidate["candidate_manifest"]==plan["candidate_manifest"],"candidate manifest path differs")
        require(sha(read(manifest_path))==plan["candidate_manifest_sha256"],"combined manifest pin differs")
        allowed_additions={candidate["candidate_manifest"]}
        for unit in units:
            allowed_additions.update(unit.get("support_files",[]))
            allowed_additions|={unit["source"],unit["header"]}|{x["source"] for x in unit["physical_objects"]}
        require(not(set(default["source_inputs"])-set(candidate["source_inputs"])),"candidate drops frozen input")
        require(set(candidate["source_inputs"])-set(default["source_inputs"])<=allowed_additions,"unrelated source-input additions")
        require([[x["object"] for x in u["physical_objects"]] for u in units]==[["cs_mari","bm_mari"],["cs_reimu","bm_reish"],["cs_mima","bm_mima"]],"six semantic producers required")
        bindings=json.loads(read(ROOT/plan["source_bindings"]))
        for name,binding in bindings["complete_combined_source_inputs"].items():
            require(candidate["source_inputs"].get(name)==binding["sha256"],"candidate source differs from final proposal: "+name)
        base=tomllib.loads(read(ROOT/"config/th03_main_exact_units.toml").decode())
        target=parse_mz(read(ROOT/".analysis/targets/th03/main.exe"))
        require(sha(target.raw)==TARGET_SHA and target.valid,"canonical target mismatch")
        truth=[];allocations=[]
        for role,images in zip(("default","candidate"),sets):
            for index,(im,rows,text,work) in enumerate(images,1):
                require(len(im.program_image)==len(target.program_image),"load size moved")
                target_rs=layout.relocs(target,HI,REM_END);rs=layout.relocs(im,HI,REM_END)
                truth.append({"role":role,"round":index,"raw_equal":im.program_image[HI:REM_END]==target.program_image[HI:REM_END],
                              "ordered_relocations_equal":rs==target_rs,"target_relocations":target_rs,"output_relocations":rs})
                allocations.append(layout.allocation_rows(rows,role=="candidate"))
                if role=="candidate":
                    layout.check_layout(rows,True);layout.check_aliases(text)
                layout.check_map_scope(rows,[base]+([manifest] if role=="candidate" else []))
                layout.check_actual(im,target,receipts[0 if role=="default" else 1]["rounds"][index-1],base,manifest,role=="candidate")
        result["target_comparisons"]=truth
        require(all(x==allocations[0] for x in allocations),"full preexisting DATA/BSS allocation rows changed")
        reference=sets[0][0][0]
        for images in sets:
            for im,rows,text,work in images:
                require(layout.outside_bytes(im)==layout.outside_bytes(reference),
                        "unaffected load-payload bytes changed")
                require(outside_relocs(im)==outside_relocs(reference),"ordered outside-owner relocations changed")
                require(im.overlay==reference.overlay,"overlay changed")
                require((im.header.minimum_extra_allocation,im.header.maximum_extra_allocation,im.header.initial_relative_ss,im.header.initial_sp,im.header.initial_relative_cs,im.header.initial_ip,im.header.overlay_number)==
                        (reference.header.minimum_extra_allocation,reference.header.maximum_extra_allocation,reference.header.initial_relative_ss,reference.header.initial_sp,reference.header.initial_relative_cs,reference.header.initial_ip,reference.header.overlay_number),
                        "allocation/stack header contract changed")
                for seg,off,size,kind,*_ in allocations[0]:
                    lo=seg*16+off;hi=lo+size
                    require(layout.relocs(im,lo,hi)==layout.relocs(reference,lo,hi),"DATA/BSS relocation sequence changed")
                    file_end=min(hi,len(im.program_image))
                    if lo<file_end:
                        require(im.program_image[lo:file_end]==reference.program_image[lo:file_end],"allocated file-backed bytes changed")
        # Entire carrier must equal the baseline with only declared edits.
        source_parts=[]
        reference_source=read(sets[0][0][3]/"th03_main.asm")
        expected=layout.apply_carrier(reference_source,units)
        for role,images in zip(("default","candidate"),sets):
            for im,rows,text,work in images:
                source=read(work/"th03_main.asm")
                require(source==(reference_source if role=="default" else expected),"carrier changes exceed declared edits")
        original_publics=layout.publics(sets[0][0][2])
        for images in sets:
            for im,rows,text,work in images:
                layout.check_publics(original_publics,text)
        result.update(baseline_preservation_proved=True,original_gates_pass=True,target_comparisons=truth,
                      target_hitbox_tail_exact=all(x["raw_equal"] and x["ordered_relocations_equal"] for x in truth),
                      preserved_scope="entire load payload except combined Marisa/Reimu/Mima [0x142D0,0x158F5) and [0x17043,0x17384); ordered relocation subsequence; DATA/BSS metadata and file-backed contents",
                      bss_note="Uninitialized virtual BSS has no file bytes; allocation metadata and aliases are checked.",
                      header_diagnostics=[{"header_size":im.header.header_size,"relocation_count":im.header.number_of_relocations,"checksum":im.header.checksum} for images in sets for im,rows,text,work in images],
                      allocation_rows=len(allocations[0]),declared_carrier_sha256=sha(expected))
    except Exception as e:
        result["error"]=repr(e)
    result["inputs"]=inputs
    try:
        for name,pin in inputs.items():
            require(sha((ROOT/name).read_bytes())==pin["sha256"],"input changed during verification: "+name)
    except Exception as e:
        result["baseline_preservation_proved"]=False
        result["post_read_guard_error"]=repr(e)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("inputs","target_comparisons")},indent=2))
    return 0 if result["baseline_preservation_proved"] else 1
if __name__=="__main__":sys.exit(main())
