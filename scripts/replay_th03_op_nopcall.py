"""Read-only actual original-call producer checkpoint; no native or acceptance."""
from pathlib import Path
import json,hashlib,importlib.util
PROOF_SHA='f2143fdb4d4677cccfb5394c1287255b598e7cabf706953e6fd1757027526122'
def replay(root,files=None):
 root=Path(root);files=Path(files) if files is not None else root;p=files/'config/op_nopcall/proof.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==PROOF_SHA;p=json.loads(raw)
 for k in ['offline_audit','offline_proof','corrected_report','original_completion']:assert hashlib.sha256((root/p[k]['path']).read_bytes()).hexdigest()==p[k]['sha256']
 path=root/p['offline_audit']['path'];s=importlib.util.spec_from_file_location('maintained_nopcall_audit',path);a=importlib.util.module_from_spec(s);s.loader.exec_module(a);return a.replay()
if __name__=='__main__':print(json.dumps(replay(Path(__file__).resolve().parents[1]),indent=2))
