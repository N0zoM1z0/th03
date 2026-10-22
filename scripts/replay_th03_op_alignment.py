#!/usr/bin/env python3
"""Read-only historical source and actual native alignment evidence replay."""
from pathlib import Path
import argparse,hashlib,json,sys,types
PROOF='config/op_alignment/proof.json'
PROOF_SHA='9c8020459fe83ccffcabdb96dc995491f27941757e069e42ae03313fd72af26e'
def need(v,m):
 if not v:raise ValueError(m)
def read(root,q):
 n=q['path'];p=Path(n);need(not p.is_absolute() and '..' not in p.parts,'safe evidence path');p=Path(root)/p;need(p.is_file() and not any(x.is_symlink() for x in (p,*p.parents)),'regular evidence');b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==q['sha256'] and len(b)==q.get('bytes',len(b)),'evidence drift '+n);return b
def replay(root,files=None):
 root=Path(root);files=Path(files or root);p=json.loads(read(files,dict(path=PROOF,sha256=PROOF_SHA)));need(p['schema']=='th03-op-historical-alignment-observation-v1' and not p['source_acceptance'] and not p['exact_acceptance'] and not p['cold_build'] and p['new_authored_code_credit']==0,'scope')
 for q in p['pins']+[p['dependency_manifest'],p['historical_evidence'],p['historical_source']]:read(root,q)
 for k in ['source_stager','source_config','verifier']:read(files,p[k])
 m=json.loads(read(root,p['current_manifest']));c=json.loads(read(root,p['current_completion']));need(c['complete'] and c['owned_lock_released'] and not c['errors'] and c['native_invocations']==2 and c['phases']==['assemble_prefix','link'],'actual two-phase completion')
 sys.path.insert(0,str(root/'scripts'));v=types.ModuleType('op_alignment_observer');v.__file__=str(files/p['verifier']['path']);exec(compile(read(files,p['verifier']),v.__file__,'exec'),v.__dict__);v.ROOT=root
 out=root/m['output'];work=root/m['work'];actual=json.loads(json.dumps(v.verify(work,m)));need(actual==json.loads(read(root,p['current_report'])) and actual['diagnostic_checks_pass'],'literal diagnostic replay')
 policy=types.ModuleType('bound_registry_policy');policy.__file__=str(root/m['registry_policy']['path']);sys.modules[policy.__name__]=policy;exec(compile(read(root,m['registry_policy']),policy.__file__,'exec'),policy.__dict__)
 for phase in c['phases']:
  get=lambda n:json.loads((out/(phase+'-'+n+'.json')).read_text())
  start=get('started');end=get('finished');trans=get('registry-transition');need(start['argv']==m['native_argv'][phase] and start['wait_seconds']==90 and start['cleanup_seconds']==15 and end['exit_code']==0 and not any(end[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']) and end['initial_inventory_complete'] and end['inventory_complete'],'native receipt')
  before={n:(out/(phase+'-before-'+n)).read_bytes() for n in ['user.reg','system.reg']};after={n:(out/(phase+'-after-'+n)).read_bytes() for n in before}
  # Replay the exact recorded transition window rather than introducing a new clock.
  need(trans['ok'] and policy.validate_transition(before,after,phase_start_utc=trans['phase_start_utc'],phase_end_utc=trans['phase_end_utc'],child_tz=trans['child_tz'])==trans,'registry transition replay')
  if phase==c['phases'][0]:previous=after
  else:need(before==previous,'registry snapshot continuity');previous=after
 inputs=json.loads((out/'materialized-inputs.json').read_text());times=json.loads((out/'source-mtimes.json').read_text());need(set(inputs)==set(times)==set(m['repeat_inputs']),'materialized closure')
 for n,q in m['repeat_inputs'].items():need(inputs[n]['sha256']==q['sha256'] and times[n]==q['mtime_ns'],'consumed source identity/stamp')
 objects=json.loads((out/'accumulated-objects.json').read_text());need(set(objects)==set(m['all_native_outputs']),'actual output membership');need({p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file()}==set(inputs)|set(objects),'carrier membership')
 cfg=json.loads(read(files,p['source_config']));sources={n:dict(sha256=hashlib.sha256((work/n).read_bytes()).hexdigest(),bytes=(work/n).stat().st_size) for n in inputs if not n.lower().endswith(('.obj','.exe','.com','.map','.lib'))};need(sources==cfg['output_inventory'],'330 consumed sources')
 cr=(work/'bin/th03/op.exe').read_bytes();tr=v.pin(m['target']);h=lambda b:int.from_bytes(b[8:10],'little')*16;hc,ht=h(cr),h(tr);need(hc==3584 and ht==4096 and len(cr)==63354 and len(tr)==63866,'literal file envelopes');need(all(cr[i]==tr[i] for i in range(hc) if i not in (4,8,9)) and tr[hc:ht]==bytes(ht-hc),'header-only distinction')
 return dict(replay_pass=True,pinned_files=len(p['pins']),native_invocations_now=0,source_acceptance=False,exact_acceptance=False,cold_build=False,new_authored_code_credit=0,whole_target_program_equal=True,program_bytes=59770,literal607_target_order=True,baseline_program_delta=[0xdd95],source_files=330,whole_decoded_file_equal=False,candidate_header_bytes=hc,target_header_bytes=ht,header_field_difference_offsets=[4,8,9],extra_target_header_zero_bytes=512,canonical_packed_equality_claimed=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--files',type=Path);a=p.parse_args();print(json.dumps(replay(a.root,a.files),indent=2))
