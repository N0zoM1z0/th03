#!/usr/bin/env python3
"""Source-only historical alignment overlay after the exact-order OP graph."""
from pathlib import Path
import argparse,hashlib,json,types
CONFIG='config/th03_op_nopcall_candidate.json'
CONFIG_SHA='5d965a28543f24f1e214fd7a40d1c237de59e26b2f9e4e32bb94c5d3d5ff1a1f'
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p);need(p.is_file() and not any(x.is_symlink() for x in (p,*p.parents)),'regular source');return p.read_bytes()
def inventory(data):return {n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())}
def config(root):
 b=read(Path(root)/CONFIG);need(sha(b)==CONFIG_SHA,'config identity');c=json.loads(b);need(c['source_acceptance'] is False and c['exact_acceptance'] is False and c['new_authored_code_credit']==0 and c['context_only'],'scope');return c
def load(root,q):
 p=Path(root)/q['path'];b=read(p);need(sha(b)==q['sha256'],'module identity');m=types.ModuleType('op_alignment_'+p.stem);m.__file__=str(p);exec(compile(b,str(p),'exec'),m.__dict__);return m
def compose(inputs,root):
 c=config(root);need(inventory(inputs)==c['input_inventory'],'exact330 aligned prerequisite graph');h=load(root,c['helper']);result=dict(inputs);result.update(h.compose(inputs['ReC98.inc']));need(inventory(result)==c['output_inventory'],'exact native-observed genuine FAR-call producer graph');return result
def payload(root):
 c=config(root);return compose(load(root,c['upstream_stage']).payload(root),root)
def stage(root,output):
 data=payload(root);output=Path(output);need(not output.exists() and not any(p.is_symlink() for p in (output,*output.parents)),'fresh source destination');output.mkdir(parents=True)
 for n,b in data.items():p=output/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 return dict(source_files=len(data),native_invocations=0,source_acceptance=False,exact_acceptance=False,new_authored_code_credit=0,cold_build=False)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(stage(a.root,a.output),indent=2))
