"""Read-only source-fed exact DIET replay, no live tool/registry/HEAD gates."""
from pathlib import Path
import json,hashlib,importlib.util,sys
PROOF_SHA='0d937b68ad739e8bd2a0bb4de4c054b016d3dc5a93635edfe6a17d2c1694a25b'
ROOT=Path(__file__).resolve().parents[1]
def need(v,m):
 if not v:raise ValueError(m)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);v=importlib.util.module_from_spec(s);sys.modules[name]=v;s.loader.exec_module(v);return v
def validate_proof(proof,root):
 need(proof['expected_packed_equal'] is True and proof['expected_restored_source_equal'] is True and proof['expected_restored_target_equal'] is True and proof['acceptance'] is False and proof['full_cold'] is False and proof['new_authored_credit']==0 and proof['original_nopcall_native_completion'] is False,'exact evidence scope')
 for q in proof['pins']:
  raw=(Path(root)/q['path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==q['sha256'] and len(raw)==q['bytes'],'immutable evidence drift '+q['path'])
def replay(root=None,files=None):
 global ROOT
 ROOT=(Path(root) if root else ROOT).resolve();files=(Path(files) if files else ROOT).resolve();raw=(files/'config/op_source_packing/proof.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==PROOF_SHA,'proof identity');proof=json.loads(raw);validate_proof(proof,ROOT)
 source=load('packing_corrected_source',ROOT/proof['corrected_source_audit']).replay();need(source['replay_pass'] and source['original_native_completion'] is False and source['whole63866_target_raw_equal'],'original false completion and corrected source audit')
 negative=load('packing_historical_negative',ROOT/proof['historical_negative_replay']).replay();need(negative['replay_pass'] and negative['packed_equal'] is False and negative['restored_target_equal'] is False,'earlier negative remains negative')
 for p in proof['pins']:
  raw=(ROOT/p['path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'] and len(raw)==p['bytes'],'pin drift '+p['path'])
 o=ROOT/proof['output'];w=ROOT/proof['work'];m=json.loads((o/'manifest.json').read_text());c=json.loads((o/'completion.json').read_text());need(c['complete'] and c['owned_lock_released'] and c['native_invocations']==5 and not c['errors'] and not c['exact_acceptance'],'completion')
 v=load('op_negative_verifier',ROOT/m['verifier']['path']);policy=load('op_negative_registry_policy',ROOT/m['registry_policy']['path']);r=v.verify(w,m);need(r==json.loads((o/'calibration-verification.json').read_text()),'raw actual report reproduction');need(r['diagnostic_checks_pass'] and r['canonical_packed_equal'] is True and r['packed_first_bytes']==36041 and r['canonical_bytes']==36041 and r['packed_difference_count']==0,'actual negative packed result')
 need(r['first_restoration']['raw_source_roundtrip_equal'] is True and r['first_restoration']['raw_decoded_target_equal'] is True and r['second_restoration']==r['first_restoration'],'literal restored comparisons')
 previous=None
 for phase in m['phases']:
  s=json.loads((o/(phase+'-started.json')).read_text());f=json.loads((o/(phase+'-finished.json')).read_text());t=json.loads((o/(phase+'-registry-transition.json')).read_text());need(s['argv']==m['native_argv'][phase] and s['cwd']==str(w/m['phase_cwds'][phase]) and s['wait_seconds']==90 and s['cleanup_seconds']==15,'actual phase argv');need(not any(f[k] for k in ['timeout','cleanup_uncertain','poison','errors','survivors']) and f['initial_inventory_complete'] and f['inventory_complete'],'owned cleanup')
  before={n:(o/(phase+'-before-'+n)).read_bytes() for n in ('user.reg','system.reg')};after={n:(o/(phase+'-after-'+n)).read_bytes() for n in before};need(previous is None or previous==before,'registry continuity');previous=after
  reproduced=policy.validate_transition(before,after,phase_start_utc=t['phase_start_utc'],phase_end_utc=t['phase_end_utc'],child_tz=t['child_tz']);need(reproduced==t and t['ok'] and t['phase_start_utc']==s['started_utc'],'recorded strict registry policy')
  check=v.check_phase(w,m,phase,f,(o/(phase+'.log')).read_bytes());need(check==json.loads((o/(phase+'-semantic-check.json')).read_text()) and check['pass'],'phase semantics')
 materialized=json.loads((o/'materialized-inputs.json').read_text());mtimes=json.loads((o/'source-mtimes.json').read_text());accumulated=json.loads((o/'accumulated-objects.json').read_text())
 def actual(path):
  raw=path.read_bytes();return dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),mode=path.stat().st_mode&0o777)
 need(set(materialized)==set(mtimes)==set(m['repeat_inputs']),'exact materialized membership')
 for name,p in m['repeat_inputs'].items():
  need((w/name).read_bytes()==(ROOT/p['path']).read_bytes(),'consumed source identity');need(actual(w/name)==materialized[name] and (w/name).stat().st_mtime_ns==mtimes[name],'consumed source mode/time identity')
 need(set(accumulated)==set(m['all_native_outputs']),'accumulated outputs closure')
 for phase,names in m['native_outputs'].items():
  for name in ([names] if isinstance(names,str) else (names or [])):need(actual(w/name)==accumulated[name]==json.loads((o/(phase+'-output.json')).read_text()),'actual output receipt')
 need({p.relative_to(w).as_posix() for p in w.rglob('*') if p.is_file()}==set(m['repeat_inputs'])|set(m['all_native_outputs']),'carrier closure')
 final=json.loads((o/'next-registry-baseline.json').read_text())
 for n,raw in previous.items():need(final[n]['sha256']==hashlib.sha256(raw).hexdigest() and final[n]['bytes']==len(raw),'historical final registry, not live state')
 return dict(replay_pass=True,pinned_files=len(proof['pins']),actual_phases=5,packed_equal=True,packed_bytes=36041,target_bytes=36041,restored_source_equal=True,restored_target_equal=True,program59770_equal=True,ordered607_equal=True,native_invocations=0,acceptance=False,new_authored_credit=0)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--files',type=Path);a=p.parse_args();print(json.dumps(replay(a.root,a.files),indent=2))
