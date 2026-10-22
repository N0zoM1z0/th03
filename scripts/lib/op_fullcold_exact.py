"""Read-only cold output verification; no target or object rewriting."""
from pathlib import Path
import collections,hashlib,json,sys,types
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'.analysis/op-fullcold-ordered-deferred-v03';sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from review_th03_cpu_link_order import rows
ORDER=ROOT/'.analysis/op-global-order-checkpoint-proposal-v01/files/scripts/lib/op_global_order.py'
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(q):
 p=ROOT/q['path'];need(not any(x.is_symlink() for x in (p,*p.parents)),'symlink');b=p.read_bytes();need(sha(b)==q['sha256'] and len(b)==q['bytes'],'pin drift '+q['path']);return b
def helper(m):
 raw=pin(m['order_helper']);v=types.ModuleType('cold_order_helper');v.__file__=str(ORDER);exec(compile(raw,str(ORDER),'exec'),v.__dict__);v.ROOT=ROOT;return v
ENV={'PATH':'/usr/bin:/bin','HOME':'/tmp/home','LANG':'C','LC_ALL':'C','TZ':'UTC','DISPLAY':'','WAYLAND_DISPLAY':'','WINEDEBUG':'-all','WINEPREFIX':str(ROOT/'.analysis/toolchain/wineprefix'),'MSDOS_PATH':r'C:\TC4\BIN'}
def clean(r):
 leader=r.get('owned_leader');owned=isinstance(leader,list) and len(leader)==5 and type(leader[0]) is int and leader[0]>0 and type(leader[1]) is int and leader[1]>0 and isinstance(leader[2],str) and leader[2].isdigit()
 return owned and r.get('ok') is True and r['exit_code']==0 and not r['poison'] and not r['timeout'] and not r['cleanup_uncertain'] and r['initial_inventory_complete'] and r['inventory_complete'] and not r['survivors'] and not r['errors']
def meta(p):
 import stat
 p=Path(p);need(not any(x.is_symlink() for x in (p,*p.parents)),'receipt symlink');r=p.read_bytes();return dict(sha256=sha(r),bytes=len(r),mode=stat.S_IMODE(p.stat().st_mode))
def load_checked(q,name):
 raw=pin(q);v=types.ModuleType(name);sys.modules[name]=v;v.__file__=str(ROOT/q['path']);exec(compile(raw,v.__file__,'exec'),v.__dict__);return v
def started_check(started,q,work,environment):
 need(started['argv']==q['argv'] and Path(started['cwd'])==work,'actual producer argv/cwd')
 need(started['environment']==ENV==environment['environment'],'exact native environment')
 need(started['wait_seconds']==90 and started['cleanup_seconds']==15,'exact90+15 native limits')
 need(isinstance(environment['cpu'],list) and len(environment['cpu'])==1 and type(environment['cpu'][0]) is int and environment['cpu'][0]>=0 and type(environment['nice']) is int and environment['nice']>=10,'one CPU/nice ownership')
def registry_check(policy,before,after,recorded,started):
 from datetime import datetime
 need(recorded['phase_start_utc']==started['started_utc'] and recorded['child_tz']=='UTC','registry phase identity')
 lo=datetime.fromisoformat(recorded['phase_start_utc']);hi=datetime.fromisoformat(recorded['phase_end_utc']);need(lo.tzinfo is not None and hi.tzinfo is not None and 0<=(hi-lo).total_seconds()<=150,'bounded actual registry interval')
 replay=policy.validate_transition(before,after,phase_start_utc=recorded['phase_start_utc'],phase_end_utc=recorded['phase_end_utc'],child_tz='UTC')
 need(replay==recorded and replay['ok'] is True and replay['errors']==[],'exact unchanged-policy registry replay')
 return replay
