"""Prepare or explicitly publish repository-local 33-owner decoded OP acceptance.
Requires installed fullcold checkpoint. No native/model execution; toolchain identity only.
"""
from pathlib import Path
import argparse,contextlib,csv,hashlib,importlib.util,io,json,subprocess,sys,tomllib
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
def bootstrap():
 # No repository code imports until this reviewed helper closure is checked.
 manifest=ROOT/'config/op_decoded_acceptance/helper-bindings.json'
 if not manifest.is_file() or any(x.is_symlink() for x in [manifest,*manifest.parents]):raise ValueError('missing regular helper manifest')
 data=json.loads(manifest.read_bytes());pins=data['pins'];names={q['path'] for q in pins}
 pre=argparse.ArgumentParser(add_help=False);pre.add_argument('--publish',type=Path);pre.add_argument('--review-sha256');pre.add_argument('--output',type=Path);args,_=pre.parse_known_args()
 if args.publish:
  rel=args.publish
  if rel.is_absolute() or '..' in rel.parts or not rel.parts or rel.parts[0]!='.analysis':raise ValueError('unsafe review path')
  review=ROOT/rel
  if not review.is_file() or any(x.is_symlink() for x in [review,*review.parents]):raise ValueError('missing regular review')
  raw=review.read_bytes()
  if not args.review_sha256 or hashlib.sha256(raw).hexdigest()!=args.review_sha256:raise ValueError('review digest mismatch before imports')
  reviewed=json.loads(raw);bindings=reviewed['input_bindings'];by_name={q['path']:q for q in bindings}
  if reviewed['state']!='review-ready' or len(by_name)!=len(bindings):raise ValueError('invalid reviewed bindings')
  manifest_name='config/op_decoded_acceptance/helper-bindings.json';raw_manifest=manifest.read_bytes();expected=dict(path=manifest_name,bytes=len(raw_manifest),sha256=hashlib.sha256(raw_manifest).hexdigest())
  if by_name.get(manifest_name)!=expected or any(by_name.get(q['path'])!=q for q in pins):raise ValueError('reviewed helper closure drift before imports')
  destination=ROOT/'config/op_decoded_acceptance/publication.json'
  if args.output!=Path('config/op_decoded_acceptance/publication.json') or destination.exists() or not destination.parent.is_dir() or any(x.is_symlink() for x in [destination,*destination.parents]):raise ValueError('invalid publication destination before imports')

 if len(names)!=len(pins) or not {'scripts/validate_tracking.py','scripts/replay_th03_op_decoded_acceptance.py','scripts/lib/op_decoded_acceptance.py','scripts/lib/__init__.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/op_diet_lineage.py','scripts/lib/toolchain.py','scripts/review_th03_decoded_code.py','scripts/replay_th03_op_fullcold.py'}<=names:raise ValueError('incomplete helper closure')
 for q in pins:
  rel=Path(q['path'])
  if rel.is_absolute() or '..' in rel.parts:raise ValueError('unsafe helper path')
  p=ROOT/rel
  if not p.is_file() or any(x.is_symlink() for x in [p,*p.parents]):raise ValueError('missing regular helper')
  raw=p.read_bytes()
  if len(raw)!=q['bytes'] or hashlib.sha256(raw).hexdigest()!=q['sha256']:raise ValueError('helper drift '+q['path'])
bootstrap()
from lib.op_decoded_acceptance import GATES,need,sha,pin,checked,regular,descriptor,validate_inventory,verify,owner_oracles,required_closure,physical_audit
from lib.pc98 import parse_mz,describe_blob
from lib.op_diet_lineage import verify_diet_lineage
from lib.omf import describe_omf
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows
import replay_th03_op_fullcold as cold
import validate_tracking as tracking

