"""Source-only maintained tiny-init recipe/verifier tests; no native execution."""
import hashlib, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
HERE = Path(__file__).resolve().parents[1]
ROOT = HERE if (HERE / 'config/targets.toml').is_file() else next(p for p in HERE.parents if (p / 'config/targets.toml').is_file())
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts')); sys.path.insert(0, str(HERE / 'scripts'))
import build_th03_zun_init as recipe
import verify_th03_zun_init_standalone as verifier
RETAINED = ROOT / '.analysis/toolchain/wineprefix/drive_c/ZC9467D4'

class SourceContract(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='unit-',dir=HERE)
        self.work=Path(self.temp.name)
        self.source=ROOT/recipe.SOURCE;self.epoch=self.source.stat().st_mtime_ns
    def tearDown(self):self.temp.cleanup()
    def test_two_exclusive_stages_same_declared_mtime(self):
        a,b=self.work/'a',self.work/'b'
        ga=recipe.stage(self.source,a,self.epoch);gb=recipe.stage(self.source,b,self.epoch)
        self.assertEqual((a/recipe.SOURCE).read_bytes(),(b/recipe.SOURCE).read_bytes())
        self.assertEqual((a/recipe.SOURCE).stat().st_mtime_ns,self.epoch)
        self.assertEqual((b/recipe.SOURCE).stat().st_mtime_ns,self.epoch)
        self.assertNotEqual((a/recipe.SOURCE).stat().st_ino,(b/recipe.SOURCE).stat().st_ino)
        self.assertEqual(hashlib.sha256((a/recipe.SOURCE).read_bytes()).hexdigest(),recipe.STAGED_SHA)
        self.assertEqual((a/'link.rsp').read_bytes(),recipe.RESPONSE)
        with self.assertRaises(FileExistsError):recipe.stage(self.source,a,self.epoch)
    def test_timestamp_is_not_fitted_afterward(self):
        with self.assertRaisesRegex(ValueError,'mtime'):recipe.stage(self.source,self.work/'bad',self.epoch+1)
        self.assertFalse((self.work/'bad').exists())
    def test_symlink_destination_rejected_without_overwrite(self):
        (self.work/'dest').symlink_to(self.work,target_is_directory=True)
        with self.assertRaises(FileExistsError):recipe.stage(self.source,self.work/'dest',self.epoch)
    def test_source_not_retained_binary_input(self):
        wrong=self.work/'wrong.asm';wrong.write_bytes(b'no target byte fallback\n')
        with self.assertRaisesRegex(ValueError,'source identity'):recipe.stage(wrong,self.work/'bad',wrong.stat().st_mtime_ns)
        self.assertFalse((self.work/'bad').exists())
    def test_exact_native_argv(self):
        asm,link=recipe.commands('/usr/bin/wine','/repo/_reference/ReC98/bin/msdos.exe')
        self.assertEqual(asm[1:], [r'C:\TASM50\BIN\TASM32.EXE','/m','/mx','/kh32768','/t',r'src\zun\init.asm,init.obj'])
        self.assertEqual(link[1:], ['/repo/_reference/ReC98/bin/msdos.exe','-e','-x','tlink','@link.rsp'])
        with self.assertRaises(ValueError):recipe.commands('wine','relative.exe')
    def test_fixed_two_phase_recipe_and_fail_stop(self):
        owner=self
        class Fake:
            native_count=0
            def __init__(self):
                self.root=owner.work;self.work=owner.work/'round';self.work.mkdir();self.inputs=[];self.calls=[]
                self.m=dict(source=recipe.SOURCE,wine='/wine',msdos_player='msdos',decoded_target='target')
                (self.root/'target').write_bytes(b'x'*0xb32)
            def consumed(self,label):self.calls.append(('guard',label))
            def native(self,label,argv,absent,required):
                self.native_count+=1;self.calls.append(('native',label))
                for n in required:(self.work/n).write_bytes(('mock-'+n).encode())
            def step(self,label,fn,seconds):return fn()
            def event(self,*unused):pass
        run=Fake()
        with patch.object(recipe,'parse_object',return_value={}),patch.object(recipe,'verify_outputs',return_value={'mock_only':True}):
            self.assertEqual(recipe.build_round(run),{'mock_only':True})
        self.assertEqual(run.calls,[('guard','before-assemble'),('native','assemble'),('guard','before-link'),('native','link')])
        self.assertEqual(run.native_count,2)
        # The same recipe stops before the second consumed guard/link.
        run.work.rename(run.root/'prior-mock-round')
        failed=Fake();primary=RuntimeError('assembly failed')
        def reject(label,argv,absent,required):
            failed.native_count+=1;failed.calls.append(('native',label));raise primary
        failed.native=reject
        with self.assertRaises(RuntimeError) as caught:recipe.build_round(failed)
        self.assertIs(caught.exception,primary)
        self.assertEqual(failed.calls,[('guard','before-assemble'),('native','assemble')])
