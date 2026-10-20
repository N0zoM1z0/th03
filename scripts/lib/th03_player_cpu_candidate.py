"""CPU-only candidate/default staging on the accepted tail. No acceptance credit."""
from pathlib import Path
import json,re,tomllib
from lib import th03_player_tail_candidate as tail,th03_yumemi_bomb_candidate as bomb,th03_score_candidate as score
from lib import th03_cpu_model as model,th03_cpu_gates as gates,th03_cpu_object as cpu,th03_cpu_display as display
from lib import th03_tail_compare as compare
from lib.omf import parse_omf,normalize_dependency_timestamps
from lib.pc98 import parse_mz
need=model.need;sha=model.sha
HERE=Path(__file__).resolve().parent
CANDIDATE_PATH='config/th03_main_player_cpu_candidate.toml'
BASELINE='.analysis/th03-main-exact/gpt-dots-player-tail-default-cold-v01'
OBJECT='obj/th03/p_cpu.obj'
ROOT_AFTER='f15dc04141d187b3dcd33f7b9ec7287b8d2983fc39b7cb5c74a2f8d86e5fc505'
RESPONSE_AFTER='1f57bc0a19a8260474bcfb578339077174daac7905573357aae9d38795200683'

def bind_candidate(accepted,additions,name):
 tail.bind_default(accepted)
 spec=json.loads((HERE/'th03_cpu_binding.json').read_text())
 need(name==CANDIDATE_PATH and additions==spec['candidate'],'exact additive CPU-only descriptor')
 need(len(additions['units'])==1 and len(additions['functions'])==4,'one CPU owner/four functions')
 return tail.bind_default(accepted)


def pre_cpu_config(accepted):
 import copy
 result=copy.deepcopy(accepted);spec=json.loads((HERE/'th03_cpu_binding.json').read_text())['candidate']
 need(result['units'][-1:]==spec['units'] and result['functions'][-4:]==spec['functions'],'exact final CPU default descriptor')
 del result['units'][-1:];del result['functions'][-4:]
 tail.bind_default(result)
 return result

def bind_default(accepted):
 import copy
 _,original=tail.bind_default(pre_cpu_config(accepted))
 return copy.deepcopy(accepted),original

def guard_baseline(root):
 pins=json.loads((HERE/'th03_cpu_baseline_pins.json').read_text())
 for n,h in pins.items():
  p=Path(root)/n;need(not p.is_symlink() and p.is_file() and sha(p.read_bytes())==h,'accepted tail baseline '+n)
 return pins

def freeze_expected(root):
 result=model.expectation();saved=json.loads((HERE/'th03_cpu_expectation.json').read_text())
 need(result['complete_literal_pairs']==saved['complete_literal_pairs'] and result['outside_literal_pairs']==saved['outside_literal_pairs'],'source/OMF prediction')
 literal,proof=display.derive(Path(root)/BASELINE/'round1/source')
 need(sha(literal)=='32f532c22b20e3e415d66c1cc4e3c4183088b9091a5ba1494a5ee45193e6163c','frozen finite display contract')
 return {'stream':result['complete_literal_pairs'],'outside':result['outside_literal_pairs'],'map_sha256':sha(literal),'display_groups':16,'timing':'frozen before either cold round; observed display metadata, not a sorting algorithm'}

