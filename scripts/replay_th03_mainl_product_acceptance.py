"""Replay MAINL mixed-product and decoded-owner acceptance without native tools.
The explicit --publish option writes the reviewed sidecar, never canonical ledgers.
Retains one reviewed full source replay while rechecking its fixed code, all pins,
current maintained source inventory, and current independent static gates.
--full-replay also reruns the complete94-phase receipt verifier (no native tools).
"""
import argparse,contextlib,csv,datetime,hashlib,importlib.util,io,json,subprocess,sys,tomllib
from pathlib import Path
ROOT=Path.cwd();PACKAGE_ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.analysis/mainl-product-acceptance-replay-current'
sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from lib.omf import describe_omf
CODE='scripts/replay_th03_mainl_fullcold_current.py'
PROOF='config/mainl_fullcold_current/proof.json'
RETAINED='.analysis/mainl-fullcold-proof-files-20261021-v01/replay-result.json'
FIXED={CODE:'e5e34fa2c08ce2d8e55d1c3e5af060f39cf36f4dca849527262b464c73edaf85',PROOF:'54bfd57109c4892b05aead8d6f56323b5d8d8e1c27d5025080a08afa2cac71a1',RETAINED:'75f050bf92e1287d281797bf5530213edb5d328c1d275fa4b59cc9ee366330df'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(name):return (ROOT/name).read_bytes()
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def main(full=False,publish=False,output=None):
 global OUT
 if output is not None:OUT=Path(output).resolve()
 elif publish:OUT=ROOT/'config/mainl_product_acceptance'
 OUT.mkdir(parents=True,exist_ok=True)
 for name,digest in FIXED.items():need(sha(read(name))==digest,'fixed replay witness drift '+name)
 proof=json.loads(read(PROOF));cold=json.loads(read(RETAINED));native=module(ROOT/CODE,'fixed_product_fullcold')
 native.validate_proof(proof)
 for row in proof['pins']:
  p=ROOT/row['path'];need(p.is_file() and not p.is_symlink(),'invalid pin');b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'fullcold pin drift '+row['path'])
 # Rebind actual source regeneration to maintained sources; the retained result
 # is not accepted from JSON alone. No dynamic executable path comes from sidecar.
 stagepath=ROOT/'scripts/stage_th03_mainl_fullcold.py';need(sha(stagepath.read_bytes())==native.STAGE_SHA,'source composer drift')
 stage=module(stagepath,'fixed_product_source_stage');files,provenance,stages,graph,archive_sha=stage.compose_all()
 need(len(files)==1904 and len(graph)==36,'current source closure differs')
 for rnd in [1,2]:
  manifest=json.loads(read(f'.analysis/mainl-fullcold-r{rnd}-g10-20261021-v02-proposal/manifest.json'));work=ROOT/manifest['work'];recipe=json.loads(read(manifest['source_recipe']['path']))
  need(recipe['archive_sha256']==archive_sha and recipe['object_graph']==graph,'source graph drift')
  for name,raw in files.items():need(raw==(work/name).read_bytes() and sha(raw)==recipe['source_inventory'][name]['sha256'],'regenerated source mismatch '+name)
  for name,pin in recipe['maintained_inputs'].items():need(sha(read(name))==pin['sha256'],'maintained input drift '+name)
 if full:
  recomputed=native.replay(ROOT,proof);need(recomputed==cold,'full replay result drift')
 need(cold['pass_checks'] and cold['native_phases_replayed']==94 and cold['groups_replayed']==20 and cold['raw_repeat_pairs']==940 and cold['decoded_and_packed_equal'],'incomplete cold witness')
 audit=module(PACKAGE_ROOT/'scripts/lib/mainl_product_audit.py','product_static_audit');audit.OUT=OUT;audit.main();owners=json.loads((OUT/'actual-cold-owner-audit.json').read_text())
 # Every fresh OMF binds the expected producer and every embedded dependency
 # to the actual declared staged source or separately pinned vendor include.
 norm=lambda value:value.replace("\\","/").casefold()
 source_bindings=dict(recipe['source_inventory'])
 for n,row in manifest['repeat_inputs'].items():
  if Path(n).suffix.lower() in {'.asm','.cpp','.c','.h','.hpp','.inc','.inl','.asp','.lua'}:source_bindings.setdefault(n,row)
 staged={norm(n):n for n in source_bindings}
 declared_tools={norm(row['path']):row for row in manifest['toolchain_inputs']}
 producer_checks=[]
 for name,obj in owners['fresh_objects'].items():
  g=obj['source_graph'];kind='tasm' if name.startswith('crtobjs/') else g['kind'];wrapper=g['wrapper']
  expected='Turbo Assembler  Version 5.0' if kind=='tasm' else 'TC86 Borland C++ 4.02'
  need(obj['translator_comments']==[expected], 'unexpected OMF producer '+name)
  need(norm(obj['module_name'])==norm(wrapper) and obj['dependency_paths'] and norm(obj['dependency_paths'][0])==norm(wrapper),'OMF wrapper dependency '+name)
  for dep in obj['dependency_paths']:
   key=norm(dep)
   if key.startswith('c:/'):
    toolkey=norm('.analysis/toolchain/wineprefix/drive_c/'+dep.replace('\\','/')[3:]);need(toolkey in declared_tools,'undeclared vendor dependency '+dep)
    pin=declared_tools[toolkey];need(sha(read(pin['path']))==pin['sha256'],'vendor dependency drift')
   else:
    need(key in staged,'dependency not in actual source materialization '+dep)
    rel=staged[key];need(sha((work/rel).read_bytes())==source_bindings[rel]['sha256'],'staged dependency drift')
  producer_checks.append(dict(object=name,producer=expected,wrapper=wrapper,dependencies=len(obj['dependency_paths']),pass_checks=True))
 need(len(producer_checks)==42,'fresh producer count')
 # Validate all extracted context objects too, not just42fresh authored/project objects.
 context_count=0
 for name in manifest['contextual_outputs']:
  describe_omf((work/name).read_bytes());context_count+=1
 need(context_count==893,'context object inventory')
 subprocess.run([sys.executable,'scripts/attest_toolchain.py','--identity-only','--output',str(OUT/'toolchain-identity-current.json')],cwd=ROOT,check=True,stdout=subprocess.PIPE)
 tool=json.loads((OUT/'toolchain-identity-current.json').read_text());need(tool['identity_pass'],'current toolchain identity')
 for row in manifest['toolchain_inputs']+[manifest['diet_tool']]:need(sha(read(row['path']))==row['sha256'],'actual tool input changed')
 # Avoid circular publication bootstrapping: verify the unchanged canonical
 # ledger here, then publish; ordinary tracking always checks the sidecar too.
 tracking=module(PACKAGE_ROOT/'scripts/validate_tracking.py','product_canonical_ledger');ledger_log=io.StringIO()
 with contextlib.redirect_stdout(ledger_log):ledger_exit=tracking.main(ROOT,validate_product=False)
 need(ledger_exit==0,'canonical ledger validation');(OUT/'ledger-current.log').write_text(ledger_log.getvalue())
 config=tomllib.loads(read('config/oracles.toml').decode());policy=config['policy'];oracles={r['id']:r for r in config['oracles']}
 target=next(t for t in tomllib.loads(read('config/targets.toml').decode())['artifacts'] if t['id']=='th03-mainl')
 packed=read(target['private_path']);candidate=(work/'MAINL.EXE').read_bytes();decoded=(work/'bin/th03/mainl.exe').read_bytes();mz=parse_mz(decoded);packed_mz=parse_mz(packed)
 need(sha(packed)==target['sha256'] and len(packed)==target['size'] and packed==candidate,'canonical identity/raw')
 need(mz.valid and packed_mz.valid,'format integrity')
 report=json.loads(read('.analysis/mainl-fullcold-r2-g10-20261021-v02-output/linked-verification.json'))
 need(report['diagnostic_checks_pass'] and len(report['linked']['checks'])==39 and all(report['linked']['checks'].values()),'full linked checks')
 need(report['global_ordered_difference_count']==0 and report['global_relocation_count']==677,'relocation order')
 rows=owners['owners'];need(len(rows)==145 and all(r['raw_equal'] and r['ordered_relocations_equal'] and r['reviewed_boundary'] and r['map_covered_bytes']==r['size'] for r in rows),'aggregate owner extent check')
 migration_path='config/mainl_product_acceptance/owner-migrations.json'
 migration_raw=(PACKAGE_ROOT/migration_path).read_bytes();need(sha(migration_raw)=='2b118337d97baf597c3a872e8d23e9d866fea253752bf3510f222ce64e4fef66','reviewed owner migration drift')
 migrations=json.loads(migration_raw)
 migration_validator=module(PACKAGE_ROOT/'scripts/lib/mainl_owner_migrations.py','product_owner_migrations')
 migration_checks=migration_validator.validate_mapping(ROOT,migrations,owners,work)
 need(migration_checks['valid'] and migration_checks['owners']==15 and migration_checks['parts']==30,'migration public/body-band check')
 need(migrations['resolved_owners']==15 and not migrations['remaining_gaps'],'migration closure')
 for pin in migrations['bindings']+[migrations['map'],migrations['linked_proof']]:
  raw=read(pin['path']);need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'migration input drift')
 by_id={r['unit_id']:r for r in rows};need(len(migrations['owners'])==15,'migration inventory')
 for migration in migrations['owners']:
  owner=by_id[migration['unit_id']];need(owner['lineage_gaps'],'migration unexpectedly replaces direct owner')
  for key in ['decoded_linear_start','size','raw_sha256','reviewed_boundary','raw_equal','ordered_relocations_equal']:need(migration[key]==owner[key],'migration owner mismatch '+key)
  cursor=owner['decoded_linear_start']
  for part in sorted(migration['parts'],key=lambda x:x['decoded_linear_start']):
   need(part['decoded_linear_start']==cursor and part['size']>0,'migration overlap/gap');cursor+=part['size']
   obj=owners['fresh_objects'][part['object']];need(obj['sha256']==part['object_sha256'] and obj['module_name']==part['module'],'migration producer drift')
   need(sha(read(part['source']))==part['source_sha256'],'migration maintained source drift')
   need(part['decoded_linear_start']==part['map_module_start']+part['object_segment_offset'],'migration MAP arithmetic')
   matched=[x for x in owner['map_parts'] if x['start']==part['map_module_start'] and x['map_segment']==part['map_segment'] and x['object_candidates']==[part['object']] and x['start']<=part['decoded_linear_start'] and cursor<=x['end']]
   need(len(matched)==1,'migration part not covered by unique actual MAP producer')
  need(cursor==owner['decoded_linear_start']+owner['size'],'migration incomplete extent')
  owner['historical_source_preserved']=owner['source'];owner['current_source_parts']=migration['parts'];owner['lineage_gaps']=[];owner['lineage_basis']='reviewed exact per-part backend migration'
 need(all(not r['lineage_gaps'] for r in rows),'incomplete decoded ownership')
 # Entire product has one mixed ownership extent. Per-unit semantic lineage is
 # deliberately separate and does not become proved merely by product equality.
 facts={
 'target-identity':'Pinned candidate-local-attested target manifest size/hash and current stored file agree; independent pristine provenance remains unknown.',
 'format-integrity':'Independent parser validates stored and decoded MZ structures.',
 'boundary-ownership':'Whole canonical file [0,37975) is one mixed product, not authored bytes; decoded145 reviewed extents have complete MAP coverage; archive/toolchain/stub/context roles remain explicit.',
 'toolchain-identity':'Fresh identity-only attestation plus all91 recorded toolchain inputs and DIET pin agree; observed original execution retained by fixed fullcold witness.',
 'toolchain-replay':'Fixed replay binds94 actual native argv/cwd, source graph1904, flags, order, inputs and producer receipts across two rounds.',
 'object-format-integrity':'All42 fresh project/authoredCRT OMF and893 extracted context OMF parse with strict framing/checksums; all42 fresh producers/wrapper dependencies and every staged/vendor dependency are checked; private893member library consumption/order bound by fullcold proof.',
 'cold-build-determinism':'Two source-only materializations, no retained project objects,940 byte-identical product pairs.',
 'layout-relocations':'All39 linked gates and677 ordered relocations match; actual MAP fully covers every145 decoded owner extent.',
 'raw-bytes':'Complete37975-byte source-built DIET output equals canonical stored artifact byte for byte.',
 'ledger-consistency':'Current canonical tracking validation passes; sidecar remains separate with no fabricated offsets, ownership totals or canonical state mutation.',
 'cold-aggregate-replay':'Both current complete MAINL graphs rebuild all project dependencies; all145 affected decoded extents rechecked against target;940 outputs agree.',
 }
 need(set(facts)==set(policy['exact_requires']),'required gate set mismatch')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z');scope='th03-mainl-mixed-stored-product';evidence={}
 witnesses={'fixed_replay':FIXED,'source_recipe':manifest['source_recipe'],'actual_owner_audit_sha256':sha((OUT/'actual-cold-owner-audit.json').read_bytes()),'toolchain_receipt_sha256':sha((OUT/'toolchain-identity-current.json').read_bytes()),'ledger_log_sha256':sha((OUT/'ledger-current.log').read_bytes()),'owner_migrations':dict(path=migration_path,sha256=sha(migration_raw))}
 bindings=OUT/'product-input-bindings.json';bindings.write_text(json.dumps(witnesses,sort_keys=True,indent=2)+'\n');proof_digest=sha(bindings.read_bytes())
 gate_results=OUT/'product-gate-results.json';gate_results.write_text(json.dumps(dict(schema='mainl-product-gate-observations-v1',input_bindings_sha256=proof_digest,oracle_results={k:dict(result='pass',observation=v) for k,v in facts.items()},native_invocations_now=0,full_replay_executed_now=full),sort_keys=True,indent=2)+'\n');gate_digest=sha(gate_results.read_bytes())
 for oracle,description in facts.items():
  global_scope=oracle in policy['global_evidence_oracles'];artifact_scope=oracle in policy['artifact_evidence_oracles'];key='ev-mainl-mixed-product-'+oracle
  evidence[key]=dict(id=key,claim_id=scope,oracle=oracle,artifact='' if global_scope else 'th03-mainl',unit_id='' if global_scope or artifact_scope else scope,extent_start='' if global_scope or artifact_scope else '0',extent_size='' if global_scope or artifact_scope else str(len(packed)),location='config/mainl_product_acceptance/product-gate-results.json',evidence_class=oracles[oracle]['accepts_evidence_classes'][0],result='pass',tool='source-bound fixed replay + independent static product audit',command='python3 scripts/replay_th03_mainl_product_acceptance.py'+(' --full-replay' if full else '')+(' --publish' if publish else ''),input_sha256=target['sha256'] if oracle=='raw-bytes' else proof_digest,output_sha256=sha(candidate) if oracle=='raw-bytes' else gate_digest,observed_utc=now,notes=description)
 check=module(PACKAGE_ROOT/'scripts/lib/mainl_product_scope.py','product_scope_check');missing=check.scoped_passes(ROOT,list(evidence),evidence,'th03-mainl',scope,0,len(packed));need(not missing,'Oracle scope/class rejected')
 # Derived decoded claims use decoded-load coordinates only. They never create
 # canonical physical offsets or add their byte totals to the physical numerator.
 decoded_claims=[]
 for owner in rows:
  unit=owner['unit_id'];start=owner['decoded_linear_start'];size=owner['size'];scoped={}
  for product_row in evidence.values():
   row=dict(product_row);oracle=row['oracle'];key='ev-mainl-decoded-'+unit+'-'+oracle
   row.update(id=key,claim_id=unit)
   if oracle not in policy['global_evidence_oracles'] and oracle not in policy['artifact_evidence_oracles']:row.update(unit_id=unit,extent_start=str(start),extent_size=str(size))
   if oracle=='raw-bytes':row.update(input_sha256=owner['raw_sha256'],output_sha256=owner['raw_sha256'],notes='Actual independent target and fresh source-built decoded extent equality, not a compressed-file offset.')
   if oracle=='boundary-ownership':row['notes']='Reviewed owner boundary; every intersecting MAP contribution has a unique direct source producer or explicit reviewed per-part composition migration.'
   scoped[key]=row
  need(not check.scoped_passes(ROOT,list(scoped),scoped,'th03-mainl',unit,start,size),'decoded owner Oracle scope/class rejected')
  decoded_claims.append(dict(owner,coordinate_space='decoded-load',oracle_gates_pass=True,oracle_evidence=scoped))
 result=dict(schema='th03-mainl-mixed-product-publication-proposal-v1',proposal_only=not publish,publication_review_required=not publish,baseline_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),product_oracle_gates_pass=True,canonical_units_changed=False,canonical_exact_credit_changed=False,factory_accepted=False,scope=dict(artifact='th03-mainl',coordinate_space='canonical-file',start=0,size=len(packed),origin='mixed-product',authored_credit_bytes=0),witnesses=witnesses,source_bound_retained_replay=True,full_replay_executed_now=full,oracle_evidence=evidence,owner_audit='actual-cold-owner-audit.json',decoded_owner_lineage_ready=sum(not r['lineage_gaps'] for r in rows),decoded_owner_acceptance_published=145 if publish else 0,decoded_owners=decoded_claims,fresh_omf_producer_checks=producer_checks,target_provenance='candidate-local-attested',remaining_boundary='Review and install maintained acceptance validator/status; all145 per-owner static lineage gates now pass without changing historical ledger.')
 (OUT/'actual-product-sidecar.json').write_text(json.dumps(result,indent=2)+'\n')
 publication=make_publication(proof,recipe,rows,target,publish)
 (OUT/'publication.json').write_text(json.dumps(publication,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['witnesses','oracle_evidence','decoded_owners','fresh_omf_producer_checks']},indent=2))
