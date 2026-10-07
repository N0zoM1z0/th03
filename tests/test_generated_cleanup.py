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


if __name__=='__main__':unittest.main()
