"""Pre-link producer-boundary model. Never reads candidate EXE/MAP or runs tools.

Literal pairs are [segment, offset]. This is a retained-baseline diagnostic,
not original-global relocation acceptance. Production requires a fresh root
whose PLAYER_M_TEXT is exactly 1741 bytes and four exact reviewed OMF schemas.
Eight caller sites retain explicit original NOP/PUSH CS/CALL near semantics.
"""
from pathlib import Path
import hashlib, re, struct
from lib.omf import parse_omf
from lib import th03_tail_warning_gate as warning_gate
from review_th03_cpu_link_order import rows, mz, module_runs, omf

BASE_PINS = {
 'obj/th03/main.obj':'cf4897509fd21eff5aeb0ac1a1441a07cf2fd4e15944375cffae809a482d32e8',
 'obj/th03/main.map':'8eaec19618c90df6d5fe084b645039c70ac0f418e8e925ebce77278c14769921',
 'bin/th03/main.exe':'8f531a234e1a770063e90ab9500a6026ab23e75ea8d7b790fc6a63e3796da7f4',
 'obj/th03/main.@l':'cfa529524d2e45b5306f6586d5715a3094e9e924fa8dd3c76659ace585baf143'}
SPECS = {
 'warning':dict(module='src/main/player/warning.cpp',start=0xc7a5,size=1560,fixups=125,sites=37,lower={'@HUD_STATIC_GAUGE_LEVELS_PUT$QI':2,'PALETTE_RESTORE_FOR_PID':2},reference='.analysis/gpt-dots-tail-warning-probe-v08/compile-first-v01/source/obj/th03/warning.obj',sha='67197a27bb95516f2322c218cc516544fc480c71c74de0db03158df8ff4cd02a'),
 'effects':dict(module='src/main/player/effects.cpp',start=0xcdbd,size=628,fixups=33,sites=11,lower={'@PLAYFIELD_FG_X_TO_SCREEN$QII':3},reference='.analysis/gpt-dots-effects-established-linkage-probe-v01/compile-first-v01/source/obj/th03/effects.obj',sha='d37d84309d2cc4d66ef62e67c2685839ac05c74bc1ea90be60d408cb4272d13a'),
 'chain1':dict(module='src/main/background/chain1.cpp',start=0xd031,size=695,fixups=43,sites=19,lower={},reference='.analysis/gpt-dots-background-cpp-tail-probe-v01/compile-first-v01/source/obj/chain1.obj',sha='5f88e781027458dfa4cefbcf59097e31d2cf57396074cd7d43845e448c16eb76'),
 'chain2':dict(module='src/main/background/chain2.cpp',start=0xd2e8,size=550,fixups=43,sites=16,lower={},reference='.analysis/gpt-dots-background-chain2-typed-probe-v02/compile-first-v01/source/obj/chain2.obj',sha='867773a6a70739f6494bf50b01a17b0fcd581170e0fef741c5feee9c3725d775')}
ORDER=tuple(SPECS)
LOW_ROOT = ((0x2c49,3,0,'_TEXT',5,None),(0x2c82,3,0,'_TEXT',5,None))
EXPLICIT_NEAR_CALLS={0x980f:('@player_effects_update$qv',0xceb2),0x9845:('_round_CA3C',0xca3c),0x984c:('ROUND_CB81',0xcb81),0x9853:('ROUND_CB81',0xcb81),0x990e:('@player_effects_render$qv',0xcee0),0x99bc:('ROUND_C9FE',0xc9fe),0x99c3:('ROUND_C9FE',0xc9fe),0xe0ea:('BOMB_EXPLOSION_ADD',0xcdbd)}
CRITICAL=('THEADR','LNAMES','SEGDEF','GRPDEF','EXTDEF','PUBDEF','LEDATA','FIXUPP','MODEND')
def need(ok,msg):
 if not ok: raise ValueError(msg)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def pin(path,digest):
 raw=Path(path).read_bytes();need(sha(raw)==digest,'pinned baseline/reference drift: '+str(path));return raw
def idx(d,i):
 need(i<len(d),'index bounds');n=d[i];i+=1
 if n&128:need(i<len(d),'wide index bounds');n=((n&127)<<8)|d[i];i+=1
 return n,i
