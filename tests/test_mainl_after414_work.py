"""Six original NEC/IBM text color dispatch APIs with 24 complete FIXUPPs."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after414_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after414_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='six-console-color-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalConsoleColors(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound console color receipt absent')
    def test_six_full_original_apis_and_full_native_link(self):
        result=review(MODE)
        self.assertEqual((result['original_CRT_members'],result['native_source_members'],
                          result['untouched_vendor_members']),(893,590,303))
        self.assertEqual((result['added_CODE_bytes'],result['source_CRT_CODE_bytes']),
                         (216,166470))
        self.assertEqual((result['native_rounds'],result['original_MZ_relocations']),(2,677))
        self.assertTrue(result['complete_original_CODE_DATA_equal'])
        self.assertTrue(result['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(result['original_literal_FIXUPP_equal'])
        self.assertFalse(result['original_library_member_program_equal'])
        self.assertFalse(result['source_acceptance'])
        self.assertFalse(result['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound console color receipt absent')
    def test_exact_six_offsets_and_twenty_four_frame_target_fields(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['ccomcolr']['index']]
        self.assertEqual(m.name,'ccomcolr')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),216)
        self.assertEqual(code_publics(original,1),[
            (0,'_textcolor'),(41,'_textbackground'),(82,'_textattr'),
            (123,'_highvideo'),(154,'_lowvideo'),(185,'_normvideo')])
        self.assertEqual(externs(original),NATIVE['ccomcolr']['imports'])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff02ff03'])
        self.assertEqual(len(F),24)
        self.assertEqual(sum(f['target']==13 for f in F),12)
        self.assertEqual(sum(f['location_type']==3 for f in F),12)
        self.assertEqual(sum(f['frame_method']==5 for f in F),12)
        record=json.loads(RECEIPT.read_text())
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        for row in record['rounds']:
            made=(ROOT/row['outputs']['ccomcolr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['ccomcolr'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
