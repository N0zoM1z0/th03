"""Read-only literal OP exact-order observation. Never emulates or repairs native output."""
from pathlib import Path
import collections,hashlib,json,re,struct,sys
ROOT=Path(__file__).resolve().parents[2]
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_cpu_link_order import rows,index
NAMES=['OP_01_TEXT','OP_MUSIC_TEXT','OP_MAIN_TEXT','OP_02_TEXT','SCOREDAT_TEXT','OP_SEL_TEXT']
def need(v,m):
 if not v:raise ValueError(m)
def pin(q):
 p=ROOT/q['path'];need(not any(x.is_symlink() for x in (p,*p.parents)),'symlink');b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==q['sha256'] and len(b)==q['bytes'],'pin drift '+q['path']);return b
def anchor_records(records):
 names=[''];segs=[None];groups=[]
 for r in records:
  d=r.data
  need(r.record_type in (0x80,0x88,0x8a,0x96,0x98,0x9a),'unexpected anchor record '+r.name)
  if r.record_type==0x96:
   i=0
   while i<len(d):n=d[i];i+=1;names.append(d[i:i+n].decode('ascii'));i+=n
  elif r.record_type==0x98:
   need(len(d)>=6 and d[0]==0x28 and int.from_bytes(d[1:3],'little')==0,'nonempty or wrong-attribute segment');ni,i=index(d,3);ci,i=index(d,i);oi,i=index(d,i);need(i==len(d),'SEGDEF trailing bytes');need(names[ci]=='CODE' and names[oi]=='','segment class/overlay');segs.append(names[ni])
  elif r.record_type==0x9a:
   need(d.hex()=='0eff06ff05ff04ff03ff02ff01','exact observed native GRPDEF bytes')
   ni,i=index(d,0);members=[]
   while i<len(d):need(d[i]==0xff,'group component');si,i=index(d,i+1);need(0<si<len(segs),'group segment');members.append(segs[si])
   groups.append(dict(name=names[ni],members=members))
  elif r.record_type==0x8a:need(d==b'\0','anchor has start address or main-module flag')
 need(segs[1:]==NAMES,'anchor segment membership/order');need(groups==[dict(name='GROUP_01',members=list(reversed(NAMES)))],'anchor group membership/order')
 return dict(pass_checks=True,segments=segs[1:],groups=groups,all_lengths_zero=True,no_data_fixups_publics_or_externals=True)
