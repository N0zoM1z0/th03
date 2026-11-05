"""Original filebuf(int,char*,int) constructor, virtual setbuf, and typed RTTI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after437_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after437_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='filebuf-virtual-setbuf-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalFilebufConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original filebuf constructor absent')
    def test_complete_original_filebuf_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,645,248))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(259,174207))
        self.assertEqual((r['profiles']['fsbctr3']['CODE_bytes'],r['profiles']['fsbctr3']['DATA_bytes']),(259,52))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original and assembled filebuf OMF pair absent')
    def test_real_virtual_call_typed_rtti_and_nineteen_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsbctr3']['index']]
        self.assertEqual(m.name,'fsbctr3')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),311)
        self.assertEqual(len(F),19)
        self.assertEqual(code_publics(original,1),[(0,'@filebuf@$bctr$qinci')])
        self.assertEqual(externs(original),NATIVE['fsbctr3']['imports'])
        code=bytes(P[1,i] for i in range(259))
        self.assertIn(bytes.fromhex('ff5f04'),code) # actual virtual setbuf call
        self.assertIn(b'filebuf\0',code)
        self.assertIn(b'streambuf\0',code)
        self.assertEqual(bytes(P[2,i] for i in range(52)),bytes.fromhex('8500')+bytes(50))
        fixes={(f['segment'],f['site']):f for f in F}
        self.assertEqual((fixes[(1,50)]['target_method'],fixes[(1,50)]['target'],fixes[(1,50)]['addend']),(0,2,8))
        self.assertEqual((fixes[(2,28)]['target_method'],fixes[(2,28)]['target']),(2,7))
        self.assertEqual((fixes[(2,32)]['target_method'],fixes[(2,32)]['target']),(2,11))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['fsbctr3']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['fsbctr3'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
