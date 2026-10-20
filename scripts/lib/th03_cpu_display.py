"""Observed finite display supplement; no rerun, sorting, normalization or waiver."""
from pathlib import Path
import hashlib,json,re,sys,tomllib
sys.dont_write_bytecode=True
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
from lib import th03_cpu_gates as g, th03_cpu_map as map_gate
RECEIPT_SHA='063d73974b1d0ce5ae73e36911653668a9f19b41085784a0cc6723fe23f9e1c2'
ACTUAL_MAP_SHA='32f532c22b20e3e415d66c1cc4e3c4183088b9091a5ba1494a5ee45193e6163c'
# Explicit observed order, independently certified below as genuine PUBDEF aliases.
# This is not a TLINK sorting algorithm and permits no other permutation.
GROUPS=[
 ('0000:08D2','root',['FONTFILE_CLOSE','DOS_CLOSE']),
 ('0000:08E8','root',['FONTFILE_OPEN','DOS_ROPEN']),
 ('0000:21AA','root',['VSYNC_END','VSYNC_LEAVE']),
 ('0000:321C','h_ldiv',['LUDIV@','F_LUDIV@']),
 ('0000:322C','h_ldiv',['F_LUMOD@','LUMOD@']),
 ('0000:3313','h_padd',['F_PSUB@','PSUB@']),
 ('1D56:007C','c0',['__version','__osversion','__osmajor']),
 ('1D56:0278','root',['_BFNT_ID','BFNT_ID']),
 ('1D56:0596','root',['TextVramAdr','_TextVramAdr']),
 ('1D56:0598','root',['_TextVramSeg','TextVramSeg']),
 ('1D56:059A','root',['_TextVramWidth','TextVramWidth']),
 ('1D56:059E','root',['_vsync_Proc','vsync_Proc']),
 ('1D56:05A2','root',['vsync_Delay','_vsync_Delay']),
 ('1D56:05B0','root',['_mem_MyOwn','mem_MyOwn']),
 ('1D56:11F8','root',['_mem_FirstHole','mem_FirstHole']),
 ('1D56:11FA','root',['_mem_EndMark','mem_EndMark']),
]
LIB_MEMBERS={
 'h_ldiv':(16688,502,'5f132ad90467c19310928c1a21d690c61293c79bc71f60defeffd321f503b80c','880a0000a306685f6c64697666'),
 'h_padd':(18240,320,'455570ca658bcc489a21d86ba9e642ad1d1566e8198abfb55f4608d7a45a6749','880a0000a306685f7061646468'),
}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pinned(path,digest):
 raw=Path(path).read_bytes();need(sha(raw)==digest,'pin drift '+str(path));return raw

def frames(raw, legacy_comment=None):
 result=[];pos=0
 while pos<len(raw):
  need(pos+3<=len(raw),'record header bounds');kind=raw[pos];size=int.from_bytes(raw[pos+1:pos+3],'little');end=pos+3+size
  need(size>=1 and end<=len(raw),'record framing bounds');framed=raw[pos:end]
  if sum(framed)%256:
   # The archived library has exactly this non-symbol COMENT at offset15.
   # Its invalid checksum is disclosed, never fixed or accepted generically.
   need(legacy_comment is not None and pos==15 and framed.hex()==legacy_comment and kind==0x88,'unexpected record checksum')
  result.append((kind,pos,framed[3:-1],framed));pos=end
 need(result[0][0]==0x80 and result[-1][0] in (0x8a,0x8b),'module bounds')
 return result

def pubdefs(raw,legacy_comment=None):
 names=[''];segments=[];pub=[];records=frames(raw,legacy_comment);module=records[0][2][1:].decode('ascii')
 for kind,pos,d,framed in records:
  if kind==0x96:
   i=0
   while i<len(d):n=d[i];i+=1;need(i+n<=len(d),'LNAME bounds');names.append(d[i:i+n].decode('ascii'));i+=n
  elif kind==0x98:
   need(d[0]>>5!=0,'absolute SEGDEF unsupported');n,i=g.index(d,3);c,i=g.index(d,i);o,i=g.index(d,i);need(i==len(d),'SEGDEF trailing');segments.append((names[n],int.from_bytes(d[1:3],'little'),d[0],names[c]))
  elif kind==0x90:
   group,i=g.index(d,0);segment,i=g.index(d,i)
   if segment==0:i+=2
   while i<len(d):
    n=d[i];i+=1;name=d[i:i+n].decode('ascii');i+=n;offset=int.from_bytes(d[i:i+2],'little');i+=2;typ,i=g.index(d,i)
    pub.append({'name':name,'group':group,'segment':segments[segment-1][0] if segment else 'ABS','segment_index':segment,'offset':offset,'type':typ,'record_offset':pos,'raw_record_hex':framed.hex()})
 return {'module':module,'pubdefs':pub,'segments':segments,'module_sha256':sha(raw),'legacy_comment_checksum_exception':legacy_comment}

