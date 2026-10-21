"""Opt-in hybrid driver source stage: fourteen maintained procedures, retained remainder.

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
RESIDENT='src/zun/driver_resident.inl'
RESIDENT_PROCS=(('sub_10C', 'sprite16_entry', 268, 412),
 ('sub_19C', 'sprite16_allocate_buffers', 412, 471),
 ('sub_1D7', 'sprite16_set_interrupt_argument', 471, 478),
 ('sub_1DE', 'sprite16_mask_test_command', 478, 513),
 ('sub_201', 'sprite16_draw_command', 513, 554),
 ('sub_22A', 'sprite16_interrupt_dispatch', 554, 579),
 ('sub_243', 'sprite16_install', 579, 685),
 ('sub_2AD', 'sprite16_uninstall', 685, 832))
RESIDENT_SYMBOLS={'word_F40': 'sprite16_int40_signature_found',
 'word_F43': 'sprite16_resident_paragraphs',
 'word_F38': 'sprite16_previous_vector_segment',
 'word_F3A': 'sprite16_previous_vector_offset',
 'word_F3C': 'sprite16_mask_buffer_segment',
 'word_F3E': 'sprite16_solid_buffer_segment',
 'byte_F42': 'sprite16_interrupt_number',
 'word_F45': 'sprite16_dispatch_target',
 'word_1070': 'sprite16_argument_count',
 'off_103E': 'sprite16_service_table',
 'aGbgvgkpkpmvOFs': 'sprite16_resize_failed_message',
 'aGbgvgkvkslvsvV': 'sprite16_memory_failed_message',
 'aPatuvVVVBbInt0': 'sprite16_installed_message',
 'aVVVPatuvVVvvVB': 'sprite16_already_installed_message',
 'aKLlcIci': 'sprite16_environment_free_failed_message',
 'aGGxgngfbGCIci': 'sprite16_mask_free_failed_message',
 'aGxgGfbGCIci': 'sprite16_solid_free_failed_message',
 'aGrbGhcIci': 'sprite16_code_free_failed_message',
 'aI': 'sprite16_removed_message',
 'aPatuvVVvvVV': 'sprite16_not_installed_message',
 'loc_137': 'entry_no_int40_signature',
 'loc_13D': 'entry_resize_block',
 'loc_161': 'entry_parse_command_tail',
 'loc_186': 'entry_no_arguments',
 'loc_191': 'entry_optional_int40',
 'locret_19B': 'entry_return',
 'loc_1B0': 'allocate_solid_buffer',
 'loc_1CD': 'allocate_buffers_done',
 'loc_2A6': 'install_already_present',
 'locret_2AC': 'install_return',
 'loc_2FC': 'uninstall_free_mask',
 'loc_30F': 'uninstall_free_solid',
 'loc_322': 'uninstall_free_code',
 'loc_331': 'uninstall_removed',
 'loc_339': 'uninstall_not_present',
 'locret_33F': 'uninstall_return'}
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
 for old,new in [(a,b) for a,b,_,_ in RESIDENT_PROCS]+list(RESIDENT_SYMBOLS.items()):
  text=re.sub(r'\b'+old+r'\b',new,text,flags=re.I)
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
def compose_resident(reference,resident):
 """Consume all eight complete procedures, preserving unowned gaps and data."""
 spans=[];expected=[]
 for old,name,start,end in RESIDENT_PROCS:
  found=list(re.finditer(r'(?im)^'+old+r'\s+proc (?:near|far)\b.*?^'+old+r'\s+endp\b[^\n]*',reference,flags=re.S))
  need(len(found)==1,'unique resident procedure '+old)
  match=found[0];spans.append(match.span())
  expected+=['public '+name]+tokens(rename_symbols(match.group()))
 need(tokens(resident)==expected,'resident procedure instruction/ABI contract differs')
 need(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])),'resident order/overlap')
 for a,b in zip(spans,spans[1:]):need(not tokens(reference[a[1]:b[0]]),'unowned code/data between resident procedures')
 first,last=spans[0][0],spans[-1][1]
 return reference[:first]+'include src\\zun\\driver_resident.inl'+reference[last:]
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
 resident=read(root/RESIDENT);need(b'\r' not in resident,'maintained resident source must be UTF8 LF')
 text=compose_resident(reference.decode('shift_jis'),resident.decode('utf-8'))
 text=compose(text,own.decode('utf-8'))
 for old,new in (('libs/master.lib/macros.inc','retained\\master.inc'),('th01/hardware/egc.inc','retained\\egc.inc')):
  need(text.count('include '+old)==1,'retained include statement differs')
  text=text.replace('include '+old,'include '+new)
 files={'driver.asm':dos_text(text),SERVICES:dos_text(own.decode('utf-8')),
        RESIDENT:dos_text(resident.decode('utf-8')),
        'link.rsp':b'-c -s -t -3 driver.obj,driver.com,driver.map,\r\n'}
 inputs={REFERENCE:sha(reference),SERVICES:sha(own),RESIDENT:sha(resident)}
 for source,expected,dest in INCLUDES:
  raw=read(root/source);need(sha(raw)==expected,'retained include identity')
  need(not re.search(rb'(?im)^\s*include\b',raw),'unexpected transitive retained include')
  files[dest]=dos_text(raw.decode('utf-8'));inputs[source]=sha(raw)
 output.mkdir()  # Never reuse any previous stage, even an empty one.
 for name,raw in files.items():
  path=output/name;path.parent.mkdir(parents=True,exist_ok=True)
  with path.open('xb') as f:f.write(raw)
 for name,expected in inputs.items():need(sha(read(root/name))==expected,'input changed during stage')
 result=dict(kind='zun-driver-resident-services-hybrid-stage',inputs=inputs,
             outputs={n:sha(v) for n,v in files.items()},maintained_procedures=14,maintained_instruction_bytes=600,
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
