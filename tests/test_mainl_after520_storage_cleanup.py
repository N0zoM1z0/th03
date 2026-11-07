"""After520 storage guard: preserve the entire latest source-bound native DAG."""
import json,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import cleanup_mainl_after520_handoff as cleanup
from cleanup_mainl_after439_handoff import verify_active_hashes

class ProtectedAfter520NativeEvidence(unittest.TestCase):
    """Historical evidence is inspectable; old apply guard remains closed."""
    @classmethod
    def setUpClass(cls):
        # The historical deletion guard MUST refuse today's after521+
        # checkout. Read-only inspection of that frozen after520 graph
        # is allowed here, but NEVER use this mock in deletion/apply.
        with patch.object(cleanup,'guard',return_value=None):
            cls.graph=cleanup.layers()
        cls.protected=cleanup.protected_paths(cls.graph)
    def test_exact_live_258_stage_source_dag_and_both_native_rounds(self):
        self.assertEqual(len(self.graph),258)
        self.assertEqual(len(set(self.graph)),258)
        self.assertEqual(self.graph[0],('after62','sprintf-calloc-puts-ctime'))
        self.assertEqual(self.graph[-1],cleanup.CURRENT)
        self.assertEqual(len(self.protected),5760)
        self.assertTrue(all(p.is_file() and not p.is_symlink() for p in self.protected))
        for suffix in ('round1-linked.exe','round2-linked.exe',
                       'round1-newcrt.lib','round2-newcrt.lib',
                       'round1-linked.map','round2-linked.map'):
            self.assertTrue(any('after520' in p.name and p.name.endswith(suffix)
                                for p in self.protected),suffix)
    def test_guard_fails_closed_on_newer_source_stage_and_changed_receipts(self):
        with self.assertRaisesRegex(ValueError,'newer source stage exists'):
            cleanup.guard()
        with patch.object(cleanup,'CURRENT_SHA256','0'*64):
            with self.assertRaisesRegex(ValueError,'after520 root'):
                cleanup.guard()
        with patch.object(cleanup,'HISTORICAL_AFTER439_SHA256','0'*64):
            with self.assertRaisesRegex(ValueError,'historical source-root'):
                cleanup.guard()
    def test_exact_superseded_alternative_not_active_or_unresolved(self):
        candidates=cleanup.selected_paths(self.graph,self.protected)
        self.assertFalse(set(candidates)&self.protected)
        self.assertTrue(all(p.name.startswith('after506-ios-iword-usersize-array-slot-boss-')
                            for p in candidates))
        self.assertIn(len(candidates),(0,15))
        self.assertIn(('after506','dos-creat-exitopen-close-callback-boss'),self.graph)
        self.assertIn(('after507','ios-iword-usersize-array-slot-boss'),self.graph)
        for name in ('mainl-after506-dos-creat-exitopen-close-callback-boss-build.json',
                     'mainl-after507-ios-iword-usersize-array-slot-boss-build.json',
                     'mainl-after506-ios-iword-usersize-array-slot-boss-build.json'):
            self.assertTrue((cleanup.WORK/name).is_file())
        self.assertTrue((ROOT/'docs/MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md').is_file())
    def test_audited_deletion_manifest_is_not_silent(self):
        if not cleanup.MANIFEST.is_file():
            self.assertEqual(len(cleanup.selected_paths(self.graph,self.protected)),15)
            return
        audit=json.loads(cleanup.MANIFEST.read_text())
        self.assertEqual(audit['status'],'applied')
        self.assertEqual(audit['root_sha256'],cleanup.CURRENT_SHA256)
        self.assertEqual(audit['protected_files'],5760)
        self.assertEqual(audit['deleted_files'],15)
        self.assertEqual(audit['retired_mode'],list(cleanup.RETIRED))
        self.assertEqual(len(audit['entries']),15)
        # Real Borland/TASM assemble logs can be exactly zero bytes/blocks.
        self.assertTrue(all(len(x['sha256'])==64 and x['bytes']>=0
                            and x['allocated_bytes']>=0
                            for x in audit['entries']))
        self.assertTrue(all(x['allocated_bytes']>0 or x['bytes']==0
                            for x in audit['entries']))
        self.assertEqual(sum(x['allocated_bytes'] for x in audit['entries']),
                         audit['allocated_bytes'])
        for entry in audit['entries']:
            self.assertFalse((ROOT/entry['path']).exists(),entry['path'])
        self.assertFalse(cleanup.selected_paths(self.graph,self.protected))
    def test_live_handoff_and_archives_do_not_confuse_current_stage(self):
        live=(ROOT/'docs/RE_HANDOFF.md').read_text()
        storage=(ROOT/'docs/STORAGE_HANDOFF_CURRENT.md').read_text()
        old=(ROOT/'docs/RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md').read_text()
        old_storage=(ROOT/'docs/STORAGE_HANDOFF_AFTER439.md').read_text()
        self.assertLess(len(live.splitlines()),180)
        for item in ('after520','728','893','194,292','258','5,760','0/250',
                     'isteldbl','h_ldiv'):
            self.assertIn(item,live)
        self.assertIn('after520',storage)
        self.assertIn('258',storage)
        self.assertIn('5,760',storage)
        self.assertIn('1,642,496',storage)
        self.assertIn('NOT the current',old)
        self.assertIn('Historical snapshot',old_storage)
        self.assertEqual(
            old.split('---\n\n',1)[1],
            subprocess.check_output(['git','show','ad05750:docs/RE_HANDOFF.md'],
                                    cwd=ROOT).decode())
        self.assertEqual(
            old_storage.split('---\n\n',1)[1],
            subprocess.check_output(['git','show',
                   'ad05750:docs/STORAGE_HANDOFF_CURRENT.md'],cwd=ROOT).decode())
        for doc in ('README.md','AGENTS.md','scripts/README.md',
                    'src/mainl/crt/README.md','docs/RE_WORKFLOW.md'):
            self.assertIn('after520',(ROOT/doc).read_text(),doc)
    def test_hash_all_258_source_driver_logs_and_original_native_outputs(self):
        verify_active_hashes(self.graph)

if __name__=='__main__':unittest.main()