def verify_anchor(path):
 b=Path(path).read_bytes();return dict(anchor_records(parse_omf(b)),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def public_sections(text):
 sections={};current=None;done=False
 for line in text.splitlines():
  stripped=line.strip()
  if stripped in ('Address         Publics by Name','Address         Publics by Value'):
   key='name' if stripped.endswith('Name') else 'value';need(key not in sections and not done,'duplicate public section');sections[key]=[];current=key;continue
  if stripped.startswith('Program entry point at '):need(current=='value','entry after Value section');current=None;done=True;continue
  if current is None or not stripped:continue
  m=re.fullmatch(r'\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(.*?)\s*',line);need(m is not None,'unparsed actual public row');body=m[3];idle=False
  if body.startswith('idle '):idle=True;body=body[5:].lstrip()
  need(bool(body) and not re.search(r'\bC=\S+.*\bS=',body),'segment contribution inside public section');sections[current].append((int(m[1],16),int(m[2],16),body,idle))
 need(set(sections)=={'name','value'} and done and all(sections.values()),'complete public sections required');need(collections.Counter(x[:3] for x in sections['name'])==collections.Counter(x[:3] for x in sections['value']),'public sections disagree');return sections
ADDED={'SOUND_I':(0,0x21e0),'SOUND_O':(0,0x21ca),'parfilename':(0xd7f,0x1a1c),'pfint21_pf':(0xd7f,0x1a9c),'pfint21_handle':(0xd7f,0x1a9e),'pfint21_entries':(0xd7f,0x1aa0),'trapezoid_hmask':(0xd7f,0x5e8)}
OLD_EXTERN_NAMES={'FILE_ROPEN','HMEM_ALLOCBYTE','FILE_READ','HMEM_FREE','FILE_CLOSE','PFCLOSE','PFREAD','PFREWIND','PFSEEK','BOPENR','BSEEK_','PFGETX0','PFGETX1','PFGETC1','BCLOSER','js_bexist','ClipYB_adr','ClipXL','ClipXW','EDGES','mem_AllocID','pferrno','js_stat','trapez_a','trapez_b','draw_trapezoid'}
def public_delta(a,b):
 a,b=public_sections(a),public_sections(b);changes={};ok=True
 for section in a:
  old=b[section];new=a[section];oldnames={x[2] for x in old};ok &= not bool(oldnames & set(ADDED));existing=[x for x in new if x[2] not in ADDED];added=[x for x in new if x[2] in ADDED]
  ok &= collections.Counter(x[:3] for x in existing)==collections.Counter(x[:3] for x in old)
  ok &= collections.Counter(x[:3] for x in added)==collections.Counter((s,o,n) for n,(s,o) in ADDED.items())
  minus=collections.Counter(old)-collections.Counter(existing);plus=collections.Counter(existing)-collections.Counter(old);d=[]
  for row,count in minus.items():
   counterpart=(*row[:3],False);valid=row[3] is True and row[2] in OLD_EXTERN_NAMES and plus[counterpart]==count;ok &= valid;d.append(dict(before=row,after=counterpart,count=count,allowed=valid));plus.subtract({counterpart:count})
  ok &= not any(v for v in plus.values());changes[section]=dict(added=added,idle_changes=d)
 return dict(pass_checks=bool(ok),sections=changes)
def same_publics(a,b):return public_delta(a,b)['pass_checks']
def contribution_split(candidate,baseline):
 positive=lambda rs:[r for r in rs if r['size']];expected=[];found=0
 for r in positive(baseline):
  if r['module']=='th03_op.asm' and r['segment']=='_TEXT':
   need(r['start']==0x272 and r['size']==11730,'actual baseline root span');expected += [dict(r,size=10472),dict(r,start=0x2b5a,size=1258,module='th03_optail.asm')];found+=1
  else:expected.append(r)
 need(found==1,'unique root code contribution');return positive(candidate)==expected

def split_object_records(records,role):
 names=[''];segments=[];pubs=[];current=None;sites=[]
 for r in records:
  d=r.data
  if r.record_type==0x96:
   i=0
   while i<len(d):n=d[i];i+=1;names.append(d[i:i+n].decode('ascii'));i+=n
  elif r.record_type==0x98:
   ni,i=index(d,3);ci,i=index(d,i);oi,i=index(d,i);need(i==len(d) and d[0]==0x48,'word/public16 segment');segments.append(dict(name=names[ni],class_name=names[ci],size=int.from_bytes(d[1:3],'little')))
  elif r.record_type in (0x99,0x9d,0xa1,0xa2,0xa3):raise ValueError('unsupported split object record')
  elif r.record_type==0xa0:
   si,i=index(d,0);current=(segments[si-1]['name'],int.from_bytes(d[i:i+2],'little'))
  elif r.record_type==0x9c:
   need(current is not None,'fixup before data');i=0
   while i<len(d):
    loc=d[i];fd=d[i+2];kind=(loc>>2)&15;at=((loc&3)<<8)|d[i+1];need(loc&128 and not(fd&128) and not(fd&8),'threaded fixup unsupported');i+=3;fm=(fd>>4)&7;tm=fd&3
    if fm<=2:_,i=index(d,i)
    elif fm==3:i+=2
    _,i=index(d,i)
    if not(fd&4):i+=2
    need(i<=len(d),'truncated fixup')
    if kind in (2,3):sites.append(dict(segment=current[0],site=current[1]+at+(2 if kind==3 else 0),kind=kind,target_method=tm))
  elif r.record_type==0x90:
   gi,i=index(d,0);si,i=index(d,i)
   if si==0:i+=2
   while i<len(d):n=d[i];i+=1;name=d[i:i+n].decode('ascii');i+=n;offset=int.from_bytes(d[i:i+2],'little');i+=2;_,i=index(d,i);pubs.append(dict(name=name,segment=segments[si-1]['name'] if si else None,offset=offset))
 expected_sizes=[10472,890,3552] if role=='prefix' else [1258,0,0]
 need(role in ('prefix','suffix'),'known role');need(segments==[dict(name=n,class_name=c,size=z) for n,c,z in zip(('_TEXT','_DATA','_BSS'),('CODE','DATA','BSS'),expected_sizes)],'exact split segment declarations/sizes')
 expected_sites=[4908-626,5136-626,5225-626,6108-626,9025-626] if role=='prefix' else [0x2c67-0x2b5a]
 need(sites==[dict(segment='_TEXT',site=x,kind=2,target_method=1) for x in expected_sites],'exact surviving literal segment fixups, no cross-FAR additions')
 if role=='prefix':need({p['name'] for p in pubs}&set(ADDED)==set(ADDED),'seven genuine added PUBLICs')
 else:need(not({p['name'] for p in pubs}&set(ADDED)),'added symbol ownership')
 return dict(pass_checks=True,role=role,segments=segments,literal_segment_fixups=sites,publics=pubs)
def verify_split_object(path,role):
 raw=Path(path).read_bytes();return dict(split_object_records(parse_omf(raw),role),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def rels(x):return [[r.segment,r.offset] for r in x.relocations]
def scoped(x,s,o,n):
 lo=s*16+o;hi=lo+n;need(hi<=len(x.program_image),'scope extent')
 for r in x.relocations:need(not(r.linear<hi and r.linear+2>lo and not(lo<=r.linear and r.linear+2<=hi)),'straddled fixup')
 return x.program_image[lo:hi],[[r.segment,r.offset] for r in x.relocations if lo<=r.linear<hi]
def header_without_relocations(b):
 h=int.from_bytes(b[8:10],'little')*16;start=int.from_bytes(b[24:26],'little');end=start+int.from_bytes(b[6:8],'little')*4;need(28<=start<=end<=h,'header bounds');return b[:start],b[end:h]
def verify(work,m):
 work=Path(work)
 for q in m['inputs']:pin(q)
 for n,q in m['repeat_inputs'].items():need((work/n).read_bytes()==pin(q),'retained input changed '+n)
 need(len(m['retained_objects'])==27,'27 original project objects retained')
 anchor=verify_anchor(work/'obj/th03/oplayout.obj')
 cr=(work/'bin/th03/op.exe').read_bytes();br=pin(m['baseline_exe']);tr=pin(m['target']);c,b,t=map(parse_mz,(cr,br,tr));need(c.valid and b.valid and t.valid,'invalid MZ')
 baseline=json.loads(pin(m['baseline_report']));specs=baseline['owners'];need(len(specs)==44 and sum(u['size'] for u in specs)==12940,'owner denominator')
 owners=[]
 for u in specs:
  cb,cf=scoped(c,u['segment'],u['offset'],u['size']);bb,bf=scoped(b,u['segment'],u['offset'],u['size']);tb,tf=scoped(t,u['segment'],u['offset'],u['size']);owners.append(dict(id=u['id'],segment=u['segment'],offset=u['offset'],size=u['size'],baseline_raw_equal=cb==bb,baseline_order_equal=cf==bf,target_raw_equal=cb==tb,target_order_equal=cf==tf))
 cc=rows(work/'obj/th03/op.map');bc=rows(ROOT/m['baseline_map']['path']);positive=lambda r:[x for x in r if x['size']]
 pfcb,pfcf=scoped(c,0,0x2ef2,281);pfbb,pfbf=scoped(b,0,0x2ef2,281);pftb,pftf=scoped(t,0,0x2ef2,281)
 candidate=rels(c);base=rels(b);target=rels(t);conditional=json.loads(pin(m['static_proof']))['conditional_pairs'];need(len(conditional)==607,'conditional evidence length')
 checks=dict(all607_target_ordered_equal=candidate==target,PFOPEN281_baseline_raw_and_order_preserved=pfcb==pfbb and pfcf==pfbf,anchor_zero_bytes=anchor['pass_checks'],whole_program_equal=c.program_image==b.program_image,header_fields_and_nonrelocation_header_equal=header_without_relocations(cr)==header_without_relocations(br),true_publics_names_addresses_multiplicity_and_idle_equal=same_publics((work/'obj/th03/op.map').read_text(),pin(m['baseline_map']).decode('ascii')),positive_contributions_order_and_starts_equal=contribution_split(cc,bc),all44_raw_and_local_order_preserved=all(u['baseline_raw_equal'] and u['baseline_order_equal'] for u in owners),relocation_count607=len(candidate)==len(base)==len(target)==607,relocation_membership_unchanged=collections.Counter(map(tuple,candidate))==collections.Counter(map(tuple,base)),CRT_suffix_unchanged=candidate[395:]==base[395:],all27_retained_objects_unchanged=all((work/n).read_bytes()==pin(q) for n,q in m['retained_objects'].items()))
 return dict(public_metadata_delta=public_delta((work/'obj/th03/op.map').read_text(),pin(m['baseline_map']).decode('ascii')),schema='th03-op-global-order-phaseB-diagnostic-v1',diagnostic_checks_pass=all(checks.values()),linked_scope_checks_pass=all(checks.values()),checks=checks,anchor=anchor,PFOPEN281_diagnostic=dict(baseline_raw_equal=pfcb==pfbb,baseline_order_equal=pfcf==pfbf,target_raw_equal=pfcb==pftb,target_order_equal=pfcf==pftf,source_credit_claimed=False),owners=owners,owner_count=44,owner_bytes=12940,actual_map_contributions=cc,actual_pairs=candidate,target_pairs=target,conditional_phaseB_equal=candidate==conditional,phaseB_hypothesis_supported=all(checks.values()) and candidate==conditional,target_different_positions=[i for i,(x,y) in enumerate(zip(candidate,target)) if x!=y],whole_target_ordered_equal=candidate==target,whole_target_program_equal=c.program_image==t.program_image,whole_file_equal_target=cr==tr,source_acceptance=False,exact_acceptance=False,whole_product_ownership=False,native_invocations_now=0,limitations='Actual native link measured literally. Exact607 target relocation order required; one known program byte remains outside this ordering experiment. Source/packing/whole-image acceptance remains separate.')
