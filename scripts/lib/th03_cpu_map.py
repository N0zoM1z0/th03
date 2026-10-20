"""Literal MAP expectation derived before native from baseline/source/CPU OMF.
No output fitting, symbol normalization, public tie sorting or waiver.
"""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
BASE=Path.cwd()/'.analysis/th03-main-exact/gpt-dots-player-tail-default-cold-v01/round1/source/obj/th03/main.map'
BASE_SHA='2a3e3ad4a2289cdb9a9e7f30d7d676f42613dcb92e76fd901d312b9291e5224b'
PUBLICS=[(0x96e,0x2c90,'idle','player_cpu_direction_for_collisi(int,int,int)'),(0x96e,0x2d53,'idle','player_cpu_approach_target(player_stuff_t near*)'),(0x96e,0x2e6a,'','player_cpu_update(player_stuff_t near*)'),(0x96e,0x2e88,'idle','player_cpu_dodge_and_aim(player_stuff_t near*)'),(0x1d56,0x67e,'','_cpu_dodge_patterns'),(0x1d56,0x756,'','_cpu_retry_directions'),(0x1d56,0x38ea,'','_cpu_dodge_pattern')]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise ValueError(s)
def once(t,a,b):need(t.count(a)==1,'nonunique literal MAP anchor '+repr(a));return t.replace(a,b)
def pline(p):
 s,o,status,name=p
 return f' {s:04X}:{o:04X} '+('idle  ' if status=='idle' else '      ')+name+'\r\n'
def derive():
 raw=BASE.read_bytes();need(sha(raw)==BASE_SHA,'baseline full MAP pin');text=raw.decode('ascii')
 # P_CPU_TEXT is first encountered after root MAIN_11_TEXT declarations and
 # before warning. Unlike the old CPU-before-root aggregate it is ungrouped.
 line=next(x for x in text.splitlines(keepends=True) if 'H WARNING_TEXT ' in x)
 text=once(text,line,line.replace('WARNING_TEXT','P_CPU_TEXT  ')+line)
 # Root prefix shrinks in place, CPU takes the exact contiguous slot.
 root=next(x for x in text.splitlines(keepends=True) if 'S=PLAYER_M_TEXT' in x and 'M=th03_main.asm ' in x)
 need(root.startswith(' 096E:29F8 06CD '),'root geometry')
 warning=next(x for x in text.splitlines(keepends=True) if 'S=PLAYER_M_TEXT' in x and 'M=src/main/player/warning.cpp ' in x)
 cpu=warning.replace('096E:30C5 0618','096E:2C90 0435').replace('src/main/player/warning.cpp','th03/p_cpu.cpp')
 need(cpu!=warning and cpu.startswith(' 096E:2C90 0435 '),'CPU geometry')
 text=once(text,root,root.replace('29F8 06CD','29F8 0298')+cpu)
 for segment,addr in [('_DATA','1D56:0BEC'),('_BSS','1D56:68DC')]:
  line=next(x for x in text.splitlines(keepends=True) if 'S='+segment+' ' in x and 'M=src/main/player/warning.cpp ' in x)
  need(line.startswith(' '+addr+' 0000 '),'zero '+segment)
  text=once(text,line,line.replace('src/main/player/warning.cpp','th03/p_cpu.cpp')+line)
 line=next(x for x in text.splitlines(keepends=True) if 'S=WARNING_TEXT ' in x and 'M=src/main/player/warning.cpp ' in x)
 need(line.startswith(' 1C90:000A 0000 ') and 'G=(none)' in line,'zero CODE placement')
 text=once(text,line,line.replace('WARNING_TEXT','P_CPU_TEXT  ').replace('src/main/player/warning.cpp','th03/p_cpu.cpp')+line)
 head,names=text.split('  Address         Publics by Name\r\n');names,values=names.split('  Address         Publics by Value\r\n')
 # Freeze actual Borland decorated-name ordering, not a generic sort of the
 # demangled names. Independent historical CPU OMF/MAP already establishes the
 # four display names/statuses and their contiguous name order.
 byname=[PUBLICS[1],PUBLICS[0],PUBLICS[3],PUBLICS[2]]
 anchor=' 096E:3800       player_effects_render()\r\n'
 names=once(names,anchor,''.join(map(pline,byname))+anchor)
 anchor=' 1D56:658A       _cpu_hit_damage_additional\r\n'
 names=once(names,anchor,pline(PUBLICS[6])+pline(PUBLICS[4])+anchor+pline(PUBLICS[5]))
 # Preserve ALL old value records and existing tie order literally. Insert only
 # new distinct-address rows into their unique strict address gaps.
 lines=values.splitlines(keepends=True)
 pattern=re.compile(r'^ ([0-9A-F]{4}):([0-9A-F]{4}) (.{6})([^\r\n]+)\r\n$')
 for pub in PUBLICS:
  s,o,_,_=pub;matches=[(i,pattern.fullmatch(line)) for i,line in enumerate(lines)];matches=[(i,m) for i,m in matches if m and m[3].strip()!='Abs']
  need(not any((int(m[1],16),int(m[2],16))==(s,o) for i,m in matches),'new public address has no old tie')
  nexts=[i for i,m in matches if int(m[1],16)==s and int(m[2],16)>o];need(nexts,'strict insertion upper bound')
  i=nexts[0];earlier=[m for j,m in matches if j<i and int(m[1],16)==s];need(earlier and int(earlier[-1][2],16)<o,'strict insertion lower bound')
  lines.insert(i,pline(pub))
 values=''.join(lines)
 old=' 096E:49A0 idle  PLAYER_BOMB\r\n';new=' 096E:49A0       PLAYER_BOMB\r\n'
 names=once(names,old,new);values=once(values,old,new)
 return (head+'  Address         Publics by Name\r\n'+names+'  Address         Publics by Value\r\n'+values).encode('ascii')
def check_frozen_expectation():
 saved=json.loads((HERE/'th03_cpu_map_expectation.json').read_text());expected=derive()
 need(saved['baseline_sha256']==BASE_SHA and saved['expected_sha256']==sha(expected) and saved['expected_text'].encode('ascii')==expected,'source-derived complete MAP freeze')
 return expected

def check_map(path):
 expected=check_frozen_expectation();actual=Path(path).read_bytes()
 need(actual==expected,'complete literal MAP differs (zero rows/public identity/status/ties/summary all strict; no normalization)')
 return {'pass_full_map':True,'literal_bytes_equal':True,'sha256':sha(actual),'existing_ties_preserved':True,'existing_status_delta':['PLAYER_BOMB idle -> active'],'new_publics':len(PUBLICS)}
