#!/usr/bin/env python3
"""Verify the retained opt-in MAINL graphics link without rewriting artifacts."""
import argparse
import hashlib
import json
from pathlib import Path
from lib import mainl_graphics_source as composer
from lib import mainl_graphics_link as verifier
ROOT=Path(__file__).resolve().parents[1]
RECIPE='config/th03_mainl_graphics_link.json'
RECIPE_SHA='309d695609b2a13a1e3cbf70e1071895d311a68cf7378f5d0ba82b80de7f600f'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def replay(root=ROOT):
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
 generated=composer.generate((root/recipe['original_root_source']).read_bytes(),(root/recipe['source']).read_bytes())
 for name,content in generated.items():need((work/name).read_bytes()==content,'consumed source split differs: '+name)
 response=(root/m['response']['path']).read_bytes();old=b'obj\\th03\\mainl.obj';need(response.count(old)==1,'original response root occurrence')
 need((work/'obj/th03/mainl.@l').read_bytes()==response.replace(old,old+b' obj\\th03\\gfxpre.obj obj\\th03\\gfxdis.obj'),'link response/order changed')
 result=verifier.verify((work/'bin/th03/mainl.exe').read_bytes(),(work/'obj/th03/mainl.map').read_bytes(),(root/m['decoded_target']['path']).read_bytes(),(root/m['context_exe']['path']).read_bytes())
 need(json.loads(json.dumps(result))==json.loads((output/'linked-verification.json').read_text()),'retained linked proof differs from replay')
 need(result['diagnostic_checks_pass'],'linked diagnostics failed')
 return dict(kind='mainl-graphics-linked-proof-replay',recipe_sha256=sha(raw),linked_graphics_bytes=355,prior_owned_preserved_bytes=6144,total_scoped_target_equal_bytes=6499,scoped_ordered_relocations=112,target_decoded_difference_count=1,remaining_difference=result['target_byte_differences'],context_changed_bytes=20,global_relocation_count=677,global_ordered_difference_count=len(result['target_relocations']['ordered_differences']),global_relocation_membership_equal=result['target_relocations']['membership_equal'],runtime_observations_equal=result['runtime_equal'],native_invocations_in_this_replay=0,original_segment_identity_preserved=False,opt_in_only=True,source_progress_changed=False,exact_acceptance=False)
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();result=replay();text=json.dumps(result,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(text)
 else:print(text,end='')
if __name__=='__main__':main()
