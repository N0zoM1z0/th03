"""Dated source-cold proof replay; never launches or asserts today's native state."""
from pathlib import Path
import argparse,hashlib,json,sys,types
PROOF_SHA='4f50ea52204458a1ede50a26fd98f0ffbc32c214ea9d3fa9731503e643c86cfd'
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(root,q):
 p=Path(root)/q['path'];need(not any(x.is_symlink() for x in (p,*p.parents)),'artifact symlink');b=p.read_bytes();need(sha(b)==q['sha256'] and ('bytes' not in q or len(b)==q['bytes']),'artifact pin drift '+q['path']);return b
def load(p):
 p=Path(p);m=types.ModuleType('cold_exact_'+sha(str(p).encode())[:12]);m.__file__=str(p);sys.modules[m.__name__]=m;exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def proof(root,files=None):
 files=Path(files) if files is not None else Path(root);raw=(files/'config/op_fullcold_exact/proof.json').read_bytes();need(sha(raw)==PROOF_SHA,'maintained proof identity');return json.loads(raw)
def terminal_contract(t,p):
 need(t['comparison_pass'] is True and t['owned_lock_released'] is True and t['current_source_tool_mtime_HEAD_guards'] is True and t['historical_replay_requires_dated_attestation'] is True,'dated live terminal guard attestation')
 need(t['rounds']==2 and t['fresh_project_objects']==60 and t['actual_native_phases']==62 and all(t['exe_map_byte_deterministic'].values()),'dated fullcold coverage')
 need(t['final_frozen_manifest_sha256']=={str(i+1):q['sha256'] for i,q in enumerate(p['final_manifests'])},'root-observed final manifests')
 need(not any(t[k] for k in ('source_acceptance','exact_acceptance','whole_product_ownership','runtime','packed_equality','new_authored_code_credit')),'honest proof boundaries')
 return True
def replay(root,files=None):
 root=Path(root).resolve();files=Path(files).resolve() if files is not None else root;sys.path.insert(0,str(root/'scripts'));p=proof(root,files)
 for q in p['pins']:pin(root,q)
 pin(files,p['observer']);v=load(files/p['observer']['path']);v.ROOT=root;v.HERE=root/'.analysis/op-fullcold-ordered-deferred-v03';v.ORDER=root/'.analysis/op-global-order-checkpoint-proposal-v01/files/scripts/lib/op_global_order.py';v.ENV['WINEPREFIX']=str(root/'.analysis/toolchain/wineprefix')
 t=json.loads(pin(root,p['terminal_attestation']));terminal_contract(t,p);ms=[json.loads(pin(root,q)) for q in p['final_manifests']];reports=[]
 for i,m in enumerate(ms):
  r=v.verify(root/m['work'],m,require_complete=True);old=t['per_round'][i];need(r['diagnostic_checks_pass'] and r['whole_file_equal_target'] and r==old,'exact dated terminal report reproduction');reports.append(r)
 need(ms[0]['work']!=ms[1]['work'] and ms[0]['repeat_inputs']==ms[1]['repeat_inputs'] and ms[0]['head']==ms[1]['head'],'independent carriers and identical dated graph')
 need(len(p['raw_object_pairs'])==30,'all30 raw OMF pairs')
 from lib.omf import parse_omf
 for q in p['raw_object_pairs']:
  a,b=(pin(root,q[k]) for k in ('round1','round2'));need(a==b and q['raw_equal'] is True and bool(parse_omf(a)),'raw OMF repeat pair')
 for n in ('bin/th03/op.exe','obj/th03/op.map'):need((root/ms[0]['work']/n).read_bytes()==(root/ms[1]['work']/n).read_bytes(),'EXE/MAP raw repeat')
 return dict(schema='th03-op-fullcold-exact-historical-replay-v1',replay_pass=True,rounds=2,fresh_project_objects=60,actual_native_phases=62,raw_OMF_pairs_equal=30,raw_OMF_bytes_per_round=80839,EXE_and_MAP_raw_repeat_equal=True,whole63866_decoded_target_equal=True,all59770_program_bytes_equal=True,all607_literal_relocations_equal=True,dated_source_tool_registry_receipts=True,current_HEAD_or_registry_asserted=False,current_source_composition_checked=False,all44_prior_scopes_and_PFOPEN_preserved=True,new_authored_code_credit=0,source_acceptance=False,exact_acceptance=False,whole_product_ownership=False,packed_equality=False,runtime=False,native_invocations_by_replay=0)
def check_current_sources(root,files=None,virtual=False):
 root=Path(root).resolve();p=proof(root,files);mods=p['source_stage_modules']
 for q in mods:pin(root,q)
 data=load(root/mods[0]['path']).payload(root)
 for q in mods[1:3]:data.update(load(root/q['path']).payload(root))
 data=load(root/mods[3]['path']).compose(data,root)
 for dep,overlay in zip(p['source_dependencies'],p['source_overlay_modules']):
  d=json.loads(pin(root,dep));base=(root/dep['path']).parent/'files' if virtual else root
  for q in d['files']:pin(base,q)
  data=load(base/'scripts'/overlay['stage']).compose(data,base)
 inventory={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())};need(inventory==p['source_inventory'] and len(data)==330,'current330 source composition equals historical cold inputs');need(not any(Path(n).suffix.lower() in {'.obj','.exe','.map','.lib','.com'} for n in data),'no binary seed')
 return dict(current_source_composition_pass=True,virtual_uninstalled_proposals=virtual,source_files=330,native_invocations=0,source_acceptance=False,exact_acceptance=False)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--files',type=Path);ap.add_argument('--check-current-source',action='store_true');ap.add_argument('--virtual-proposals',action='store_true');a=ap.parse_args();need(not a.virtual_proposals or a.check_current_source,'virtual option belongs to separate source check');print(json.dumps(check_current_sources(a.root,a.files,a.virtual_proposals) if a.check_current_source else replay(a.root,a.files),indent=2))
