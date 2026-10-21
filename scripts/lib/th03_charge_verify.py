"""Read-only scoped MAIN charge diagnostic, not acceptance or runtime proof."""
from pathlib import Path
import hashlib,json,sys,struct
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_cpu_link_order import rows,omf
START=0x16983;END=START+1645
EXPECTED=[(0x139d,0x2fb3+x) for x in (875,850,713,689,671,639,551,482,363,333,1527,1500)]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def pinned(root,row):
 p=Path(root)/row['path'];need(p.is_file() and not p.is_symlink(),'pin path '+str(p));b=p.read_bytes();need(sha(b)==row['sha256'] and len(b)==row['bytes'],'pin bytes '+str(p));return b
def records(raw):
 rs=parse_omf(raw);ordinary=[];deps=[];source=[];terminal=0
 need(rs[0].name=='THEADR' and rs[-1].name=='MODEND','one ordinary OMF module')
 for r in rs:
  d=r.data
  if r.name=='COMENT' and d[:2]==b'\0\xe9':
   if d==b'\0\xe9':terminal+=1;continue
   need(len(d)>=7 and len(d)==7+d[6],'E9 framing');deps.append((d[7:].decode('ascii'),d[2:6]));continue
  if r.name=='COMENT' and d[:2]==b'\0\xe8':
   need(len(d)>=8 and d[2]==1 and len(d)==8+d[3],'E8 framing');source.append((d[4:-4].decode('ascii'),d[-4:]));ordinary.append((r.record_type,d[:-4]));continue
  ordinary.append((r.record_type,d))
 need(terminal==1 and len(source)==1 and deps and source[0]==deps[0],'source-time dependency binding')
 return ordinary,[x[0] for x in deps]
def object_contract(new,old,newpath):
 a,paths=records(old);b,actual=records(new)
 expected=[paths[0],'src/main/player/chargeshot_yumemi.cpp']+[{'yumemi_gameplay.hpp':'src/main/player/yumemi_gameplay.hpp','target_enemy_record.hpp':'src/main/enemy/target_record.hpp'}.get(x,x) for x in paths[1:]]
 need(actual==expected,'explicit maintained dependency order/multiplicity')
 need(a==b,'all nondependency OMF records including CODE/FIXUPP/publics/segments')
 module,blocks=omf(newpath,[dict(module='th03/cs_yume.cpp',segment='PELLET_PUT',start=START)])
 fixups=[f for block in blocks for f in block['fixups']]
 need(len(fixups)==133,'133 fixups');need(sum(f['target_method']==2 for f in fixups)==124,'124external fixups')
 need(sum(f['kind']==3 for f in fixups)==13,'13 far pointers before linker relaxation')
 need([(x['offset'],x['size']) for x in blocks]==[(0,1024),(1024,621)],'natural two LEDATA records')
 return dict(pass_=True,all_nondependency_records_equal=True,symbolic_fixups=133,external_fixups=124,internal_fixups=9,far_pointers_before_link=13,explicit_dependency_transition=True,module=module,sha256=sha(new))
def pairs(m):return [(r.segment,r.offset) for r in m.relocations]
def inside(q):return START<=q[0]*16+q[1]<END
def byte_order_contract(current,baseline,target):
 need(current.valid and baseline.valid and target.valid,'valid MZ images')
 need(current.program_image==baseline.program_image,'complete accepted baseline load image preservation')
 need(current.program_image[START:END]==target.program_image[START:END],'complete1645 canonical charge bytes')
 cp=pairs(current);bp=pairs(baseline);tp=pairs(target)
 need([q for q in cp if inside(q)]==EXPECTED==[q for q in tp if inside(q)],'charge12 literal order')
 outside=[q for q in cp if not inside(q)];need(len(outside)==1541 and outside==[q for q in bp if not inside(q)],'outside1541 literal order')
 # Relocation list serialization differs by design, but allocation and entry fields do not.
 need(current.header==baseline.header,'complete MZ header fields unchanged')
 return dict(pass_=True,complete_baseline_load_equal=True,canonical_charge1645_equal=True,charge12_literal_equal=True,outside1541_literal_equal=True,load_bytes=len(current.program_image))
def verify(work,manifest):
 work=Path(work);plan=json.loads(pinned(ROOT,manifest['charge_plan']));old=pinned(ROOT,manifest['historical_charge_object']);baseline_raw=pinned(ROOT,manifest['prior_exe']);target_raw=pinned(ROOT,manifest['target']);mapold=pinned(ROOT,manifest['prior_map'])
 newpath=work/'obj/th03/cs_yume.obj';new=newpath.read_bytes();obj=object_contract(new,old,newpath)
 current=parse_mz((work/'bin/th03/main.exe').read_bytes());baseline=parse_mz(baseline_raw);target=parse_mz(target_raw);byteproof=byte_order_contract(current,baseline,target)
 need([list(x) for x in EXPECTED]==plan['expected_charge_literal_pairs'],'plan charge pairs');need([list(x) for x in pairs(baseline) if not inside(x)]==plan['outside_literal_pairs'],'plan baseline outside pairs')
 rs=rows(work/'obj/th03/main.map');pellet=[r for r in rs if r['segment']=='PELLET_PUT'];charge=[r for r in pellet if r['module']=='th03/cs_yume.cpp'];root=[r for r in pellet if r['module']=='th03_main.asm'];bullet=[r for r in pellet if r['module']=='th03/bullet.cpp']
 need(len(charge)==1 and charge[0]['start']==START and charge[0]['size']==1645 and charge[0]['group']=='MAIN_04' and charge[0]['acbp']=='28','charge MAP owner')
 need(len(root)==1 and root[0]['size']==0 and root[0]['start']==START,'root zero PELLET scaffold')
 need(len(bullet)==1 and bullet[0]['start']==END and bullet[0]['size']==83,'following bullet placement')
 # Initial diagnostic reports full MAP changes; it does not claim a fully reviewed MAP contract.
 newmap=(work/'obj/th03/main.map').read_bytes()
 return dict(kind='main-yumemi-charge-retained-context-diagnostic',diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,native_runtime_proved=False,cold_build_proved=False,object=obj,linked=byteproof,map_scope_pass=True,pellet_map=pellet,full_map_raw_equal=newmap==mapold,full_map_sha256=sha(newmap),full_map_acceptance_pending=True,all_other_loaded_bytes_preserved=True,notes='Full MAP display changes and every accepted-owner integration gate require independent review; this is not default acceptance.')
