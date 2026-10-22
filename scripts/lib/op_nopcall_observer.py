"""Literal phase-A observation, never link/layout emulation or binary repair."""
from pathlib import Path
import collections,hashlib,json,re,struct,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
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
 need([s for s in sites if s['kind']==2]==[dict(segment='_TEXT',site=x,kind=2,target_method=1) for x in expected_sites],'original segment16 fixups unchanged')
 need(len([s for s in sites if s['kind']==3])==(30 if role=='prefix' else 0),'all30 genuine FAR fixups, no chosen subset')
 if role=='prefix':need({p['name'] for p in pubs}&set(ADDED)==set(ADDED),'seven genuine added PUBLICs')
 else:need(not({p['name'] for p in pubs}&set(ADDED)),'added symbol ownership')
 return dict(pass_checks=True,role=role,segments=segments,literal_segment_fixups=sites,publics=pubs)
def verify_split_object(path,role):
 raw=Path(path).read_bytes();return dict(split_object_records(parse_omf(raw),role),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def code_bytes(path):
    image={};spans=[]
    for r in parse_omf(Path(path).read_bytes()):
        if r.record_type==0xa0:
            si,i=index(r.data,0);at=int.from_bytes(r.data[i:i+2],'little');data=r.data[i+2:]
            if si==1:
                need(at+len(data)<=10472,'code record bounds');need(not(set(image)&set(range(at,at+len(data)))),'overlapping code records');image.update({at+j:v for j,v in enumerate(data)});spans.append([at,at+len(data)])
    holes=sorted(set(range(10472))-set(image));need(holes==[0x2054,0x2055,0x2056,0x2057],'exact genuine uninitialized code storage topology');return image,spans

def verify_calls(work,m,prefix):
    baseline_manifest=json.loads(pin(m['baseline_manifest']));oldwork=ROOT/baseline_manifest['work'];oldcode,oldspans=code_bytes(oldwork/'obj/th03/op.obj');newcode,newspans=code_bytes(work/'obj/th03/op.obj');need(set(oldcode)==set(newcode) and oldspans==newspans,'unchanged actual LEDATA topology');far=[s for s in prefix['literal_segment_fixups'] if s['kind']==3];calls=[];windows=set()
    for s in far:
        at=s['site']-3;window=set(range(at,at+5));need(window<=set(oldcode) and window<=set(newcode) and not(window&windows),'actual five-byte call window coverage');windows.update(window);old=bytes(oldcode[i] for i in range(at,at+5));new=bytes(newcode[i] for i in range(at,at+5));need(s['segment']=='_TEXT' and old[:3]==bytes.fromhex('900ee8') and new[0]==0x9a,'genuine original five-byte far-call form');need(at+5+int.from_bytes(old[3:5],'little',signed=True)==int.from_bytes(new[1:3],'little'),'same genuine callee offset');need(new[3:5]==b'\0\0','segment field supplied by genuine FIXUPP');calls.append(dict(offset=at,old_assembly=old.hex(),new_assembly=new.hex()))
    need(len({q['offset'] for q in calls})==30,'unique30 CALL producers');need(all(oldcode[i]==newcode[i] for i in set(oldcode)-windows),'all other explicitly covered code bytes preserved');return dict(calls=calls,covered_bytes=len(oldcode),declared_bytes=10472,holes=[0x2054,0x2055,0x2056,0x2057],spans=oldspans,unchanged_covered_bytes_outside_call_windows=len(oldcode)-len(windows),filled_bytes=0)
def rels(x):return [[r.segment,r.offset] for r in x.relocations]
def scoped(x,s,o,n):
 lo=s*16+o;hi=lo+n;need(hi<=len(x.program_image),'scope extent')
 for r in x.relocations:need(not(r.linear<hi and r.linear+2>lo and not(lo<=r.linear and r.linear+2<=hi)),'straddled fixup')
 return x.program_image[lo:hi],[[r.segment,r.offset] for r in x.relocations if lo<=r.linear<hi]
def header_without_relocations(b):
 h=int.from_bytes(b[8:10],'little')*16;start=int.from_bytes(b[24:26],'little');end=start+int.from_bytes(b[6:8],'little')*4;need(28<=start<=end<=h,'header bounds');return b[:start],b[end:h]
def literal_checks(candidate,baseline,target):
    need(len(candidate.program_image)==len(baseline.program_image)==len(target.program_image)==59770,'program size')
    delta=[i for i,(a,b) in enumerate(zip(candidate.program_image,baseline.program_image)) if a!=b]
    return dict(entire_baseline_program_unchanged=delta==[],
                whole_target_program_equal=candidate.program_image==target.program_image,
                all607_target_ordered_equal=rels(candidate)==rels(target) and len(rels(candidate))==607,
                complete_baseline_order_preserved=rels(candidate)==rels(baseline))
def verify(work,m):
    work=Path(work)
    for q in m['inputs']:pin(q)
    for n,q in m['repeat_inputs'].items():need((work/n).read_bytes()==pin(q),'retained input changed '+n)
    need(len(m['retained_objects'])==29,'29 retained context/suffix/anchor objects')
    anchor=verify_anchor(work/'obj/th03/oplayout.obj');prefix=verify_split_object(work/'obj/th03/op.obj','prefix');calls=verify_calls(work,m,prefix)
    cr=(work/'bin/th03/op.exe').read_bytes();br=pin(m['baseline_exe']);tr=pin(m['target']);c,b,t=map(parse_mz,(cr,br,tr));need(c.valid and b.valid and t.valid,'valid MZ')
    baseline=json.loads(pin(m['baseline_report']));specs=baseline['owners'];need(len(specs)==44 and sum(u['size'] for u in specs)==12940,'owner denominator')
    owners=[]
    for u in specs:
        cb,cf=scoped(c,u['segment'],u['offset'],u['size']);bb,bf=scoped(b,u['segment'],u['offset'],u['size']);tb,tf=scoped(t,u['segment'],u['offset'],u['size'])
        owners.append(dict(id=u['id'],segment=u['segment'],offset=u['offset'],size=u['size'],baseline_raw_equal=cb==bb,baseline_order_equal=cf==bf,target_raw_equal=cb==tb,target_order_equal=cf==tf))
    pfc,pfb,pft=(scoped(x,0,0x2ef2,281) for x in (c,b,t));cc=rows(work/'obj/th03/op.map');bc=rows(ROOT/m['baseline_map']['path']);positive=lambda rs:[r for r in rs if r['size']]
    checks=literal_checks(c,b,t)
    checks.update(complete_raw_decoded_target_equal=cr==tr,complete_header_raw_target_equal=cr[:c.header.header_size]==tr[:t.header.header_size],true_publics_names_addresses_multiplicity_and_idle_equal=public_sections((work/'obj/th03/op.map').read_text())==public_sections(pin(m['baseline_map']).decode('ascii')),positive_contributions_order_and_starts_equal=positive(cc)==positive(bc),all44_raw_and_local_order_preserved=all(u['baseline_raw_equal'] and u['baseline_order_equal'] for u in owners),PFOPEN281_raw_and_local_order_preserved=pfc==pfb==pft,all29_retained_objects_unchanged=all((work/n).read_bytes()==pin(q) for n,q in m['retained_objects'].items()),anchor_zero_bytes=anchor['pass_checks'],prefix_segment_and_literal_fixups=prefix['pass_checks'])
    return dict(schema='th03-op-original-farcall-producer-diagnostic-v1',diagnostic_checks_pass=all(checks.values()),checks=checks,original_far_call_producers=calls,owners=owners,owner_count=44,owner_bytes=12940,PFOPEN281_preserved=pfc==pfb,anchor=anchor,prefix=prefix,actual_pairs=rels(c),target_pairs=rels(t),program_difference_from_baseline=[i for i,(x,y) in enumerate(zip(c.program_image,b.program_image)) if x!=y],whole_target_program_equal=c.program_image==t.program_image,whole_target_ordered_equal=rels(c)==rels(t),whole_file_equal_target=cr==tr,source_acceptance=False,exact_acceptance=False,source_progress_changed=False,cold_build=False,whole_product_ownership=False,alignment_authored_credit=0,native_invocations_now=0,limitations='Uniform original vendor FAR call producer semantics; no new authored credit, packed equality, cold build, runtime or formal acceptance.')
