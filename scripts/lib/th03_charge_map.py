"""Finite observed MAP edit contract; does not normalize arbitrary rows or ties."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
CONTRACT_SHA='d670c354729d27b266218f1cb45c84eefe1a0c1fbf95a7e483aa8e30c9aad95b'
def verify(baseline,candidate):
 raw=(HERE/'th03_charge_map_contract.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==CONTRACT_SHA
 c=json.loads(raw);assert hashlib.sha256(baseline).hexdigest()==c['baseline_sha256']
 lines=baseline.decode('ascii').splitlines(keepends=True);out=[];at=0
 for e in c['literal_changes']:
  i,j=e['old_start'],e['old_end'];assert at<=i<=j;assert lines[i:j]==e['old_lines'];out.extend(lines[at:i]);out.extend(e['new_lines']);at=j
 out.extend(lines[at:]);expected=''.join(out).encode('ascii');assert hashlib.sha256(expected).hexdigest()==c['candidate_sha256'];assert candidate==expected,'MAP outside finite literal transition differs'
 return {'literal_changes':len(c['literal_changes']),'candidate_sha256':c['candidate_sha256'],'generic_normalization':False}