def prepare(out):
 need(not out.exists(),'output directory exists');out.mkdir(parents=True)
 proof=json.loads(regular(ROOT,'config/op_fullcold/proof.json').read_bytes())
 replay=cold.replay(ROOT,proof);need(replay['pass_checks'] and replay['native_phases_replayed']==56,'full cold replay')
 (out/'fullcold.json').write_text(json.dumps(replay,indent=2)+'\n')
 targets=load_target_manifest(ROOT/'config/targets.toml');stored=read_verified_artifact(ROOT,find_artifact(targets,'th03-op'));need(parse_mz(stored).valid,'stored format')
 diet=tomllib.loads(regular(ROOT,'config/th03_diet.toml').read_text());decl=next(x for x in diet['artifacts'] if x['id']=='th03-op')
 cohort=json.loads(regular(ROOT,'config/op_decoded_acceptance/cohort.json').read_bytes())['owners'];units={u['id']:u for u in csv.DictReader((ROOT/'config/units.csv').open())}
 for d in cohort:need(descriptor(units[d['unit_id']])==d,'reviewed current descriptor')
 owners,object_audit=physical_audit(ROOT,cohort)
 validate_inventory(owners,cohort)
 need(len(object_audit)==54,'54 object observations');(out/'objects.json').write_text(json.dumps(object_audit,indent=2)+'\n')
 (out/'owners.json').write_text(json.dumps(owners,indent=2)+'\n')
 subprocess.run([sys.executable,'-B','scripts/attest_toolchain.py','--identity-only','--output',str(out/'toolchain.json')],cwd=ROOT,check=True,stdout=subprocess.PIPE)
 need(json.loads((out/'toolchain.json').read_text())['identity_pass'],'current toolchain identity')
 log=io.StringIO()
 with contextlib.redirect_stdout(log):rc=tracking.main(ROOT,validate_product=False)
 need(rc==0,'current ledger');(out/'ledger.log').write_text(log.getvalue())
 subprocess.run([sys.executable,'-B','scripts/verify_targets.py','--game','th03'],cwd=ROOT,check=True,stdout=subprocess.PIPE)
 identity,lineage_pins=verify_diet_lineage(ROOT,describe_blob)
 (out/'identity.json').write_text(json.dumps(identity,indent=2)+'\n')
 # Retain original inventory and every physical/source binding, not just results.
 inv=json.loads(checked(ROOT,proof['inventory']));names={q['path'] for q in inv['pins']};names.add(proof['inventory']['path'])
 names.update(['config/units.csv','config/oracles.toml','config/targets.toml','config/th03_diet.toml','config/toolchain.toml','config/evidence.csv','config/hypotheses.csv','config/knowledge.csv','config/op_fullcold/proof.json','config/op_decoded_acceptance/cohort.json','scripts/stage_th03_op_fullcold.py','scripts/replay_th03_op_fullcold.py','scripts/lib/op_decoded_acceptance.py','scripts/replay_th03_op_decoded_acceptance.py','scripts/validate_tracking.py','scripts/verify_targets.py','scripts/attest_toolchain.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/op_diet_lineage.py','scripts/lib/toolchain.py','scripts/review_th03_decoded_code.py',find_artifact(targets,'th03-op')['private_path']])
 names.update(q['path'] for q in lineage_pins);names.update(required_closure(ROOT));names.add('config/op_decoded_acceptance/helper-bindings.json');names.update(q['path'] for q in json.loads(regular(ROOT,'config/op_decoded_acceptance/helper-bindings.json').read_bytes())['pins'])
 evidence=[pin(ROOT,str((out/n).relative_to(ROOT))) for n in ['fullcold.json','owners.json','toolchain.json','ledger.log','identity.json','objects.json']]
 policy=tomllib.loads(regular(ROOT,'config/oracles.toml').read_text());spec={x['id']:x for x in policy['oracles']};witness={'target-identity':'identity.json','format-integrity':'identity.json','boundary-ownership':'owners.json','toolchain-identity':'toolchain.json','toolchain-replay':'fullcold.json','object-format-integrity':'objects.json','cold-build-determinism':'fullcold.json','layout-relocations':'owners.json','raw-bytes':'owners.json','ledger-consistency':'ledger.log','cold-aggregate-replay':'fullcold.json'}
 p=dict(schema='op-decoded-acceptance-v1',state='review-ready',scope='reviewed-33-decoded-owners',target_provenance='candidate-local-attested',product_exact=False,mixed_physical_exact_bytes=0,factory_accepted=False,canonical_credit_changed=False,whole_game_percentage=None,runtime_rerun=False,runtime_support_required=False,owners=owners,input_bindings=[pin(ROOT,n) for n in sorted(names)],evidence_bindings=evidence,gates={k:dict(result='pass',evidence_class=spec[k]['accepts_evidence_classes'][0],witness=str((out/witness[k]).relative_to(ROOT))) for k in GATES})
 p['inputs']={q['path']:q['sha256'] for q in p['input_bindings']+p['evidence_bindings']}
 p['owner_oracles']=owner_oracles(owners,p['gates'],evidence,policy,p['input_bindings'],'python3 scripts/replay_th03_op_decoded_acceptance.py --prepare '+str(out.relative_to(ROOT)))
 verify(ROOT,p,allow_review=True)
 (out/'review.json').write_text(json.dumps(p,indent=2)+'\n');print('Review ready, no acceptance published')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare',type=Path);ap.add_argument('--publish',type=Path);ap.add_argument('--review-sha256');ap.add_argument('--output',type=Path);a=ap.parse_args();need(bool(a.prepare)^bool(a.publish),'choose prepare or publish')
 if a.prepare:
  rel=a.prepare;need(not rel.is_absolute() and '..' not in rel.parts and rel.parts[0]=='.analysis','prepare requires repository-relative analysis directory');dest=ROOT/rel;need(not dest.exists() and not any(x.is_symlink() for x in [dest,*dest.parents]),'new regular output only');prepare(dest);return
 need(a.review_sha256 and a.output,'publish requires exact reviewed digest and new output');need(a.output==Path('config/op_decoded_acceptance/publication.json'),'fixed publication destination');dest=ROOT/a.output;need(not dest.exists() and dest.parent.is_dir() and not any(x.is_symlink() for x in [dest,*dest.parents]),'new regular publication only');need(a.publish.parts and a.publish.parts[0]=='.analysis','review must be repository-local analysis');b=regular(ROOT,str(a.publish)).read_bytes();need(sha(b)==a.review_sha256,'review digest mismatch');p=json.loads(b);need(p['state']=='review-ready','invalid transition');verify(ROOT,p,allow_review=True);p['state']='repository-local-accepted'
 with dest.open('x') as f:json.dump(p,f,indent=2);f.write('\n')
 print('Published only decoded owners; canonical/physical/Factory credit unchanged')
if __name__=='__main__':main()
