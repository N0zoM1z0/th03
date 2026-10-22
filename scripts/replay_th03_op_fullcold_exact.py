"""Dated source-cold proof replay; never launches or asserts today's native state."""
from pathlib import Path
import argparse,contextlib,hashlib,io,json,re,subprocess,sys,types
PROOF_SHA='4f50ea52204458a1ede50a26fd98f0ffbc32c214ea9d3fa9731503e643c86cfd'
SOURCE_BINDING_PATH = 'config/op_fullcold_exact/source_bindings_v2.json'
SOURCE_BINDING_SHA = '717324a3b8ae1d65930597085222d4684c96267985a570cfa41a0e22f9a77ae3'
LEDGER_BINDING_PATH = 'config/op_fullcold_exact/ledger_bindings_v1.json'
LEDGER_BINDING_SHA = '028b46e97d898278df6b30aae2abee61a9620fd6d47575f9bdab7c9a0a96675e'
ARCHIVAL_LEDGER_PATHS = {'config/evidence.csv', 'config/knowledge.csv'}
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
def read_source_bindings(root):
 binding = json.loads(pin(root, dict(path=SOURCE_BINDING_PATH, sha256=SOURCE_BINDING_SHA)))
 need(set(binding) == {'schema', 'dependency', 'pfopen_replay_binding', 'replacements'}
      and binding['schema'] == 'th03-op-fullcold-source-bindings-v2', 'source binding schema')
 need(set(binding['replacements']) == {'scripts/replay_th03_op_pfopen_source.py',
                                     'tests/test_op_pfopen_replay.py'}, 'source binding scope')
 pin(root, binding['dependency'])
 pin(root, binding['pfopen_replay_binding'])
 for name, entry in binding['replacements'].items():
  need(entry['current']['path'] == entry['historical_install_entry']['path'] == name,
       'source binding logical path')
  need(entry['snapshot']['path'].startswith('config/recovery/')
       and entry['snapshot']['path'].endswith('.py.txt'), 'inert source binding snapshot')
  for q in (entry['current'], entry['snapshot']):
   pin(root, q)
   need((Path(root)/q['path']).stat().st_mode & 0o777 == q['mode'], 'source binding mode '+q['path'])
 return binding

def read_git_ledger_snapshot(root, snapshot):
 need(set(snapshot) == {'commit', 'blob', 'path', 'sha256', 'bytes', 'mode', 'git_mode'},
      'archival Git snapshot schema')
 need(snapshot['path'] in ARCHIVAL_LEDGER_PATHS, 'archival ledger scope')
 need(all(isinstance(snapshot[k], str) and re.fullmatch('[0-9a-f]{40}', snapshot[k])
          for k in ('commit', 'blob')), 'immutable archival Git identity')
 need(snapshot['git_mode'] == (0o100755 if snapshot['mode'] & 0o111 else 0o100644),
      'archival Git executable mode')
 tree = subprocess.check_output(
     ['git', '-C', str(root), 'ls-tree', '-z', snapshot['commit'], '--', snapshot['path']],
     timeout=10)
 expected = ('%06o blob %s\t%s\0' %
             (snapshot['git_mode'], snapshot['blob'], snapshot['path'])).encode()
 need(tree == expected, 'archival Git tree identity/mode')
 raw = subprocess.check_output(
     ['git', '-C', str(root), 'cat-file', 'blob', snapshot['blob']], timeout=10)
 need(len(raw) == snapshot['bytes'] and sha(raw) == snapshot['sha256'],
      'archival Git blob identity')
 return raw

def read_ledger_bindings(root):
 binding = json.loads(pin(root, dict(path=LEDGER_BINDING_PATH, sha256=LEDGER_BINDING_SHA)))
 need(set(binding) == {'schema', 'role', 'dependency', 'current_ledger_validator', 'entries'}
      and binding['schema'] == 'th03-op-fullcold-archival-ledgers-v1'
      and binding['role'] == 'archival-install-metadata-not-composed-source',
      'archival ledger binding schema')
 need(set(binding['entries']) == ARCHIVAL_LEDGER_PATHS, 'archival ledger binding scope')
 need(binding['dependency'] == read_source_bindings(root)['dependency'],
      'archival ledger historical dependency')
 original = json.loads(pin(root, binding['dependency']))
 validator = binding['current_ledger_validator']
 need(validator['path'] == 'scripts/validate_tracking.py', 'current ledger validator scope')
 pin(root, validator)
 for name, entry in binding['entries'].items():
  need(set(entry) == {'historical_install_entry', 'git_snapshot'}, 'archival entry schema')
  historical, snapshot = entry['historical_install_entry'], entry['git_snapshot']
  need(historical in original['files'] and historical['path'] == snapshot['path'] == name,
       'archival install entry identity')
  need(all(snapshot[k] == historical[k] for k in ('sha256', 'bytes', 'mode')),
       'archival install content identity')
  read_git_ledger_snapshot(root, snapshot)
 return binding

