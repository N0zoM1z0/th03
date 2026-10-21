"""Opt-in hybrid driver source stage: six maintained setters, retained remainder.

This is NOT a maintained whole-driver build or default integration. Reference
scaffold and two includes stay explicitly pinned diagnostic inputs. No target
bytes, object reuse, compiler execution, padding synthesis or acceptance changes.
"""
from pathlib import Path
import argparse,hashlib,json,re,stat
ROOT=Path(__file__).resolve().parents[1]
REFERENCE='_reference/ReC98/libs/sprite16/sprite16.asm'
REFERENCE_SHA='d0b5366a317911fcd45b6d8e9abb80331ed999a73110cd8090fac98a26b0739d'
SERVICES='src/zun/driver_services.inl'
SETTERS=(
 ('sub_340','sprite16_set_mono_enabled','word_1064','sprite16_mono_enabled'),
 ('sub_346','sprite16_set_mono_color','word_1066','sprite16_mono_color'),
 ('sub_34C','sprite16_set_overlap','word_1068','sprite16_overlap'),
 ('sub_352','sprite16_set_access_plane','word_106E','sprite16_access_plane'),
 ('sub_358','sprite16_set_rop','word_106A','sprite16_rop'),
 ('sub_35E','sprite16_set_mask','word_106C','sprite16_mask'),
)
INCLUDES=(
 ('_reference/ReC98/libs/master.lib/macros.inc','6e38bd2a6af911890250376d7e3d87343a6e726eced227958669d6f420427ae9','retained/master.inc'),
 ('_reference/ReC98/th01/hardware/egc.inc','29e30717870bb69635bf082114ccb4a0e9795803c80adbd1283449f80e32a188','retained/egc.inc'),
)
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def tokens(text):
 return [re.sub(r'\s+',' ',line.split(';',1)[0].strip()).lower() for line in text.splitlines() if line.split(';',1)[0].strip()]
def validate_services(text):
 expected=[]
 for _,name,_,field in SETTERS:expected += ['public '+name,name+' proc near','mov cs:'+field+', dx','retn',name+' endp']
 need(tokens(text)==expected,'six complete setter bodies/ABI differ')
def rename_symbols(text):
 for old,new,field,name in SETTERS:
  text=re.sub(r'\b'+old+r'\b',new,text,flags=re.I)
  text=re.sub(r'\b'+field+r'\b',name,text,flags=re.I)
 return text
def compose(reference,services):
 """Replace only six complete procedures; rename their true references/state."""
 validate_services(services)
 spans=[]
 for old,name,field,state in SETTERS:
  pattern=r'(?im)^'+old+r'\s+proc near\b.*?^'+old+r'\s+endp\b[^\n]*'
  found=list(re.finditer(pattern,reference,flags=re.S))
  need(len(found)==1,'unique retained procedure '+old)
  match=found[0]
  need(tokens(match.group())==[old.lower()+' proc near','mov cs:'+field.lower()+', dx','retn',old.lower()+' endp'],'retained setter body differs')
  spans.append(match.span())
 need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'setter order/overlap')
 for a,b in zip(spans,spans[1:]):need(not tokens(reference[a[1]:b[0]]),'unowned code/data between setters')
 first,last=spans[0][0],spans[-1][1]
 composed=reference[:first]+'include src\\zun\\driver_services.inl'+reference[last:]
 return rename_symbols(composed)
def dos_text(text):
 text=text.replace('\r\n','\n')
 need('\r' not in text and text.endswith('\n'),'strict LF text with final newline required')
 return text.replace('\n','\r\n').encode('shift_jis',errors='strict')
def plain(path):
 path=Path(path)
 for p in (path,*path.parents):need(not p.is_symlink(),'symlink path')
 return path
def read(path):
 path=plain(path);a=path.stat();need(stat.S_ISREG(a.st_mode),'regular source required')
 raw=path.read_bytes();b=path.stat()
 need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_mode)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_mode),'source changed')
 return raw
def stage(output,root=ROOT):
 root=Path(root);output=Path(output).absolute();plain(output.parent);need(output.parent.is_dir(),'stage parent missing')
 reference=read(root/REFERENCE);need(sha(reference)==REFERENCE_SHA,'frozen retained driver identity')
 own=read(root/SERVICES);need(b'\r' not in own,'maintained source must be UTF8 LF')
 text=compose(reference.decode('shift_jis'),own.decode('utf-8'))
 for old,new in (('libs/master.lib/macros.inc','retained\\master.inc'),('th01/hardware/egc.inc','retained\\egc.inc')):
  need(text.count('include '+old)==1,'retained include statement differs')
  text=text.replace('include '+old,'include '+new)
 files={'driver.asm':dos_text(text),SERVICES:dos_text(own.decode('utf-8')),
        'link.rsp':b'-c -s -t -3 driver.obj,driver.com,driver.map,\r\n'}
 inputs={REFERENCE:sha(reference),SERVICES:sha(own)}
 for source,expected,dest in INCLUDES:
  raw=read(root/source);need(sha(raw)==expected,'retained include identity')
  need(not re.search(rb'(?im)^\s*include\b',raw),'unexpected transitive retained include')
  files[dest]=dos_text(raw.decode('utf-8'));inputs[source]=sha(raw)
 output.mkdir()  # Never reuse any previous stage, even an empty one.
 for name,raw in files.items():
  path=output/name;path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('xb') as f:f.write(raw)
 for name,expected in inputs.items():need(sha(read(root/name))==expected,'input changed during stage')
 result=dict(kind='zun-driver-six-setter-hybrid-stage',inputs=inputs,
             outputs={n:sha(v) for n,v in files.items()},maintained_procedures=6,
             complete_driver_source_owned=False,native_invocations=0,exact_acceptance=False)
 with (output/'stage.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 return result
def native_commands(wine,msdos):
 """Recipe only. A parent-owned bounded supervisor must execute these."""
 return ([str(wine),r'C:\TASM50\BIN\TASM32.EXE','/m','/mx','/kh32768','/t','/dTHIEF','driver.asm,driver.obj'],
         [str(wine),str(msdos),'-e','-x','tlink','@link.rsp'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 print(json.dumps(stage(args.output),indent=2))
if __name__=='__main__':main()