def identity(f):return tuple(f[k] for k in ('site','kind','target_method','target','frame_method','frame'))
def describe(path,maprows):
 """The existing decoder keeps FIXUPP subrecord and LEDATA order verbatim."""
 recs=parse_omf(Path(path).read_bytes());need(recs and recs[0].name=='THEADR','one THEADR')
 need(sum(r.name=='THEADR' for r in recs)==1,'one object module')
 need(not any(r.name in ('LIDATA32','COMDAT','COMDAT32','COMDEF','LCOMDEF','LEDATA32','FIXUPP32','SEGDEF32') for r in recs),'unsupported allocation/32-bit dialect')
 last_data=None
 for r in recs:
  if r.name in ('LIDATA','LEDATA'):last_data=r.name
  elif r.name=='FIXUPP':need(last_data=='LEDATA','no LIDATA FIXUPP dialect')
 names=[''];segments=[];data={};coverage={}
 for r in recs:
  d=r.data
  if r.name=='LNAMES':
   p=0
   while p<len(d):n=d[p];p+=1;need(p+n<=len(d),'name bounds');names.append(d[p:p+n].decode('ascii'));p+=n
  elif r.name=='SEGDEF':
   need(len(d)>=6 and d[0]>>5!=0,'SEGDEF dialect');n,p=idx(d,3);c,p=idx(d,p);ov,p=idx(d,p);need(p==len(d),'SEGDEF trailing bytes');segments.append((names[n],int.from_bytes(d[1:3],'little'),d[0],names[c],names[ov]))
  elif r.name=='LEDATA':
   si,p=idx(d,0);need(si and si<=len(segments),'LEDATA segment');o=int.from_bytes(d[p:p+2],'little');p+=2;seg=segments[si-1];need(o+len(d)-p<=seg[1],'LEDATA segment bounds')
   data.setdefault(seg[0],bytearray(seg[1]));coverage.setdefault(seg[0],bytearray(seg[1]));need(not any(coverage[seg[0]][o:o+len(d)-p]),'LEDATA overlap');data[seg[0]][o:o+len(d)-p]=d[p:];coverage[seg[0]][o:o+len(d)-p]=b'\1'*(len(d)-p)
 mod,blocks=omf(Path(path),maprows)
 for b in blocks:
  for f in b['fixups']:
   need(f['kind'] in (0,1,2,3),'unsupported FIXUPP location kind')
   f['segment']=b['segment'];f['record']=b['record'];f['block_offset']=b['offset']
 return dict(module=mod,records=recs,segments=segments,blocks=blocks,data=data,coverage=coverage)
def base_context(base):
 base=Path(base);raw={n:pin(base/n,h) for n,h in BASE_PINS.items()};rs=rows(base/'obj/th03/main.map');rel=mz(base/'bin/th03/main.exe',rs);runs=module_runs(rel)
 roots=[r for r in runs if r['module']=='th03_main.asm'];need(len(roots)==1,'one attributed baseline root run');run=roots[0];old=describe(base/'obj/th03/main.obj',rs)
 rootrel=[r for r in rel if r['module']==old['module']];far=[f for b in old['blocks'] for f in b['fixups'] if 'mz_site' in f];actual={r['site'] for r in rootrel};lower=[f for f in far if f['mz_site'] not in actual];need(tuple(map(identity,lower))==LOW_ROOT,'only two baseline root lowerings')
 need([f['mz_site'] for f in far if identity(f) not in LOW_ROOT]==[r['site'] for r in rootrel],'baseline OMF-to-MZ complete literal correspondence')
 need(len(rootrel)==506 and len(far)==508,'baseline root counts')
 removed=[r for r in rootrel if 0xc7a5<=r['site'] and r['site']+2<=0xd50e];need(len(removed)==83,'exact baseline tail83')
 root_rows=[r for r in rs if r['module']=='th03_main.asm' and r['segment']=='PLAYER_M_TEXT'];need(len(root_rows)==1 and root_rows[0]['start']==0xc0d8 and root_rows[0]['size']==5174,'baseline root geometry')
 exe=raw['bin/th03/main.exe'];header=int.from_bytes(exe[8:10],'little')*16;im=exe[header:];found={}
 for row in rs:
  if row['module']!='th03_main.asm' or row['segment'] in ('_DATA','_BSS'):continue
  for a in range(row['start'],row['start']+row['size']-4):
   if 0xc7a5<=a<0xd50e:continue
   if im[a:a+3]==b'\x90\x0e\xe8':
    dest=a+5+struct.unpack_from('<h',im,a+3)[0]
    if 0xc7a5<=dest<0xd50e:
     need(row['group']=='MAIN_01','new lowering source group');found[a]=dest
 need(found=={a:t for a,(_,t) in EXPLICIT_NEAR_CALLS.items()},'exact eight baseline moved-target call sites')
 return dict(base=base,raw=raw,rows=rs,rel=rel,runs=runs,run=run,old=old,rootrel=rootrel,removed=removed)
