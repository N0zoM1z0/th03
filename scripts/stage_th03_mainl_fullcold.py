"""Source-only current MAINL chain and fresh36-object cold source snapshots.
No native tools, cached objects, target bytes, or output products are consumed.
"""
from pathlib import Path
import sys,inspect,importlib,json,hashlib,re
sys.path.insert(0,str(Path.cwd()/'scripts'))
import stage_th03_mainl_cold as base
sha=base.sha
FAMILIES=['snow','regmusic','regdata','staff_prefix','staff_extension','staff_transition','staff_paired','staff_verdict','staff_complete','staff_data','continue','root_prefix','root_intro','root_shots','root_data','root_complete_data']
ALIASES={'root':'th03_mainl.asm','response':'obj/th03/mainl.@l','snow':'src/mainl/staff/snow.asm','staff':'src/mainl/staff/staff.asm','staff_body':'src/mainl/staff/staff.asm','root_body':'src/mainl/root/root.asm','flow':'src/mainl/linked_game/staff_flow.asm','tail':'regtail.asm','snow_prefix':'snowpre.inc','rootpre':'rootpre.asm'}
def compose_all(context=None):
 files,provenance,stages,oldgraph,archive_sha=base.compose_all(context)
 response=files['obj/th03/mainl.@l'];assert response.count(b' cl.lib')==1
 files['obj/th03/mainl.@l']=response.replace(b' cl.lib',b' crt.lib')
 provenance['obj/th03/mainl.@l']='declared source-built CRT substitution; vendor startup/EMU/MATH context'
 for family in FAMILIES:
  proof=json.loads(base.read('config/mainl_'+family+'_backend/proof.json'))
  module=importlib.import_module('lib.mainl_'+family+'_backend')
  args=[];transport={}
  for name in inspect.signature(module.generate).parameters:
   path=proof['cpp_path'] if name=='cpp' else ALIASES[name]
   if family=='regmusic' and name=='staff':path='src/mainl/linked_game/staff_flow.asm'
   raw=base.read(path) if name=='cpp' else files[path]
   variants={'unchanged':raw,'LF':base.lf(raw),'CRLF':base.crlf(raw)}
   matches=[(style,b) for style,b in variants.items() if sha(b)==module.PINS[name]]
   if not matches:raise ValueError(f'{family} {name} {path}: pin mismatch '+sha(raw))
   style,b=matches[0];args.append(b);transport[name]=dict(path=path,line_endings=style,sha256=sha(b))
  payload=module.generate(*args)
  for n,b in payload.items():files[n]=b;provenance[n]='maintained '+family+' composer'
  stages.append(dict(name='maintained '+family,outputs=sorted(payload),source_inputs=transport))
 return files,provenance,stages,oldgraph,archive_sha

_compose_chain=compose_all
def compose_all(context=None):
 files,provenance,stages,oldgraph,archive_sha=_compose_chain(context)
 # These two maintained declarations were staged LF in the aligned producer.
 for name in ['src/mainl/display_hardware/cdg_data.asm','src/mainl/display_hardware/vsync_data.asm']:
  files[name]=base.lf(files[name])
 # Newly introduced compiler TUs bring their own explicit forwarding dependencies.
 changed=True
 while changed:
  changed=False
  for name,raw in list(files.items()):
   for dep in re.findall(rb'^\s*#include\s+"((?:src|compat)/[^\"]+)"',raw,re.M):
    dep=dep.decode()
    if dep not in files:
     files[dep]=base.crlf(base.read(dep));provenance[dep]='transitive maintained compatibility dependency';changed=True
 # The final compiler include was installed LF by the maintained producer.
 files['compat/rec98/th03/formats/hfliplut.h']=base.lf(files['compat/rec98/th03/formats/hfliplut.h'])
 previous={r['output']:r for r in oldgraph}
 new={'rootpre':('rootpre.asm','generated root DATA prefix','root_data'),'rootdata':('rootdata.cpp','src/mainl/root/complete_data.cpp','root_complete_data'),'contmenu':('contmenu.cpp','src/mainl/root/continue.cpp','continue'),'regdata':('regdata.cpp','src/mainl/hiscore/regdata.cpp','regdata'),'regpre':('regpre.asm','generated registration DATA prefix','staff_data'),'staffdat':('staffdat.cpp','src/mainl/staff/data.cpp','staff_data'),'regtail':('regtail.asm','generated registration DATA suffix','staff_data')}
 objects=[x.replace('\\','/') for x in re.findall(r'obj\\[^\s,]+\.obj',files['obj/th03/mainl.@l'].decode())]
 assert len(objects)==len(set(objects))==36
 graph=[]
 for ordinal,out in enumerate(objects):
  if out in previous:row=previous[out].copy()
  else:
   wrapper,source,family=new[Path(out).stem];kind='tasm' if wrapper.endswith('.asm') else 'tcc'
   flags=['/m','/mx','/kh32768','/t','/dGAME=3'] if kind=='tasm' else ['-c','-I.','-O','-b-','-3','-Z','-d','-DGAME=3','-ml',"-DBINARY='L'",'-nobj/th03/']
   row=dict(original_object=out,output=out,kind=kind,game=3,binary='L',first_binary='mainl',flags=flags,source=source,wrapper=wrapper,recipe='scripts/lib/mainl_'+family+'_backend.py')
  row['ordinal']=ordinal;assert row['wrapper'] in files;graph.append(row)
 return files,provenance,stages,graph,archive_sha

