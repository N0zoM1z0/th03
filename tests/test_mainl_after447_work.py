"""Original locale-weight collation state machine and exact OMF calls."""
import sys
import json
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after447_work import PREFIX, WORK, NATIVE, retained, original_library_member
from review_th03_mainl_after447_work import review
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='locale-collation-state-machine-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalLocaleCollationBoss(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native locale-collation source missing')
    def test_full_original_and_two_native_link_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,655,238))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (265,176421))
        self.assertEqual((r['profiles']['_strcoll']['CODE_bytes'],
                          r['profiles']['_strcoll']['DATA_bytes']),(265,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native collation OMF missing')
    def test_weight_iteration_locales_near_calls_and_third_segment(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['_strcoll']['index']]
        self.assertEqual(m.name,'_strcoll')
        original=original_library_member(m)
        P=payload(original)
        F=literal_fields(original)
        self.assertEqual(len(P),265)
        self.assertEqual(len(F),3)
        self.assertEqual(code_publics(original,1),
                         [(0,'__strcoll'),(66,'_LevelCollate')])
        self.assertEqual(externs(original),NATIVE['_strcoll']['imports'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'], ['08ff02'])
        fields={f['site']:f for f in F}
        self.assertEqual((fields[12]['target_method'],fields[12]['target']),
                         (2,7))  # locale pointer
        self.assertEqual((fields[113]['frame_method'],fields[113]['frame'],
                          fields[113]['target_method'],fields[113]['target']),
                         (0,1,2,1))  # first weight
        self.assertEqual((fields[129]['frame_method'],fields[129]['frame'],
                          fields[129]['target_method'],fields[129]['target']),
                         (0,1,2,1))  # second weight
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['_strcoll']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['_strcoll'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