SAME=('head','work','round','repeat_inputs','sources','toolchain_inputs','fixed_mtimes','owned_process','bounded_process','registry_policy','lock_helper','runner','composer','verifier','cold_plan','order_helper','nopcall_helper','producer_baseline_manifest','producer_baseline_prefix','cold_baseline_exe','cold_baseline_map','cold_baseline_report','target','stored_target','source_recipe','work_budget_seconds','factory_timeout_seconds','native_wait_seconds','owned_cleanup_seconds','native_round_phase_count','all_native_outputs')
def group_contract(mm,m,group,plan):
 need(all(mm[k]==m[k] for k in SAME),'earlier manifest source/tool/runner/round binding')
 g=group['group'];selected=plan['producers'][(g-1)*5:g*5]
 need(mm['group']==g and mm['phases']==group['phases'] and mm['output']==f'.analysis/op-fullcold-exact-r{m["round"]}-g{g}-output-v01','exact earlier group identity')
 need(mm['native_argv']=={q['phase']:q['argv'] for q in selected} and mm['native_outputs']=={q['phase']:q['output'] for q in selected},'exact earlier producer graph')
 need(mm['verify_after_group']==(g==7) and not mm['retained_objects'] and not mm['output_seeds'] and not mm['generated_copies'] and not mm['compose_sources'] and not mm['extra_outputs'] and not mm['phase_cwds'],'source-only earlier group contract')
def expected_receipts(phases,terminal):
 names={'manifest.json','environment.json','materialized-inputs.json','source-mtimes.json'}
 if terminal:names|={'completion.json','accumulated-objects.json','next-registry-baseline.json'}
 for phase in phases:
  names|={phase+x for x in ('.log','-started.json','-finished.json','-output.json','-registry-transition.json','-before-user.reg','-before-system.reg','-before-registry.json','-after-user.reg','-after-system.reg','-after-registry.json')}
  if phase=='link':names.add('link-map-output.json')
 if 'link' in phases and terminal:names.add('linked-verification.json')
 return names

