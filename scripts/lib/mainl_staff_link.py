"""Full coherent MAINL graphics/snow/staff decoded proof; no packed exact credit."""
from pathlib import Path
import sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.mainl_graphics_link import verify as graphics_verify, parse_mz, relocs, sha, need
import review_th03_mainl_snow as snow
import review_th03_mainl_transitions as staff

def verify(exe,map_raw,target_raw,context_raw):
    result=graphics_verify(exe,map_raw,target_raw,context_raw)
    target=parse_mz(target_raw);candidate=parse_mz(exe)
    bodies=[]
    for name,offset,size in [('snow',0x2576,443),('staff',0x2804,2541)]:
        start=0x95f*16+offset;end=start+size
        a=target.program_image[start:end];b=candidate.program_image[start:end]
        tr=[r for r in relocs(target) if start<=r[0]*16+r[1]<end]
        cr=[r for r in relocs(candidate) if start<=r[0]*16+r[1]<end]
        bodies.append(dict(name=name,bytes=size,raw_equal=a==b,target_sha256=sha(a),candidate_sha256=sha(b),target_relocations=tr,candidate_relocations=cr,ordered_relocations_equal=tr==cr,relocation_membership_equal=Counter(tr)==Counter(cr)))
    runtime=[]
    for label,m in [('target',target),('candidate',candidate)]:
        observations=dict(snow=snow.matrix(m),frames=staff.frame_matrix(m),transitions=staff.transition_matrix(m),verdict=staff.verdict_matrix(m),staff=staff.staff_matrix(m))
        runtime.append(dict(label=label,observations=observations))
    equal=runtime[0]['observations']==runtime[1]['observations']
    result.update(kind='mainl-coherent-graphics-snow-staff-link',staff_bodies=bodies,staff_runtime=runtime,staff_runtime_equal=equal,maintained_contribution_bytes=3339,total_scoped_bytes=9483,source_progress_changed=False)
    result['diagnostic_checks_pass']=bool(result['diagnostic_checks_pass'] and all(r['raw_equal'] and r['relocation_membership_equal'] for r in bodies) and equal)
    return result
