"""Source-only snow function split. No native tools, OMF or EXE modifications."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2]
PINS={
 'root':'40e3ab37730ddb5302c79c020742769f828f2ef4bb7a4ae33550f65b26ee74e4',
 'response':'c42a98ee7f2dc05ac8b3a8c76bfa82c6ef62d886673cb6b1ccc18e63f92af514',
 'snow':'faa5f056630d6d05753ae10668494a467071c821fd33db46f19b91e949904d0e',
 'cpp':'307d81e9b8c855548bd4f7a192316e4cc0d5d943077c3cd5bf07e9fae703e9d8'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(raw,old,new):
 need(raw.count(old)==1,'nonunique source anchor '+repr(old));return raw.replace(old,new)
def generate(root,snow,cpp,response):
 for k,b in [('root',root),('snow',snow),('cpp',cpp),('response',response)]:need(sha(b)==PINS[k],'pinned source drift '+k)
 r=root.replace(b'\r\n',b'\n');s=snow.replace(b'\r\n',b'\n')
 a=s.index(b'; Spawn:');proc=s.index(b'sub_BB80\tproc near\n',a);end=s.index(b'sub_BB80\tendp',proc)+len(b'sub_BB80\tendp')
 need(s[a:proc].count(b'\n')==1,'spawn header boundary');prefix=s[:a];tail=s[end:]
 need(prefix.count(b' proc near')+prefix.count(b'\tproc near')==1,'one reset procedure')
 tail=once(tail,b'call\tsub_BB80',b'call\t_mainl_snow_spawn')
 need(b'sub_BB80' not in prefix+tail,'old spawn symbol survives')
 old=b"MAINL_SNOW_TEXT segment byte public 'CODE' use16\ninclude src/mainl/staff/snow.asm\nMAINL_SNOW_TEXT ends"
 new=b"""MAINL_SNOW_TEXT segment byte public 'CODE' use16
include snowpre.inc
MAINL_SNOW_TEXT ends
MAINL_SPAWN_TEXT segment byte public 'CODE' use16
 extern _mainl_snow_spawn:near
MAINL_SPAWN_TEXT ends
MAINL_SNOW_TAIL_TEXT segment byte public 'CODE' use16
include snowpost.inc
MAINL_SNOW_TAIL_TEXT ends"""
 r=once(r,old,new)
 r=once(r,b'MAINL_SNOW_TEXT, MAINL_DISSOLVE_TEXT',b'MAINL_SNOW_TEXT, MAINL_SPAWN_TEXT, MAINL_SNOW_TAIL_TEXT, MAINL_DISSOLVE_TEXT')
 r=once(r,b'byte_106B0\tdb ?',b'public _mainl_snow_slot_limit\n_mainl_snow_slot_limit label byte\nbyte_106B0\tdb ?')
 r=once(r,b'word_10BB2\tdw ?',b'public _mainl_snow_frame\n_mainl_snow_frame label word\nword_10BB2\tdw ?')
 rsp=once(response,b'obj\\th03\\mainl.obj ',b'obj\\th03\\mainl.obj obj\\th03\\snow_cpp.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(r),'snowpre.inc':crlf(prefix),'snowpost.inc':crlf(tail),'snow_cpp.cpp':cpp,'obj/th03/mainl.@l':rsp}
def compose(work,manifest):
 """Fresh source worktree only. Existing aligned root/response are pinned.
 manifest optional snow_source/cpp_source are repository-relative frozen inputs.
 No automatic input copying and no build tools are invoked.
 """
 work=Path(work).resolve()
 baseline=(ROOT/'.analysis/toolchain/wineprefix/drive_c/MVA04').resolve()
 need(work!=baseline and not work.is_relative_to(baseline),'must not modify retained baseline')
 snow_path=ROOT/manifest.get('snow_source','src/mainl/staff/snow.asm')
 cpp_path=ROOT/manifest.get('cpp_source','src/mainl/staff/snow_spawn.cpp')
 out=generate((work/'th03_mainl.asm').read_bytes(),snow_path.read_bytes(),cpp_path.read_bytes(),(work/'obj/th03/mainl.@l').read_bytes())
 for name in ('snowpre.inc','snowpost.inc','snow_cpp.cpp'):need(not (work/name).exists(),'fresh generated output required '+name)
 for name,b in out.items():p=work/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 return dict(kind='source-only-snow-spawn-composition',outputs={n:sha(b) for n,b in out.items()},split_code_lengths=[26,169,248],source_inputs=PINS,native_invoked=False,objects_modified=False,exact_acceptance=False)
