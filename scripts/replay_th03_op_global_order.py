#!/usr/bin/env python3
"""Replay actual object/link evidence only. No compiler, linker, registry mutation or acceptance publication."""
from pathlib import Path
import argparse,hashlib,json,sys,types
PROOF='config/op_global_order/proof.json'
PROOF_SHA='c3b0d366b546b00b90df459b0a3a70d82891ec53ecd4814cd2b47ac0b3e28eac'
def need(v,m):
 if not v:raise ValueError(m)
def read(root,q):
 n=q['path'];p=Path(n);need(not p.is_absolute() and '..' not in p.parts,'unsafe evidence path');p=Path(root)/p;need(not any(x.is_symlink() for x in (p,*p.parents)) and p.is_file(),'regular evidence');a=p.stat();b=p.read_bytes();z=p.stat();need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns),'unstable evidence');need(hashlib.sha256(b).hexdigest()==q['sha256'] and ('bytes' not in q or len(b)==q['bytes']),'evidence drift '+n);return b
def replay(root,files=None):
 root=Path(root);files=Path(files or root);raw=read(files,dict(path=PROOF,sha256=PROOF_SHA));p=json.loads(raw);need(p['schema']=='th03-op-global-order-observation-v1' and p['source_acceptance'] is False and p['exact_acceptance'] is False and p['new_authored_code_credit']==0,'scope inflation')
 for q in list(p['actual_receipts'].values())+list(p['actual_objects'].values())+list(p['parser_inputs'].values())+p['history']+[p['current_manifest'],p['current_report'],p['current_completion'],p['observed_exe'],p['observed_map']]:read(root,q)
 read(root,dict(path=p['dependency_manifest'],sha256=p['dependency_manifest_sha256']));read(files,p['source_stager']);read(files,p['source_config']);code=read(files,p['verifier']);sys.path.insert(0,str(root/'scripts'));v=types.ModuleType('op_global_order_observer');v.__file__=str(files/p['verifier']['path']);exec(compile(code,v.__file__,'exec'),v.__dict__);v.ROOT=root
 m=json.loads(read(root,p['current_manifest']));complete=json.loads(read(root,p['current_completion']));need(complete['complete'] and complete['owned_lock_released'] and not complete['errors'] and complete['native_invocations']==2 and complete['phases']==['assemble_suffix','link'],'actual suffix/link producer success')
 for phase in complete['phases']:
  started=json.loads(read(root,p['actual_receipts'][phase+'-started.json']));finished=json.loads(read(root,p['actual_receipts'][phase+'-finished.json']));transition=json.loads(read(root,p['actual_receipts'][phase+'-registry-transition.json']));need(started['argv']==m['native_argv'][phase] and finished['exit_code']==0 and not finished['timeout'] and not finished['cleanup_uncertain'] and finished['inventory_complete'] and finished['initial_inventory_complete'] and not finished['survivors'] and not finished['errors'] and not finished['poison'] and transition['ok'],'actual phase receipts')
 work=root/m['work'];prefix=v.verify_split_object(work/'obj/th03/op.obj','prefix');suffix=v.verify_split_object(work/'obj/th03/optail.obj','suffix');report=json.loads(json.dumps(v.verify(work,m)));need(report==json.loads(read(root,p['current_report'])),'replayed literal report differs');need(report['diagnostic_checks_pass'] and report['whole_target_ordered_equal'] and report['target_different_positions']==[],'literal607 target order');need(report['public_metadata_delta']==p['public_metadata_delta'],'exact observed metadata changes')
 candidate=v.parse_mz((work/'bin/th03/op.exe').read_bytes());target=v.parse_mz(v.pin(m['target']));diff=[i for i,(a,b) in enumerate(zip(candidate.program_image,target.program_image)) if a!=b];need(len(candidate.program_image)==len(target.program_image) and diff==[0xdd95] and candidate.program_image[0xdd95]==0 and target.program_image[0xdd95]==0x90,'known remaining unowned program byte')
 return dict(replay_pass=True,literal607_target_order=True,target_different_positions=[],whole_program_preserved=True,remaining_target_program_differences=diff,public_additions_per_section=7,idle_changes_per_section=21,prefix=prefix['sha256'],suffix=suffix['sha256'],native_invocations_now=0,source_acceptance=False,exact_acceptance=False,whole_product_ownership=False,new_authored_code_credit=0)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--files',type=Path);a=p.parse_args();print(json.dumps(replay(a.root,a.files),indent=2))
