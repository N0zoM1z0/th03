"""Read-only paired composition diagnostics. Context is not owned source credit."""
import json
from pathlib import Path
import re
import sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import replay_th03_mainl_regist as reg
import replay_th03_mainl_cutscene as cut
from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows,extent_observation
from importlib.metadata import version
sha=reg.sha
require=reg.require
OWNED=(('th03/cutscene.cpp',0x0b3e,3195,'CUTSCENE_TEXT',56),
       ('th03/scoredat.cpp',0x17b9,229,'SCOREDAT_TEXT',0),
       ('th03/regist.cpp',0x189e,2720,'REGIST_TEXT',54))

def byte_differences(left,right):
    return [{'linear':i,'left':left[i] if i<len(left) else None,
             'right':right[i] if i<len(right) else None}
            for i in range(max(len(left),len(right)))
            if (left[i] if i<len(left) else None)!=(right[i] if i<len(right) else None)]

def relocation_differences(left,right):
    a=reg.ordered_relocations(left);b=reg.ordered_relocations(right)
    ac=Counter(map(tuple,a));bc=Counter(map(tuple,b))
    return {'left_count':len(a),'right_count':len(b),'ordered_equal':a==b,
            'membership_equal':ac==bc,
            'ordered_differences':[{'index':i,'left':a[i] if i<len(a) else None,
                                    'right':b[i] if i<len(b) else None}
                for i in range(max(len(a),len(b)))
                if (a[i] if i<len(a) else None)!=(b[i] if i<len(b) else None)],
            'left_only':[[*key,count] for key,count in sorted((ac-bc).items())],
            'right_only':[[*key,count] for key,count in sorted((bc-ac).items())]}

def scoped_rows(text,image):
    rows=code_rows(text,len(image.program_image));result=[]
    for module,offset,size,name,relocs in OWNED:
        found=[r for r in rows if r['module']==module and r['size']]
        require(len(found)==1,'owned module not unique '+module)
        row=found[0]
        require((row['segment'],row['offset'],row['size'],row['name'])==(0x095f,offset,size,name),'owned coordinates differ '+module)
        result.append(row)
    scanner=[r for r in rows if r['module']=='th03/input_s.cpp' and r['size']]
    require(len(scanner)==1 and (scanner[0]['segment'],scanner[0]['offset'],scanner[0]['size'])==(0x0c7e,0x0388,418),'frozen contextual scanner coordinates/418-byte extent differ')
    for symbol,offset in [('pi_palette_apply',0x052a),('pi_put_8',0x054f),('pi_put_interlace_8',0x05d7)]:
        found=set((int(a,16),int(b,16)) for a,b in re.findall(r'^\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+'+re.escape(symbol)+r'\(',text,re.M))
        require(found=={(0x0c7e,offset)},'PI public coordinate differs '+symbol)
    return result,scanner[0]