def validate_current_ledgers(root, binding):
 q = binding['current_ledger_validator']
 need(q['path'] == 'scripts/validate_tracking.py', 'current ledger validator scope')
 pin(root, q)
 need((Path(root)/q['path']).stat().st_mode & 0o777 == q['mode'], 'current ledger validator mode')
 validator = load(Path(root)/q['path'])
 with contextlib.redirect_stdout(io.StringIO()):
  status = validator.main(Path(root), validate_product=False)
 need(status == 0, 'current canonical ledger validation')
 return True

def pin_source_dependency(root, dependency, entry, binding, ledger_binding=None):
 if ledger_binding is not None and entry['path'] in ledger_binding['entries']:
  replacement = ledger_binding['entries'][entry['path']]
  need(entry['path'] in ARCHIVAL_LEDGER_PATHS
       and replacement['git_snapshot']['path'] == entry['path'], 'archival ledger scope')
  need(dependency == ledger_binding['dependency']
       and entry == replacement['historical_install_entry'], 'archival ledger historical dependency')
  need(all(replacement['git_snapshot'][k] == entry[k] for k in ('sha256', 'bytes', 'mode')),
       'archival install content identity')
  # Git supplies only nonconsumed historical install metadata. The actual current
  # composers still read the workspace and must reproduce every one of330 inputs.
  return read_git_ledger_snapshot(root, replacement['git_snapshot'])
 if binding is None or entry['path'] not in binding['replacements']:
  return pin(root, entry)
 replacement = binding['replacements'][entry['path']]
 need(dependency == binding['dependency'] and entry == replacement['historical_install_entry'],
      'source binding historical dependency')
 # Historical install-package files are inert evidence. The current replay and
 # its regression tests have separate exact pins; no build source uses a fallback.
 pin(root, replacement['snapshot'])
 return pin(root, replacement['current'])

def check_current_sources(root,files=None,virtual=False):
 root=Path(root).resolve();p=proof(root,files);mods=p['source_stage_modules']
 if not virtual:need(ARCHIVAL_LEDGER_PATHS.isdisjoint(p['source_inventory']),
                     'archival ledgers must not be composed source inputs')
 binding = None if virtual else read_source_bindings(root)
 ledger_binding = None if virtual else read_ledger_bindings(root)
 if ledger_binding is not None:validate_current_ledgers(root, ledger_binding)
 for q in mods:pin(root,q)
 data=load(root/mods[0]['path']).payload(root)
 for q in mods[1:3]:data.update(load(root/q['path']).payload(root))
 data=load(root/mods[3]['path']).compose(data,root)
 for dep,overlay in zip(p['source_dependencies'],p['source_overlay_modules']):
  d=json.loads(pin(root,dep));base=(root/dep['path']).parent/'files' if virtual else root
  for q in d['files']:pin_source_dependency(base,dep,q,binding,ledger_binding)
  data=load(base/'scripts'/overlay['stage']).compose(data,base)
 inventory={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())};need(inventory==p['source_inventory'] and len(data)==330,'current330 source composition equals historical cold inputs');need(not any(Path(n).suffix.lower() in {'.obj','.exe','.map','.lib','.com'} for n in data),'no binary seed')
 return dict(current_source_composition_pass=True,virtual_uninstalled_proposals=virtual,source_files=330,native_invocations=0,source_acceptance=False,exact_acceptance=False,source_bindings_schema=binding['schema'] if binding else None,archival_ledger_bindings_schema=ledger_binding['schema'] if ledger_binding else None,current_ledgers_validated=ledger_binding is not None)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--files',type=Path);ap.add_argument('--check-current-source',action='store_true');ap.add_argument('--virtual-proposals',action='store_true');a=ap.parse_args();need(not a.virtual_proposals or a.check_current_source,'virtual option belongs to separate source check');print(json.dumps(check_current_sources(a.root,a.files,a.virtual_proposals) if a.check_current_source else replay(a.root,a.files),indent=2))
