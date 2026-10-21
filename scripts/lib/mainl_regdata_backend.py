"""Pure semantic DATA ownership split; no binary input or output transformations."""
import hashlib,re
PINS={'root': 'ac000a0e7a171a45b4990eba995fabee4076e531dcf951b1b12e907d45647248', 'response': '6ac5a74963b50e6cc256d258862608eb198b4f1547baeceec331265c64802b05', 'cpp': 'e22195338f005967bd60a0c8e8cda263a47279de44bbbbf26a8bea83151131b7'}
NAMES=['none','reimu','mima','marisa','ellen','kotohime','kana','rikako','chiyuri','yumemi']
STRINGS=['aNoEntry','aB@b@sCB@b@','aB@b@cgcvb@b@','aB@cvcanB@','aB@gggmgub@','aB@pmuexpb@','aB@Gjgi','aB@canboq','aB@vVfvsb@','aB@CF']
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def once(raw,old,new):
 need(raw.count(old)==1,'nonunique source anchor '+repr(old));return raw.replace(old,new)
def generate(root,response,cpp):
 for n,b in [('root',root),('response',response),('cpp',cpp)]:need(sha(b)==PINS[n],'source drift '+n)
 r=root.replace(b'\r\n',b'\n')
 a=r.index(b'public _REGIST_PLAYCHARS\n');t=r.index(b'public _REGI_PLAYCHAR\n',a);end=r.index(b'\t.data?\n',t)
 table=r[a:t];tail=r[t:end]
 targets=re.findall(rb'^\s*dd\s+(\S+)',table,re.M)
 need(targets==[x.encode() for x in STRINGS],'logical table source order changed')
 # All actual tail data labels become public at their existing positions.
 labels=[]
 for line in tail.splitlines():
  m=re.match(rb'^([A-Za-z_@][A-Za-z_0-9@]*)\s+(?:label\s+(byte|word|dword)|(db|dw|dd))\b',line,re.I)
  if m:
   kind=(m[2] or {b'db':b'byte',b'dw':b'word',b'dd':b'dword'}[m[3].lower()]).lower()
   labels.append((m[1],kind))
 # Two tail-owned include definitions are explicit, not inferred binary labels.
 labels += [(b'_sFLAKE',b'byte'),(b'CDG_DISSOLVE_PATTERN',b'word')]
 need(len({n for n,k in labels})==len(labels),'duplicate tail label')
 existing_public={b'_sFLAKE'} # Already public in retained flake.asp include
 for line in tail.splitlines():
  if line.lower().startswith(b'public '):existing_public.update(x.strip() for x in line[7:].split(b','))
 exports=b''.join(b'public '+n+b'\n' for n,k in labels if n not in existing_public)
 imports=b'extern _REGIST_PLAYCHARS:dword\n'+b''.join(b'extern '+n+b':'+k+b'\n' for n,k in labels)
 for semantic,original in zip(NAMES,STRINGS):
  name=original.encode();pattern=re.compile(rb'^'+re.escape(name)+rb'(?=\s+db\b)',re.M)
  need(len(pattern.findall(tail))==1,'string source anchor '+original)
  alias=b'_mainl_name_'+semantic.encode()
  tail=pattern.sub(b'public '+alias+b'\n'+alias+b' label byte\n'+name,tail)
 header_start=r.index(b'\t\t.386\n');header_end=r.index(b'include th03/formats/scoredat.inc\n')+len(b'include th03/formats/scoredat.inc\n')
 tail_source=b'; Maintained-source DATA tail; symbolic string and pointer ownership preserved.\n'+r[header_start:header_end]+b'\n\t.data\n'+exports+tail+b'\n\tend\n'
 # Only the root owns ReC98.inc's BINARY-guarded absolute _address_0 singleton.
 tail_source=once(tail_source,b"BINARY = 'E'\n",b'')
 root_out=r[:a]+b'; Registration array and following DATA are owned by separate source producers.\n'+imports+r[end:]
 response=once(response,br'obj\th03\regmusic.obj ',br'obj\th03\regdata.obj obj\th03\regtail.obj ')
 crlf=lambda b:b.replace(b'\n',b'\r\n')
 return {'th03_mainl.asm':crlf(root_out),'regdata.cpp':cpp,'regtail.asm':crlf(tail_source),'obj/th03/mainl.@l':response}
