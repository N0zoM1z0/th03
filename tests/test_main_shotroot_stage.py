"""Guard complete procedure transfer and zero-storage source aliases."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shotroot_stage', ROOT/'scripts/stage_th03_main_shotroot.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def fixture():
    calls = ''.join('call '+old+'\r\n' for old, _ in s.ENTRIES if s.EXPECTED_REFS[old])
    bodies = ''.join(old+'\tproc near\r\n retn\r\n'+old+'\tendp\r\n' for old, _ in s.ENTRIES)
    data = ''.join(old+'\t'+{'byte':'db', 'word':'dw', 'dword':'dd'}[kind]+' ?\r\n'
                   for old, _, kind in s.DATA_ALIASES)
    return (calls+"P_SHOT_TEXT segment byte public 'CODE' use16\r\n"+bodies+
            'P_SHOT_TEXT ends\r\n'+data).encode()


class StageTests(unittest.TestCase):
    def transform_fixture(self, raw):
        with patch.object(s, 'ROOT_SHA', s.sha(raw)):
            return s.transform_root(raw)

    def test_complete_transfer_preserves_all_allocations(self):
        raw = fixture()
        changed, refs = self.transform_fixture(raw)
        self.assertEqual(refs, s.EXPECTED_REFS)
        self.assertEqual(s.allocation_lines(raw.decode()), s.allocation_lines(changed.decode()))
        self.assertNotIn(b'proc near', changed)
        self.assertEqual(changed.count(b':near\r\n'), 4)
        self.assertEqual(changed.count(b' label '), 17)

    def test_unattested_source_rejected(self):
        for transform in (s.transform_root, s.transform_score, s.transform_response):
            with self.subTest(transform=transform.__name__), self.assertRaisesRegex(ValueError, 'identity'):
                transform(b'unattested input')

    def test_extra_function_inside_interval_rejected(self):
        raw = fixture().replace(b'sub_E737\tproc near', b'extra proc near\r\n retn\r\nextra endp\r\nsub_E737\tproc near')
        with self.assertRaisesRegex(ValueError, 'five complete'):
            self.transform_fixture(raw)

    def test_missing_or_wrong_distance_procedure_rejected(self):
        raw = fixture().replace(b'sub_E313\tproc near', b'sub_E313\tproc far')
        with self.assertRaisesRegex(ValueError, 'five complete'):
            self.transform_fixture(raw)

    def test_changed_outside_caller_graph_rejected(self):
        raw = b'call sub_E266\r\n'+fixture()
        with self.assertRaisesRegex(ValueError, 'caller membership'):
            self.transform_fixture(raw)

    def test_missing_storage_anchor_rejected(self):
        raw = fixture().replace(b'score_23DF0\tdd ?', b'other_score\tdd ?')
        with self.assertRaisesRegex(ValueError, 'existing storage alias'):
            self.transform_fixture(raw)

    def test_new_data_inside_removed_code_rejected(self):
        raw = fixture().replace(b'sub_E313\tendp', b'surprise db 1\r\nsub_E313\tendp')
        with self.assertRaisesRegex(ValueError, 'allocations preserved'):
            self.transform_fixture(raw)

    def test_existing_alias_cannot_be_shadowed(self):
        raw = fixture()+b'_result_bonus_step label word\r\n'
        with self.assertRaisesRegex(ValueError, 'existing storage alias'):
            self.transform_fixture(raw)

    def test_score_alias_adds_only_symbol_definitions(self):
        raw = (b'score_bonus_digits_put proc far\n retf 8\nscore_bonus_digits_put endp\n'
               b'score_hud_render proc near\n retn\nscore_hud_render endp\n')
        with patch.object(s, 'SCORE_SHA', s.sha(raw)):
            changed = s.transform_score(raw)
        expected = ('public '+s.SCORE_ALIAS+'\n'+s.SCORE_ALIAS+' label far\n').encode()
        near_alias = b'public _score_hud_render\n_score_hud_render label near\n'
        self.assertEqual(changed.replace(expected, b'').replace(near_alias, b''), raw)

    def test_response_insertion_keeps_existing_vector(self):
        raw = b'a.obj obj\\th03\\p_shot.obj b.obj, output.exe, map, cl.lib'
        with patch.object(s, 'RESPONSE_SHA', s.sha(raw)):
            changed = s.transform_response(raw)
        self.assertEqual(changed.replace(b'obj\\th03\\shotroot.obj ', b''), raw)
        with patch.object(s, 'RESPONSE_SHA', s.sha(changed)), self.assertRaisesRegex(ValueError, 'sole ordered'):
            s.transform_response(changed)

    def test_stage_rejects_nonprivate_or_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'.analysis').mkdir()
            existing = root/'.analysis/existing'
            existing.mkdir()
            with patch.object(s, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'ignored output'):
                    s.stage(root, root/'public')
                with self.assertRaisesRegex(ValueError, 'fresh output'):
                    s.stage(root, existing)


if __name__ == '__main__':
    unittest.main()
