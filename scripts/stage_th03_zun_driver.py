"""Stage the maintained TH03 ZUNSP driver without reference or target inputs.

This opt-in route assembles semantic procedure modules plus explicit layout/data.
It does not execute tools, reuse objects, normalize bytes or grant exact credit.
"""
from pathlib import Path
import argparse,hashlib,json,re,stat
ROOT=Path(__file__).resolve().parents[1]
LAYOUT='src/zun/driver.asm'
DATA='src/zun/driver_data.inl'
HARDWARE='src/zun/driver_hardware.inc'
MODULES=tuple('src/zun/driver_'+n+'.inl' for n in
 ('resident','services','graphics','format','command','numbers','strings'))
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def plain(path):
 path=Path(path)
 for p in (path,*path.parents):need(not p.is_symlink(),'symlink path')
 return path
def read(path):
 path=plain(path);a=path.stat();need(stat.S_ISREG(a.st_mode),'regular source required')
 raw=path.read_bytes();b=path.stat()
 need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_mode)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_mode),'source changed')
 return raw
def source(raw):
 need(b'\r' not in raw and raw.endswith(b'\n'),'maintained UTF-8 LF source required')
 return raw.decode('utf-8',errors='strict')
def dos_text(text):return text.replace('\n','\r\n').encode('shift_jis',errors='strict')
def bodies(text):
 """Select complete authored procedures only; never synthesize instructions."""
 found={};rest=text
 pattern=r'(?im)^([a-z_][a-z0-9_]*)\s+proc\s+(?:near|far)\b.*?^\1\s+endp\b[^\n]*'
 for m in re.finditer(pattern,text,re.S):
  name=m[1];need(name.startswith('sprite16_') and name not in found,'unique named procedure')
  found[name]='public '+name+'\n'+m[0]+'\n'
  rest=rest.replace(m[0],'',1)
 public=[]
 for line in rest.splitlines():
  line=line.split(';',1)[0].strip()
  if line:
   m=re.fullmatch(r'public (sprite16_[a-z0-9_]+)',line)
   need(m is not None,'unexpected source outside procedure');public.append(m[1])
 need(sorted(public)==sorted(found),'one public per complete procedure')
 return found
def prepare(inputs):
 text={n:source(raw) for n,raw in inputs.items()}
 functions={}
 for n in MODULES:
  selected=bodies(text[n]);need(not functions.keys()&selected.keys(),'duplicate procedure across modules')
  functions.update(selected)
 need(len(functions)==55,'all fifty-five procedures required')
 includes=re.findall(r'(?im)^include\s+([^\s;]+)\s*$',text[LAYOUT])
 expected={DATA,HARDWARE}|{'procs/'+n+'.inc' for n in functions}
 actual=[n.replace('\\','/') for n in includes]
 need(len(actual)==len(expected) and set(actual)==expected,'complete one-time layout include membership')
 for n in (DATA,HARDWARE,*MODULES):
  need(not re.search(r'(?im)^\s*(include|incbin|org)\b',text[n]),'unexpected transitive include or origin')
 need('_reference' not in '\n'.join(text.values()) and 'incbin' not in text[LAYOUT].lower(),'no retained source or raw blob')
 files={'driver.asm':dos_text(text[LAYOUT]),DATA:dos_text(text[DATA]),HARDWARE:dos_text(text[HARDWARE]),
        'link.rsp':b'-c -s -t -3 driver.obj,driver.com,driver.map,\r\n'}
 files.update({'procs/'+n+'.inc':dos_text(body) for n,body in functions.items()})
 return files
def stage(output,root=ROOT):
 root=Path(root);output=Path(output).absolute();plain(output.parent);need(output.parent.is_dir(),'stage parent missing')
 inputs={n:read(root/n) for n in (LAYOUT,DATA,HARDWARE,*MODULES)}
 files=prepare(inputs)
 output.mkdir() # Exclusive fresh output, never reuse even an empty directory.
 for name,raw in files.items():
  p=output/name;p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('xb') as f:f.write(raw)
 for name,raw in inputs.items():need(read(root/name)==raw,'input changed during stage')
 result=dict(kind='zun-driver-maintained-stage',inputs={n:sha(v) for n,v in inputs.items()},
  outputs={n:sha(v) for n,v in files.items()},maintained_procedures=55,
  maintained_instruction_bytes=2844,maintained_nonprocedure_bytes=1380,
  all_driver_procedures_owned=True,complete_driver_source_owned=True,
  retained_source_inputs=[],native_invocations=0,exact_acceptance=False,
  expected_target_differing_bytes=10)
 with (output/'stage.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 return result
def native_commands(wine,msdos):
 """Recipe only; parent-owned bounded supervisor executes these two commands."""
 return ([str(wine),r'C:\TASM50\BIN\TASM32.EXE','/m','/mx','/kh32768','/t','/dTHIEF','driver.asm,driver.obj'],
         [str(wine),str(msdos),'-e','-x','tlink','@link.rsp'])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
 print(json.dumps(stage(ap.parse_args().output),indent=2))
if __name__=='__main__':main()
