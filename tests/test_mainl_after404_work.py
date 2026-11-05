"""Original DOS absolute INT 25h/26h disk I/O full two-entry member."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after404_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after404_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
MODE='absolute-dos-disk-io-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalAbsoluteDosDiskIo(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-bound absolute disk receipt absent')
    def test_complete_original_disk_io_and_both_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,561,332))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (292,163850))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual((r['profiles']['absread']['DATA_bytes'],
                          r['profiles']['absread']['BSS_bytes']),(2,2))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native disk source/OBJ vectors absent')
    def test_original_private_probe_two_ints_and_eight_real_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['absread']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),294)
        self.assertEqual([(v['name'],v['class'],v['size']) for v in segment_definitions(original)],
                         [('_TEXT','CODE',292),('_DATA','DATA',2),('_BSS','BSS',2)])
        self.assertEqual(code_publics(original,1),[(86,'_absread'),(189,'_abswrite')])
        self.assertEqual(externs(original),['_getfat','_errno','N_LXMUL@'])
        self.assertEqual(bytes(P[2,i] for i in range(2)),b'\xff\xff')
        self.assertEqual([r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual([f['site'] for f in F],[13,19,75,78,32,54,176,279])
        self.assertEqual([f['frame_method'] for f in F],[1,1,1,1,5,0,5,5])
        report=json.loads(RECEIPT.read_text())
        for row in report['rounds']:
            made=(ROOT/row['outputs']['absread']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['absread'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