def response_check(baseline_response,candidate_response):
 anchor=b'obj\\th03\\main.obj obj\\th03\\score_hud.obj';need(baseline_response.count(anchor)==1,'unique root/score anchor')
 inserted=b'obj\\th03\\main.obj obj\\th03\\warning.obj obj\\th03\\effects.obj obj\\chain1.obj obj\\chain2.obj obj\\th03\\score_hud.obj'
 need(candidate_response==baseline_response.replace(anchor,inserted,1),'exact response-only four-producer insertion')
 return [*ORDER]
def producer_stream(repo,name,path):
 if name=='warning':return strict_warning_stream(repo,path)
 spec=SPECS[name];ref=pin(Path(repo)/spec['reference'],spec['sha']);recs=parse_omf(Path(path).read_bytes());old=parse_omf(ref)
 need([r.name for r in recs]==[r.name for r in old],'record-type sequence '+name)
 for typ in CRITICAL:need([r.data for r in recs if r.name==typ]==[r.data for r in old if r.name==typ],'exact reviewed producer '+name+' '+typ)
 obj=describe(path,[dict(module=spec['module'],segment='PLAYER_M_TEXT',start=spec['start'])]);need(obj['module']==spec['module'],'producer THEADR')
 need([s[1] for s in obj['segments']]==[0,0,0,spec['size']],'producer zero allocation and full code');need(obj['segments'][3][:4]==('PLAYER_M_TEXT',spec['size'],0x28,'CODE'),'BYTE PUBLIC code segment');need(all(obj['coverage']['PLAYER_M_TEXT']),'whole producer coverage')
 fs=[f for b in obj['blocks'] for f in b['fixups']];need(len(fs)==spec['fixups'],'producer full FIXUPP count');out=[];lower=[];counts={}
 for f in fs:
  if 'mz_site' not in f:continue
  local=f['site']-spec['start']
  if f['kind']==3 and f['target'] in spec['lower']:
   need((f['target_method'],f['frame_method'],f['frame'])==(2,5,None),'same-group genuine external far fixup');need(obj['data']['PLAYER_M_TEXT'][local-1:local+4]==b'\x9a\0\0\0\0','far lowering call opcode/addend');counts[f['target']]=counts.get(f['target'],0)+1;lower.append(dict(f))
  else:out.append(dict(pair=[0x96e,f['mz_site']-0x96e0],module=spec['module'],segment='PLAYER_M_TEXT',site=f['mz_site'],record=f['record'],fixup=f))
 need(counts==spec['lower'],'only exact reviewed lowerings');need(len(out)==spec['sites'],'producer surviving literal count');return out,lower

