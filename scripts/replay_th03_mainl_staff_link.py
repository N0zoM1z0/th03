#!/usr/bin/env python3
"""Verify the retained opt-in MAINL coherent staff link without rewriting artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
from lib import mainl_staff_source as composer
from lib import mainl_staff_link as verifier
ROOT=Path(__file__).resolve().parents[1]
RECIPE='config/th03_mainl_staff_link.json'
RECIPE_SHA='64f6e2dc055ba642c70ac62abd2cbcb372499bb5d850a19e576f851e3f0f4f00'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def validate_partition(units):
 need(len(units)==11 and len({r['unit_id'] for r in units})==11 and sum(r['bytes'] for r in units)==3339,'existing unit partition differs')
 cursor=0x24e6
 for unit in units:
  need(unit['segment']==0x95f and unit['offset']==cursor and unit['bytes']>0,'unit gap or overlap');cursor+=unit['bytes']
 need(cursor==0x31f1,'complete contribution boundary differs')
 snow=[r for r in units if r['unit_id']=='th03-mainl-decoded-snow-cluster']
 need(len(snow)==1 and snow[0]['bytes']==464 and snow[0]['source_paths']==['src/mainl/formats/cdg_effects.cpp','src/mainl/staff/snow.asm'],'snow464 requires both clear21 and snow443 producers')
def check_repeat(root,recipe,work):
 proposal=root/recipe['repeat_proposal'];output=root/recipe['repeat_output'];second=root/recipe['repeat_work']
 m=json.loads((proposal/'manifest.json').read_text());done=json.loads((output/'completion.json').read_text())
 need(done['complete'] and done['native_invocations']==2 and done['owned_lock_released'] and not done['errors'],'two-phase repeat incomplete')
 need('obj/th03/mainl.obj' not in m['repeat_inputs'] and 'bin/th03/mainl.exe' not in m['repeat_inputs'],'repeat must freshly produce root and EXE')
 for row in m['inputs']:need(sha((root/row['path']).read_bytes())==row['sha256'],'repeat provider changed: '+row['path'])
 mtimes=json.loads((output/'source-mtimes.json').read_text())
 for name,row in m['repeat_inputs'].items():
  first=root/row['path'];copied=second/name
  need(first.stat().st_mtime_ns==row['mtime_ns']==copied.stat().st_mtime_ns==mtimes[name],'declared input mtime differs: '+name)
  need(first.read_bytes()==copied.read_bytes(),'copied repeat input differs: '+name)
 for phase in ['root','link']:
  start=json.loads((output/(phase+'-started.json')).read_text());end=json.loads((output/(phase+'-finished.json')).read_text());transition=json.loads((output/(phase+'-registry-transition.json')).read_text())
  need(start['argv']==m['native_argv'][phase] and start['wait_seconds']==90 and start['cleanup_seconds']==15,'repeat native command/budget changed')
  need(end['exit_code']==0 and not end['timeout'] and not end['cleanup_uncertain'] and not end['poison'] and not end['survivors'] and not end['errors'] and transition['ok'],'repeat phase failed')
 for name in ['obj/th03/mainl.obj','bin/th03/mainl.exe','obj/th03/mainl.map']:
  need((work/name).read_bytes()==(second/name).read_bytes(),'raw repeat OBJ/EXE/MAP differs: '+name)
 proof=json.loads((output/'linked-verification.json').read_text())
 need(proof['diagnostic_checks_pass'] and proof['whole_exe_raw_equal'] and proof['root_obj_raw_equal'] and proof['map_raw_equal'],'repeat raw identity proof failed')
 model_raw=(root/recipe['full_model_replay_receipt']).read_bytes();need(sha(model_raw)==recipe['full_model_replay_receipt_sha256'],'full model replay receipt changed')
 model=json.loads(model_raw);need(model['recipe_sha256']==recipe['full_model_replay_recipe_sha256'] and model['runtime_observations_equal'] and model['native_fragment_consumption_proven'],'retained full model proof incomplete')
 return proof

def retained_verify(exe,map_raw,target_raw,context_raw,saved):
 from collections import Counter
 from lib.mainl_graphics_link import parse_mz,code_rows,diffs,relocs
 need(saved['input_sha256']==dict(exe=sha(exe),map=sha(map_raw),target=sha(target_raw),context=sha(context_raw)),'model product identities changed')
 target=parse_mz(target_raw);candidate=parse_mz(exe);context=parse_mz(context_raw)
 need(all(m.valid for m in [target,candidate,context]),'invalid MZ')
 need(diffs(target.program_image,candidate.program_image)==saved['target_byte_differences'],'raw full-image target differences changed')
 need(diffs(context.program_image,candidate.program_image)==saved['context_byte_differences'],'raw full-image context differences changed')
 a=relocs(target);b=relocs(candidate);r=saved['target_relocations']
 need(len(a)==r['target_count'] and len(b)==r['candidate_count'] and (a==b)==r['ordered_equal'] and (Counter(a)==Counter(b))==r['membership_equal'],'global relocations changed')
 actual=[dict(index=i,target=list(x),candidate=list(y)) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
 need(actual==r['ordered_differences'],'global relocation order differences changed')
 rows=code_rows(map_raw.decode('ascii'),len(candidate.program_image));names={r['name'] for r in saved['new_segment_rows']}
 need([r for r in rows if r['name'] in names and r['size']]==saved['new_segment_rows'],'MAP scope boundaries changed')
 need(saved['diagnostic_checks_pass'] and saved['staff_runtime_equal'] and saved['runtime_equal'],'retained model proof failed')
 return saved

def replay(root=ROOT,full_models=False):
 raw=(root/RECIPE).read_bytes();need(sha(raw)==RECIPE_SHA,'linked recipe identity changed');recipe=json.loads(raw)
 for name,expected in recipe['proof_inputs_sha256'].items():need(sha((root/name).read_bytes())==expected,'retained link input changed: '+name)
 for pathkey,hashkey in [('source','source_sha256'),('composer','composer_sha256'),('verifier','verifier_sha256')]:need(sha((root/recipe[pathkey]).read_bytes())==recipe[hashkey],'maintained link source/helper changed: '+pathkey)
 proposal=root/recipe['native_proposal'];output=root/recipe['native_output'];work=root/recipe['native_work']
 m=json.loads((proposal/'manifest.json').read_text());completion=json.loads((output/'completion.json').read_text())
 need(completion['complete'] and completion['native_invocations']==4 and completion['owned_lock_released'] and not completion['errors'],'four-phase link incomplete')
 for row in m['inputs']:need(sha((root/row['path']).read_bytes())==row['sha256'],'native guarded provider changed: '+row['path'])
 for phase in ['root','prefix','dissolve','link']:
  start=json.loads((output/(phase+'-started.json')).read_text());end=json.loads((output/(phase+'-finished.json')).read_text());transition=json.loads((output/(phase+'-registry-transition.json')).read_text())
  need(start['argv']==m['native_argv'][phase] and start['wait_seconds']==90 and start['cleanup_seconds']==15,'native command/budget changed: '+phase)
  need(end['exit_code']==0 and not end['timeout'] and not end['cleanup_uncertain'] and not end['poison'] and not end['survivors'] and not end['errors'] and transition['ok'],'native success/cleanup/registry failed: '+phase)
 source_raw=(root/recipe['source_recipe']).read_bytes();need(sha(source_raw)==recipe['source_recipe_sha256'],'source recipe changed');source_recipe=json.loads(source_raw)
 fragments={n:(root/r['path']).read_bytes() for n,r in source_recipe['fragments'].items()}
 for n,r in source_recipe['fragments'].items():need(sha(fragments[n])==r['sha256'],'maintained fragment changed: '+n)
 generated=composer.generate((root/recipe['original_root_source']).read_bytes(),(root/recipe['source']).read_bytes(),fragments)
 for name,content in generated.items():need((work/name).read_bytes()==content,'consumed source split differs: '+name)
 response=(root/m['response']['path']).read_bytes();old=b'obj\\th03\\mainl.obj';need(response.count(old)==1,'original response root occurrence')
 need((work/'obj/th03/mainl.@l').read_bytes()==response.replace(old,old+b' obj\\th03\\gfxpre.obj obj\\th03\\gfxdis.obj'),'link response/order changed')
 repeat=check_repeat(root,recipe,work)
 products=((work/'bin/th03/mainl.exe').read_bytes(),(work/'obj/th03/mainl.map').read_bytes(),(root/m['decoded_target']['path']).read_bytes(),(root/m['context_exe']['path']).read_bytes())
 saved=json.loads((output/'linked-verification.json').read_text())
 result=verifier.verify(*products) if full_models else retained_verify(*products,saved)
 need(json.loads(json.dumps(result))==json.loads((output/'linked-verification.json').read_text()),'retained linked proof differs from replay')
 need(result['diagnostic_checks_pass'],'linked diagnostics failed')
 units=recipe['units'];validate_partition(units)
 return dict(kind='mainl-coherent-staff-linked-proof-replay',recipe_sha256=sha(raw),maintained_contribution_bytes=3339,prior_owned_preserved_bytes=6144,total_scoped_target_equal_bytes=9483,existing_source_units=units,source_owned_bytes_eligible=3339,existing_scoped_ordered_relocations=112,new_snow_staff_ordered_relocations_equal=False,new_snow_staff_relocation_membership_equal=all(r['relocation_membership_equal'] for r in result['staff_bodies']),target_decoded_difference_count=1,remaining_difference=result['target_byte_differences'],context_changed_bytes=20,global_relocation_count=677,global_ordered_difference_count=len(result['target_relocations']['ordered_differences']),global_relocation_membership_equal=result['target_relocations']['membership_equal'],runtime_observations_equal=result['runtime_equal'] and result['staff_runtime_equal'],native_invocations_in_this_replay=0,native_fragment_consumption_proven=True,fresh_root_link_builds=2,raw_repeat_obj_exe_map_equal=True,models_rerun=full_models,models_retained_by_complete_exe_identity=not full_models,full_model_replay_receipt_sha256=recipe['full_model_replay_receipt_sha256'],original_segment_identity_preserved=False,opt_in_only=True,cold_aggregate=False,exact_acceptance=False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--full-models',action='store_true');a=p.parse_args();result=replay(full_models=a.full_models);text=json.dumps(result,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(text)
 else:print(text,end='')
if __name__=='__main__':main()
