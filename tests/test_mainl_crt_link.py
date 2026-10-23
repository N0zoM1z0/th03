"""Retained actual CRT proof regression; no native tools or CPU matrices launched."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/mainl-crt-asm-probe-20261021-v02/manifest.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
ROOT=Path(os.environ.get('TH03_CRT_TEST_ROOT',ROOT))
sys.path.insert(0,str(ROOT/'scripts'))
MODULE=Path(os.environ.get('TH03_CRT_REPLAY_MODULE',ROOT/'scripts/replay_th03_mainl_crt_link.py'))
spec=importlib.util.spec_from_file_location('crt_replay_under_test',MODULE)
replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
if os.environ.get('TH03_CRT_RECIPE'):replay.RECIPE=os.environ['TH03_CRT_RECIPE']
class CrtLinkTests(unittest.TestCase):
    def test_complete_actual_proof(self):
        r=replay.replay(ROOT)
        self.assertEqual((r['existing_source_units'],r['source_owned_bytes_eligible']),(6,628))
        self.assertTrue(r['runtime_equal']);self.assertTrue(r['raw_library_exe_map_repeat_equal'])
        self.assertFalse(r['models_rerun']);self.assertFalse(r['exact_acceptance'])
    def test_changed_source_object_library_or_model_is_rejected(self):
        recipe=json.loads((ROOT/replay.RECIPE).read_bytes())
        paths=[recipe['producers'][0]['source'],recipe['producers'][0]['repeat_object'],recipe['links'][1]['work']+'/crt.lib',recipe['models']['candidate']]
        original=Path.read_bytes
        for name in paths:
            target=ROOT/name
            def altered(path):
                raw=original(path)
                return raw+b'changed' if path==target else raw
            with self.subTest(name=name),patch.object(Path,'read_bytes',altered):
                with self.assertRaisesRegex(ValueError,'proof input differs'):
                    replay.replay(ROOT)
if __name__=='__main__':unittest.main()