def root_unresolved_bytes(ctx,obj):
 """Exact retained coverage and all bytes outside actual OMF operands.
The eight explicit NOP/PUSH CS/E8 prefixes are checked, never masked."""
 old=ctx['old'];widths={0:1,1:2,2:2,3:4};masked={};checked={}
 for name,size,*_ in obj['segments']:
  before=old['data'].get(name,bytearray(old_size(old,name)))[:size];after=obj['data'].get(name,bytearray(size))
  oldcov=old['coverage'].get(name,bytearray(old_size(old,name)))[:size];newcov=obj['coverage'].get(name,bytearray(size))
  need(len(before)==len(after)==size and oldcov==newcov,'exact retained LEDATA coverage '+name)
  mask=bytearray(size)
  row=next(r for r in ctx['rows'] if r['module']=='th03_main.asm' and r['segment']==name)
  for source in (old,obj):
   for block in source['blocks']:
    if block['segment']!=name:continue
    for f in block['fixups']:
     off=f['site']-row['start'];width=widths[f['kind']]
     if off>=size:continue
     need(off>=0 and off+width<=size,'fixup retained boundary '+name)
     need(all(newcov[off:off+width]),'fixup LEDATA coverage '+name);mask[off:off+width]=b'\1'*width
  for a in EXPLICIT_NEAR_CALLS:
   if not(row['start']<=a<row['start']+size):continue
   off=a-row['start'];need(before[off:off+3]==b'\x90\x0e\xe8','old exact nopcall prefix')
   need(after[off:off+5]==b'\x90\x0e\xe8\0\0','explicit NOP/PUSH CS/near CALL bytes');mask[off+3:off+5]=b'\1'*2
  need(all(a==b for i,(a,b) in enumerate(zip(before,after)) if not mask[i]),'unresolved retained LEDATA byte drift '+name)
  masked[name]=sum(mask);checked[name]=sum(newcov)-sum(mask)
 return dict(coverage_equal=True,nonfixup_bytes_equal=True,masked_operand_or_call_bytes=masked,compared_unmasked_emitted_bytes=checked)
def old_size(obj,name):
 return next(s[1] for s in obj['segments'] if s[0]==name)

def root_stream(ctx,fresh_root):
 rs=[dict(r,size=1741) if r['module']=='th03_main.asm' and r['segment']=='PLAYER_M_TEXT' else r for r in ctx['rows']]
 obj=describe(fresh_root,rs);need(obj['module']=='th03_main.asm','fresh root module identity')
 for typ in ('LIDATA','GRPDEF'):
  need([r.data for r in obj['records'] if r.name==typ]==[r.data for r in ctx['old']['records'] if r.name==typ],'retained root exact '+typ)
 expected=[(n,1741 if n=='PLAYER_M_TEXT' else z,a,c,o) for n,z,a,c,o in ctx['old']['segments']];need(obj['segments']==expected,'fresh root entire SEGDEF vector except exact3433 removal')
 byte_report=root_unresolved_bytes(ctx,obj)
 need(all(obj['coverage'].get('PLAYER_M_TEXT',())) and len(obj['coverage'].get('PLAYER_M_TEXT',()))==1741,'retained1741 whole root coverage')
 fs=[f for b in obj['blocks'] for f in b['fixups'] if 'mz_site' in f];lower=[f for f in fs if identity(f) in LOW_ROOT];need(tuple(map(identity,lower))==LOW_ROOT,'fresh root two known lowerings')
 for f in lower:
  row=next(r for r in rs if r['module']==obj['module'] and r['segment']==f['segment']);o=f['site']-row['start'];need(obj['data'][f['segment']][o-1]==0x9a,'retained root far-call lowering opcode')
 near_calls=[]
 all_fixups=[f for b in obj['blocks'] for f in b['fixups']]
 for f in all_fixups:
  if f['site']-3 not in EXPLICIT_NEAR_CALLS:continue
  a=f['site']-3;symbol,dest=EXPLICIT_NEAR_CALLS[a]
  need(identity(f)==(a+3,1,2,symbol,1,2),'exact explicit external near-call identity')
  need(not(int(f['raw'][:2],16)&0x40) and bytes.fromhex(f['raw'])[2]==0x16,'near self-relative OFFSET16/MAIN_01/no displacement')
  row=next(r for r in rs if r['module']==obj['module'] and r['segment']==f['segment']);o=a-row['start']
  need(row['group']=='MAIN_01' and obj['data'][f['segment']][o:o+5]==b'\x90\x0e\xe8\0\0','explicit NOP/PUSHCS/nearcall group/opcode/zero addend')
  displacement=(dest-(a+5))&65535
  near_calls.append(dict(f,call_site=a,target_load_address=dest,target_group='MAIN_01',bound_displacement=displacement,stack_contract='NOP; PUSH CS; CALL near to genuine far-return callee'))
 need({f['site']-3 for f in near_calls}==set(EXPLICIT_NEAR_CALLS) and len(near_calls)==8,'exact eight explicit near-call bindings present')
 survivors=[f for f in fs if identity(f) not in LOW_ROOT];retained=[r for r in ctx['rootrel'] if not(0xc7a5<=r['site'] and r['site']+2<=0xd50e)]
 need([f['mz_site'] for f in survivors]==[r['site'] for r in retained],'fresh root literal traversal must preserve every outside root site/order');need(len(survivors)==423 and len(fs)==425,'fresh root exact far counts')
 return [dict(pair=r['pair'],module=obj['module'],segment=f['segment'],site=f['mz_site'],record=f['record'],fixup=f) for f,r in zip(survivors,retained)],lower,near_calls,byte_report

