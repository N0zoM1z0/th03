import contextlib
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import clean_generated as c


class CleanupProofControls(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.analysis=self.root/'.analysis';self.analysis.mkdir()
        self.evidence=self.root/'evidence.csv'
        self.evidence.write_text('location\n.analysis/ledger.log\n')
        self.patch=patch.multiple(c,ROOT=self.root,ANALYSIS=self.analysis,EVIDENCE=self.evidence,
                                PRESERVED_ANALYSIS_FILES={self.analysis/'target-import.json'},
                                PRESERVED_ANALYSIS_ROOTS={self.analysis/'targets'})
        self.patch.start();self.addCleanup(self.patch.stop)
    def put(self,p,text='keep'):
        path=self.root/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);return path
    def clean(self,dry=False):
        with contextlib.redirect_stdout(io.StringIO()):return c.clean_analysis(dry)
    def test_guarded_input_survives_and_unreferenced_sibling_is_removed(self):
        proof=self.put('.analysis/review.json',json.dumps({'inputs':{'.analysis/work/input.obj':'sha'}}))
        kept=self.put('.analysis/work/input.obj');junk=self.put('.analysis/work/junk.obj')
        self.assertEqual(self.clean(),4);self.assertTrue(proof.exists());self.assertTrue(kept.exists());self.assertFalse(junk.exists())
    def test_complete_receipt_tree_keeps_unlisted_archive_and_outputs(self):
        self.put('.analysis/cold/run/receipt.json','{}')
        archive=self.put('.analysis/cold/run/reference.tar');output=self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertEqual(self.clean(),0);self.assertTrue(archive.exists());self.assertTrue(output.exists())

    def prune_receipts(self,dry=False,extra=None,documented=None):
        with patch.object(c,'documented_analysis_paths',return_value=documented or set()),contextlib.redirect_stdout(io.StringIO()):
            return c.prune_unreferenced_receipts(dry,extra or set())

    def test_aggressive_prune_removes_unreferenced_receipt_tree(self):
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        output=self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertGreater(self.prune_receipts(),0)
        self.assertFalse(receipt.exists());self.assertFalse(output.exists())

    def test_aggressive_prune_keeps_ledger_receipt_tree(self):
        self.evidence.write_text('location\n.analysis/cold/run/receipt.json\n')
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        output=self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertEqual(self.prune_receipts(),0)
        self.assertTrue(receipt.exists());self.assertTrue(output.exists())

    def test_aggressive_prune_keeps_documented_receipt_tree(self):
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        output=self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertEqual(self.prune_receipts(documented={receipt}),0)
        self.assertTrue(receipt.exists());self.assertTrue(output.exists())

    def test_aggressive_prune_keeps_explicit_active_run(self):
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        output=self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertEqual(self.prune_receipts(extra={receipt.parent}),0)
        self.assertTrue(receipt.exists());self.assertTrue(output.exists())

    def test_aggressive_prune_dry_run_never_deletes_receipt(self):
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        self.put('.analysis/cold/run/source/obj/owner.obj')
        self.assertGreater(self.prune_receipts(dry=True),0)
        self.assertTrue(receipt.exists())

    def test_main_source_inputs_keep_transitive_cold_receipt(self):
        top = self.put('.analysis/current/receipt.json', json.dumps({
            'source_inputs': {'.analysis/prior/receipt.json': 'sha'},
        }))
        prior = self.put('.analysis/prior/receipt.json', json.dumps({
            'inputs': {'.analysis/required/image.exe': 'sha'},
        }))
        image = self.put('.analysis/required/image.exe')
        output = self.put('.analysis/prior/unlisted.obj')
        junk = self.put('.analysis/obsolete/receipt.json', '{}')
        self.prune_receipts(documented={top})
        self.clean()
        for path in (top, prior, image, output):
            self.assertTrue(path.exists())
        self.assertFalse(junk.exists())

    def test_source_inputs_keep_standalone_proof_and_guarded_cache(self):
        cache = self.put('scripts/__pycache__/required.pyc')
        report = self.put('.analysis/main.json', json.dumps({
            'source_inputs': {'scripts/__pycache__/required.pyc': 'sha'},
        }))
        self.clean()
        with patch.object(c, 'CACHE_ROOTS', []), contextlib.redirect_stdout(io.StringIO()):
            c.clean_caches(False)
        self.assertTrue(report.exists())
        self.assertTrue(cache.exists())

    def test_standalone_guarded_diagnostic_keeps_input_receipt_without_doc_link(self):
        report = self.put('.analysis/diagnostic.json', json.dumps({
            'source_inputs': {'.analysis/provider/receipt.json': 'sha'},
        }))
        provider = self.put('.analysis/provider/receipt.json', '{}')
        output = self.put('.analysis/provider/unlisted.exe')
        junk = self.put('.analysis/obsolete/receipt.json', '{}')
        self.prune_receipts()
        self.clean()
        for path in (report, provider, output):
            self.assertTrue(path.exists())
        self.assertFalse(junk.exists())

    def test_retained_parent_keeps_nested_receipt_and_report_dependencies(self):
        top = self.put('.analysis/current/receipt.json', '{}')
        nested = self.put('.analysis/current/nested/receipt.json', '{}')
        report = self.put('.analysis/current/report.json', json.dumps({
            'inputs': {'.analysis/provider/receipt.json': 'sha'},
        }))
        provider = self.put('.analysis/provider/receipt.json', '{}')
        output = self.put('.analysis/provider/source/input.obj')
        self.assertEqual(self.prune_receipts(documented={top}), 0)
        for path in (top, nested, report, provider, output):
            self.assertTrue(path.exists())

    def test_keep_analysis_protects_nonreceipt_active_tree_through_full_cli(self):
        active = self.put('.analysis/active/unrecorded.obj')
        child = self.put('.analysis/active/nested/receipt.json', '{}')
        junk = self.put('.analysis/obsolete/receipt.json', '{}')
        with patch.object(sys, 'argv', ['clean_generated.py', '--apply',
                '--prune-unreferenced-receipts', '--keep-analysis', '.analysis/active']), \
                patch.object(c, 'CACHE_ROOTS', []), \
                patch.object(c, 'documented_analysis_paths', return_value=set()), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(), 0)
        self.assertTrue(active.exists())
        self.assertTrue(child.exists())
        self.assertFalse(junk.exists())

    def test_keep_analysis_protects_standalone_file_in_conservative_cli(self):
        active = self.put('.analysis/active.obj')
        junk = self.put('.analysis/obsolete.obj')
        with patch.object(sys, 'argv', ['clean_generated.py', '--apply',
                '--keep-analysis', '.analysis/active.obj']), \
                patch.object(c, 'CACHE_ROOTS', []), \
                patch.object(c, 'documented_analysis_paths', return_value=set()), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(), 0)
        self.assertTrue(active.exists())
        self.assertFalse(junk.exists())

    def test_documented_symlink_alias_and_destination_survive(self):
        target = self.put('.analysis/real/report.json', '{}')
        alias = self.analysis / 'alias.json'
        alias.symlink_to(target)
        self.put('README.md', 'Current proof: .analysis/alias.json\n')
        with patch.object(c.subprocess, 'check_output', return_value=b'README.md\0'):
            self.clean()
        self.assertTrue(alias.is_symlink())
        self.assertTrue(target.exists())

    def test_aggressive_prune_accepts_hash_bound_text_with_json_name(self):
        output,row=self.factory_query('.analysis/functions.json')
        self.record_query(row)
        receipt=self.put('.analysis/cold/run/receipt.json','{}')
        self.put('.analysis/cold/run/source/obj/owner.obj')
        with patch.object(c,'documented_analysis_paths',return_value=set()),contextlib.redirect_stdout(io.StringIO()):
            self.assertGreater(c.prune_unreferenced_receipts(False,set()),0)
        self.assertTrue(output.exists());self.assertFalse(receipt.exists())

    def test_nested_guards_and_transitive_receipts_remain(self):
        self.put('.analysis/top.json',json.dumps({'observations':[{'inputs':{'.analysis/child.json':'sha'}}]}))
        child=self.put('.analysis/child.json',json.dumps({'inputs':{'.analysis/image.exe':'sha'}}));image=self.put('.analysis/image.exe')
        self.clean();self.assertTrue(child.exists());self.assertTrue(image.exists())
    def test_broken_receipt_stops_before_any_deletion(self):
        junk=self.put('.analysis/a-junk');self.put('.analysis/z/receipt.json','{bad')
        with self.assertRaisesRegex(ValueError,'receipt'):self.clean()
        self.assertTrue(junk.exists())
    def test_documented_nonreceipt_review_file_stays_live(self):
        """A tracked concrete JSON review must not be removed by cleanup."""
        report=self.put('.analysis/next-frontier/v3.json', '{"provisional":true}')
        junk=self.put('.analysis/next-frontier/superseded.json', '{"provisional":true}')
        expected=len(junk.read_bytes())
        with patch.object(c,'documented_analysis_paths',return_value={report}):
            self.assertEqual(self.clean(),expected)
        self.assertTrue(report.is_file())
        self.assertFalse(junk.exists())

    def test_documented_source_binary_path_survives_replay_cache_cleanup(self):
        """A real artifact referred to by tracked config pins that byte path."""
        exe=self.put('.analysis/cold/build/source/bin/game.exe','game code')
        temp=self.put('.analysis/cold/build/source/bin/other.exe','junk')
        with patch.object(c,'documented_analysis_paths',return_value={exe}):
            self.clean()
        self.assertTrue(exe.is_file())
        self.assertFalse(temp.exists())

    def test_dry_run_never_deletes(self):
        junk=self.put('.analysis/junk');self.assertEqual(self.clean(True),4);self.assertTrue(junk.exists())
    def test_ledger_and_private_state_still_survive(self):
        ledger=self.put('.analysis/ledger.log');target=self.put('.analysis/targets/op.exe');self.clean()
        self.assertTrue(ledger.exists());self.assertTrue(target.exists())
    def test_guarded_symlink_and_its_local_destination_survive(self):
        target=self.put('.analysis/real/input.obj');alias=self.analysis/'alias.obj';alias.symlink_to(target)
        self.put('.analysis/review.json',json.dumps({'inputs':{'.analysis/alias.obj':'sha'}}));self.clean()
        self.assertTrue(alias.is_symlink());self.assertTrue(target.exists())
    def test_guarded_missing_input_is_not_recreated(self):
        self.put('.analysis/review.json',json.dumps({'inputs':{'.analysis/missing.exe':'sha'}}));junk=self.put('.analysis/junk')
        self.clean();self.assertFalse(junk.exists());self.assertFalse((self.analysis/'missing.exe').exists())
    def test_cache_cleanup_respects_guarded_inputs_outside_analysis(self):
        cache=self.put('scripts/__pycache__/guarded.pyc')
        self.put('.analysis/review.json',json.dumps({'inputs':{'scripts/__pycache__/guarded.pyc':'sha'}}))
        with patch.object(c,'CACHE_ROOTS',[]),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.clean_caches(False),0)
        self.assertTrue(cache.exists())
    def test_broken_ledger_json_stops_before_deletion(self):
        self.evidence.write_text('location\n.analysis/retained.json\n')
        self.put('.analysis/retained.json','{bad');junk=self.put('.analysis/junk')
        with self.assertRaisesRegex(ValueError,'retained proof'):self.clean()
        self.assertTrue(junk.exists())
    def test_ledger_symlink_alias_and_destination_survive(self):
        target=self.put('.analysis/real/proof.log');alias=self.analysis/'alias.log';alias.symlink_to(target)
        self.evidence.write_text('location\n.analysis/alias.log\n');self.clean()
        self.assertTrue(alias.is_symlink());self.assertTrue(target.exists())

    def factory_query(self,location='.analysis/functions.json'):
        output=self.put(location,'address: 0x0001A40C\nname: FUN_196e_0d2c\n')
        row=dict(location=location,tool='Factory-native-same-process-attested-headless-Ghidra-query',
                 command=f'python3 scripts/factory_ghidra.py --artifact th03-main query {location} function 196E:0D2C',
                 output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
        return output,row
    def record_query(self,row):
        with self.evidence.open('w',newline='') as f:
            writer=csv.DictWriter(f,list(row));writer.writeheader();writer.writerow(row)
    def test_hash_bound_factory_text_json_name_is_retained(self):
        output,row=self.factory_query();self.record_query(row);junk=self.put('.analysis/junk')
        self.clean();self.assertTrue(output.exists());self.assertFalse(junk.exists())
    def test_changed_factory_text_stops_before_deletion(self):
        output,row=self.factory_query();self.record_query(row);output.write_text('changed')
        junk=self.put('.analysis/junk')
        with self.assertRaisesRegex(ValueError,'retained proof'):self.clean()
        self.assertTrue(junk.exists())
    def test_factory_text_requires_the_recorded_output_and_query_kind(self):
        output,row=self.factory_query();junk=self.put('.analysis/junk')
        for command in [row['command'].replace('function','decompile'),row['command'].replace('query .analysis/functions.json','query .analysis/other.json')]:
            with self.subTest(command=command):
                changed=dict(row,command=command);self.record_query(changed)
                with self.assertRaisesRegex(ValueError,'retained proof'):self.clean()
                self.assertTrue(junk.exists());self.assertTrue(output.exists())
    def test_factory_metadata_cannot_exempt_a_broken_cold_receipt(self):
        output,row=self.factory_query('.analysis/cold/receipt.json');self.record_query(row)
        junk=self.put('.analysis/junk')
        with self.assertRaisesRegex(ValueError,'retained proof'):self.clean()
        self.assertTrue(output.exists());self.assertTrue(junk.exists())


class CleanupCacheCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.analysis = self.root / '.analysis'
        self.analysis.mkdir()
        self.output = self.analysis / 'unreferenced.tmp'
        self.output.write_text('keep analysis')
        self.cache = self.root / 'scripts/__pycache__/stale.pyc'
        self.cache.parent.mkdir(parents=True)
        self.cache.write_bytes(b'cache')
        self.standard = self.root / '.cache/stale'
        self.standard.parent.mkdir()
        self.standard.write_text('cache')
        (self.root / 'evidence.csv').write_text('location\n')
        self.patch = patch.multiple(c, ROOT=self.root, ANALYSIS=self.analysis,
                                   EVIDENCE=self.root / 'evidence.csv',
                                   CACHE_ROOTS=[self.root / '.cache'])
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def invoke(self, *args):
        with patch.object(sys, 'argv', ['clean_generated.py', '--caches-only', *args]), \
                patch.object(c, 'documented_analysis_paths', return_value=set()), \
                contextlib.redirect_stdout(io.StringIO()):
            return c.main()

    def test_cache_apply_preserves_even_unreferenced_analysis(self):
        self.assertEqual(self.invoke('--apply'), 0)
        self.assertEqual(self.output.read_text(), 'keep analysis')
        self.assertFalse(self.cache.exists())
        self.assertFalse(self.standard.exists())

    def test_cache_preview_does_not_delete_anything(self):
        self.assertEqual(self.invoke(), 0)
        self.assertTrue(self.output.exists())
        self.assertTrue(self.cache.exists())
        self.assertTrue(self.standard.exists())

    def test_conflicting_analysis_prune_is_rejected_before_deletion(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            self.invoke('--apply', '--prune-unreferenced-receipts')
        self.assertEqual(error.exception.code, 2)
        self.assertTrue(self.output.exists())
        self.assertTrue(self.cache.exists())
        self.assertTrue(self.standard.exists())


if __name__ == '__main__':
    unittest.main()
