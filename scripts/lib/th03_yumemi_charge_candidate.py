"""One charge owner on accepted CPU/tail/bomb/score graph; no acceptance writes."""
from pathlib import Path
import copy,hashlib,json,re,struct
from lib import th03_player_cpu_candidate as cpu,th03_player_tail_candidate as tail,th03_yumemi_bomb_candidate as bomb,th03_score_candidate as score
from lib import th03_charge_verify as verify,th03_charge_map as map_gate
from lib.omf import parse_omf,normalize_dependency_timestamps
from lib.pc98 import parse_mz
HERE=Path(__file__).resolve().parent
CANDIDATE_PATH='config/th03_main_yumemi_charge_candidate.toml'
OBJECT='obj/th03/cs_yume.obj'
CONTRACT_SHA='76be5fcde93d6840bcb923b446c93ca6e8a4f193b2c44593961e94d6a4772ccd'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def contract():
 raw=(HERE/'th03_charge_contract.json').read_bytes();need(sha(raw)==CONTRACT_SHA,'charge contract identity');return json.loads(raw)
def bind_candidate(accepted,additions,name):
 need(name==CANDIDATE_PATH and additions==contract()['candidate'],'exact charge-only descriptor')
 return cpu.bind_default(accepted)
def bind_default(accepted):
 out=copy.deepcopy(accepted);c=contract()['candidate'];need(out['units'][-1:]==c['units'] and out['functions'][-10:]==c['functions'],'exact appended charge default descriptor');del out['units'][-1:];del out['functions'][-10:]
 _,original=cpu.bind_default(out);return copy.deepcopy(accepted),original
def source_gate(work):
 work=Path(work)
 for n,h in contract()['source_pins'].items():need(sha((work/n).read_bytes())==h,'charge maintained source '+n)
 need((work/'th03/cs_yume.cpp').read_bytes()==b'#include "src/main/player/chargeshot_yumemi.cpp"\n','charge wrapper')
def transform(raw):
 c=contract();need(sha(raw)==c['root_before'],'charge must follow accepted CPU source stage');lines=raw.splitlines(True);out=[];at=0
 for e in c['root_edits']:
  i,j=e['start'],e['end'];need(at<=i<=j and b''.join(lines[i:j])==e['before'].encode('latin1'),'finite charge root source edit');out.extend(lines[at:i]);out.append(e['after'].encode('latin1'));at=j
 out.extend(lines[at:]);result=b''.join(out);need(sha(result)==c['root_after'],'charge root result');return result
def guard_baseline(root):
 root=Path(root);c=contract()
 for row in c['baseline_pins'].values():verify.pinned(root,row)
 for row in c['diagnostic_inputs'].values():verify.pinned(root,row)
 verify.pinned(root,c['candidate_root_object'])
 return c['baseline_pins']
def freeze_expected(root):
 from importlib.metadata import version
 need({k:version(k) for k in ('unicorn','capstone')}=={'unicorn':'1.0.3','capstone':'5.0.6'},'charge runtime supported package versions; launch with .venv/bin/python3')
 c=contract();guard_baseline(root)
 return dict(root_sha256=c['root_after'],response_sha256=c['response_sha256'],map_sha256='05c0762f95aa5a2c37dc367a6e3b23c03da03d57927f0d61d2d6b5114fb8c245',timing='finite source/OMF/MAP contracts fixed before cold native rounds')
