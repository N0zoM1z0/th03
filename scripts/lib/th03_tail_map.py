"""Separate retained MAP diagnostic. No original receipt or acceptance mutation."""
from pathlib import Path
import re,hashlib
from lib.omf import parse_omf
from lib.th03_score_candidate import map_rows,public_sections
from lib.th03_yumemi_bomb_candidate import publics
BASE_MAP_SHA='8eaec19618c90df6d5fe084b645039c70ac0f418e8e925ebce77278c14769921'
ORDER=('warning','effects','chain1','chain2')
SPECS={'warning':('obj/th03/warning.obj','src/main/player/warning.cpp',1560,0x30c5),'effects':('obj/th03/effects.obj','src/main/player/effects.cpp',628,0x36dd),'chain1':('obj/chain1.obj','src/main/background/chain1.cpp',695,0x3951),'chain2':('obj/chain2.obj','src/main/background/chain2.cpp',550,0x3c08)}
TIES={(0,0x08d2):('FONTFILE_CLOSE','DOS_CLOSE'),(0,0x3224):('F_LMOD@','LMOD@'),(0,0x3313):('F_PSUB@','PSUB@'),(0x139d,0x2fb3):('sub_16983','ELLEN_TARGET_SET'),(0x1d56,0x007c):('__osversion','__version','__osmajor'),(0x1d56,0x0278):('_BFNT_ID','BFNT_ID'),(0x1d56,0x030a):('_SdiExists','SdiExists'),(0x1d56,0x0312):('_random_seed','random_seed'),(0x1d56,0x0596):('TextVramAdr','_TextVramAdr'),(0x1d56,0x0598):('_TextVramSeg','TextVramSeg'),(0x1d56,0x05ae):('mem_TopSeg','_mem_TopSeg'),(0x1d56,0x05b4):('mem_Reserve','_mem_Reserve'),(0x1d56,0x11f4):('mem_OutSeg','_mem_OutSeg'),(0x1d56,0x11f6):('mem_TopHeap','_mem_TopHeap')}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def idx(b,i):
 n=b[i];i+=1
 if n&128:n=((n&127)<<8)|b[i];i+=1
 return n,i
def segdefs(path):
 rs=parse_omf(Path(path).read_bytes());ns=[''];out=[]
 for r in rs:
  d=r.data
  if r.name=='LNAMES':
   i=0
   while i<len(d):n=d[i];i+=1;ns.append(d[i:i+n].decode());i+=n
  elif r.name=='SEGDEF':
   n,i=idx(d,3);c,i=idx(d,i);ov,i=idx(d,i);out.append((ns[n],ns[c],int.from_bytes(d[1:3],'little'),d[0]))
 return out

def aggregates(text):
 return [(int(a,16),int(z,16),int(n,16),s,c) for a,z,n,s,c in re.findall(r'^ ([0-9A-F]+)H ([0-9A-F]+)H ([0-9A-F]+)H (\S+)\s+(\S+)\s*$',text,re.M)]