def providers(work):
 root=pinned(g.B/'obj/th03/main.obj',g.PINS['obj/th03/main.obj'])
 config=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
 library=ROOT/next(s['path'] for s in config['surfaces'] if s['id']=='tc40j-lib')
 c0=pinned(library/'C0L.OBJ','09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2')
 lib=pinned(library/'CL.LIB','7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7')
 out={'root':pubdefs(root),'c0':pubdefs(c0)};out['root']['map_module']='th03_main.asm';out['c0']['map_module']='c0.ASM'
 # Validate exact genuine page-aligned module boundaries, not a rewritten OMF.
 page=int.from_bytes(lib[1:3],'little')+3;need(lib[0]==0xf0 and page==16,'library header');cursor=page;members={}
 while cursor<len(lib) and lib[cursor]==0x80:
  start=cursor
  while True:
   need(cursor+3<=len(lib),'library record header');kind=lib[cursor];size=int.from_bytes(lib[cursor+1:cursor+3],'little');cursor+=3+size;need(size>=1 and cursor<=len(lib),'library record bounds')
   if kind in (0x8a,0x8b):break
  members[start]=cursor-start;cursor=((cursor+page-1)//page)*page
 need(cursor<len(lib) and lib[cursor]==0xf1,'library member terminator')
 for name,(offset,size,digest,comment) in LIB_MEMBERS.items():
  need(members.get(offset)==size,'genuine member boundary');raw=lib[offset:offset+size];need(sha(raw)==digest,'member identity')
  out[name]=pubdefs(raw,comment);need(out[name]['module']==name+'.asm','exact THEADR provider');out[name]['map_module']=name;out[name]['library_offset']=offset
 return out

def derive(work):
 base=map_gate.check_frozen_expectation();marker=b'  Address         Publics by Value\r\n';need(base.count(marker)==1,'by-value marker')
 prefix,body=base.split(marker);lines=body.splitlines(keepends=True);proof=[];ps=providers(work);rows=g.rows(g.B/'obj/th03/main.map')
 for address,provider,order in GROUPS:
  matches=[i for i,line in enumerate(lines) if line.startswith((' '+address+' ').encode())]
  need(len(matches)==len(order) and matches==list(range(matches[0],matches[0]+len(matches))),'exact contiguous alias slot '+address)
  before=[lines[i] for i in matches];byname={line.decode().strip().split()[-1]:line for line in before}
  need(len(byname)==len(order) and set(byname)==set(order),'alias membership '+address)
  chosen=[p for p in ps[provider]['pubdefs'] if p['name'] in order]
  need(len(chosen)==len(order) and {p['name'] for p in chosen}==set(order),'unique provider PUBDEF membership')
  identity={(p['group'],p['segment'],p['segment_index'],p['offset'],p['type']) for p in chosen};need(len(identity)==1,'genuine same-location aliases')
  group,segment,segment_index,offset,typ=next(iter(identity));need(typ==0,'PUBDEF type')
  all_aliases=[p['name'] for p in ps[provider]['pubdefs'] if (p['group'],p['segment_index'],p['offset'],p['type'])==(group,segment_index,offset,typ)]
  need(len(all_aliases)==len(order) and set(all_aliases)==set(order),'complete OMF alias class')
  owner=[r for r in rows if r['module']==ps[provider]['map_module'] and r['segment']==segment];need(len(owner)==1,'unique MAP provider contribution')
  seg,off=(int(v,16) for v in address.split(':'));need(owner[0]['start']+offset==seg*16+off,'provider PUBDEF resolved address')
  after=[byname[name] for name in order];need(before!=after,'observed changed display order')
  lines[matches[0]:matches[-1]+1]=after
  proof.append({'address':address,'provider':provider,'map_module':ps[provider]['map_module'],'module_sha256':ps[provider]['module_sha256'],'library_offset':ps[provider].get('library_offset'),'provider_row':owner[0],'pubdefs':chosen,'before':[x.decode() for x in before],'observed_after':[x.decode() for x in after],'legacy_comment_checksum_exception':ps[provider]['legacy_comment_checksum_exception']})
 need(len(proof)==16 and sum(len(p['before']) for p in proof)==33,'finite sixteen/33 contract')
 return prefix+marker+b''.join(lines),proof

def check_map(raw,work):
 expected,proof=derive(work);need(raw==expected,'finite literal MAP supplement mismatch; no generic ties permitted')
 return {'pass_map_supplement':True,'changed_groups':16,'changed_rows':33,'all_other_literal_map_bytes_preserved':True,'map_sha256':sha(raw),'observed_display_metadata_only':True}