def verify(first_exe,second_exe,first_map,second_map,cached_exe,cached_map,target_exe):
    inputs=dict(first_exe=first_exe,second_exe=second_exe,first_map=first_map,second_map=second_map,cached_exe=cached_exe,cached_map=cached_map,target_exe=target_exe)
    require(all(type(v) is bytes for v in inputs.values()),'immutable bytes required')
    require(sha(cached_exe)==reg.CACHED_EXE_SHA256 and sha(cached_map)==reg.CACHED_MAP_SHA256,'old carrier pins differ')
    require(sha(target_exe)==reg.TARGET_EXE_SHA256,'decoded target pin differs')
    require(first_exe==second_exe and first_map==second_map,'paired raw EXE/MAP differ')
    images={n:parse_mz(inputs[n]) for n in ['first_exe','second_exe','cached_exe','target_exe']}
    require(all(m.valid for m in images.values()),'invalid MZ')
    target=images['target_exe'];first=images['first_exe'];extents=[];observations=[];summaries=[]
    for label in ('first','second'):
        image=images[label+'_exe'];rows,scanner=scoped_rows(inputs[label+'_map'].decode('ascii'),image)
        current=[]
        for row,spec in zip(rows,OWNED):
            extent=extent_observation(target,image,row);start=row['start'];end=start+row['size']
            require(target.program_image[start:end]==image.program_image[start:end],'owned raw target mismatch '+row['module'])
            words=reg.scoped_relocation_words(image,row);target_words=reg.scoped_relocation_words(target,row)
            require(extent['ordered_relocations_equal'] and len(words)==spec[4] and words==target_words,'owned ordered relocation words differ '+row['module'])
            current.append(dict(extent,raw_difference_offsets=[],ordered_relocation_words=words,ordered_relocation_words_equal=True))
        observed={'registration':reg.runtime_matrix(image),'cutscene':cut.runtime_matrix(image)}
        observations.append(observed);summaries.append({'product':label,'registration':reg.runtime_summary(observed['registration']),'cutscene':cut.runtime_summary(observed['cutscene'])});extents.append(current)
    target_observed={'registration':reg.runtime_matrix(target),'cutscene':cut.runtime_matrix(target)}
    require(observations[0]==observations[1]==target_observed,'paired/target selected runtime differs')
    summaries.append({'product':'target','registration':reg.runtime_summary(target_observed['registration']),'cutscene':cut.runtime_summary(target_observed['cutscene'])})
    require(extents[0]==extents[1],'paired owned extent diagnostics differ')
    full_diffs=byte_differences(target.program_image,first.program_image)
    intervals=[(r['start'],r['start']+r['size']) for r in rows]
    require(not any(any(a<=d['linear']<b for a,b in intervals) for d in full_diffs),'full differences overlap owned scopes')
    return {'kind':'th03-mainl-contextual-pi-composition-diagnostics','diagnostic_checks_pass':True,
        'inputs_sha256':{n:sha(v) for n,v in inputs.items()},'raw_exe_pair_equal':True,'raw_map_pair_equal':True,
        'raw_exe_equal_old_carrier':first_exe==cached_exe,'raw_map_equal_old_carrier':first_map==cached_map,
        'raw_exe_equal_target':first_exe==target_exe,'decoded_image_equal_target':first.program_image==target.program_image,
        'owned_bytes':6144,'owned_extents':extents[0],'owned_raw_target_equal':True,'owned_ordered_relocation_words_equal':True,
        'contextual_scanner':dict(scanner,owned=False,trailing_original_codestring_unowned=True),
        'pi_entries':{'palette':'0C7E:052A','put':'0C7E:054F','interlace':'0C7E:05D7'},
        'full_decoded_target_differences':full_diffs,'full_decoded_target_difference_count':len(full_diffs),
        'full_decoded_old_carrier_differences':byte_differences(images['cached_exe'].program_image,first.program_image),
        'full_target_relocations':relocation_differences(target,first),
        'full_old_carrier_relocations':relocation_differences(images['cached_exe'],first),
        'full_pair_relocations':relocation_differences(first,images['second_exe']),
        'runtime_runs':summaries,'selected_runtime':observations[0],'runtime_observations_equal':True,
        'runtime_scope':'Per image: registration152 calls (151 terminal,1 deliberate budget), cutscene65 selected calls/53 scenarios. Three images explicitly executed; foreign interfaces modeled. No physical or whole-runtime proof.',
        'cold_whole_program':False,'whole_runtime_proved':False,'source_acceptance':False,'exact_acceptance':False,
        'native_provenance':'Caller separately binds current link commands and preexisting independently compiled maintained object pairs. Scanner is frozen context only.',
        'tools':{n:version(n) for n in ('capstone','unicorn')}}

