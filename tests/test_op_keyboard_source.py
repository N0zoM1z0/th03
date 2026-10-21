"""OP scanner source/receipt guards; never execute native tools or a runtime model."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
stage = load('stage_th03_op_keyboard')
replay = load('replay_th03_op_keyboard')

class StageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'
        for name in stage.INPUTS:
            dest = self.source / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)

    def test_repeatable_source_only_stage(self):
        with patch('subprocess.Popen', side_effect=AssertionError('native execution forbidden')), patch('os.system', side_effect=AssertionError('shell forbidden')):
            a = stage.stage(self.source, self.base / 'a')
            b = stage.stage(self.source, self.base / 'b')
        self.assertEqual(a, b)
        self.assertEqual(len(a['files']), 7)
        self.assertEqual((a['scanner_bytes'], a['carrier_context_bytes'], a['nop_source_credit'], a['compiler_invocations']), (417, 418, 0, 0))
        self.assertIs(a['source_acceptance'], False)
        self.assertIs(a['exact_acceptance'], False)
        for name in (*a['files'], 'source_inventory.json'):
            self.assertEqual((self.base/'a'/name).read_bytes(), (self.base/'b'/name).read_bytes())
        self.assertEqual((self.base/'a/th03/input_s.cpp').read_text(), '#include "th03/hardware/input_s.cpp"\n')
        self.assertEqual((self.base/'a/th03/hardware/input_s.cpp').read_text(), '#include "src/op/hardware/input_sense.cpp"\n')

    def test_existing_output_untouched(self):
        out = self.base / 'out'; out.mkdir(); (out/'sentinel').write_text('keep')
        with self.assertRaises(ValueError): stage.stage(self.source, out)
        self.assertEqual(list(out.iterdir()), [out/'sentinel'])
        self.assertEqual((out/'sentinel').read_text(), 'keep')

    def rejected(self):
        with self.assertRaises(ValueError): stage.stage(self.source, self.base/'out')
        self.assertFalse((self.base/'out').exists())

    def test_owner_mutation(self):
        p = self.source/stage.OWNER; p.write_bytes(p.read_bytes()+b'// changed\n'); self.rejected()

    def test_original_nop_removal(self):
        p = self.source/stage.OWNER; old=p.read_bytes(); new=old.replace(b'#pragma codestring "\\x90"\n',b'')
        self.assertNotEqual(old,new); p.write_bytes(new); self.rejected()

    def test_original_nop_replacement(self):
        p=self.source/stage.OWNER; old=p.read_bytes(); new=old.replace(b'\\x90',b'\\x91')
        self.assertNotEqual(old,new); p.write_bytes(new); self.rejected()

    def test_every_forwarding_header_mutation(self):
        for name in stage.INPUTS:
            if name==stage.OWNER: continue
            with self.subTest(name=name):
                p=self.source/name; old=p.read_bytes(); p.write_text('#include "unreviewed.hpp"\n')
                self.rejected(); p.write_bytes(old)

    def test_symlink_input(self):
        p=self.source/stage.OWNER; p.unlink(); p.symlink_to((ROOT/stage.OWNER).resolve()); self.rejected()

    def test_symlink_output_parent(self):
        link=self.base/'linked'; link.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError): stage.stage(self.source,link/'out')

    def test_missing_input(self):
        (self.source/stage.INPUTS[0]).unlink()
        with self.assertRaises(FileNotFoundError): stage.stage(self.source,self.base/'out')
        self.assertFalse((self.base/'out').exists())

class ProofTests(unittest.TestCase):
    def setUp(self): self.p=json.loads((ROOT/'config/op_keyboard/proof.json').read_text())
    def test_valid(self): replay.validate_proof(self.p)
    def test_flags(self):
        for key in replay.CREDIT_FLAGS:
            for value in (True, 0, None):
                with self.subTest(key=key,value=value):
                    q=copy.deepcopy(self.p); q[key]=value
                    with self.assertRaises(ValueError): replay.validate_proof(q)
    def test_counts(self):
        for key in ('native_phases','scanner_bytes','carrier_context_bytes','runtime_images','runtime_calls'):
            with self.subTest(key=key):
                q=copy.deepcopy(self.p); q[key]+=1
                with self.assertRaises(ValueError): replay.validate_proof(q)
    def test_duplicate_pins(self):
        self.p['pins'].append(copy.deepcopy(self.p['pins'][0]))
        with self.assertRaises(ValueError): replay.validate_proof(self.p)
    def test_recipe_identities(self):
        for key in ('manifest_sha256','verifier_sha256','schema'):
            with self.subTest(key=key):
                q=copy.deepcopy(self.p); q[key]='0'*64
                with self.assertRaises(ValueError): replay.validate_proof(q)
    def test_source_closure(self):
        self.p['maintained_sources'].pop(next(iter(self.p['maintained_sources'])))
        with self.assertRaises(ValueError): replay.validate_proof(self.p)

class PhaseTests(unittest.TestCase):
    def setUp(self):
        self.env={'environment':{'DISPLAY':'','WAYLAND_DISPLAY':'','TZ':'UTC'},'cpu':[0],'nice':10}
        self.m={'native_argv':{'compile':['wine','tcc'],'link':['wine','tlink']},'work':'.analysis/toolchain/wineprefix/drive_c/OPKEY01'}
        self.s={'argv':['wine','tcc'],'cwd':self.m['work'],'environment':copy.deepcopy(self.env['environment']),'wait_seconds':90,'cleanup_seconds':15}
        self.f={'exit_code':0,'timeout':False,'cleanup_uncertain':False,'poison':False,'initial_inventory_complete':True,'inventory_complete':True,'survivors':[],'errors':[]}
    def check(self): replay.validate_phase('compile',self.s,self.f,self.m,self.env)
    def test_valid(self): self.check()
    def test_actual_argv(self):
        self.s['argv'].append('-changed')
        with self.assertRaises(ValueError): self.check()
    def test_cleanup_failures(self):
        for key,value in [('exit_code',False),('exit_code',1),('timeout',True),('cleanup_uncertain',True),('poison',True),('inventory_complete',False),('initial_inventory_complete',False),('survivors',[123]),('errors',['failure'])]:
            with self.subTest(key=key,value=value):
                old=copy.deepcopy(self.f); self.f[key]=value
                with self.assertRaises(ValueError): self.check()
                self.f=old
    def test_headless_environment(self):
        self.s['environment']['DISPLAY']=self.env['environment']['DISPLAY']=':0'
        with self.assertRaises(ValueError): self.check()
    def test_bounds(self):
        self.s['wait_seconds']=91
        with self.assertRaises(ValueError): self.check()

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        # Synthetic retained report tests validation, not game behavior or exactness.
        coverage=dict(positions=278,complete=True,invocations=268,returns=264,prefixes=4)
        rows=[dict(terminal=i<264,visited=list(range(278)) if i==0 else [],physical_outside_stack_checked=True,unchanged_outside_state_checked=True,states=[0]) for i in range(268)]
        self.r=dict(diagnostic_checks_pass=True,runtime_run=True,source_acceptance=False,exact_acceptance=False,maintained_cohort_preserved=False,runtime=dict(target_coverage=copy.deepcopy(coverage),candidate_coverage=copy.deepcopy(coverage),semantic_equal=True,target_rows=rows,candidate_rows=copy.deepcopy(rows)))
    def test_valid(self): replay.validate_runtime(self.r)
    def test_changed_stats(self):
        for key in ('positions','invocations','returns','prefixes'):
            with self.subTest(key=key):
                q=copy.deepcopy(self.r);q['runtime']['candidate_coverage'][key]+=1
                with self.assertRaises(ValueError): replay.validate_runtime(q)
    def test_changed_trace(self):
        self.r['runtime']['candidate_rows'][0]['states']=[1]
        with self.assertRaises(ValueError): replay.validate_runtime(self.r)
    def test_missing_row(self):
        self.r['runtime']['candidate_rows'].pop()
        with self.assertRaises(ValueError): replay.validate_runtime(self.r)
    def test_false_memory_checks_even_when_both_traces_match(self):
        for kind in ('target_rows','candidate_rows'): self.r['runtime'][kind][0]['physical_outside_stack_checked']=False
        with self.assertRaises(ValueError): replay.validate_runtime(self.r)
    def test_false_semantic_verdict(self):
        self.r['runtime']['semantic_equal']=False
        with self.assertRaises(ValueError): replay.validate_runtime(self.r)

if __name__=='__main__': unittest.main()
