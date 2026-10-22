#!/usr/bin/env python3
"""Additive source-only raster overlay. Previous stagers and original context stay unchanged."""
from pathlib import Path
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];CONFIG='config/th03_op_raster_candidate.json'
CONFIG_SHA='844409c2adfa5a03e9bf30cea5b4d154c057a2d0893241ba4cbb3d4eab819479'
EXPECTED=[('nopoly_B_put','src/op/music/nopoly_blit.inl','th03/op_music.cpp','th03/op_music.cpp',0xcf6,30,'void near nopoly_B_put(void)'),('box_column16_unput','src/op/menu/column_restore.inl','th03/op_main.cpp','th03/op/m_main.cpp',0x180a,94,'void pascal near box_column16_unput(uscreen_x_t left)')]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 p=Path(p);need(not any(q.is_symlink() for q in (p,*p.parents)) and p.is_file(),'regular input required '+str(p));return p.read_bytes()
def validate_config(c):
 need(c['schema']=='th03-op-raster-source-v1' and c['code_bytes']==124 and c['physical_translation_units']==2 and len(c['units'])==2,'two complete124-byte raster functions')
 need(c['source_acceptance'] is False and c['exact_acceptance'] is False and c['original_runner_complete'] is False and c['separate_offline_audit_pass'] is True,'historical outcome/credit scope')
 for u,e in zip(c['units'],EXPECTED):
  need(tuple(u[k] for k in ('name','source','wrapper','carrier','offset','size','signature'))==e,'real original function/TU/extent')
  need(u['segment']=='decoded:0990' and u['compare_size']==u['size'] and u['owned_relocation_words']==0,'decoded scope, no canonical offsets')
  need(u['physical_game_macro']==3 and u['compiler']=='tcc' and u['language']=='cpp','original GAME3 C++ producer')
  need(u['original_command']=="bin\\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='O' -nobj/th03/ "+u['wrapper'],'original compiler command')
 need(c['retained_context_objects']==25 and c['preserved_prior_owner_count']==42 and c['preserved_prior_code_bytes']==12816,'context/source scope')
 need(c['excluded_vendor_alignment']==dict(program_offset=0xdd95,target=0x90,candidate=0,authored_credit=0),'vendor alignment excluded')
def read_inputs(root):
 root=Path(root);raw=regular(root/CONFIG);need(sha(raw)==CONFIG_SHA,'candidate config changed');c=json.loads(raw);validate_config(c);sources={}
 for u in c['units']:
  b=regular(root/u['source']);need(sha(b)==u['source_sha256'],'maintained source changed');text=re.sub(rb'//[^\n]*',b'',b)
  need(text.count(b'asm {')==1 and u['signature'].encode() in text,'complete genuine ASM function')
  need(not re.search(rb'__emit__|\b(?:db|dw|org|align|even|naked|ret)\b',text,re.I),'no emission/padding/fake return');need(not re.search(rb'\b(?:push|pop)\s+bp\b|mov\s+bp\s*,',text,re.I),'compiler owns real frame')
  sources[u['source']]=b
 return c,sources
def replace_function(original,u):
 need(sha(original)==u['original_carrier_sha256'],'original full source carrier drift')
 signature=u['signature'].encode();need(original.count(signature)==1,'unique original function')
 start=original.index(signature);at=original.index(b'{',start);end=at+1;depth=1
 while depth:
  need(end<len(original),'unterminated original function');depth+=(original[end]==123)-(original[end]==125);end+=1
 need(sha(original[start:end])==u['original_function_sha256'],'original complete function drift')
 replacement=('#include "'+u['source']+'"').encode();changed=original[:start]+replacement+original[end:]
 need(sha(changed)==u['overlay_sha256'],'exact source-only function replacement');return changed

def payload(root,reference):
 c,result=read_inputs(root)
 for u in c['units']:result[u['carrier']]=replace_function(regular(Path(reference)/u['carrier']),u)
 return result

def compose(inputs,root):
 c,sources=read_inputs(root);result=dict(inputs)
 for u in c['units']:
  need(u['source'] not in inputs,'fresh maintained owner destination');result[u['carrier']]=replace_function(inputs[u['carrier']],u)
 result.update(sources);return result

def stage(root,output,reference):
 data=payload(root,reference);output=Path(output);need(not any(p.is_symlink() for p in (output,*output.parents)) and not output.exists(),'fresh source-only output')
 output.mkdir(parents=True)
 for n,b in data.items():p=output/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 report=dict(schema='th03-op-raster-overlay-v1',files={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())},code_bytes=124,physical_translation_units=2,compiler_invocations=0,original_runner_complete=False,source_acceptance=False,exact_acceptance=False)
 (output/'source_inventory.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(stage(a.root,a.output,a.reference),indent=2))
