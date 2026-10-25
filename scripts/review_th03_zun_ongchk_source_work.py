#!/usr/bin/env python3
"""Review ONGCHK's native source candidate without granting exact acceptance."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import review_th03_zun_directory_work as directory
from review_th03_zun_format_work import images
import review_th03_ongchk as behavior
import build_th03_zun_work as build
from lib.zun_ongchk_source import SOURCE,verify_outputs
from lib.zun import parse_launcher

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/zun-ongchk-source-build.json'
INPUTS=(*directory.INPUTS,'scripts/review_th03_zun_ongchk_source_work.py',
    'scripts/lib/zun_ongchk_source.py','scripts/review_th03_ongchk.py',SOURCE)

def need(v,m):
    if not v:raise ValueError('ONGCHK source candidate review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs():return {n:sha((ROOT/n).read_bytes()) for n in INPUTS}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--current-cold',action='store_true',help='revalidate the complete current source/SDK/recipe/output pair; rerun ONGCHK candidate checks')
    o=p.parse_args()
    r=dict(schema='th03-zun-ongchk-source-candidate-review-v1',complete=False,implementation_sha256=inputs(),
        provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,source_presence_only=True,
        exact_acceptance=False,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_directory_work.py')],cwd=ROOT,check=True)
    work,_,_,_,files,maintained,cold_raw=images(ROOT);cold=json.loads(cold_raw)
    need(cold['consumed_runtime_sha256']==build.runtime_inventory()
         and cold['consumed_sdk_sha256']==build.sdk_inventory(),'current consumed runtime and SDK identities')
    target=(work/'product/zun.target.com').read_bytes();candidate=(work/'product/zun.com').read_bytes()
    directory.current_scope(ROOT,work,target,candidate,files,maintained,cold_raw)
    need('libs/kaja/ongchk.com' not in files and SOURCE in maintained
         and [v['path'] for v in cold['source_context']['vendor_inputs']]==['bin/masters.lib'],
         'no ONGCHK binary seed in complete source graph')
    need(files['ongchk/ongchk.asm']==maintained[SOURCE].replace(b'\n',b'\r\n')
         and maintained[SOURCE]==(ROOT/SOURCE).read_bytes(),'actual maintained ASCII/LF source transport')
    child=parse_launcher(target,223)['payloads'][0];at,size=child['decoded_file_offset'],child['size']
    target_child=target[at:at+size];candidate_child=(work/'ongchk/ongchk.com').read_bytes()
    native=verify_outputs(*[(work/('ongchk/ongchk.'+ext)).read_bytes() for ext in ('obj','com','map')],target_child)
    need(native==cold['ongchk_source_candidate'],'cold native source/BSS evidence')
    structure=behavior.decode(target_child);need(structure==behavior.decode(candidate_child),'complete direct code/data/edge partition')
    results=[]
    for image in (target_child,candidate_child):
        terminal,stalls=behavior.runtime_matrix(image)
        need(len(terminal)==30 and len(stalls)==4,'thirty terminal scenarios and four distinct nonterminal polling cases')
        results.append(dict(terminal=terminal,stalls=stalls))
    need(results[0]==results[1],'current target/native behavior observations agree')
    r.update(cold_report_sha256=sha(cold_raw),directory_review_sha256=sha(directory.REPORT.read_bytes()),
        source_inventory_sha256=behavior.sha(json.dumps(cold['source_sha256'],sort_keys=True).encode()),
        native=native,structure=structure,
        constructed_runtime=dict(images=2,terminal_cases_per_image=30,nonterminal_polling_cases_per_image=4,
            trace_sha256=sha(json.dumps(results[0],sort_keys=True).encode()),observations=results[0],
            physical_devices_emulated=False,full_register_flag_store_memory_contract=False,
            instruction_coverage_proved=False,scoped_exact_owners_added=0))
    need(r['implementation_sha256']==inputs(),'candidate inputs changed during review')
    r['complete']=True;save()
    print('ONGCHK native source candidate: 892 CODE + 34 DATA + 42 BSS; all 926 file bytes and constructed device scenarios pass; exact acceptance remains open')
    return 0
if __name__=='__main__':raise SystemExit(main())
