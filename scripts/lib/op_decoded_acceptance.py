"""Decoded OP publication validation. No physical/file/Factory acceptance."""
from pathlib import Path
import csv,hashlib,json,tomllib,importlib.util,datetime,ast,contextlib,io
GATES=('target-identity','format-integrity','boundary-ownership','toolchain-identity','toolchain-replay','object-format-integrity','cold-build-determinism','layout-relocations','raw-bytes','ledger-consistency','cold-aggregate-replay')
PUBLICATION='config/op_decoded_acceptance/publication.json'
class Invalid(ValueError):pass
def need(ok,msg):
 if not ok:raise Invalid(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(root,name):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe path');p=Path(root)/p
 need(p.is_file() and not any(x.is_symlink() for x in [p,*p.parents]),'missing regular input '+name);return p
def pin(root,name):
 b=regular(root,name).read_bytes();return dict(path=name,bytes=len(b),sha256=sha(b))
def checked(root,q):
 need(pin(root,q['path'])==q,'binding drift '+q['path']);return regular(root,q['path']).read_bytes()
def descriptor(u):
 need(u['artifact']=='th03-op' and u['segment'].startswith('decoded:'),'decoded OP scope')
 need(u['state']=='source-present' and int(u['compare_size'],0)==int(u['size'],0),'complete maintained owner extent')
 need(not u['file_offset'] and u['boundary_state'] in ('reviewed','shared') and u['origin']=='authored' and u['source'],'owner eligibility')
 return dict(unit_id=u['id'],source=u['source'],start=int(u['segment'].split(':')[1],16)*16+int(u['offset'],0),size=int(u['compare_size'],0),origin=u['origin'])
def validate_inventory(owners,cohort):
 need(len(cohort)==33 and sum(x['size'] for x in cohort)==9530,'fixed cohort count/bytes')
 expected={x['unit_id']:x for x in cohort};need(len(expected)==33 and not any('character-selection' in x for x in expected),'cohort IDs')
 need(len(owners)==33 and {x['unit_id'] for x in owners}==set(expected),'owner set')
 spans=[]
 for o in owners:
  need({k:o[k] for k in ('unit_id','source','start','size','origin')}==expected[o['unit_id']],'descriptor drift')
  need(o['coordinate_space']=='decoded-load' and o['canonical_file_offset'] is None,'fabricated physical offset')
  need(o['size']>0 and o['start']>=0,'extent bounds')
  need(not any(o['start']<r and l<o['start']+o['size'] for l,r in spans),'owner overlap');spans.append((o['start'],o['start']+o['size']))
  need(len(o['rounds'])==2,'two owner observations')
  for r in o['rounds']:
   need(r['raw_equal'] and r['ordered_relocations_equal'] and r['map_covered_bytes']==o['size'] and r['source_lineage_verified'],'owner proof gap')
   need(r['target_sha256']==r['candidate_sha256'],'owner digest mismatch')
def validate_gates(gates,policy,evidence):
 need(set(gates)==set(GATES),'eleven gates required')
 for gate,r in gates.items():
  need(r['result']=='pass' and r['witness'] in evidence,'missing verified gate witness')
  spec=next(x for x in policy['oracles'] if x['id']==gate);need(r['evidence_class'] in spec['accepts_evidence_classes'],'gate class')
def require_bindings(provided,required,label='mandatory proof closure'):
 for name,q in required.items():need(provided.get(name)==q,label+' '+name)
def required_closure(root):
 proof=json.loads(regular(root,'config/op_fullcold/proof.json').read_bytes());inv=json.loads(checked(root,proof['inventory']))
 result={q['path']:q for q in inv['pins']};result[proof['inventory']['path']]=proof['inventory']
 stage='scripts/stage_th03_op_fullcold.py';raw=regular(root,stage).read_bytes();need(sha(raw)==proof['stage_sha256'],'stage binding')
 tree=ast.parse(raw);matches=[ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INPUT_HASHES' for t in n.targets)]
 need(len(matches)==1,'stage input closure')
 for name,digest in matches[0].items():
  q=pin(root,name);need(q['sha256']==digest,'stage input drift '+name);result[name]=q
 literals={t.id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) for t in n.targets if isinstance(t,ast.Name)}
 archive=pin(root,literals['ARCHIVE']);need(archive['sha256']==literals['ARCHIVE_SHA'],'stage archive binding');result[archive['path']]=archive
 result[stage]=pin(root,stage)
 for name in ('config/th03_main_authored_functions.csv','config/evidence.csv','config/hypotheses.csv','config/knowledge.csv','config/toolchain.toml'):result[name]=pin(root,name)
 return result
def owner_oracles(owners,gates,evidence,policy,input_bindings,command,observed_utc=None):
 witnesses={q['path']:q for q in evidence};spec={x['id']:x for x in policy['oracles']}
 now=observed_utc or datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 need(now.endswith('Z'),'Oracle timestamp must use UTC Z')
 input_digest=sha(json.dumps(input_bindings,sort_keys=True).encode());result={}
 for o in owners:
  rows={}
  for gate in GATES:
   glob=gate in policy['policy']['global_evidence_oracles'];artifact=gate in policy['policy']['artifact_evidence_oracles'];key='ev-op-decoded-'+o['unit_id']+'-'+gate;location=gates[gate]['witness']
   rows[key]=dict(id=key,claim_id=o['unit_id'],oracle=gate,artifact='' if glob else 'th03-op',unit_id='' if glob or artifact else o['unit_id'],extent_start='' if glob or artifact else str(o['start']),extent_size='' if glob or artifact else str(o['size']),location=location,evidence_class=spec[gate]['accepts_evidence_classes'][0],result='pass',tool='current source-bound fullcold replay plus independent decoded owner audit',command=command,input_sha256=o['rounds'][0]['target_sha256'] if gate=='raw-bytes' else input_digest,output_sha256=o['rounds'][0]['candidate_sha256'] if gate=='raw-bytes' else witnesses[location]['sha256'],observed_utc=now)
  result[o['unit_id']]=rows
 return result
def validate_row_binding(owner,key,row,gates,evidence,input_digest):
 gate=row['oracle'];expected='ev-op-decoded-'+owner['unit_id']+'-'+gate
 need(key==row['id']==expected and row['claim_id']==owner['unit_id'],'owner Oracle claim identity')
 need(row['location']==gates[gate]['witness'] and row['evidence_class']==gates[gate]['evidence_class'],'owner gate witness binding')
 need(row['input_sha256']==(owner['rounds'][0]['target_sha256'] if gate=='raw-bytes' else input_digest),'owner gate input binding')
 need(row['output_sha256']==(owner['rounds'][0]['candidate_sha256'] if gate=='raw-bytes' else evidence[row['location']]['sha256']),'owner gate output binding')
def verify(root,p,allow_review=False):
 need(p['schema']=='op-decoded-acceptance-v1','publication schema')
 need(p['state']=='repository-local-accepted' or (allow_review and p['state']=='review-ready'),'pending publication')
 need(p['product_exact'] is False and p['mixed_physical_exact_bytes']==0 and p['factory_accepted'] is False and p['canonical_credit_changed'] is False and p['whole_game_percentage'] is None,'accounting boundary')
 pins=p['input_bindings'];need(len(pins)==len({q['path'] for q in pins}),'duplicate bindings')
 for q in pins:checked(root,q)
 bound={q['path'] for q in pins};need({'config/units.csv','config/oracles.toml','config/targets.toml','config/th03_diet.toml','scripts/lib/op_decoded_acceptance.py','scripts/replay_th03_op_decoded_acceptance.py','scripts/replay_th03_op_fullcold.py','config/op_fullcold/proof.json','config/op_decoded_acceptance/cohort.json','scripts/validate_tracking.py','scripts/lib/__init__.py','config/op_decoded_acceptance/helper-bindings.json'}<=bound,'required bindings')
 helpers=json.loads(regular(root,'config/op_decoded_acceptance/helper-bindings.json').read_bytes())['pins'];provided={q['path']:q for q in pins}
 for q in helpers:need(provided.get(q['path'])==q,'missing reviewed helper binding '+q['path']);checked(root,q)
 require_bindings(provided,required_closure(root))
 cohort=json.loads(regular(root,'config/op_decoded_acceptance/cohort.json').read_bytes())['owners'];validate_inventory(p['owners'],cohort)
 recomputed_owners,recomputed_objects=physical_audit(Path(root),cohort);need(p['owners']==recomputed_owners,'independent physical owner audit')
 units={u['id']:u for u in csv.DictReader(regular(root,'config/units.csv').open())}
 for u in cohort:need(u==descriptor(units[u['unit_id']]),'current owner ledger drift')
 policy=tomllib.loads(regular(root,'config/oracles.toml').read_text());need(set(policy['policy']['exact_requires'])==set(GATES),'gate policy change')
 evidence={q['path']:q for q in p['evidence_bindings']};need(len(evidence)==len(p['evidence_bindings']),'duplicate witnesses')
 for q in evidence.values():checked(root,q)
 need(p['inputs']=={q['path']:q['sha256'] for q in pins+list(evidence.values())},'retention mirror drift')
 validate_gates(p['gates'],policy,evidence)
 # The publication cannot substitute new owner observations for the bound audit.
 def witness(g):return checked(root,evidence[p['gates'][g]['witness']])
 need(json.loads(witness('boundary-ownership'))==p['owners'],'owner witness mismatch')
 for g in ('raw-bytes','layout-relocations'):need(p['gates'][g]['witness']==p['gates']['boundary-ownership']['witness'],'owner witness scope')
 cold=json.loads(witness('cold-build-determinism'))
 need(cold['pass_checks'] and cold['native_phases_replayed']==56 and cold['native_invocations_now']==0 and cold['two_independent_source_builds'] and cold['raw_repeat_products']==29 and cold['raw_and_ordered_candidate_cohort_bytes']==9530,'cold witness dimensions')
 for g in ('toolchain-replay','cold-aggregate-replay'):need(p['gates'][g]['witness']==p['gates']['cold-build-determinism']['witness'],'cold witness scope')
 from lib.toolchain import attest_surface
 surfaces=[attest_surface(Path(root),item) for item in tomllib.loads(regular(root,'config/toolchain.toml').read_text())['surfaces'] if not item.get('bootstrap_only')]
 attestation=json.loads(witness('toolchain-identity'));need(attestation['identity_pass'] is True and attestation['surfaces']==surfaces and all(x['pass'] or not x['required'] for x in surfaces),'independent toolchain identity')
 from lib.op_diet_lineage import verify_diet_lineage
 from lib.pc98 import describe_blob
 recomputed_identity,lineage_pins=verify_diet_lineage(root,describe_blob)
 for q in lineage_pins:need(provided.get(q['path'])==q,'mandatory DIET lineage binding '+q['path'])
 need(json.loads(witness('target-identity'))==recomputed_identity,'independent restoration lineage')
 # Full historical registry replay runs once in explicit prepare.
 # Status validates the reviewed witness and its complete mandatory input closure.
 need(cold['selection_ordered_negative'] is True and cold['whole_program_different_bytes']==6,'preserved whole-program negatives')
 identity=json.loads(witness('target-identity'));need(identity['candidate_local_attested'] is True and identity['independent_pristine_attestation'] is False,'target provenance witness')
 need(p['gates']['format-integrity']['witness']==p['gates']['target-identity']['witness'],'format witness scope')
 objects=json.loads(witness('object-format-integrity'));need(objects==recomputed_objects,'independent physical object audit');need(len(objects)==54 and len({(x['round'],x['object']) for x in objects})==54 and all(x['valid'] and x['dependencies_bound'] for x in objects),'fresh object witness')
 # Use existing exact-grade scope/class rules for every same-ID decoded unit.
 spec=importlib.util.spec_from_file_location('op_decoded_tracking',regular(root,'scripts/validate_tracking.py'));tracking=importlib.util.module_from_spec(spec);spec.loader.exec_module(tracking)
 with contextlib.redirect_stdout(io.StringIO()):ledger_rc=tracking.main(Path(root),validate_product=False)
 need(ledger_rc==0,'current ledger replay')
 policy_rules=policy['policy'];known={x['id']:x for x in policy['oracles']}
 need(set(p['owner_oracles'])=={o['unit_id'] for o in p['owners']},'owner Oracle set')
 for o in p['owners']:
  rows=p['owner_oracles'][o['unit_id']];need(len(rows)==11 and {r['oracle'] for r in rows.values()}==set(GATES),'owner eleven gates')
  for key,row in rows.items():validate_row_binding(o,key,row,p['gates'],evidence,sha(json.dumps(p['input_bindings'],sort_keys=True).encode()))
  passed=tracking.accepted_oracle_passes(list(rows),rows,known,set(policy_rules['non_acceptance_evidence_classes']),artifact='th03-op',unit_id=o['unit_id'],extent_start=o['start'],extent_size=o['size'],global_evidence_oracles=set(policy_rules['global_evidence_oracles']),artifact_evidence_oracles=set(policy_rules['artifact_evidence_oracles']))
  need(set(GATES)<=passed,'owner Oracle scope/class/replay metadata')
 need(p['scope']=='reviewed-33-decoded-owners' and p['target_provenance']=='candidate-local-attested','scope/provenance')
 accepted=p['state']=='repository-local-accepted'
 return dict(repository_local=True,factory_accepted=False,product_exact=False,mixed_physical_exact_bytes=0,canonical_credit_changed=False,whole_game_percentage=None,decoded_exact_units=33 if accepted else 0,decoded_authored_bytes=9530 if accepted else 0,decoded_exact_unit_ids=sorted(x['unit_id'] for x in cohort) if accepted else [],reviewed_proof_ready=True)
def load_status(root):
 try:return verify(root,json.loads(regular(root,PUBLICATION).read_bytes()))
 except Exception as e:return dict(repository_local=True,factory_accepted=False,product_exact=False,mixed_physical_exact_bytes=0,decoded_exact_units=0,decoded_authored_bytes=0,decoded_exact_unit_ids=[],whole_game_percentage=None,reason=str(e))

def audit_owner(d,t,c,maps,graph,work,manifest,*,root,object_parser):
 start,end=d['start'],d['start']+d['size'];need(end<=len(t.program_image) and end<=len(c.program_image),'owner bounds')
 a,b=t.program_image[start:end],c.program_image[start:end];need(a==b,'owner raw mismatch '+d['unit_id'])
 rel=[]
 for image in (t,c):
  need(not any(r.linear<end and r.linear+2>start and not(start<=r.linear and r.linear+2<=end) for r in image.relocations),'straddling relocation')
  rel.append([[r.segment,r.offset,int.from_bytes(image.program_image[r.linear:r.linear+2],'little')] for r in image.relocations if start<=r.linear<end])
 need(rel[0]==rel[1],'owner ordered relocation mismatch')
 producers=[p for p in graph['project_producers'] if d['source'] in p['maintained_owner_sources']];need(len(producers)==1,'unique source producer');producer=producers[0]
 carriers=[x for x in maps if x['module']==producer['source'] and x['segment']*16+x['offset']<=start and end<=x['segment']*16+x['offset']+x['size']];need(len(carriers)==1,'complete unique MAP owner')
 obj=object_parser((work/producer['object']).read_bytes());deps=[n.replace('\\','/') for n in obj['dependency_paths']]
 need(obj['valid'] and producer['source'] in deps and d['source'] in deps,'source OMF lineage')
 for n in (producer['source'],d['source']):need(sha((work/n).read_bytes())==manifest['repeat_inputs'][n]['sha256'],'consumed source binding')
 need((work/d['source']).read_bytes()==regular(root,d['source']).read_bytes(),'current owner source binding')
 return dict(raw_equal=True,ordered_relocations_equal=True,target_sha256=sha(a),candidate_sha256=sha(b),map_covered_bytes=d['size'],source_lineage_verified=True,object=producer['object'],object_sha256=sha((work/producer['object']).read_bytes()),relocations=rel[0])

def physical_audit(root,cohort):
 from lib.pc98 import parse_mz
 from lib.omf import describe_omf
 from review_th03_decoded_code import code_rows
 diet=tomllib.loads(regular(root,'config/th03_diet.toml').read_text());decl=next(x for x in diet['artifacts'] if x['id']=='th03-op')
 owners=[dict(d,coordinate_space='decoded-load',canonical_file_offset=None,rounds=[]) for d in cohort];object_audit=[]
 for rnd in (1,2):
  name=f'.analysis/op-fullcold-r{rnd}-g6-v01-output/manifest.json';m=json.loads(regular(root,name).read_bytes());work=root/m['work'];g=json.loads(checked(root,{k:m['source_recipe'][k] for k in ('path','bytes','sha256')}));t_raw=checked(root,{k:m['target'][k] for k in ('path','bytes','sha256')});t=parse_mz(t_raw);c=parse_mz((work/'bin/th03/op.exe').read_bytes());need(t.valid and c.valid,'decoded MZ integrity')
  need(len(t_raw)==decl['decoded_size'] and sha(t_raw)==decl['decoded_sha256'],'decoded target identity')
  maps=code_rows((work/'obj/th03/op.map').read_text(),len(c.program_image))
  # Strictly parse and bind every fresh object, including unowned context producers.
  for pr in g['project_producers']:
   obj=describe_omf((work/pr['object']).read_bytes());need(obj['valid'],'fresh OMF integrity')
   expected='Turbo Assembler  Version 5.0' if pr['source'].endswith('.asm') else 'TC86 Borland C++ 4.02';need(expected in obj['translator_comments'],'fresh OMF producer')
   for n in [x.replace('\\','/') for x in obj['dependency_paths']]:
    if n.lower().startswith('c:/'):
     path='.analysis/toolchain/wineprefix/drive_c/'+n[3:];q=next((q for q in m['toolchain_inputs'] if q['path'].casefold()==path.casefold()),None);need(q is not None,'undeclared vendor dependency');checked(root,{k:q[k] for k in ('path','bytes','sha256')})
    else:need(n in m['repeat_inputs'] and sha((work/n).read_bytes())==m['repeat_inputs'][n]['sha256'],'unbound object dependency '+n)
   object_audit.append(dict(round=rnd,object=pr['object'],valid=True,dependencies_bound=True,sha256=sha((work/pr['object']).read_bytes()),producer=expected,dependencies=obj['dependency_paths']))
  for o in owners:o['rounds'].append(audit_owner(o,t,c,maps,g,work,m,root=root,object_parser=describe_omf))
 return owners,object_audit
