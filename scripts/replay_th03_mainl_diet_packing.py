#!/usr/bin/env python3
"""Replay pinned DIET diagnostics without invoking native tools or granting credit."""
import argparse,hashlib,json,sys,types
from pathlib import Path

def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def load_json(path):return json.loads(path.read_text())
def validate_proof(proof):
 need(proof['schema']=='mainl-diet-packing-diagnostic-v1','schema')
 need(not any(proof[k] for k in ['source_acceptance','exact_acceptance','source_progress_changed']),'diagnostic cannot grant credit')
 need([r['label'] for r in proof['runs']]==['target_control','source_product'],'two distinct input roles required')
 paths=[p['path'] for p in proof['pins']];need(len(paths)==len(set(paths)),'duplicate pins')
def replay(root,proof):
 validate_proof(proof);root=root.resolve();pins={r['path']:r for r in proof['pins']}
 def read(path):
  key=str(path);need(key in pins,'unbound input '+key);p=root/key;need(p.is_file() and not p.is_symlink(),'regular bound input required');raw=p.read_bytes();r=pins[key];need(len(raw)==r['bytes'] and sha(raw)==r['sha256'],'pin drift '+key);return raw
 for p in pins:read(p)
 rows=[]
 for run in proof['runs']:
  out=Path(run['output']);proposal=Path(run['proposal']);work=root/run['work'];m=json.loads(read(proposal/'manifest.json'))
  need(read(out/'manifest.json')==read(proposal/'manifest.json'),'native manifest differs')
  need(m['work']==run['work'] and m['output']==run['output'],'manifest namespace')
  done=json.loads(read(out/'completion.json'));need(done['complete'] and done['owned_lock_released'] and done['native_invocations']==5 and not done['errors'],'native completion')
  need(done['exact_acceptance'] is False and done['full_historical_replay'] is False,'native acceptance inflation')
  launch=read(proposal/'launch.sh').decode();need(sha(read(proposal/'manifest.json')) in launch and m['runner']['sha256'] in launch,'launch identity')
  for row in m['inputs']:need(sha(read(row['path']))==row['sha256'],'manifest input binding')
  materialized=json.loads(read(out/'materialized-inputs.json'));mtimes=json.loads(read(out/'source-mtimes.json'))
  for name,row in m['repeat_inputs'].items():
   actual=read(Path(run['work'])/name);need(sha(actual)==row['sha256']==materialized[name]['sha256'],'consumed seed/tool differs');need(mtimes[name]==row['mtime_ns'],'declared seed timestamp')
  vrow=m['verifier'];raw=read(vrow['path']);need(sha(raw)==vrow['sha256'],'verifier identity');v=types.ModuleType('bound_diet_verifier');v.__file__=str(root/vrow['path']);exec(compile(raw,v.__file__,'exec'),v.__dict__)
  phases=[]
  for phase in m['phases']:
   started=json.loads(read(out/(phase+'-started.json')));finished=json.loads(read(out/(phase+'-finished.json')));transition=json.loads(read(out/(phase+'-registry-transition.json')));log=read(out/(phase+'.log'))
   need(started['argv']==m['native_argv'][phase] and started['cwd']==str(work/m['phase_cwds'][phase]),'actual native argv/cwd')
   need(started['wait_seconds']==90 and started['cleanup_seconds']==15,'native bound')
   need(finished['exit_code']==(0 if phase=='selfcheck' else 1),'observed DIET exit convention')
   need(not any(finished[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']) and finished['initial_inventory_complete'] and finished['inventory_complete'],'native cleanup')
   need(transition['ok'],'native registry transition')
   actual=v.check_phase(work,m,phase,finished,log);need(actual==json.loads(read(out/(phase+'-semantic-check.json'))) and actual['pass'],'phase semantic replay')
   phases.append(dict(phase=phase,exit_code=finished['exit_code'],cleanup_certain=True))
  result=v.verify(work,m);need(result==json.loads(read(out/'calibration-verification.json')) and result['diagnostic_checks_pass'],'full packing replay')
  need(not result['source_acceptance'] and not result['source_progress_changed'] and not result['exact_acceptance'],'result credit')
  need(result['restoration_is_same_tool_separate_invocation'],'decoder limitation omitted')
  if run['label']=='target_control':need(result['target_fed'] and result['canonical_packed_equal'],'positive control differs')
  else:
   need(not result['target_fed'] and result['source_fed'] and not result['full_cold_build'],'source role differs')
   source=json.loads(read(m['source_proof']['path']));need(source['exe_sha256']==result['decoded_sha256'] and len(source['raw_repeat_pairs'])==9 and all(r['raw_equal'] for r in source['raw_repeat_pairs']),'actual source provenance')
  rows.append(dict(label=run['label'],phases=phases,packed_sha256=result['packed_first_sha256'],packed_bytes=result['packed_first_bytes'],canonical_packed_equal=result['canonical_packed_equal'],packed_difference_count=result['packed_difference_count'],raw_repeat_equal=result['raw_repeat_equal'],both_roundtrips_equal=result['first_roundtrip_equal'] and result['second_roundtrip_equal']))
 return dict(schema=proof['schema'],pass_checks=True,pinned_files=len(pins),native_phases_replayed=10,native_invocations_now=0,runs=rows,source_acceptance=False,exact_acceptance=False,source_progress_changed=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();proof=a.proof or a.repo_root/'config/mainl_diet_packing/proof.json';result=replay(a.repo_root,load_json(proof));raw=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