class RetainedVerifierRegression(unittest.TestCase):
    """Existing files are read only as fixtures, never copied into a build round."""
    def setUp(self):
        self.obj=(RETAINED/'init.obj').read_bytes();self.com=(RETAINED/'init.com').read_bytes();self.map=(RETAINED/'init.map').read_bytes()
    def test_strict_contract_and_full_partition(self):
        proof=verifier.verify_outputs(self.obj,self.com,self.map,self.com)
        self.assertEqual((proof['procedure_count'],proof['code_bytes'],proof['data_bytes']),(9,607,783))
        self.assertEqual(len(proof['procedures']),9);self.assertTrue(proof['complete_partition']);self.assertFalse(proof['exact_acceptance'])
        fixups=verifier.parse_object(self.obj)['fixups']
        self.assertEqual(len(fixups),48);self.assertEqual(sum(f['fixdat']==0x14 for f in fixups),35);self.assertEqual(sum(f['fixdat']==0x54 for f in fixups),13)
    def test_no_map_public_or_empty_data_relaxation(self):
        obj=verifier.parse_object(self.obj)
        for bad in (self.map+b'unknown\r\n',self.map.replace(b'066E',b'0670'),self.map.replace(b'idle',b'xxxx',1),self.map.replace(b'Publics by Value',b'Publics by Name')):
            with self.assertRaises(ValueError):verifier.verify_map(bad,obj)
    def test_raw_output_not_normalized(self):
        for bad in (self.com+b'\x00',b'\x00'+self.com,self.com[:-1]+bytes([self.com[-1]^1])):
            with self.assertRaises(ValueError):verifier.verify_outputs(self.obj,bad,self.map,self.com)

class ColdMaterializations(unittest.TestCase):
    def test_independent_raw_pair_and_terminal_receipt(self):
        other=ROOT/'.analysis/toolchain/wineprefix/drive_c/ZCC3A129'
        for name in recipe.OUTPUTS:
            a,b=RETAINED/name,other/name
            self.assertNotEqual(a.stat().st_ino,b.stat().st_ino)
            self.assertEqual(a.read_bytes(),b.read_bytes())
        p=ROOT/'.analysis/zun-init-cold-continuation-output-20261021-v01/completion.json'
        raw=p.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'4fb3cf03ef57da9ae3da738f0f650da385b546abb3fff35975760d75449f70c8')
        result=json.loads(raw)
        self.assertTrue(result['complete']);self.assertEqual(result['errors'],[])
        self.assertTrue(result['owned_lock_release_complete'])
        self.assertEqual(result['original_factory_terminal'],'unknown')
        self.assertFalse(result['exact_acceptance']);self.assertFalse(result['wrapper_integration'])
        self.assertEqual(result['result']['independent_materializations'],2)
        self.assertEqual(result['result']['equality'],dict(raw_omf_equal=True,raw_com_equal=True,raw_map_equal=True,normalization=False))
    def test_omf_corruption_rejected(self):
        obj=bytearray((RETAINED/'init.obj').read_bytes());obj[-1]^=1
        with self.assertRaises(ValueError):verifier.parse_object(bytes(obj))

if __name__=='__main__':unittest.main(verbosity=2)
