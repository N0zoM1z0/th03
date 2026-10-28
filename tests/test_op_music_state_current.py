"""Native checks for the complete Music Room state/track prefix."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.op_music_state_layout import START, verify as layout
from review_th03_op_cfg_work import images

@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpMusicStateCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)

    def test_complete_native_layout(self):
            result=layout(ROOT,self.work,self.target,self.candidate)
            self.assertEqual((result['functions'],result['code_bytes'],len(result['ordered_native_fields']),
                              len(result['ordered_relocations'])),(4,216,12,4))

    def test_equal_mutated_images_cannot_inherit_native_layout(self):
            raw=bytearray(self.target.program_image);raw[START+1]^=1
            bad=replace(self.target,program_image=bytes(raw))
            with self.assertRaisesRegex(ValueError,'all216 independently resolved'):
                layout(ROOT,self.work,bad,bad)
