#!/usr/bin/env python3
"""Source-only PFOPEN overlay in the unchanged physical th03_op.asm TU."""
from pathlib import Path
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
CONFIG='config/th03_op_pfopen_source_candidate.json'
CONFIG_SHA='b943545e69d4ab78000b9cce0ccb4440cd67d68a9940b43b207013441ca24064'
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 p=Path(p);need(not any(q.is_symlink() for q in (p,*p.parents)) and p.is_file(),'regular source '+str(p));return p.read_bytes()
def instructions(b):return [x.strip().lower() for x in re.sub(rb';[^\r\n]*',b'',b).splitlines() if x.strip()]
def validate_config(c):
 need(c['schema']=='th03-op-pfopen-source-v1' and c['name']=='PFOPEN','scope')
 need((c['segment'],c['offset'],c['size'],c['compare_size'],c['code_bytes'])==('decoded:0000',0x2ef2,281,281,281),'decoded whole PFOPEN extent')
 need(c['canonical_extent'] is None and not any(c[n] for n in ['source_acceptance','exact_acceptance','whole_root_credit']),'credit boundary')
 need((c['physical_producer'],c['physical_object'],c['overlay_destination'])==('th03_op.asm','obj/th03/op.obj','th03/formats/pfopen.asm'),'original mixed physical producer')
 need(len(c['physical_context'])==142 and len(c['compatibility_closure'])==12,'complete genuine context/headers')
 need(len({q['path'] for q in c['physical_context']})==142 and len({q['stage_destination'] for q in c['compatibility_closure']})==12,'unique context inventory')
 need((c['preserved_prior_owners'],c['preserved_prior_bytes'],c['total_scoped_bytes'],c['project_objects'],c['retained_context_objects'])==(44,12940,13221,28,27),'verified scope and graph')
 need(c['abi']==dict(model='use16 large _TEXT',return_type='far',argument_bytes=8,file_bp_offset=6,parfile_bp_offset=10,preserved=['SI','DI']),'real ABI')
def read_inputs(root):
 root=Path(root);raw=regular(root/CONFIG);need(sha(raw)==CONFIG_SHA,'candidate config drift');c=json.loads(raw);validate_config(c)
 source=regular(root/c['source']);need(sha(source)==c['source_sha256'],'maintained source drift');result={c['overlay_destination']:source}
 for q in c['compatibility_closure']:
  b=regular(root/q['path']);need(sha(b)==q['sha256'] and len(b)==q['bytes'],'genuine macro closure drift');result[q['stage_destination']]=b
 return c,result

def compose(inputs,root):
 c,overlay=read_inputs(root)
 for q in c['physical_context']:
  need(q['path'] in inputs and sha(inputs[q['path']])==q['sha256'] and len(inputs[q['path']])==q['bytes'],'physical context drift '+q['path'])
 q=c['original_source'];need(q['path'] in inputs and sha(inputs[q['path']])==q['sha256'],'original PFOPEN drift')
 need(instructions(inputs[q['path']])==instructions(overlay[c['overlay_destination']]),'only semantic comments may change original code')
 for q in c['compatibility_closure']:need(inputs[q['stage_destination']]==overlay[q['stage_destination']],'header context changed')
 result=dict(inputs);result.update(overlay);return result

def payload(root,reference):
 c,_=read_inputs(root);names=[q['path'] for q in c['physical_context']]+[c['original_source']['path']]
 return compose({n:regular(Path(reference)/n) for n in names},root)
def stage(root,output,reference):
 data=payload(root,reference);output=Path(output);need(not any(p.is_symlink() for p in (output,*output.parents)) and not output.exists(),'fresh source-only output');output.mkdir(parents=True)
 for n,b in data.items():p=output/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 report=dict(schema='th03-op-pfopen-source-overlay-v1',files={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())},new_source_scope_bytes=281,physical_producer='th03_op.asm',compiler_invocations=0,source_acceptance=False,exact_acceptance=False,whole_root_credit=False)
 (output/'source_inventory.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(stage(a.root,a.output,a.reference),indent=2))