def derive_zero_and_contribution_model(baseline,work):
 """No candidate MAP read. Four SEGDEFs plus old map and exact response insertion."""
 baseline,work=Path(baseline),Path(work);raw=(baseline/'obj/th03/main.map').read_bytes();need(sha(raw)==BASE_MAP_SHA,'baseline MAP pin');text=raw.decode('latin1');rows=map_rows(text);agg=aggregates(text)
 oldrsp=(baseline/'obj/th03/main.@l').read_bytes();rsp=(work/'obj/th03/main.@l').read_bytes();anchor=b'obj\\th03\\main.obj obj\\th03\\score_hud.obj';insert=b'obj\\th03\\main.obj obj\\th03\\warning.obj obj\\th03\\effects.obj obj\\chain1.obj obj\\chain2.obj obj\\th03\\score_hud.obj';need(oldrsp.count(anchor)==1 and rsp==oldrsp.replace(anchor,insert),'exact response four insertion')
 definitions={n:segdefs(work/SPECS[n][0]) for n in ORDER}
 for n,ds in definitions.items():need(ds==[(n.upper()+'_TEXT','CODE',0,0x28),('_DATA','DATA',0,0x48),('_BSS','BSS',0,0x48),('PLAYER_M_TEXT','CODE',SPECS[n][2],0x28)],'four exact producer SEGDEF '+n)
 root='th03_main.asm';score='src/main/hud/score.asm'
 # Baseline root declared every live code segment before producers. The next
 # first-seen ungrouped CODE segment is EX_SHFLY_TEXT after the inserted objects.
 code_anchor=next(r for r in rows if r[4]=='EX_SHFLY_TEXT');need(code_anchor[2]==0,'code zero anchor')
 code_end=next(a+length for a,z,length,s,c in agg if s=='MAIN_11_TEXT');need(code_end==code_anchor[0]*16+code_anchor[1],'old final declared code cursor')
 zeros={};expected=[]
 for cls,seg in [('DATA','_DATA'),('BSS','_BSS')]:
  rr=[r for r in rows if r[6]==root and r[4]==seg];need(len(rr)==1,'unique root storage row');r=rr[0];end=r[1]+r[2];zeros[seg]=[(r[0],end,0,cls,seg,'DGROUP',SPECS[n][1],48) for n in ORDER]
 zeros['CODE']=[(code_anchor[0],code_anchor[1],0,'CODE',definitions[n][0][0],'(none)',SPECS[n][1],28) for n in ORDER]
 for r in rows:
  if r==code_anchor:expected.extend(zeros['CODE'])
  if r[6]==score and r[4] in ('_DATA','_BSS'):expected.extend(zeros[r[4]])
  if r[6]==root and r[4]=='PLAYER_M_TEXT':
   need(r[:3]==(0x96e,0x29f8,5174),'root prior5174');expected.append((r[0],r[1],1741,*r[3:]));expected.extend((0x96e,SPECS[n][3],SPECS[n][2],'CODE','PLAYER_M_TEXT','MAIN_01',SPECS[n][1],28) for n in ORDER)
  else:expected.append(r)
 ea=[]
 for a in agg:
  if a[3]=='EX_SHFLY_TEXT':ea.extend((code_end,code_end,0,definitions[n][0][0],'CODE') for n in ORDER)
  ea.append(a)
 need(len(expected)==len(rows)+16 and sum(not r[2] for r in expected)==349 and sum(not r[2] for r in rows)==337,'exact detailed row counts')
 return dict(detailed_rows=expected,aggregate_rows=ea,added_zero_rows=[r for key in ('CODE','_DATA','_BSS') for r in zeros[key]],baseline_map_sha256=BASE_MAP_SHA,response_sha256=sha(rsp),producer_hashes={n:sha((work/SPECS[n][0]).read_bytes()) for n in ORDER},derivation='SEGDEF and response-only twelve zero contributions, cursor from accepted baseline',public_ties_rule='explicit observed fourteen transitions; no generic linker algorithm claim',full_map_pass=False)

def validate_aggregate_prefix(baseline_raw,candidate_raw,model):
 """Literal baseline prefix plus four independently derived zero rows only."""
 marker=b'Detailed map of segments'
 need(baseline_raw.count(marker)==candidate_raw.count(marker)==1,'unique detailed MAP boundary')
 old=baseline_raw.split(marker)[0];actual=candidate_raw.split(marker)[0]
 anchor=b' 1C90AH 1C90AH 00000H EX_SHFLY_TEXT      CODE\r\n'
 need(old.count(anchor)==1,'exact baseline aggregate insertion anchor')
 added=[]
 for name in ORDER:
  segment=name.upper()+'_TEXT'
  need(model['aggregate_rows'].count((0x1c90a,0x1c90a,0,segment,'CODE'))==1,'OMF-derived zero aggregate geometry')
  added.append(anchor.replace(b'EX_SHFLY_TEXT     ',segment.encode().ljust(18)))
 need(actual==old.replace(anchor,b''.join(added)+anchor,1),'complete literal aggregate prefix')
 return True

def validate_rows(model,text):
 need(map_rows(text)==[tuple(x) for x in model['detailed_rows']],'complete literal detailed contributions')
 need(aggregates(text)==[tuple(x) for x in model['aggregate_rows']],'complete literal aggregate contributions')
 return True

def display_name(raw):
 if raw.startswith('@') and raw.endswith('$qv'):return raw[1:-3]+'()'
 need(not raw.startswith('@'),'unmodelled new public demangling')
 return raw

def resolved_public(p,rows):
 seg=p['segment'];need(seg is not None,'new public absolute unsupported')
 found=[r for r in rows if r[6]==p['module'].replace('\\','/') and r[4]==seg['name']];need(len(found)==1,'unique public OMF contribution')
 r=found[0];return (r[0],r[1]+p['offset'],display_name(p['name']))

