#!/usr/bin/env python3
"""Review five complete MAINL root helpers against the current native cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_root_helpers_layout import PROCEDURES,verify as layout
from lib.decoded_mainl_root_helpers_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/mainl-root-helpers-build.json'
INPUTS=(*sound.INPUTS,'scripts/review_th03_mainl_root_helpers_work.py',
    'scripts/lib/decoded_mainl_root_helpers_layout.py','scripts/lib/decoded_mainl_root_helpers_runtime.py',
    *tuple(sorted({'src/mainl/root_tail/'+p[5] for p in PROCEDURES})))
COUNTS=dict(keyclear=520,setcolor=776,off=264,rand=131080,compare=65624)

def need(v,m):
    if not v:raise ValueError('MAINL root helper review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}

def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],
          r['exhaustive_random_seed_WORD_lanes'],r['exhaustive_character_pairs'],r['ignored_stack_bytes'])
         ==(2,5,150,150,396528,65536,65536,0),'complete runtime / exhaustive input / physical memory dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
         ==[(0x1000,198264,COUNTS,150,6),(0x3000,198264,COUNTS,150,6)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'complete native paths, foreign SS and full high-half/flag witnesses')
    need(not r['physical_DOS_or_pixels_emulated'],'bounded DOS / hardware requests')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==26
        and c['actual_guest_instruction_mutations'] and not c['alignment_mutations_counted'],'twenty-six actual instruction mutations')
    l=scope['layout'];need(l['functions']==5 and l['code_bytes']==150 and len(l['ordered_native_fields'])==5
        and l['ordered_relocations']==[] and l['excluded_adjacent_NOPs']==[0xC5F,0xC65,0x2C2F]
        and not l['containing_producer_accepted'] and not l['whole_product_accepted'],'five whole root owners; adjacent layout excluded')

def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:rows.append([m.run(kind,**p) for kind,p in (
            ('rand',dict(random_seed=0xEBE3)),('rand',dict(random_seed=0xFFFFFFFF)),
            ('setcolor',dict(mode=0xFFC0,color=0xFF87,flags=0xED7,stack=0x80,ss=0x8000)),
            ('off',dict(flags=0x402)),('keyclear',dict(dos_status=0xFFFF,reply_seed=0)),
            ('compare',dict(strings=(b'\xFFaZ\0',b'\xFFAz\0'),flags=0xED7)),
            ('compare',dict(strings=(b'ABC\0',b'ABD\0'),pointers=((0x5000,0xFFFF),(0x6000,0xFFFE)))) )])
        finally:m.close()
    need(rows[0]==rows[1],'current raw arithmetic/string/port/DOS ABI smoke')
    return dict(images=2,cases_per_image=7,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-root-helpers-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-mainl-root-helpers-current-review-v1','complete helper report')
    need(r['implementation_sha256']==inputs(root),'current source / implementation binding')
    need(r['cold_report_sha256']==sha(cold_raw) and r['sound_review_sha256']==sha(sound.REPORT.read_bytes()),'current cold / sound report binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate,graph,files),'current full native root ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--current-cold',action='store_true',help='revalidate the existing source/SDK/recipe/output pair; rerun all new helper gates')
    o=p.parse_args()
    r=dict(schema='th03-mainl-root-helpers-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_sound_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    sound.current_scope(ROOT,work,target,candidate,raw,graph,files)
    r['cold_report_sha256']=sha(raw);r['sound_review_sha256']=sha(sound.REPORT.read_bytes())
    r['source_inventory_sha256']=sound.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),negative_controls=negative_controls(target))
    witness(r['scope']);need(r['implementation_sha256']==inputs(ROOT),'helper inputs changed during review')
    r['complete']=True;save()
    print('MAINL root helpers: five complete functions / 150 CODE bytes; native ownership and exhaustive runtime contracts pass',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