def make_publication(proof,recipe,rows,target,publish):
 def pin(path,logical=None):
  raw=path.read_bytes();return dict(path=logical or path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw))
 names={r['path'] for r in proof['pins'] if not r['path'].startswith('.analysis/')}
 names.update(['config/evidence.csv', 'config/hypotheses.csv', 'config/knowledge.csv', 'config/th03_main_authored_functions.csv', 'config/th03_function_boundaries.csv'])
 names.update(recipe['maintained_inputs']);names.update(r['source'] for r in rows)
 names.update([CODE,PROOF,RETAINED,'config/units.csv','config/oracles.toml','config/targets.toml','config/toolchain.toml','scripts/validate_tracking.py',target['private_path']])
 pins={name:pin(ROOT/name) for name in names}
 for name in ['scripts/validate_tracking.py','scripts/replay_th03_mainl_product_acceptance.py','scripts/lib/mainl_product_acceptance.py','scripts/lib/mainl_product_scope.py','scripts/lib/mainl_product_audit.py','scripts/lib/mainl_owner_migrations.py','config/mainl_product_acceptance/owner-migrations.json']:
  pins[name]=pin(PACKAGE_ROOT/name,name)
 # Bind actual target/candidate and final proof products without replaying the
 # 13,422 archival native-intermediate pins during ordinary status rendering.
 for rnd in [1,2]:
  for suffix in ['proposal/manifest.json','output/linked-verification.json']:
   name=f'.analysis/mainl-fullcold-r{rnd}-g10-20261021-v02-'+suffix;pins[name]=pin(ROOT/name)
  m=json.loads(read(f'.analysis/mainl-fullcold-r{rnd}-g10-20261021-v02-proposal/manifest.json'))
  for item in ['bin/th03/mainl.exe','obj/th03/mainl.map','MAINL.EXE','RESTORE.EXE']:
   name=m['work']+'/'+item;pins[name]=pin(ROOT/name)
 prefix='config/mainl_product_acceptance/'
 return dict(schema='mainl-product-acceptance-publication-v1',state='repository-local-accepted' if publish else 'review-ready',repository_local=True,factory_accepted=False,receipt=pin(OUT/'actual-product-sidecar.json',prefix+'actual-product-sidecar.json'),evidence_files=[pin(OUT/n,prefix+n) for n in ['product-input-bindings.json','product-gate-results.json','actual-cold-owner-audit.json','toolchain-identity-current.json','ledger-current.log']],input_bindings=sorted(pins.values(),key=lambda x:x['path']))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full-replay',action='store_true');p.add_argument('--publish',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();main(a.full_replay,a.publish,a.output)