def derive_public_inventory(baseline,work,model):
 baseline,work=Path(baseline),Path(work);oldtext=(baseline/'obj/th03/main.map').read_text('latin1');oldrows=map_rows(oldtext);newrows=[tuple(r) for r in model['detailed_rows']];before=publics(baseline/'obj/th03/main.obj');after=publics(work/'obj/th03/main.obj');bn={p['name']:p for p in before};an={p['name']:p for p in after};need(len(bn)==len(before) and len(an)==len(after),'unique root PUBDEF names')
 removed=[resolved_public(p,oldrows) for p in before if p['name'] not in an];added=[resolved_public(p,newrows) for p in after if p['name'] not in bn];providers=[]
 for n in ORDER:
  for p in publics(work/SPECS[n][0]):
   added.append(resolved_public(p,newrows));providers.append(p)
 # Moved established bomb names are removed from root but supplied once by effects.
 retained=[]
 for x in removed:
  if x in added:added.remove(x);retained.append(x)
 removed=[x for x in removed if x not in retained]
 need(len(added)==36 and len(removed)==3 and len(retained)==3,'exact public inventory delta')
 need({x[2] for x in removed}=={'sub_CDBD','sub_CE0C','sub_CE5B'},'only obsolete root aliases removed')
 root_tie_names={n for address,names in TIES.items() if address not in ((0,0x3224),(0,0x3313),(0x1d56,0x7c)) for n in names}
 bp=[p for p in before if p['name'] in root_tie_names];ap=[p for p in after if p['name'] in root_tie_names]
 keys=('name','module','segment_index','segment','group_index','group','offset','frame','type_index','record_sha256','public_ordinal')
 need(len(bp)==len(root_tie_names)==len(ap),'all22 root tied providers')
 need([{k:p[k] for k in keys} for p in bp]==[{k:p[k] for k in keys} for p in ap],'root tied PUBDEF identity/rawrecord/literal order unchanged')
 for p in bp:
  address=next(a for a,ns in TIES.items() if p['name'] in ns);need(resolved_public(p,oldrows)[:2]==address and resolved_public(an[p['name']],newrows)[:2]==address,'root tied address unchanged')
 return dict(additions=added,removals=removed,moved_established=retained,root_tie_provider_proof=[{k:p[k] for k in keys} for p in bp],new_producer_providers=providers)

def capture_observed_public_positions(baseline_text,candidate_text,inventory):
 """Explicit observed display metadata, authorized supplement; NOT linker derivation."""
 from collections import Counter
 flag_contract=check_idle_transitions(baseline_text,candidate_text)
 old=public_sections(baseline_text);new=public_sections(candidate_text);adds=[tuple(x) for x in inventory['additions']];removes=[tuple(x) for x in inventory['removals']]
 for before,after in zip(old,new):
  need(Counter(after)==Counter([x for x in before if x not in removes]+adds),'complete OMF-derived public name/address/multiplicity')
  need(all(after.count(x)==1 for x in adds),'unique new providers')
 oldnames=[x for x in old[0] if x not in removes];newnames=[x for x in new[0] if x not in adds];need(newnames==oldnames,'all old Names order retained')
 expected=[x for x in old[1] if x not in removes]
 for address,names in TIES.items():
  positions=[i for i,x in enumerate(expected) if x[:2]==address];need([expected[i][2] for i in positions]==list(names),'exact complete old tie group')
  need(positions==list(range(positions[0],positions[0]+len(names))),'contiguous old tie');expected[positions[0]:positions[-1]+1]=[(address[0],address[1],n) for n in reversed(names)]
 need([x for x in new[1] if x not in adds]==expected,'only fourteen exact old Value tie transitions')
 return dict(explicit_idle_flag_transitions=flag_contract,complete_names=new[0],complete_values=new[1],complete_public_display_lines=public_lines(candidate_text),observed_new_entry_positions=[[{'index':i,'entry':x} for i,x in enumerate(section) if x in adds] for section in new],observed_old_tie_transitions=[dict(address=a,before=ns,after=list(reversed(ns))) for a,ns in TIES.items()],provenance='Observed retained v06 display positions, independently constrained OMF-derived inventory. Not generic sorting algorithm. Cold reproduction required.')

def validate_public_vectors(display,text):
 actual=public_sections(text)
 need(public_lines(text)==display['complete_public_display_lines'],'complete literal public display including idle flags')
 need(actual[0]==[tuple(x) for x in display['complete_names']],'complete literal Names vector')
 need(actual[1]==[tuple(x) for x in display['complete_values']],'complete literal Value vector')
 return True