def prepare(destination,context=None):
 import os,subprocess
 destination=Path(destination)
 if destination.exists():raise ValueError('fresh destination required')
 files,provenance,stages,graph,archive_sha=compose_all(context)
 assert all(Path(n).suffix.lower() not in {'.obj','.exe','.map','.lib','.dll','.com'} for n in files)
 source=destination/'sources';source.mkdir(parents=True)
 rows={}
 for n,b in sorted(files.items()):
  p=source/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);os.utime(p,ns=(base.STAMP,base.STAMP));rows[n]=dict(sha256=sha(b),bytes=len(b),mtime_ns=base.STAMP,provenance=provenance[n])
 phases=[dict(name='compile_%02d_%s'%(r['ordinal'],Path(r['output']).stem),**r) for r in graph]+[dict(name='link',kind='tlink',flags=['@obj/th03/mainl.@l'],output='bin/th03/mainl.exe')]
 groups=[dict(group=i//5+1,phases=phases[i:i+5],native_seconds=90,cleanup_seconds=15,work_budget_seconds=900,factory_timeout_seconds=1000) for i in range(0,len(phases),5)]
 tracked=subprocess.check_output(['git','ls-files','src/mainl','src/shared','compat','config/mainl_cold_context','config/mainl_*_backend/proof.json','config/th03_mainl*','config/th03_shared*','scripts/lib/mainl*','scripts/stage_th03_mainl*']).decode().splitlines()
 bindings={n:dict(sha256=sha(base.read(n)),bytes=len(base.read(n))) for n in tracked if Path(n).is_file()}
 digest=sha(json.dumps({n:r['sha256'] for n,r in rows.items()},sort_keys=True,separators=(',',':')).encode())
 report=dict(schema='mainl-fullcold-source-proposal-v2',reference_revision=base.REV,archive_sha256=archive_sha,source_mtime_ns=base.STAMP,source_inventory=rows,source_snapshot_sha256=digest,maintained_inputs=bindings,stages=stages,object_graph=graph,groups=groups,project_objects=36,retained_project_objects=0,native_phases_per_round=37,rounds=2,native_execution_performed=False,exact_acceptance=False,historical_cold_proof_applies_to_current_sources=False,full_cold_build_pending=True,context=['Frozen reference source headers/macros/declarations remain explicit context.','Generated flake.asp is a documented source asset, not regenerated from BMP.','Response retains vendor C0L/EMU/MATH and demands newly source-built private crt.lib. The separate bounded CRT adapter must supply this before project linking; no binary providers are included here.'],verification=['Every project object, EXE and MAP must be absent before each fresh build.','Both rounds must use identical source bytes and fixed timestamps.','Compile all36 project objects in each round; no retained objects.','Compare all36 project objects, EXE and MAP raw between rounds.','Apply current39 linked gates and full decoded target equality read-only; do not infer packed acceptance.'])
 (destination/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(destination=str(destination),project_objects=36,sources=len(rows),groups=len(groups),snapshot=digest,manifest=sha((destination/'manifest.json').read_bytes()))))
 return report

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',required=True,type=Path)
 parser.add_argument('--context-directory',type=Path)
 args=parser.parse_args()
 if args.output.is_absolute() or '..' in args.output.parts or args.output.parts[0]!='.analysis':raise ValueError('dedicated ignored source destination required')
 prepare(args.output,args.context_directory)
