#!/usr/bin/env python3
"""Source-only exact-order composition: real selection/root boundaries and zero-byte layout declarations."""
from pathlib import Path
import argparse,hashlib,json,re,types
ROOT=Path(__file__).resolve().parents[1]
CONFIG='config/th03_op_global_order_candidate.json'
CONFIG_SHA='8756b623aeceda7990e7af4d18a13afcb516c283e8e2a9e15c325024b05329dd'
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def regular(p):
 p=Path(p);need(not any(q.is_symlink() for q in (p,*p.parents)) and p.is_file(),'regular source required');return p.read_bytes()
def inventory(data):return {n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())}
def config(root):
 raw=regular(Path(root)/CONFIG);need(sha(raw)==CONFIG_SHA,'composition config identity');c=json.loads(raw);need(c['schema']=='th03-op-global-order-source-v1' and c['source_acceptance'] is False and c['exact_acceptance'] is False and c['new_authored_code_credit']==0,'scope');return c
def compose(inputs,root):
 c=config(root);need(inventory(inputs)==c['input_inventory'],'exact prerequisite source graph, including PFOPEN');audit=c['root_dependencies'];source=inputs['th03_op.asm'].decode().replace('\r\n','\n')
 cut=source.index('include libs/master.lib/pfint21.asm');end=source.index('_TEXT\tends',cut);opening=source[:source.index('include libs/master.lib/bfnt_entry_pat.asm')]
 # Exactly the original function/include boundary. All original data/BSS stay in prefix.
 private=['SOUND_I','SOUND_O','parfilename','pfint21_pf','pfint21_handle','pfint21_entries','trapezoid_hmask']
 need(set(x.lower() for x in private)==set(audit['private_cross_symbols']),'private dependency set')
 definitions={}
 for n in audit['prefix_includes']+audit['storage_includes']:
  for line in inputs[n].decode().replace('\r\n','\n').splitlines():
   line=line.split(';')[0];m=re.match(r'\s*(?:func\s+([\w]+)|([\w]+)\s+(proc\s+(?:near|far)|db|dw|dd|label\s+\w+))',line,re.I)
   if m:definitions[(m[1] or m[2]).lower()]=(m[1] or m[2],'far' if m[1] else m[3].lower().replace('proc ','').replace('label ',''),n)
 code=[];data=[];bss=[]
 for token in audit['cross_symbols']:
  name,kind,n=definitions[token];typ={'db':'byte','dw':'word','dd':'dword'}.get(kind,kind)
  declaration=f'\textrn {name}:{typ}\n'
  (code if kind in ('far','near') else bss if '[bss]' in n else data).append(declaration)
 prefix=source[:cut].replace('include libs/master.lib/bfnt_entry_pat.asm','\tpublic '+','.join(private)+'\n\textrn draw_trapezoid:near\n\ninclude libs/master.lib/bfnt_entry_pat.asm')+source[end:]
 suffix=opening+'; Preserve assembler state inherited before the original include boundary.\nIFDEF ??version\n\tJUMPS\n\tWARN\nENDIF\n'+''.join(code)+'\n'+source[cut:end]+"_TEXT\tends\n\n\t.data\n"+''.join(data)+"\n\t.data?\n"+''.join(bss)+"\n\tend\n"
 pf=inputs['libs/master.lib/pfint21.asm'].decode().replace('\r\n','\n');changes=[]
 for name,kind,n in definitions.values():
  if kind!='far':continue
  pattern=re.compile(r'^(\s*)call(\s+)('+re.escape(name)+r')(\s*(?:;[^\n]*)?)$',re.M|re.I)
  def subst(m):changes.append(dict(file='libs/master.lib/pfint21.asm',symbol=m[3],before=m[0].strip(),after=('_call'+m[2]+m[3]+m[4]).strip()));return m[1]+'_call'+m[2]+m[3]+m[4]
  pf=pattern.sub(subst,pf)
 need(len(changes)==11,'exact eleven lexical cross-FAR call sites (eight active GAME3, three inactive GAME5)')
 # The existing master.lib _call macro preserves FAR return ABI via push CS + near call.
 need('push\tCS\n\tcall\tnear ptr place' in inputs['libs/master.lib/func.inc'].decode().replace('\r\n','\n'),'existing same-segment FAR-call macro')
 result=dict(inputs);result.update({'th03_op.asm':prefix.encode(),'th03_optail.asm':suffix.encode(),'libs/master.lib/pfint21.asm':pf.encode()})
 anchor=regular(Path(root)/c['anchor_source']);need(sha(anchor)==c['anchor_sha256'],'anchor source identity');result['oplayout.asm']=anchor
 # Split the maintained whole-function source; no function text is synthesized.
 selection=inputs['src/op/menu/character_selection.inl'];split=selection.index(b'// Coincidentally, these were the only characters available in the trial');helper,tail=selection[:split],selection[split:];need(helper+tail==selection,'whole selection source preservation');result['probe/select155_helper.inl']=helper;result['probe/select155_tail.inl']=tail
 original=inputs['th03/op/m_select.cpp'].decode().replace('\r\n','\n');header=original[:original.index('/// Constants')];prefix_cpp='#pragma option -zCOP_SEL_TEXT\n'
 result['th03/selhelp.cpp']=(prefix_cpp+header+'\n#include "src/op/formats/score_load.inl"\n#include "probe/select155_helper.inl"\n').encode()
 state=original[:original.index('#include "src/op/formats/score_load.inl"')]
 result['th03/seltail.cpp']=(prefix_cpp+state+'// Same genuine near function, now supplied by the helper TU.\nunsigned char near playchars_available_load(void);\n#include "probe/select155_tail.inl"\n').encode()
 order=c['object_order'];need(len(order)==30 and len(set(order))==30,'thirty real project objects');need(order.index('obj\\th03\\op.obj')+1==order.index('obj\\th02\\exit_dos.obj') and order.index('obj\\th02\\exit_dos.obj')+1==order.index('obj\\th03\\optail.obj'),'root/exit/root chronology')
 result['obj/th03/op.@l']=('-c -s -E c0l.obj '+' '.join(order)+', bin\\th03\\op.exe, obj\\th03\\op.map, emu.lib mathl.lib cl.lib\n').encode()
 need(inventory(result)==c['output_inventory'],'native-observed exact source graph');return result

def load(root,name,digest):
 p=Path(root)/name;b=regular(p);need(sha(b)==digest,'source stager identity');m=types.ModuleType(Path(name).stem);m.__file__=str(p);exec(compile(b,str(p),'exec'),m.__dict__);return m
def payload(root):
 c=config(root);names=list(c['chain_scripts']);stages=[load(root,n,c['chain_scripts'][n]) for n in names];data=stages[0].payload(root)
 for m in stages[1:3]:data.update(m.payload(root))
 data=stages[3].compose(data,root);p=c['pfopen_stage'];data=load(root,p['path'],p['sha256']).compose(data,root);return compose(data,root)
def stage(root,output):
 data=payload(root);output=Path(output);need(not any(p.is_symlink() for p in (output,*output.parents)) and not output.exists(),'fresh source destination');output.mkdir(parents=True)
 for n,b in data.items():p=output/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 return dict(source_files=len(data),native_invocations=0,source_acceptance=False,exact_acceptance=False,whole_product_ownership=False)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(stage(a.root,a.output),indent=2))