def assemble_prediction(ctx,root_entries,producer_entries):
 """Internal pure splice. Production caller has already checked actual objects."""
 a=ctx['run']['start'];z=a+ctx['run']['count'];old=ctx['rel'];entries=old[:a]+root_entries+[e for n in ORDER for e in producer_entries[n]]+old[z:];pairs=[r['pair'] for r in entries]
 outside=lambda es:[r['pair'] for r in es if not(0xc7a5<=r['site'] and r['site']+2<=0xd50e)]
 need(outside(entries)==outside(old),'complete1470 outside literal sequence');need(len(pairs)==len(old)==1553,'complete1553 count');need(len(outside(entries))==1470,'outside1470 count')
 need(len({tuple(p) for p in pairs})==len(pairs),'no duplicated literal relocation words')
 packed=b''.join(struct.pack('<HH',o,s) for s,o in pairs)
 return dict(full_literal_stream=pairs,packed_stream_sha256=sha(packed),attribution=entries,baseline_root_run=dict(ctx['run']),derived_new_producer_start=a+len(root_entries),outside_count=1470,owned_count=83,total_count=1553,original_global_interposition_proved=False,exact_acceptance=False)

def target_owned_check(repo,producer_entries):
 raw=pin(Path(repo)/'.analysis/targets/th03/main.exe','f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b');count=int.from_bytes(raw[6:8],'little');off=int.from_bytes(raw[24:26],'little');expected=[]
 for i in range(count):
  o,g=struct.unpack_from('<HH',raw,off+i*4);a=g*16+o
  if 0xc7a5<=a and a+2<=0xd50e:expected.append([g,o])
 actual=[r['pair'] for n in ORDER for r in producer_entries[n]]
 need(len(expected)==83 and actual==expected,'all83 owned original literal pairs/order')
 return True

def build_model(repo,baseline,fresh_root,producer_paths,candidate_response):
 """Production gate; no baseline-test flag and no candidate result input.

Call only after four fresh compiler objects and fresh root assembly exist,
BEFORE the single link. Persist the returned model and pin all input hashes.
"""
 need(set(producer_paths)==set(ORDER),'exact four producer set');ctx=base_context(baseline);response_check(ctx['raw']['obj/th03/main.@l'],candidate_response);root,root_lower,root_near,root_bytes=root_stream(ctx,fresh_root)
 ps={};lower={}
 for n in ORDER:ps[n],lower[n]=producer_stream(repo,n,producer_paths[n])
 target_owned_check(repo,ps)
 result=assemble_prediction(ctx,root,ps);result.update(kind='pre-link actual-OMF producer-boundary prediction',warning_call_validation=warning_gate.validate(producer_paths['warning'],repo),producer_lowerings=lower,root_lowerings=root_lower,root_explicit_near_calls=root_near,root_unresolved_bytes=root_bytes,input_hashes={'root':sha(Path(fresh_root).read_bytes()),'response':sha(candidate_response),**{n:sha(Path(producer_paths[n]).read_bytes()) for n in ORDER}},baseline_pins=BASE_PINS)
 return result


def strict_warning_stream(repo,path):
 warning_gate.validate(path,repo)
 spec=SPECS['warning'];obj=describe(path,[dict(module=spec['module'],segment='PLAYER_M_TEXT',start=spec['start'])])
 out=[dict(pair=[0x96e,f['mz_site']-0x96e0],module=spec['module'],segment='PLAYER_M_TEXT',site=f['mz_site'],record=f['record'],fixup=f) for b in obj['blocks'] for f in b['fixups'] if 'mz_site' in f]
 need(len(out)==37,'warning37 genuine literal sites')
 return out,[]