def attest(work,m,require_complete=False):
 plan=json.loads(pin(m['cold_plan']));expected=plan['producers'];seen=[];objects={};previous=None;boundaries=[];source_names=set(m['repeat_inputs'])
 need(m['group']==7 and m['round'] in (1,2),'final cold group');need(len(source_names)==330 and not any(Path(n).suffix.lower() in {'.obj','.exe','.map','.lib','.com'} for n in source_names),'330 source-only inputs')
 if m['round']==2:
  r1=ROOT/'.analysis/op-fullcold-exact-r1-g7-output-v01';first=json.loads((ROOT/'.analysis/op-fullcold-exact-r2-g1-output-v01/manifest.json').read_text());need(first['registry_baseline']==json.loads((r1/'next-registry-baseline.json').read_text()),'inter-round registry continuity')
 source_meta={n:{k:q[k] for k in ('sha256','bytes','mode')} for n,q in m['repeat_inputs'].items()};source_times={n:q['mtime_ns'] for n,q in m['repeat_inputs'].items()}
 for n,q in source_meta.items():need(content_equal(work/n,q),'historical source content; mode/time from dated receipts')
 for group in plan['groups']:
  g=group['group'];out=ROOT/f'.analysis/op-fullcold-exact-r{m["round"]}-g{g}-output-v01';frozen=HERE/f'r{m["round"]}g{g}-manifest.json'
  need((out/'manifest.json').read_bytes()==frozen.read_bytes(),'frozen versus actual group manifest')
  mm=json.loads((out/'manifest.json').read_text());group_contract(mm,m,group,plan);dated_descriptors(mm)
  need(mm['accumulated_objects']==objects,'declared prior fresh-object inventory')
  if g==1:need(mm['predecessor'] is None and mm['materialized_inputs']=={} and mm['source_mtimes']=={},'fresh first group')
  else:
   need(pin(mm['predecessor'])==(previous/'completion.json').read_bytes(),'exact predecessor completion pin')
   need(mm['registry_baseline']==json.loads((previous/'next-registry-baseline.json').read_text()),'inter-group registry continuity')
   need(mm['materialized_inputs']==source_meta and mm['source_mtimes']==source_times,'declared continuation sources')
   previous_rows={q['path']:q for q in mm['inputs']};expected_paths={str(p.relative_to(ROOT)) for p in previous.iterdir() if p.is_file()}
   need(expected_paths<=set(previous_rows),'every prior producer/registry receipt pinned')
  need(json.loads((out/'materialized-inputs.json').read_text())==source_meta,'materialized source receipt')
  need(json.loads((out/'source-mtimes.json').read_text())==source_times,'source timestamp receipt')
  terminal=g<7 or require_complete
  need({p.name for p in out.iterdir() if p.is_file()}==expected_receipts(group['phases'],terminal),'exact actual group receipt closure')
  environment=json.loads((out/'environment.json').read_text());policy=load_checked(mm['registry_policy'],'cold_policy_'+str(g));last=None
  for phase in group['phases']:
   q=expected[len(seen)];need(q['phase']==phase,'literal producer sequence');started=json.loads((out/(phase+'-started.json')).read_text());finished=json.loads((out/(phase+'-finished.json')).read_text());recorded=json.loads((out/(phase+'-registry-transition.json')).read_text())
   started_check(started,q,work,environment);need(clean(finished),'full actual owned cleanup')
   before={n:(out/(phase+'-before-'+n)).read_bytes() for n in ('user.reg','system.reg')};after={n:(out/(phase+'-after-'+n)).read_bytes() for n in before}
   for label,values in (('before',before),('after',after)):need(json.loads((out/(phase+'-'+label+'-registry.json')).read_text())=={n:sha(b) for n,b in values.items()},'registry snapshot digest receipt')
   if last is None:need(all(sha(before[n])==mm['registry_baseline'][n]['sha256'] and len(before[n])==mm['registry_baseline'][n]['bytes'] for n in before),'frozen live registry baseline')
   else:need(before==last,'within-group registry chain')
   registry_check(policy,before,after,recorded,started);last=after
   observed=json.loads((out/(phase+'-output.json')).read_text());need(content_equal(work/q['output'],observed),'fresh output full metadata attestation');objects[q['output']]=observed
   if phase=='link':qmap=json.loads((out/'link-map-output.json').read_text());need(content_equal(work/'obj/th03/op.map',qmap),'MAP metadata receipt');objects['obj/th03/op.map']=qmap
   seen.append(phase)
  if terminal:
   c=json.loads((out/'completion.json').read_text());need(c['complete'] is True and c['owned_lock_released'] is True and c['errors']==[] and c['native_invocations']==len(group['phases']) and c['round']==m['round'] and c['group']==g and c['phases']==group['phases'],'exact terminal group completion')
   need(json.loads((out/'accumulated-objects.json').read_text())==objects,'growing actual output inventory')
   nxt=json.loads((out/'next-registry-baseline.json').read_text());need(set(nxt)==set(last) and all(nxt[n]['sha256']==sha(last[n]) and nxt[n]['bytes']==len(last[n]) and nxt[n]['mode']==mm['registry_baseline'][n]['mode'] for n in last),'terminal registry snapshot binding')
  previous=out
 need(len(seen)==31 and len(objects)==32 and sum(x!='link' for x in seen)==30,'full actual producer coverage')
 need({str(p.relative_to(work)) for p in work.rglob('*') if p.is_file()}==source_names|set(m['all_native_outputs']),'exact final carrier closure')
 return dict(project_objects_fresh=30,actual_phases=31,no_project_object_seed=True,all_actual_phase_receipts_valid=True,registry_transitions_replayed=31,every_prior_group_receipt_pinned=True,source_and_accumulated_object_receipts_replayed=True,final_completion_checked=require_complete,registry_baselines='Initial group uses the then-live frozen baseline; this dedicated run requires exact predecessor continuity across subsequent groups and rounds.')

def core_checks(c,b,t):
 return dict(full59770_program_target_exact=len(c.program_image)==len(t.program_image)==59770 and c.program_image==t.program_image,literal607_target_exact=len(c.relocations)==607 and [[r.segment,r.offset] for r in c.relocations]==[[r.segment,r.offset] for r in t.relocations],whole_program_baseline_equal=c.program_image==b.program_image)

def file_checks(cr,tr):
 c,t=map(parse_mz,(cr,tr));return dict(full63866_decoded_target_equal=len(cr)==63866 and cr==tr,header4096_target_exact=c.header.header_size==t.header.header_size==4096 and cr[:4096]==tr[:4096])