RUNTIME='.analysis/toolchain/wineprefix/drive_c/TC4/LIB'
RUNTIME_PINS={'C0L.OBJ':'09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2','CL.LIB':'7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7'}
RUNTIME_RECORDS=[('C0L.OBJ',0,850,'01060b5f5f6f7376657273696f6e7c0000','__osversion'),('C0L.OBJ',0,1209,'0106095f5f6f736d616a6f727c0000','__osmajor'),('C0L.OBJ',0,1228,'0106095f5f76657273696f6e7c0000','__version'),('CL.LIB',16688,191,'000107465f4c4d4f4440120000','F_LMOD@'),('CL.LIB',16688,208,'0001054c4d4f4440120000','LMOD@'),('CL.LIB',18240,141,'000107465f5053554240320000','F_PSUB@'),('CL.LIB',18240,175,'0001055053554240320000','PSUB@')]
def runtime_provider_proof(repo,baseline_text):
 """Pinned immutable runtime bytes, no repair/normalization of historical COMENT."""
 import json
 historical=Path(repo)/'.analysis/gpt-dots-yumemi-bomb-producer-boundary-review-v01/provider-report.json';hraw=historical.read_bytes();need(sha(hraw)=='7b4a81372a3d0adeb59b7ce41a74ef3a8c8dea751516a2b70162701e8bbacc1a','accepted runtime provider report pin');historical=json.loads(hraw)
 for name,digest in RUNTIME_PINS.items():
  entries=[x for x in historical['runtime_inputs'] if x['logical'].upper()==name];need(len(entries)==1 and entries[0]['byte_identical'] and entries[0]['baseline']['sha256']==entries[0]['candidate']['sha256']==digest,'historical runtime pin bridge')
 root=Path(repo)/RUNTIME
 from lib.toolchain import tree_identity
 hist=historical['historical_runtime_evidence']
 for name in ('config','attestation_log'):
  item=hist[name];need(sha((Path(repo)/item['path']).read_bytes())==item['sha256'],'historical runtime attestation pin '+name)
 tree=tree_identity(root);need(tree.sha256==hist['tree']['sha256'] and tree.file_count==41,'historical41file runtime tree')
 raw={n:(root/n).read_bytes() for n in RUNTIME_PINS}
 for n,h in RUNTIME_PINS.items():need(sha(raw[n])==h,'runtime provider file pin '+n)
 members=[(16688,502,'5f132ad90467c19310928c1a21d690c61293c79bc71f60defeffd321f503b80c'),(18240,320,'455570ca658bcc489a21d86ba9e642ad1d1566e8198abfb55f4608d7a45a6749')]
 for start,n,h in members:need(sha(raw['CL.LIB'][start:start+n])==h,'exact runtime member bytes')
 evidence=[]
 for file,member,off,data,name in RUNTIME_RECORDS:
  b=raw[file];a=member+off;n=int.from_bytes(b[a+1:a+3],'little');record=b[a:a+3+n];need(record[0]==0x90 and record[3:-1]==bytes.fromhex(data) and sum(record)%256==0,'exact genuine runtime PUBDEF '+name)
  evidence.append(dict(file=file,member_offset=member,record_offset=off,name=name,data=data,record_sha256=sha(record),checksum_valid=True))
 rows=map_rows(baseline_text)
 for module,seg,offset,address in [('c0.ASM','_DATA',124,(0x1d56,0x7c)),('h_ldiv','_TEXT',18,(0,0x3224)),('h_padd','_TEXT',50,(0,0x3313))]:
  rr=[r for r in rows if r[6]==module and r[4]==seg];need(len(rr)==1 and (rr[0][0],rr[0][1]+offset)==address,'runtime provider exact MAP binding')
 return dict(input_pins=RUNTIME_PINS,historical_provider_report_sha256=sha(hraw),records_literal_provider_order=evidence,historical_comment_checksum_issue='Pinned h_ldiv/h_padd COMENT checksums are historically nonzero. Bytes preserved; exact file/member pins and each PUBDEF checksum validated without normalization.',provenance_commands=['c9d5783036614e8da6c46d717a2edaf9','a85820b44a5c4d54a4b22df103596eeb'])


def public_lines(text):
 before,values=text.split('Publics by Value');names=before.split('Publics by Name')[1]
 return [[line.rstrip('\r') for line in section.splitlines() if re.match(r'^\s*[0-9A-F]{4}:[0-9A-F]{4}\s+',line)] for section in (names,values)]


IDLE_TRANSITIONS={(0,0x0536,'PALETTE_BLACK_OUT'),(0,0x2086,'TEXT_PUTSA')}
def flags_by_section(text):
 out=[]
 for lines in public_lines(text):
  values=[]
  for line in lines:
   match=re.fullmatch(r'\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:(idle)\s+)?(\S[^\r\n]*?)\s*',line);need(match is not None,'strict public flag grammar')
   s,o,idle,name=match.groups();values.append(((int(s,16),int(o,16),name),bool(idle)))
  need(len(dict(values))==len(values),'unique flag identities');out.append(dict(values))
 return out

