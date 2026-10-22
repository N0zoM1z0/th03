"""Guard the state transfer, caller ABI names and a fixed-size BSS storage view."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

shot = load('stage_th03_main_shotroot')
with patch.dict('sys.modules', {'stage_th03_main_shotroot': shot}):
    s = load('stage_th03_main_playerstate')


def fixture():
    def bodies(entries):
        return ''.join(old + '\tproc near\r\n retn\r\n' + old + '\tendp\r\n' for old, _ in entries)
    calls = ''.join(('call ' + old + '\r\n') * count for old, count in {**shot.EXPECTED_REFS, **s.EXPECTED_REFS}.items())
    data = ''.join(old + '\t' + {'byte': 'db', 'word': 'dw', 'dword': 'dd'}[kind] + ' ?\r\n' for old, _, kind in shot.DATA_ALIASES)
    return (calls + "P_SHOT_TEXT segment byte public 'CODE' use16\r\n" + bodies(shot.ENTRIES)
            + "main_010_TEXT\tsegment\tbyte public 'CODE' use16\r\n" + bodies(s.ENTRIES)
            + bodies(s.CODE_ALIASES) + data + s.RESERVE + '\tdb 100 dup(?)\r\n').encode()


class StateStageTests(unittest.TestCase):
    def transform(self, raw):
        with patch.object(shot, 'ROOT_SHA', shot.sha(raw)):
            return s.transform_root(raw)

    def test_complete_transfer_and_fixed_storage(self):
        raw = fixture()
        changed, refs = self.transform(raw)
        self.assertEqual(refs, dict(shot=shot.EXPECTED_REFS, state=s.EXPECTED_REFS))
        self.assertEqual(shot.allocation_lines(raw.decode()), shot.allocation_lines(changed.decode().replace(s.VIEW, s.RESERVE)))
        self.assertEqual(changed.count(b'proc near'), 2)
        self.assertEqual(changed.count(b'_shot_release_frames db 2 dup(?)'), 1)

    def test_wrong_provenance_rejected(self):
        with self.assertRaisesRegex(ValueError, 'baseline root identity'):
            s.transform_root(fixture())

    def test_changed_caller_rejected(self):
        with self.assertRaisesRegex(ValueError, 'state caller membership'):
            self.transform(fixture() + b'call sub_DA43\r\n')

    def test_incomplete_or_extra_procedure_rejected(self):
        for replacement in (b'sub_DF18\tproc far', b'extra proc near\r\nextra endp\r\nsub_DF18\tproc near'):
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, 'five complete state'):
                self.transform(fixture().replace(b'sub_DF18\tproc near', replacement))

    def test_removed_data_cannot_be_hidden(self):
        with self.assertRaisesRegex(ValueError, 'allocations preserved'):
            self.transform(fixture().replace(b'sub_DF18\tendp', b'hidden db 1\r\nsub_DF18\tendp'))

    def test_reserve_size_or_alias_drift_rejected(self):
        for raw in (fixture().replace(b'db 5 dup(?)', b'db 6 dup(?)'), fixture() + b'_shot_release_frames label byte\r\n'):
            with self.subTest(raw=raw[-80:]), self.assertRaisesRegex(ValueError, 'five-byte reserve'):
                self.transform(raw)

    def test_existing_animation_alias_rejected(self):
        raw = fixture() + (s.CODE_ALIASES[0][1] + ' label near\r\n').encode()
        with self.assertRaisesRegex(ValueError, 'existing code alias'):
            self.transform(raw)

    def test_ordered_response_preserves_prior_objects(self):
        raw = b'a.obj obj\\th03\\main_010.obj obj\\th03\\p_shot.obj b.obj, out.exe'
        with patch.object(shot, 'RESPONSE_SHA', shot.sha(raw)):
            changed = s.transform_response(raw)
        self.assertEqual(changed.replace(b'obj\\th03\\state.obj ', b'').replace(b'obj\\th03\\shotroot.obj ', b''), raw)

    def test_missing_state_object_anchor_rejected(self):
        raw = b'a.obj obj\\th03\\p_shot.obj b.obj, out.exe'
        with patch.object(shot, 'RESPONSE_SHA', shot.sha(raw)), self.assertRaisesRegex(ValueError, 'state insertion'):
            s.transform_response(raw)


if __name__ == '__main__':
    unittest.main()
