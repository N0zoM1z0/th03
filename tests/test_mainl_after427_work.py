"""Original istream(streambuf*,ostream*) ctor, two RTTI and tied-stream ABI."""
import json, sys, unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after427_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after427_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='istream-tied-stream-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalTiedIstreamConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound native receipt absent')
    def test_complete_boss_and_two_original_japanese_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,623,270))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(305,170978))
        self.assertEqual((r['profiles']['istctr3']['CODE_bytes'],r['profiles']['istctr3']['DATA_bytes']),(305,20))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original native OBJ source pair absent')
    def test_skip_tie_exact_original_rtti_adjustment_and_fifteen_fields(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['istctr3']['index']]
        self.assertEqual(m.name,'istctr3')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),325)
        self.assertEqual(len(F),15)
        self.assertEqual(code_publics(orig,1),[(0,'@istream@$bctr$qn9streambufin7ostream')])
        self.assertEqual(externs(orig),NATIVE['istctr3']['imports'])
        self.assertEqual(bytes(P[1,i] for i in range(173,181)),bytes.fromhex('8bdc36834704faea'))
        self.assertEqual(bytes(P[2,i] for i in range(20)),
                         bytes.fromhex('b9000000000000000000000006000800ad000000'))
        sites={f['site']:f for f in F if f['segment']==1}
        self.assertEqual((sites[120]['target_method'],sites[120]['target']),(2,5))
        self.assertEqual((sites[138]['target_method'],sites[138]['target']),(2,4))
        fields=sorted(tuple(f[k] for k in KEYS) for f in F)
        data=json.loads(RECEIPT.read_text())
        for q in data['rounds']:
            made=(ROOT/q['outputs']['istctr3']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),fields)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(q['literal_omf_fixupp_equal_by_member']['istctr3'])
            exe=(ROOT/q['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
