"""Original filebuf destructor, public openprot DATA and 20 FIXUPPs."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after438_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after438_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='filebuf-close-destructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalFilebufDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original destructor native receipt absent')
    def test_complete_filebuf_destructor_and_whole_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,646,247))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(247,174454))
        self.assertEqual((r['profiles']['fsbdtr']['CODE_bytes'],r['profiles']['fsbdtr']['DATA_bytes']),(247,54))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'filebuf destructor original/native OMF pair absent')
    def test_real_openprot_data_export_close_overflow_and_all_twenty_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsbdtr']['index']]
        self.assertEqual(m.name,'fsbdtr')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),301)
        self.assertEqual(len(F),20)
        self.assertEqual(code_publics(orig,1),[(0,'@filebuf@$bdtr$qv')])
        self.assertEqual(code_publics(orig,2),[(0,'@filebuf@openprot')])
        self.assertEqual(externs(orig),NATIVE['fsbdtr']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(54)),bytes.fromhex('80017900')+bytes(50))
        C=bytes(P[1,i] for i in range(247))
        self.assertIn(bytes.fromhex('ff5f18'),C)  # original virtual overflow(-1)
        by={(f['segment'],f['site']):f for f in F}
        self.assertEqual((by[(1,37)]['target_method'],by[(1,37)]['target'],by[(1,37)]['addend']),(0,2,10))
        self.assertEqual((by[(1,51)]['target_method'],by[(1,51)]['target']),(2,9))
        self.assertEqual((by[(2,2)]['target_method'],by[(2,2)]['target'],by[(2,2)]['addend']),(0,1,121))
        self.assertEqual((by[(2,10)]['target_method'],by[(2,10)]['target'],by[(2,10)]['addend']),(0,1,0))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fsbdtr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(code_publics(made,2),[(0,'@filebuf@openprot')])
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['fsbdtr'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