def precompile_and_stage(work,env,logs,execute):
 work=Path(work);source_gate(work);tail.check_sources(work);bomb.check_sources(work);bomb.check_build(work,default=True)
 need(sha((work/'th03_main.asm').read_bytes())==contract()['root_before'],'exact accepted CPU root before charge')
 need(not (work/OBJECT).exists(),'no cached charge object');before={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')}
 argv=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml '+"-DBINARY='M' -nobj/th03/ th03/cs_yume.cpp"]
 result=execute(argv,work,env,Path(logs)/'charge-maintained-compile.log');need(result.get('exit_code')==0,'charge native compile')
 after={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')};need(set(after)-set(before)=={OBJECT} and all(after[n]==h for n,h in before.items()),'only fresh charge object')
 c=contract();old=verify.pinned(verify.ROOT,c['diagnostic_inputs']['historical_charge_object']);obj=verify.object_contract((work/OBJECT).read_bytes(),old,work/OBJECT);source_gate(work)
 raw=(work/'th03_main.asm').read_bytes();(work/'th03_main.asm').write_bytes(transform(raw))
 return dict(compile=result,object=obj,retained_object_used=False,fresh_native_compilations=1)
def complete_literal_transition(current,baseline,target):
 # Comparison-only finite reference transition. Never mutates executable bytes.
 before=[(5021,12924),(5021,12544),(5021,12574),(5021,12693),(5021,12762),(5021,12850),(5021,12882),(5021,12900),(5021,13061),(5021,13086),(5021,13711),(5021,13738)]
 after=[(5021,13086),(5021,13061),(5021,12924),(5021,12900),(5021,12882),(5021,12850),(5021,12762),(5021,12693),(5021,12574),(5021,12544),(5021,13738),(5021,13711)]
 need(len(current)==len(baseline)==1553,'complete literal population')
 need([i for i,q in enumerate(baseline) if verify.inside(q)]==list(range(881,893)),'baseline charge block placement')
 need(baseline[881:893]==before,'pinned baseline charge order')
 need([q for q in target if verify.inside(q)]==after,'pinned canonical charge order')
 need(len(before)==len(after)==len(set(before))==12 and set(before)==set(after),'finite owner relocation membership')
 expected=baseline[:881]+after+baseline[893:]
 need(current==expected,'complete1553 finite charge literal transition')
 need([i for i,q in enumerate(current) if verify.inside(q)]==list(range(881,893)),'actual charge block interposition')
 need([q for q in current if not verify.inside(q)]==[q for q in baseline if not verify.inside(q)],'outside1541 exact literal order')
 return dict(pass_=True,whole_literal_count=1553,unchanged_outside_count=1541,charge_block=[881,893],before=before,after=after,executable_mutation=False)

def check_round(root,work,target,proof,expected,default=False):
 from lib import th03_cpu_object,th03_tail_compare,th03_charge_root
 root,work=Path(root),Path(work);c=contract();source_gate(work);tail.check_sources(work);bomb.check_sources(work);bomb.check_build(work,default=True)
 need(expected==freeze_expected(root),'frozen charge expectations');need(sha((work/'th03_main.asm').read_bytes())==c['root_after'],'charge root source');need(sha((work/'obj/th03/main.@l').read_bytes())==c['response_sha256'],'complete literal response')
 rootproof=th03_charge_root.verify(work/'obj/th03/main.obj')
 objproof=verify.verify(work,c['diagnostic_inputs']);need(objproof['diagnostic_checks_pass'],'charge linked contract')
 base=root/c['baseline'];mapproof=map_gate.verify((base/'round1/source/obj/th03/main.map').read_bytes(),(work/'obj/th03/main.map').read_bytes())
 # Keep unchanged accepted producer gates; only root and MAP use source-reviewed replacement contracts.
 cpuproved=th03_cpu_object.validate(work/cpu.OBJECT)
 tailproved={n:th03_tail_compare.validate_producer(n,work/p,root,parse_omf) for n,p in tail.OBJECTS.items()}
 bomb.validate_object((work/bomb.OBJECT).read_bytes());need(sha(normalize_dependency_timestamps((work/'obj/th03/score_hud.obj').read_bytes()))==score.SCORE_OMF_NORMALIZED_SHA,'score exact OMF')
 providers=bomb.check_providers(root,work);need(providers['pass_'],'accepted bomb providers')
 actual={p.relative_to(work).as_posix() for p in (work/'obj').rglob('*.obj')};receipt=json.loads((base/'receipt.json').read_text());checks=[]
 for number in (1,2):
  prior=receipt['rounds'][number-1];old=base/f'round{number}/source';need(actual==set(prior['all_objects'])|{OBJECT},'whole cold object inventory plus only charge')
  raw=(work/'bin/th03/main.exe').read_bytes();previous=(old/'bin/th03/main.exe').read_bytes();current=parse_mz(raw);previous_mz=parse_mz(previous)
  need(current.program_image==previous_mz.program_image and current.header==previous_mz.header,'complete baseline loaded bytes/header')
  literal_transition=complete_literal_transition(verify.pairs(current),verify.pairs(previous_mz),verify.pairs(parse_mz(target)))
  need(th03_tail_compare.header_parts(raw)==th03_tail_compare.header_parts(previous) and len(raw)==len(previous),'all nonrelocation header bytes/file size')
  hb=struct.unpack_from('<H',raw,8)[0]*16;ha=struct.unpack_from('<H',previous,8)[0]*16
  need(raw[hb+len(current.program_image):]==previous[ha+len(previous_mz.program_image):],'all overlay bytes')
  expected_objects={**prior['game_objects'],**{n:prior['all_objects'][n] for n in tail.EXTRA_GAME_PATHS}}
  need(all(sha(normalize_dependency_timestamps((work/n).read_bytes()))==h for n,h in expected_objects.items() if n!='obj/th03/main.obj'),'every old nonroot game object')
  products=sorted(n for n in (p.relative_to(old).as_posix() for p in (old/'bin').rglob('*') if p.is_file()) if re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',n));maps=sorted(p.relative_to(old).as_posix() for p in old.rglob('*.map'))
  need(len(products)==31 and len(maps)==43,'baseline complete product/map inventory')
  newproducts=sorted(p.relative_to(work).as_posix() for p in (work/'bin').rglob('*') if p.is_file() and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',p.relative_to(work).as_posix()));need(newproducts==products and sorted(p.relative_to(work).as_posix() for p in work.rglob('*.map'))==maps,'fresh product/map inventory')
  need(all((work/n).read_bytes()==(old/n).read_bytes() for n in products if n!='bin/th03/main.exe'),'other30products');need(all((work/n).read_bytes()==(old/n).read_bytes() for n in maps if n!='obj/th03/main.map'),'other42maps')
  checks.append(dict(baseline_round=number,pass_=True,prior_nonroot_objects=True,other30_products=True,other42_maps=True,literal_transition=literal_transition))
 preserved=dict(pass_=True,baselines=checks,full_loaded_image_equal=True,outside1541_literal_equal=True)
 return dict(pass_=True,root=rootproof,charge=objproof,map=mapproof,cpu=cpuproved,tail=tailproved,bomb_providers=providers,baselines=checks,score_preservation=preserved,bomb_preservation=preserved,exact_acceptance=False,default_staging=default)

def runtime_pair(root,work,logs,env,execute):
 import sys
 root,work,logs=Path(root),Path(work),Path(logs)
 model=root/'scripts/review_th03_main_yumemi_charge_runtime.py';compare=root/'scripts/compare_th03_main_yumemi_charge_runtime.py'
 commands=[];reports={}
 for role,exe in [('target',root/'.analysis/targets/th03/main.exe'),('candidate',work/'bin/th03/main.exe')]:
  pin=sha(exe.read_bytes())
  for mode in ('runtime','controls'):
   out=logs/('charge-'+role+'-'+mode+'.json');need(not out.exists(),'fresh runtime receipt')
   argv=[sys.executable,str(model),'--exe',str(exe),'--expected-sha256',pin,'--json',str(out),'--seconds','150']
   if mode=='controls':argv.append('--negative-controls')
   command=execute(argv,root,env,logs/('charge-'+role+'-'+mode+'.log'));need(command.get('exit_code')==0,'fresh charge '+role+' '+mode);commands.append(command);reports[role+'-'+mode]=out
   need(sha(exe.read_bytes())==pin,'runtime image unchanged')
 out=logs/'charge-runtime-comparison.json';need(not out.exists(),'fresh strict comparison')
 argv=[sys.executable,str(compare),'--candidate-exe',str(work/'bin/th03/main.exe'),'--target-exe',str(root/'.analysis/targets/th03/main.exe')]
 for name,path in reports.items():argv.extend(['--'+name,str(path)])
 argv.extend(['--json',str(out)]);command=execute(argv,root,env,logs/'charge-runtime-comparison.log');need(command.get('exit_code')==0,'strict charge runtime comparison');commands.append(command)
 result=json.loads(out.read_text());need(result['pass_'] is True,'charge runtime pair failed')
 return dict(pass_=True,commands=commands,comparison=result,receipt_sha256=sha(out.read_bytes()),fresh_images=True)