def check_idle_transitions(baseline_text,candidate_text):
 old=flags_by_section(baseline_text);new=flags_by_section(candidate_text);proof=[]
 for section,(before,after) in enumerate(zip(old,new)):
  changed={key for key in before.keys()&after.keys() if before[key]!=after[key]}
  need(changed==IDLE_TRANSITIONS,'exact two retained idle-to-active flags')
  for key in IDLE_TRANSITIONS:need(before[key] is True and after[key] is False,'exact idle to active direction')
  proof.append(dict(section=('Names','Value')[section],transitions=[dict(address=list(key[:2]),name=key[2],before='idle',after='active') for key in ((0,0x0536,'PALETTE_BLACK_OUT'),(0,0x2086,'TEXT_PUTSA'))],all_other_retained_flags_equal=True))
 return proof

def idle_provider_reference_proof(baseline,work,model):
 from review_th03_cpu_link_order import omf
 baseline,work=Path(baseline),Path(work);wanted={'TEXT_PUTSA':(0xccc8,'cd235615',7700,'0bff56e634211c638c884c7c3664893e9f1e0576b8b4a12315afbfe6200bd315'),'PALETTE_BLACK_OUT':(0xc7bd,'cc185614',708,'18407869a96309403f7b01f8b4644b843efb82aac06de5191a282e61b0edcb6e')}
 old=publics(baseline/'obj/th03/main.obj');new=publics(work/'obj/th03/main.obj');old=[p for p in old if p['name'] in wanted];new=[p for p in new if p['name'] in wanted]
 keys=('name','module','segment_index','segment','group_index','group','offset','frame','type_index','record_sha256','public_ordinal')
 need(len(old)==len(new)==2 and [{k:p[k] for k in keys} for p in old]==[{k:p[k] for k in keys} for p in new],'two exact idle provider records and literal order')
 for p in new:
  _,_,off,h=wanted[p['name']];need(p['offset']==off and p['record_sha256']==h,'exact idle provider identity')
  resolved=resolved_public(p,[tuple(r) for r in model['detailed_rows']]);need(resolved in IDLE_TRANSITIONS,'exact idle provider address')
 _,blocks=omf(work/'obj/th03/warning.obj',[dict(module='src/main/player/warning.cpp',segment='PLAYER_M_TEXT',start=0xc7a5)])
 refs=[f for b in blocks for f in b['fixups'] if f['target'] in wanted];need(len(refs)==2,'exact two genuine warning references')
 for f in refs:
  site,raw,_,_=wanted[f['target']];need((f['site'],f['kind'],f['target_method'],f['frame_method'],f['frame'],f['raw'],f['mz_site'])==(site,3,2,5,None,raw,site+2),'exact warning idle-to-active EXTDEF/FIXUPP reference')
 return dict(providers=[{k:p[k] for k in keys} for p in new],genuine_warning_references=refs,independent_review_command='bba140026fe444c397373fd0aca1a111',scope='Exact two previously root-local-only callees now genuinely referenced by warning producer; both display sections idle to active only.')

def validate(repo,baseline,work):
 """Production entry: conjunctive fresh-input proofs and frozen observed displays."""
 import json
 repo,baseline,work=Path(repo),Path(baseline),Path(work)
 display_raw=(Path(__file__).parent/'th03_tail_public_display.json').read_bytes();need(sha(display_raw)=='3219df80ac6d56269c1c83af0d5fd4e43286a304ca93bcea09606496cf1b7cb9','frozen observed display pin');display=json.loads(display_raw)
 model=derive_zero_and_contribution_model(baseline,work);inventory=derive_public_inventory(baseline,work,model);bt=(baseline/'obj/th03/main.map').read_text('latin1');ct=(work/'obj/th03/main.map').read_text('latin1')
 validate_aggregate_prefix((baseline/'obj/th03/main.map').read_bytes(),(work/'obj/th03/main.map').read_bytes(),model)
 validate_rows(model,ct);capture_observed_public_positions(bt,ct,inventory);validate_public_vectors(display,ct)
 runtime=runtime_provider_proof(repo,bt);idle=idle_provider_reference_proof(baseline,work,model)
 return dict(retained_map_supplement_pass=True,cold_reproduction_required=True,exact_acceptance=False,accepted_credit=0,aggregate_rows=len(model['aggregate_rows']),detailed_rows=len(model['detailed_rows']),public_vectors=[len(display['complete_names']),len(display['complete_values'])],runtime_provider_proof=runtime,idle_provider_reference_proof=idle,scope='Literal retained display supplement; original HOLD unchanged. Cold generation and raw/relocation gates are separate obligations.')
