"""Complete original istream::ipfx(int) stream-prefix control flow."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after436_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after436_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='istream-prefix-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalIstreamPrefix(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound native prefix receipt absent')
    def test_complete_original_prefix_and_japanese_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,644,249))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(262,173948))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original/native prefix OMF pair absent')
    def test_all_four_far_calls_and_original_buffer_state_bytes(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['istdipfx']['index']]
        self.assertEqual(m.name,'istdipfx')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),262)
        self.assertEqual(len(F),4)
        self.assertEqual([f['site'] for f in F],[229,198,166,39])
        self.assertEqual(code_publics(original,1),[(0,'@istream@ipfx$qi')])
        self.assertEqual(externs(original),NATIVE['istdipfx']['imports'])
        code=bytes(P[1,i] for i in range(262))
        self.assertIn(bytes.fromhex('26c747040000'),code) # gcount zeroed
        self.assertIn(bytes.fromhex('26f6470d01'),code) # ios::skipws flag
        self.assertIn(bytes.fromhex('e9cd00'),code) # original branch layout
        fields=sorted(tuple(f[k] for k in KEYS) for f in F)
        rec=json.loads(RECEIPT.read_text())
        for row in rec['rounds']:
            made=(ROOT/row['outputs']['istdipfx']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),fields)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['istdipfx'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
