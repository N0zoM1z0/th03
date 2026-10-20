"""Source-only proposal. No subprocess/native execution, no historical writes."""
from pathlib import Path
import hashlib,json,re,sys
sys.dont_write_bytecode=True
ROOT=Path.cwd(); HERE=Path(__file__).resolve().parent
from review_th03_cpu_link_order import rows,mz,omf,module_runs
B=ROOT/'.analysis/th03-main-exact/gpt-dots-player-tail-default-cold-v01/round1/source'
CPU=ROOT/'.analysis/gpt-dots-player-cpu-source-v03/probe-v01/compile-first-v01/source/obj/th03/p_cpu.obj'
PINS={'th03_main.asm':'759aea527019dff7355cd831cc33176d60eb62d35ef0a8ce3dbd55f210c8bfa8','obj/th03/main.obj':'debc7907810f8128047039e5f8e072d7dd50705fc46dbbd3122dc2998dfc93d7','obj/th03/main.map':'2a3e3ad4a2289cdb9a9e7f30d7d676f42613dcb92e76fd901d312b9291e5224b','obj/th03/main.@l':'5eb21ee316fc68a7ae0ac083ef9cceb1a20f3a0055a0a4db6c6de3bf427e9c87','bin/th03/main.exe':'94f8fd8801290242f623c7059f92657310f9e16160f92a598931b89cc1b33f93'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def once(b,a,c):
 need(b.count(a)==1,'nonunique anchor '+repr(a));return b.replace(a,c)
def transform(raw):
 need(sha(raw)==PINS['th03_main.asm'],'root pin')
 a=raw.index(b'sub_C370\tproc near'); end=b'\t\tdw offset loc_C653\r\n'; b=raw.index(end,a)+len(end)
 removed=raw[a:b]
 need(re.findall(rb'^(sub_[A-F0-9]+)\tproc near',removed,re.M)==[b'sub_C370',b'sub_C433',b'sub_C54A',b'sub_C568'],'four complete CPU functions')
 out=raw[:a]+b'; Complete CPU interval supplied by maintained CPU producer.\r\nextern @PLAYER_CPU_UPDATE$QP14PLAYER_STUFF_T:near\r\n'+raw[b:]
 out=once(out,b'call\tsub_C54A',b'call\t@PLAYER_CPU_UPDATE$QP14PLAYER_STUFF_T')
 out=once(out,b'word_20E4A\tdw ?',b'public _cpu_dodge_pattern\r\n_cpu_dodge_pattern label word\r\nword_20E4A\tdw ?')
 lines=out.splitlines(keepends=True);idx=lines.index(b'public _yumemi_bomb_triangle_angles\r\n')
 need(all(re.fullmatch(rb'\s*db\s+[0-9A-Fa-f]+h?\r\n',l) for l in lines[idx-270:idx]),'270 literal existing DATA directives')
 lines.insert(idx-54,b'public _cpu_retry_directions\r\n_cpu_retry_directions label word\r\n');lines.insert(idx-270,b'public _cpu_dodge_patterns\r\n_cpu_dodge_patterns label word\r\n');out=b''.join(lines)
 for sym in [b'_pid',b'ELLEN_TARGET_SET',b'PLAYER_BOMB',b'_ellen_target_x',b'_ellen_target_y']:
  need(len(re.findall(rb'^public[^\r\n]*\b'+re.escape(sym)+rb'\b',out,re.M))+len(re.findall(rb'^\tpublic[^\r\n]*\b'+re.escape(sym)+rb'\b',out,re.M))==1,'one existing export '+repr(sym))
 prefix=raw[raw.index(b'sub_C0D8\tproc near'):a];need(prefix in out,'genuine prefix preserved verbatim')
 need(not re.search(rb'\b(?:sub_C370|sub_C433|sub_C54A|sub_C568|off_C536|off_C791)\b',out),'deleted CPU symbols remain')
 return out

def expectation():
 for n,h in PINS.items():need(sha((B/n).read_bytes())==h,'baseline '+n)
 need(sha(CPU.read_bytes())=='26bcae741b3d4579cd10e14209e46f6de10e214e15f474f5e182d2c59fa1a7d6','CPU native object')
 rs=rows(B/'obj/th03/main.map');rel=mz(B/'bin/th03/main.exe',rs);runs=module_runs(rel)
 root=[r for r in runs if r['module']=='th03_main.asm'];need(root==[dict(module='th03_main.asm',start=472,count=423)],'root run')
 cpu=[r for r in rel if 0xc370<=r['site']<0xc7a5];need([r['index'] for r in cpu]==[848,849] and [r['site'] for r in cpu]==[0xc452,0xc5bb],'old CPU sites')
 cpurows=[dict(module='th03/p_cpu.cpp',segment='PLAYER_M_TEXT',start=0xc370)]
 mod,blocks=omf(CPU,cpurows);fs=[f for b in blocks for f in b['fixups']];need(len(fs)==64,'CPU fixups')
 sites=[f['mz_site'] for f in fs if 'mz_site' in f];need(sites==[0xc5bb,0xc452],'native CPU order')
 old=[r['pair'] for r in rel];residual=[r['pair'] for r in rel[472:895] if not 0xc370<=r['site']<0xc7a5];need(len(residual)==421,'residual root421')
 predicted=old[:472]+residual+[[0x96e,s-0x96e0] for s in sites]+old[895:]
 outside=[r['pair'] for r in rel if not 0xc370<=r['site']<0xc7a5]
 need(predicted[:893]+predicted[895:]==outside and len(predicted)==1553,'outside1551 exact literal preservation')
 return dict(kind='pre-native-source-and-untouched-OMF-derived-expectation',native_invoked=False,exact_acceptance=False,baseline_pins=PINS,cpu_object_sha256=sha(CPU.read_bytes()),root_old_run=root[0],root_new_run={'start':472,'count':421},cpu_new_indices=[893,894],cpu_sites=sites,complete_literal_pairs=predicted,outside_literal_pairs=outside,expected_stream_sha256=sha(json.dumps(predicted,separators=(',',':')).encode()),cpu_64_fixups=fs,limitations=['fresh root LEDATA/FIXUPP reframing is unknown and must fail closed before linking','retained object compile is not maintained-path cold acceptance'])
