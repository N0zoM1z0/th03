import contextlib
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


if __name__=='__main__':unittest.main()