def verify_product(work,m):
 work=Path(work);dated_descriptors(m);h=helper(m)
 for n,q in m['repeat_inputs'].items():need((work/n).read_bytes()==pin(q),'source changed '+n)
 cr=(work/'bin/th03/op.exe').read_bytes();br=pin(m['cold_baseline_exe']);tr=pin(m['target']);c,b,t=map(parse_mz,(cr,br,tr));need(c.valid and b.valid and t.valid,'valid MZ')
 cm=(work/'obj/th03/op.map').read_bytes();bm=pin(m['cold_baseline_map']);baseline=json.loads(pin(m['cold_baseline_report']));owners=[]
 for q in baseline['owners']:
  a,z,y=(h.scoped(x,q['segment'],q['offset'],q['size']) for x in (c,b,t));owners.append(dict(id=q['id'],size=q['size'],baseline_equal=a==z,target_equal=a==y))
 need(len(owners)==44 and sum(x['size'] for x in owners)==12940,'original owner denominator')
 pfc,pfb,pft=(h.scoped(x,0,0x2ef2,281) for x in (c,b,t));anchor=h.verify_anchor(work/'obj/th03/oplayout.obj');nh=load_checked(m['nopcall_helper'],'cold_nopcall_helper');nh.ROOT=ROOT;pin(m['producer_baseline_prefix']);prefix=nh.verify_split_object(work/'obj/th03/op.obj','prefix');calls=nh.verify_calls(work,{'baseline_manifest':m['producer_baseline_manifest']},prefix);suffix=h.verify_split_object(work/'obj/th03/optail.obj','suffix')
 checks=core_checks(c,b,t);checks.update(file_checks(cr,tr));checks.update(thirty_genuine_far_producers=len(calls["calls"])==30 and calls["filled_bytes"]==0,whole_exe_actual_baseline_equal=cr==br,whole_map_actual_baseline_equal=cm==bm,header_baseline_equal=h.header_without_relocations(cr)==h.header_without_relocations(br),publics_all_names_addresses_multiplicity_idle_strict=h.public_sections(cm.decode('ascii'))==h.public_sections(bm.decode('ascii')),all_positive_contributions_strict=[r for r in rows(work/'obj/th03/op.map') if r['size']]==[r for r in rows(ROOT/m['cold_baseline_map']['path']) if r['size']],all44_scopes_preserved=all(x['baseline_equal'] and x['target_equal'] for x in owners),PFOPEN281_preserved=pfc==pfb==pft,anchor_zero_bytes=anchor['pass_checks'],prefix_structure=prefix['pass_checks'],suffix_structure=suffix['pass_checks'])
 return dict(schema='th03-op-fullcold-exact-diagnostic-v3',diagnostic_checks_pass=all(checks.values()),checks=checks,original_far_call_producers=calls,owners=owners,owner_count=44,owner_bytes=12940,exe_sha256=sha(cr),map_sha256=sha(cm),actual_pairs=h.rels(c),target_pairs=h.rels(t),target_program_differences=[i for i,(x,y) in enumerate(zip(c.program_image,t.program_image)) if x!=y],whole_file_equal_target=cr==tr,decoded_target_header_difference_expected=False,source_acceptance=False,exact_acceptance=False,whole_product_ownership=False,packed_equality=False,runtime=False,new_authored_code_credit=0)

def verify(work,m,require_complete=False):
 provenance=attest(Path(work),m,require_complete=require_complete);report=verify_product(work,m);return dict(report,provenance=provenance,cold_round_pending_terminal_completion=not require_complete)

def content_equal(p,q):
 need(set(q)=={'sha256','bytes','mode'} and isinstance(q['mode'],int) and 0<=q['mode']<=0o7777,'dated file metadata shape')
 b=Path(p).read_bytes();return sha(b)==q['sha256'] and len(b)==q['bytes']
def dated_descriptors(m):
 inputs={q['path']:q for q in m['inputs']};need(len(inputs)==len(m['inputs']),'unique dated input descriptors')
 need(len(m['toolchain_inputs'])==90 and set(m['fixed_mtimes'])=={q['path'] for q in m['toolchain_inputs']},'dated90 tool timestamps')
 for q in m['toolchain_inputs']+list(m['repeat_inputs'].values()):
  need(inputs[q['path']]=={k:q[k] for k in ('path','sha256','bytes','mode')},'dated source/tool descriptor binding')
 need(len(m['sources'])>0 and all(len(q['sha256'])==64 and q['bytes']>=0 and isinstance(q['mode'],int) for q in m['sources'].values()),'dated tracked source inventory')
 return True