PROOF_DIRECTORY = ".analysis/mainl-pi-composition-output-20261021-v01"
WORK = ".analysis/toolchain/wineprefix/drive_c/MPC01"
RETAINED_PINS = {'.analysis/mainl-pi-composition-output-20261021-v01/manifest.json': 'a62849ace60e1c6dd5ba907784a534331dcc5be47b13a1e0c5a28a4e6d64bbcc', '.analysis/mainl-pi-composition-output-20261021-v01/completion.json': 'eb14782edab4967c9684d8051f61b5aa63374d579be7124b8c4a7df056a5219c', '.analysis/mainl-pi-composition-output-20261021-v01/scope.json': '4d459309ea0584cd02ad2301b1936bbdebd882bf56d413e0eaa88d37be77de5d', '.analysis/mainl-pi-composition-output-20261021-v01/scanner-object.json': '43197673a4bed364e2928491b106f8cebc63ef77ceac18c804cd195f02beab30', '.analysis/mainl-pi-composition-output-20261021-v01/scanner-producer.json': 'dec685a7620a62d67d0ce3f18972796f8fed541779038753c1a8b7b760c5777f', '.analysis/mainl-pi-composition-output-20261021-v01/linked-verification.json': 'a3a553c4cb58efb8ffe875c2c978f4f1a25926bd5355823c1aa2611a6a8eb0f4', '.analysis/mainl-pi-composition-output-20261021-v01/materialized-inputs.json': '8353ae9b341c84da0f9dc491e130ca430922bd4a770f765f16fc66820a2ad18e', '.analysis/mainl-pi-composition-output-20261021-v01/link1-outputs.json': '91182418a929e03bd94c9d54fcec8479eaab3fecd3dba00316b917c6822beeee', '.analysis/mainl-pi-composition-output-20261021-v01/link2-outputs.json': '91182418a929e03bd94c9d54fcec8479eaab3fecd3dba00316b917c6822beeee', '.analysis/mainl-pi-composition-output-20261021-v01/scanner-started.json': '31fcb0746770917f55e319d92d51a822b6cb9da6d366e368b05edd784b40e228', '.analysis/mainl-pi-composition-output-20261021-v01/scanner-finished.json': '2c311a1ab38b912d5e4749304615601e925c7753eb4c6e25a7399c233bbb23d2', '.analysis/mainl-pi-composition-output-20261021-v01/scanner-registry-transition.json': '2eef8cb11ab1aa3179b2075020349926dc5595e01006499598d7cf46e6af3d04', '.analysis/mainl-pi-composition-output-20261021-v01/link1-started.json': '1012e41f20cfb5e9d5288b6efd0126aeddedddcfcbb10ca6cfa6f38761dca119', '.analysis/mainl-pi-composition-output-20261021-v01/link1-finished.json': 'fbe8c6b7b6fedb1b91ba2da2ce6d4c232cc9724af3845ba49f1ceffc56b973b2', '.analysis/mainl-pi-composition-output-20261021-v01/link1-registry-transition.json': '3bc5d3e87a9771768461cf40fbb3a4f2232a72a27df3b4c8d12f1622dc38613b', '.analysis/mainl-pi-composition-output-20261021-v01/link2-started.json': '73627cb2c663af013672f44cc413db576e17344c783f6fc1e1539704471d51e3', '.analysis/mainl-pi-composition-output-20261021-v01/link2-finished.json': 'b7b30203cfc26d6baa507575b64325ce48bbde914d13bc385df813c8afefbf80', '.analysis/mainl-pi-composition-output-20261021-v01/link2-registry-transition.json': '1498e7032c658d1e5673c41971443c206c9cf620d09c6c46bfa0e43fa18f97e8'}

def retained(name):
    path=PROOF_DIRECTORY+"/"+name+".json"
    return json.loads(reg.read_verified(path,RETAINED_PINS[path]))

