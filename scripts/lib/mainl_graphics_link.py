"""Read-only source-split graphics link diagnostics; segment lineage changed."""
from pathlib import Path
import sys, hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows
import replay_th03_mainl_regist as reg
import replay_th03_mainl_cutscene as cut
import review_th03_mainl_transitions as effects
from review_th03_mainl_snow import SnowProbe

def need(ok,message):
 if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def diffs(a,b):return [dict(linear=i,target=a[i] if i<len(a) else None,candidate=b[i] if i<len(b) else None) for i in range(max(len(a),len(b))) if (a[i] if i<len(a) else None)!=(b[i] if i<len(b) else None)]
def relocs(m):return [(r.segment,r.offset) for r in m.relocations]
def clear(m):
 result=[]
 for df in (False,True):
  p=SnowProbe(m,df=df);before=bytes(p.uc.mem_read(0xa8000,65538));p.run(0x2561)
  after=bytes(p.uc.mem_read(0xa8000,65538))
  result.append(dict(df=df,before=sha(before),after=sha(after),writes=p.writes,flags=p.get('EFLAGS')))
 return result

def check_far_pointer_call(encoded):
 need(len(encoded)==8 and encoded[:3]==bytes.fromhex('66ff36') and encoded[5]==0xe8,'loader call must push4-byte FAR pointer then near CALL')

def verify(exe,map_raw,target_raw,context_raw):
 candidate=parse_mz(exe);target=parse_mz(target_raw);context=parse_mz(context_raw)
 need(all(x.valid for x in (candidate,target,context)),'valid MZ required')
 image=candidate.program_image;original=target.program_image
 at=0x95f*16+0x241e
 check_far_pointer_call(original[at:at+8]);check_far_pointer_call(image[at:at+8])
 need(image[at:at+8]==original[at:at+8],'loader source lowering changed original argument/call')
 rows=code_rows(map_raw.decode('ascii'),len(image))
 expected=[('MAINL_03_TEXT',0x24e6,144),('MAINL_SNOW_TEXT',0x2576,443),('MAINL_DISSOLVE_TEXT',0x2731,211),('MAINL_STAFF_TEXT',0x2804,2541)]
 segment_rows=[]
 for name,offset,size in expected:
  found=[r for r in rows if r['name'].upper()==name and r['size']]
  need(len(found)==1,'new segment row '+name)
  row=found[0];need((row['segment'],row['offset'],row['size'])==(0x95f,offset,size),'source-level group layout '+name)
  segment_rows.append(row)
 bodies=[]
 for name,offset,size in [('unput',0x24e6,123),('clear',0x2561,21),('dissolve',0x2731,211)]:
  start=0x95f*16+offset;end=start+size
  bodies.append(dict(name=name,offset=offset,bytes=size,raw_equal=image[start:end]==original[start:end],target_sha256=sha(original[start:end]),candidate_sha256=sha(image[start:end]),ordered_target_relocations=[r for r in relocs(target) if start<=r[0]*16+r[1]<end],ordered_candidate_relocations=[r for r in relocs(candidate) if start<=r[0]*16+r[1]<end]))
 preserved=[]
 for name,offset,size,count in [('CUTSCENE_TEXT',0xb3e,3195,56),('SCOREDAT_TEXT',0x17b9,229,0),('REGIST_TEXT',0x189e,2720,54)]:
  start=0x95f*16+offset;end=start+size
  a=[r for r in relocs(target) if start<=r[0]*16+r[1]<end];b=[r for r in relocs(candidate) if start<=r[0]*16+r[1]<end]
  preserved.append(dict(name=name,bytes=size,raw_equal=image[start:end]==original[start:end],ordered_relocations_equal=a==b,relocations=len(b)))
  need(len(b)==count,'prior owned relocation count')
 runtime=[]
 for label,m in [('target',target),('candidate',candidate)]:
  observations=dict(effects=effects.native_matrix(m),clear=clear(m),registration=reg.runtime_matrix(m),cutscene=cut.runtime_matrix(m))
  runtime.append(dict(label=label,observations=observations))
 differences=diffs(original,image);context_diffs=diffs(context.program_image,image)
 a=relocs(target);b=relocs(candidate)
 from collections import Counter
 result=dict(kind='mainl-graphics-source-split-link',input_sha256=dict(exe=sha(exe),map=sha(map_raw),target=sha(target_raw),context=sha(context_raw)),new_segment_rows=segment_rows,original_segment_identity_preserved=False,group_contract='Four byte-aligned public CODE contributions in group_01; original combined3339 split into144/443/211/2541',graphics_bodies=bodies,graphics_bytes=355,prior_owned6144=preserved,target_byte_differences=differences,target_byte_difference_count=len(differences),context_byte_differences=context_diffs,context_byte_difference_count=len(context_diffs),target_relocations=dict(target_count=len(a),candidate_count=len(b),ordered_equal=a==b,membership_equal=Counter(a)==Counter(b),ordered_differences=[dict(index=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]),runtime_equal=runtime[0]['observations']==runtime[1]['observations'],runtime=runtime,exact_acceptance=False,cold_aggregate=False,source_progress_changed=False)
 result['diagnostic_checks_pass']=(all(r['raw_equal'] for r in bodies) and all(r['raw_equal'] and r['ordered_relocations_equal'] for r in preserved) and differences==[dict(linear=0xe3f*16+0x849,target=0x90,candidate=0)] and result['runtime_equal'])
 return result