def precompile_and_stage(work,env,logs,execute,default=False):
 work=Path(work);cpu.source_gate(work);tail.check_sources(work);bomb.check_build(work,default=default)
 need(sha((work/'th03_main.asm').read_bytes())==tail.ROOT_AFTER,'accepted tail source boundary')
 output=work/OBJECT;need(not output.exists() and not output.is_symlink(),'fresh CPU object absence')
 need(not (work/'obj/th03/p_cpre.obj').exists() and not (work/'th03/p_cpre.asm').exists(),'no extracted prefix producer')
 before={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')}
 output.parent.mkdir(parents=True,exist_ok=True)
 argv=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml '+"-DBINARY='M' -nobj/th03/ th03/p_cpu.cpp"]
 result=execute(argv,work,env,Path(logs)/'cpu-maintained-compile.log');need(result.get('exit_code')==0,'CPU compile failed')
 after={p.relative_to(work).as_posix():sha(p.read_bytes()) for p in (work/'obj').rglob('*.obj')}
 need(set(after)-set(before)=={OBJECT} and all(after.get(n)==h for n,h in before.items()),'CPU output inventory/non-CPU mutation')
 cpu.source_gate(work);proof=cpu.validate(output)
 raw=(work/'th03_main.asm').read_bytes();new=model.transform(raw);need(sha(new)==ROOT_AFTER,'CPU transformed root')
 (work/'th03_main.asm').write_bytes(new)
 return {'default_staging':default,'fresh_native_compilations':1,'cached_object_used':False,'compile':result,'object':proof,'prefix664_retained_uncredited':True,'source_sha256':ROOT_AFTER}

def check_round(root,work,target,proof,expected,default=False):
 root,work=Path(root),Path(work);cpu.source_gate(work);tail.check_sources(work);bomb.check_sources(work);bomb.check_build(work,default=default)
 need(sha((work/'th03_main.asm').read_bytes())==ROOT_AFTER,'cold CPU root source')
 need(sha((work/'obj/th03/main.@l').read_bytes())==RESPONSE_AFTER,'complete literal CPU response')
 need(not (work/'obj/th03/p_cpre.obj').exists() and not (work/'obj/th03/bm_yume.obj').exists() and not (work/bomb.ALIAS).exists(),'no extra prefix/bomb producers')
 structure=gates.root_gate(work/'obj/th03/main.obj');producer=cpu.validate(work/OBJECT)
 need(model.expectation()['complete_literal_pairs']==expected['stream'],'frozen CPU relocation model')
 linked=gates.linked_bytes(work);mapped=display.check_map((work/'obj/th03/main.map').read_bytes(),work)
 tail_producers={n:compare.validate_producer(n,work/p,root,parse_omf) for n,p in tail.OBJECTS.items()}
 bomb.validate_object((work/bomb.OBJECT).read_bytes());need(sha(normalize_dependency_timestamps((work/'obj/th03/score_hud.obj').read_bytes()))==score.SCORE_OMF_NORMALIZED_SHA,'score exact OMF')
 providers=bomb.check_providers(root,work);need(providers['pass_'],'bomb providers')
 current=parse_mz((work/'bin/th03/main.exe').read_bytes());original=parse_mz(target)
 need(compare.literal(current,compare.SPANS)==compare.literal(original,compare.SPANS) and len(compare.literal(current,compare.SPANS))==83,'tail83 exact literal order')
 need(all(current.program_image[a:b]==original.program_image[a:b] for a,b in compare.SPANS),'tail3433 raw')
 need(score.ordered_literal(current,score.SPANS)==score.PAIRS,'score6 exact literal order')
 need(score.ordered_literal(current,bomb.SPANS)==bomb.PAIRS,'bomb20 exact literal order')
 receipt=json.loads((root/BASELINE/'receipt.json').read_text());checks=[]
 allpaths={p.relative_to(work).as_posix() for p in (work/'obj').rglob('*.obj')}
 for number in (1,2):
  base=root/BASELINE/f'round{number}/source';prior=receipt['rounds'][number-1]
  need(allpaths==set(prior['all_objects'])|{OBJECT},'complete cold object inventory plus only CPU')
  need(all(sha(normalize_dependency_timestamps((work/n).read_bytes()))==h for n,h in prior['game_objects'].items() if n!='obj/th03/main.obj'),'all accepted nonroot game objects')
  prefix=f'{BASELINE}/round{number}/source/'
  products=sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',n[len(prefix):]))
  maps=sorted(n[len(prefix):] for n in proof if n.startswith(prefix) and n.endswith('.map'))
  need(len(products)==31 and len(maps)==43,'accepted product/map vector')
  need(sorted(p.relative_to(work).as_posix() for p in (work/'bin').rglob('*') if p.is_file() and re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',p.relative_to(work).as_posix()))==products,'cold products membership')
  need(sorted(p.relative_to(work).as_posix() for p in work.rglob('*.map'))==maps,'cold maps membership')
  need(all((work/n).read_bytes()==(base/n).read_bytes() for n in products if n!='bin/th03/main.exe'),'other30 products')
  need(all((work/n).read_bytes()==(base/n).read_bytes() for n in maps if n!='obj/th03/main.map'),'other42 MAPs')
  # Full program-image equality already proves all DATA/BSS/STACK storage and
  # score/bomb/tail bytes; the full literal model preserves all outside1551.
  checks.append({'baseline_round':number,'pass_':True,'other30_products':True,'other42_maps':True,'prior_nonroot_objects':True,'all_storage_raw_equal':True})
 return {'pass_':True,'default_staging':default,'root':structure,'cpu':producer,'linked':linked,'map':mapped,'producer_schemas':tail_producers,'accepted_bomb_providers':providers,'baselines':checks,'score_preservation':{'pass_':True,'baselines':checks},'bomb_preservation':{'pass_':True,'baselines':checks},'exact_acceptance':False,'fresh_structural_timing':'CPU object pre-build; actual root FIXUPP post-build, as established tail pipeline; no prelink-root claim'}
