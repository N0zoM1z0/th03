"""Read-only evidence replay; never executes native tools or diagnostic code."""
from pathlib import Path
import argparse, hashlib, json, sys
sys.dont_write_bytecode=True

def replay(root, proof):
 root=Path(root).resolve(); p=json.loads(Path(proof).read_text())
 assert p['schema']=='mainl-main-negative-controls-v1'
 assert all(p[k] is False for k in ('exact_acceptance','product_source_credit','progress_changed'))
 assert p['native_replay_invocations']==0
 for name,digest in p['pins'].items():
  q=root/name
  assert not q.is_symlink() and q.resolve().is_relative_to(root)
  assert hashlib.sha256(q.read_bytes()).hexdigest()==digest, name
 expected={'MRC06':2462,'MHC01':67,'MHR01':63,'MTR01':2456}
 rejected={'MRA01':b'Undefined symbol \'large\'','MPL01':b'Undefined symbol \'L\'','MPD01':b'Invalid combination of opcode and operands'}
 bycase={c['case']:c for c in p['cases']}
 assert set(bycase)==set(expected)|set(rejected)
 for tag,c in bycase.items():
  out=root/c['output'];done=json.loads((out/'completion.json').read_text())
  assert done['native_invocations']==1 and done['owned_lock_released'] and done['exact_acceptance'] is False
  if tag in rejected:
   assert not done['complete'] and rejected[tag].lower() in (out/'compile.log').read_bytes().lower()
   assert not (root/c['work']/c['object']).exists()
  else:
   a=json.loads((out/'linked-verification.json').read_text())
   assert done['complete'] and not done['errors'] and a['diagnostic_checks_pass'] and not a['hypothesis_checks_pass']
   assert a.get('candidate_code_bytes',a.get('code_bytes'))==expected[tag]
   if tag=='MTR01':
    assert len(a['non_fixup_difference_offsets'])==344
    assert all(not b['non_fixup_difference_offsets'] for b in a['body_bands'] if b['name']!='main')
    assert all(a['public_checks'].values()) and not a['ordered_far_sites_equal']
   if tag in ('MHC01','MHR01'):
    assert a['execl_instruction_offsets']==([25] if tag=='MHC01' else [53])
 sys.path.insert(0,str(root/'scripts'))
 from lib.omf import parse_omf
 c=bycase['MTR01'];code=bytearray(2456);covered=bytearray(2456)
 for rec in parse_omf((root/c['work']/c['object']).read_bytes()):
  if rec.name=='LEDATA' and rec.data[0]==1:
   off=int.from_bytes(rec.data[1:3],'little');data=rec.data[3:]
   assert off+len(data)<=len(code) and not any(covered[off:off+len(data)])
   code[off:off+len(data)]=data;covered[off:off+len(data)]=b'\1'*len(data)
 assert all(covered)
 main=code[1930:];assert main[9:11]==bytes.fromhex('7401')
 destination=11+int.from_bytes(main[10:11],'little',signed=True)
 assert destination==12 and main[11]==0x1e and main[destination]==0x68
 assert main[524:526]==bytes.fromhex('c9cb')
 assert p['critical_mtr01']==dict(branch_main_offset=9,bytes='7401',decoded_destination=12,intended_final_return=524,destination_skips_push_ds=True)
 return dict(passed=True,pins=len(p['pins']),negative_cases=len(bycase),native_invocations=0,critical_wrong_short_branch_confirmed=True,exact_acceptance=False,progress_changed=False)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--proof',type=Path);args=parser.parse_args()
 print(json.dumps(replay(args.root,args.proof or args.root/'config/mainl_main_negative_controls/proof.json'),indent=2))
