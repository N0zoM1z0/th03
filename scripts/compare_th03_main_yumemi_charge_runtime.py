"""Strict four-receipt runtime comparison; never runs an emulator or model.
Only runtime EXE identity/elapsed and control EXE identity may differ. No other
fields, registers, flags, traces, hashes or memory observations are normalized.
"""
from pathlib import Path
from importlib.metadata import version
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
MODEL='scripts/review_th03_main_yumemi_charge_runtime.py'
TARGET_SHA='f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b'
CLOSURE_PATHS=(MODEL,'scripts/lib/pc98.py','scripts/lib/__init__.py')
SUPPORTED_VERSIONS={'unicorn':'1.0.3','capstone':'5.0.6'}
COUNTS={'reset':12,'add':12,'update':632,'target':46,'hit':202,'ring':194,'render':154,'gauge':870,'pellet':212,'bullet':212}
CONTROLS=['target-default-x','reset-state','add-state','update-delta','hit-return','ring-count','render-width','gauge-speed','pellet-type','bullet-type']
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,separators=(',',':')).encode()
def main():
 p=argparse.ArgumentParser()
 for name in ('target-runtime','candidate-runtime','target-controls','candidate-controls'):
  p.add_argument('--'+name,required=True)
 p.add_argument('--output','--json',dest='output',required=True);p.add_argument('--candidate-exe',required=True);p.add_argument('--target-exe',default='.analysis/targets/th03/main.exe');a=p.parse_args();out=Path(a.output);need(not out.exists(),'fresh comparison output required');reports={};inputs={}
 for name in ('target_runtime','candidate_runtime','target_controls','candidate_controls'):
  path=Path(getattr(a,name));raw=path.read_bytes();pin=sha(raw);reports[name]=json.loads(raw);inputs[str(path)]=pin
 CLOSURE={path:sha((ROOT/path).read_bytes()) for path in CLOSURE_PATHS};MODEL_SHA=CLOSURE[MODEL];CONTROL_SHA=MODEL_SHA;VERSIONS={k:version(k) for k in ('unicorn','capstone')};EXES={'target':(a.target_exe,TARGET_SHA),'candidate':(a.candidate_exe,reports['candidate_runtime']['exe_sha256'])}
 for path,pin in {**CLOSURE,**{v[0]:v[1] for v in EXES.values()}}.items():need(sha((ROOT/path).read_bytes())==pin,'live consumed input identity '+path);inputs[path]=pin
 need(VERSIONS==SUPPORTED_VERSIONS and {k:version(k) for k in VERSIONS}==VERSIONS,'unsupported package version or drift')
 for role,(path,pin) in EXES.items():
  r=reports[role+'_runtime'];c=reports[role+'_controls']
  for name,report in [('runtime',r),('controls',c)]:
   need(report['pass_'] is True and report['inputs_unchanged'] is True,role+' '+name+' did not pass/retain inputs')
   need(report['source_inputs']==CLOSURE and report['package_versions']==VERSIONS,role+' '+name+' consumed closure/version mismatch')
   need(report['exe_sha256']==pin and report['exact_acceptance'] is False,role+' '+name+' EXE/acceptance identity')
  need(r['kind']=='yumemi-charge-native-byte-semantic-model' and r['source_sha256']==MODEL_SHA,'runtime model identity')
  need(r['cases']==2546 and r['case_counts']==COUNTS and len(r['case_observation_digests'])==2546,'complete ordered case population')
  for pair in r['case_observation_digests']:need(len(pair)==2 and all(isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x) for x in pair),'invalid case/observation hash')
  need(sha(canonical(r['case_observation_digests']))==r['observations_sha256'],'observation aggregate recomputation')
  need(set(r['coverage'])==set(COUNTS),'all ten functions')
  for name,cov in r['coverage'].items():need(cov['missing']==[] and cov['instructions']==cov['visited'] and cov['visited']>0,'instruction coverage '+name)
  need(sum(v['visited'] for v in r['coverage'].values())==583 and len(r['visited'])==583 and r['visited']==sorted(set(r['visited'])),'full583 instruction positions')
  need((r['owned_extent_bytes'],r['owned_instruction_bytes'],r['switch_data_bytes'],r['functions'])==(1645,1613,32,10),'owner partition')
  need(r['maximum_instructions_per_case']==3661 and r['instruction_budget']==20000,'execution instruction bounds')
  need(isinstance(r['elapsed_seconds'],(float,int)) and 0<r['elapsed_seconds']<240,'wall budget')
  need(c['kind']=='yumemi-charge-native-negative-controls' and c['model_sha256']==MODEL_SHA and c['control_source_sha256']==CONTROL_SHA,'control implementation identity')
  need(c['target_files_modified'] is False,'mutations must be memory-only')
  need([v['name'] for v in c['controls']]==CONTROLS,'ten named negative controls')
  need(all(v['rejected'] is True and isinstance(v['reason'],str) and v['reason'] for v in c['controls']),'negative control rejection evidence')
 def compare(left,right,excluded):
  need(set(left)==set(right),'receipt schema mismatch')
  need({k:v for k,v in left.items() if k not in excluded}=={k:v for k,v in right.items() if k not in excluded},'strict cross-image observation mismatch')
 compare(reports['target_runtime'],reports['candidate_runtime'],{'exe_sha256','elapsed_seconds'})
 compare(reports['target_controls'],reports['candidate_controls'],{'exe_sha256'})
 # Recheck every consumed file immediately before creating the result.
 for path,pin in inputs.items():need(sha(Path(path).read_bytes() if Path(path).is_absolute() else (ROOT/path).read_bytes())==pin,'comparison input changed '+path)
 report=dict(kind='yumemi-charge-four-receipt-strict-runtime-comparison',pass_=True,inputs=inputs,comparison_source_sha256=sha(Path(__file__).read_bytes()),source_inputs=CLOSURE,package_versions=VERSIONS,cases_per_image=2546,instruction_positions_per_image=583,functions=10,negative_controls_per_image=10,observations_sha256=reports['target_runtime']['observations_sha256'],runtime_excluded_fields=['exe_sha256','elapsed_seconds'],control_excluded_fields=['exe_sha256'],all_other_receipt_fields_equal=True,exact_acceptance=False)
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