def source_bindings(manifest):
    from stage_th03_mainl_regist import INPUTS as REGIST_INPUTS
    from stage_th03_mainl_cutscene import INPUTS as CUTSCENE_INPUTS
    for name in sorted(set(REGIST_INPUTS+CUTSCENE_INPUTS+("scripts/replay_th03_mainl_regist.py","scripts/replay_th03_mainl_cutscene.py"))):
        reg.read_verified(name,manifest["sources"][name]["sha256"])

def replay():
    manifest=retained("manifest");completion=retained("completion")
    require(completion["complete"] and not completion["errors"] and completion["native_invocations"]==3
            and completion["owned_lock_released"],"composition native proof incomplete")
    require(completion["retained_other_objects"]==29 and completion["preexisting_independent_owned_object_pairs"]
            and completion["frozen_scanner_context_only"] and not completion["cold_whole_program"]
            and not completion["exact_acceptance"],"composition scope changed")
    source_bindings(manifest)
    for phase,kind in (("scanner","input_s"),("link1","link"),("link2","link")):
        started=retained(phase+"-started")
        require(started["argv"]==manifest["native_argv"][kind] and started["wait_seconds"]==90
                and started["cleanup_seconds"]==15,"composition native command/budget differs")
        reg.native_finished(retained(phase+"-finished"))
        require(retained(phase+"-registry-transition")["ok"],"composition registry transition differs")
    scanner=retained("scanner-producer")
    require(scanner["segments"]==['48a201020301','480000040501','480000060701']
            and scanner["context_only"] and scanner["owned"] is False,"scanner context scope differs")
    scanner_hash=retained("scanner-object")["sha256"]
    for role in ("R1","R2"):
        reg.read_verified(WORK+"/"+role+"/obj/th03/input_s.obj",scanner_hash)
    owned={}
    for unit in ("cutscene","scoredat","regist"):
        pair=[]
        for role in ("R1","R2"):
            row=manifest["owned_objects"][role][unit]
            raw=reg.read_verified(row["path"],row["sha256"])
            require(raw==reg.read_verified(WORK+"/"+role+"/obj/th03/"+unit+".obj",row["sha256"]),"consumed owner differs")
            pair.append(raw)
        require(pair[0]==pair[1],"owned object pair differs")
        owned[unit]=sha(pair[0])
    for name,row in manifest["carrier_files"].items():
        reg.read_verified(row["path"],row["sha256"])
    def product(role,name):
        receipt=retained("link1-outputs" if role=="R1" else "link2-outputs")
        return reg.read_verified(WORK+"/"+role+"/"+name,receipt[name]["sha256"])
    args=[product(role,name) for name in ("bin/th03/mainl.exe","obj/th03/mainl.map") for role in ("R1","R2")]
    args += [reg.read_verified(manifest[name]["path"],manifest[name]["sha256"]) for name in ("cached_exe","cached_map","decoded_target")]
    result=verify(*args)
    require(json.dumps(result,sort_keys=True)==json.dumps(retained("linked-verification"),sort_keys=True),"fresh composition observations differ")
    return dict(kind="th03-mainl-contextual-pi-composition-replay",checks_pass=True,retained_receipts=RETAINED_PINS,
                owned_object_hashes=owned,owned_bytes=6144,nine_historical_pi_gaps_closed_contextually=True,
                native_invocations_this_replay=0,retained_other_objects=29,fresh_scanner_context_only=True,
                preexisting_independent_owned_object_pairs=True,linked_diagnostics=result,
                source_counts_changed=False,exact_acceptance=False,cold_whole_program=False)

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
    require(not args.output.is_absolute() and args.output.parts[:1]==(".analysis",) and ".." not in args.output.parts,"output must be under .analysis")
    result=replay();output=ROOT/args.output;output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("x") as stream:stream.write(json.dumps(result,indent=2)+"\n")
    print("PASS composition: 6144 owned bytes target-equal; whole-image/relocation-order and exact gates remain open")
    return 0
if __name__=="__main__":raise SystemExit(main())
