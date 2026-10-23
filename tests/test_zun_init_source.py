"""Static evidence only; no compiler, emulator, native runtime or build calls."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/th03-diet/sol-diet-restoration-20261006-b/zun.com').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

from pathlib import Path
import hashlib, json, re, struct, sys, tomllib, unittest, subprocess, tempfile
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/"config/targets.toml").is_file())
CANDIDATE=HERE.parent if (HERE.parent/"src/zun/init.asm").is_file() else ROOT
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(CANDIDATE/'scripts'))
from stage_th03_zun_init import stage_bytes
from review_th03_zun_init import decode
from lib.zun import parse_launcher
from lib.targets import load_target_manifest,find_artifact,read_verified_artifact
sha=lambda b:hashlib.sha256(b).hexdigest()
TOKEN=re.compile(r"'[^']*'|[A-Za-z_@][A-Za-z_0-9@]*|[^\s]")
def strip_comment(line):
    quote = None
    for index, char in enumerate(line):
        if char in ("'", '"'):
            if quote is None: quote = char
            elif quote == char: quote = None
        elif char == ';' and quote is None:
            return line[:index]
    return line

def tokens(text, inverse=None):
    inverse=inverse or {}
    result=[]
    for line in text.splitlines():
        line=strip_comment(line)
        result.append([inverse.get(t,t) for t in TOKEN.findall(line)])
    return [r for r in result if r]

def data_regions(text):
    regions=[[],[]]; region=None
    for line in text.splitlines():
        line=strip_comment(line).strip()
        if line.startswith('ZUNP ' ) or re.match(r'ZUNP\s',line):region=0
        if re.match(r'aIntvectorSetPr\s',line):region=1
        m=re.fullmatch(r'(?:(\S+)\s+)?(db|dw|dd)\s+(.+)',line)
        if region is not None and m:regions[region].append(m.groups())
        elif region is not None and line and not line.startswith(';'):region=None
    symbols={}; output=[]
    for rows,base in zip(regions,[0x23d,0x535]):
        offset=base
        for name,kind,expr in rows:
            if name:symbols[name]=offset
            for token in re.findall(r"'[^']*'|[^,]+",expr):
                token=token.strip(); offset+=(len(token[1:-1].encode('shift_jis')) if token.startswith("'") and kind=='db' else {'db':1,'dw':2,'dd':4}[kind])
        data=bytearray()
        for name,kind,expr in rows:
            for token in re.findall(r"'[^']*'|[^,]+",expr):
                token=token.strip(); size={'db':1,'dw':2,'dd':4}[kind]
                if token.startswith("'"):
                    raw=token[1:-1].encode('shift_jis'); data.extend(raw if kind=='db' else raw[::-1]);continue
                n=symbols[token[7:]] if token.startswith('offset ') else int(token[:-1],16) if token.lower().endswith('h') else int(token)
                data.extend(n.to_bytes(size,'little'))
        output.append(bytes(data))
    return output

class StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(CANDIDATE/'src/zun/init.asm').read_bytes();cls.staged=stage_bytes(cls.source)
        cls.reference=(ROOT/'_reference/ReC98/th02_zuninit.asm').read_bytes()
        cls.lf=cls.reference.replace(b'\r\n',b'\n')
        cls.mapping=json.loads((CANDIDATE/'config/th03_zun_init_labels.json').read_text())
        config=tomllib.loads((ROOT/'config/th03_zun_launcher.toml').read_text())
        cls.decoded=(ROOT/config['decoded_path']).read_bytes()
        cls.target=cls.decoded[0x5c4:0xb32]
    def test_reference_lineage(self):
        self.assertEqual(sha(self.reference),'f5506af2546a2fb66fb51b1ac7e2e468b83de9f1d1d205007f33859fcdd7a999')
        self.assertEqual(sha(self.lf),'72281210345c697384157bb46216a0f313cf99893b6b4aa21026481462fa93e5')
        self.assertNotIn(b'\r',self.lf);self.assertEqual(self.lf.replace(b'\n',b'\r\n'),self.reference)
    def test_complete_tokens_and_directives(self):
        self.assertEqual(tokens(self.lf.decode('shift_jis')),tokens(self.source.decode(),{v:k for k,v in self.mapping.items()}))
        self.assertEqual(len(re.findall(r'\bproc (?:near|far)',self.source.decode())),9)
    def test_encoding_roundtrip(self):
        self.assertEqual(self.staged.decode('shift_jis').replace('\r\n','\n').encode(),self.source)
        self.assertIn('\u301c',self.source.decode());self.assertIn(b'\x81\x60',self.staged)
        self.assertNotIn(b'\n',self.staged.replace(b'\r\n',b''))
    def test_reject_bad_encoding(self):
        for invalid in [b'bad\r\n',b'bad\r',b'\xff\n','\ufffd\n'.encode(),'\ufeffx\n'.encode(),'\U0001f600\n'.encode(),'\uff5e\n'.encode(),'\u00a5\n'.encode(),b'missing newline']:
            with self.assertRaises((ValueError,UnicodeError)):stage_bytes(invalid)
    def test_data_matches_target(self):
        original=data_regions(self.lf.decode('shift_jis'))
        mapped=self.source.decode()
        for new,old in sorted(((v,k) for k,v in self.mapping.items()),key=lambda x:-len(x[0])):
            mapped=re.sub(r'(?<![\w@])'+re.escape(new)+r'(?![\w@])',old,mapped)
        self.assertEqual(data_regions(mapped),original)
        self.assertEqual([len(x) for x in original],[470,313])
        self.assertEqual(original[0],self.target[0x13d:0x313])
        self.assertEqual(original[1],self.target[0x435:])
        self.assertEqual(original[0][:4],bytes.fromhex('55 5a 50 4e'))
    def test_target_lineage_boundaries(self):
        stored=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-zun'))
        self.assertEqual(sha(stored),'5896bbd673aeb10f0df9c1e34716c64fda83655a788ae1ac0fcf58e3616add27')
        self.assertEqual(sha(self.decoded),'83b034a59fabfd0c4dd48e44a4be5287ac1ea6ea0c0e9677311071113eff9e26')
        self.assertEqual(sha(self.target),'27fe52738878c1fa267c5dc82b0d70957d72dca5a6da375620a74d163b61e2d8')
        p=parse_launcher(self.decoded,223)['payloads'][1]
        self.assertEqual((p['name'],p['decoded_file_offset'],p['runtime_start'],p['size']),('-2',0x5c4,0x6c4,1390))
        rows=decode(self.target);self.assertEqual(sum(r['size'] for r in rows),607)
        self.assertEqual(self.target[0x42e:0x430],b'\xeb\x00')
        coverage=set()
        for r in rows:
            for n in range(r['start']-0x100,r['start']-0x100+r['size']):self.assertNotIn(n,coverage);coverage.add(n)
        for lo,hi in [(0x13d,0x313),(0x435,0x56e)]:
            for n in range(lo,hi):self.assertNotIn(n,coverage);coverage.add(n)
        self.assertEqual(coverage,set(range(1390)))
    def test_label_bijection_and_pins(self):
        self.assertEqual(len(self.mapping),59)
        self.assertEqual(len(set(self.mapping.values())),59)
        self.assertEqual(sha(self.source),'078525c35dfa4b499feb661980733964e16fa5654e8403ee55b0de221e828dc2')
        self.assertEqual(sha(self.staged),'6f35dcba455a9d9ab9bb9545e55141da7ca25186749df6749d8ac4c3c43a1e55')
        self.assertEqual(sha((CANDIDATE/'scripts/stage_th03_zun_init.py').read_bytes()),'79e5f5273b7366828493025b44ddd30b8ed77532c4e651d633e662394cb9d0c9')
        self.assertEqual(sha((CANDIDATE/'config/th03_zun_init_labels.json').read_bytes()),'8040d0afbad767dc06d2831d27e97dab5c416a50b6c2ad123c735252b5aed6a6')
    def test_quote_aware_comments(self):
        self.assertEqual(strip_comment("db 'a;b';comment"),"db 'a;b'")
        self.assertEqual(strip_comment('db "a;b";comment'),'db "a;b"')
        self.assertNotEqual(tokens("db 'a;b'"),tokens("db 'a;c'"))
    def test_exclusive_stage_cli(self):
        with tempfile.TemporaryDirectory(prefix='stage-cli-',dir=HERE) as tmp:
            destination=Path(tmp)/'init.asm'
            args=[sys.executable,str(CANDIDATE/'scripts/stage_th03_zun_init.py'),str(CANDIDATE/'src/zun/init.asm'),str(destination)]
            first=subprocess.run(args,capture_output=True,text=True,check=False)
            self.assertEqual(first.returncode,0,first.stderr)
            self.assertEqual(destination.read_bytes(),self.staged)
            second=subprocess.run(args,capture_output=True,text=True,check=False)
            self.assertNotEqual(second.returncode,0)
            self.assertIn('FileExistsError',second.stderr)
            self.assertEqual(destination.read_bytes(),self.staged)
if __name__=='__main__':unittest.main(verbosity=2)
