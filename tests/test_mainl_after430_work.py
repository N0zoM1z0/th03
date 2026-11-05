"""Complete original istream/ostream base destructors and real vtable OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after430_work import PREFIX,WORK,NATIVE,MODES,retained,original_library_member,scope
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after430_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='base-istream-ostream-destructor-bosses'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalBaseStreamDestructors(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original destructors absent')
    def test_complete_two_destructors_and_full_native_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,628,265))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(483,172082))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound exact original OMF pair absent')
    def test_both_symbolic_vtable_fields_rtti_and_unique_flush_branch(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),2)
        self.assertFalse(set(names)&set(carry[0][0]))
        r=json.loads(RECEIPT.read_text())
        for name,code,sites,rtti_off,thunk,offset in [
                ('istdtr1',230,12,110,98,6),
                ('ostdtr1',253,13,133,121,4)]:
            orig=original_library_member(members[NATIVE[name]['index']]);P=payload(orig);F=literal_fields(orig)
            self.assertEqual(len(P),code+20)
            self.assertEqual(len(F),sites)
            self.assertEqual(code_publics(orig,1),NATIVE[name]['publics'])
            self.assertEqual(externs(orig),NATIVE[name]['imports'])
            original_sites={(f['segment'],f['site']):f for f in F}
            for pos,add in ((38,8),(46,16)):
                f=original_sites[(1,pos)]
                self.assertEqual((f['target_method'],f['target'],f['addend']),
                                 (0,2,add))
            self.assertEqual(bytes(P[2,i] for i in range(2)),
                             rtti_off.to_bytes(2,'little'))
            self.assertEqual(bytes(P[2,i] for i in (12,13)),
                             offset.to_bytes(2,'little'))
            self.assertEqual(bytes(P[2,i] for i in (16,17)),
                             thunk.to_bytes(2,'little'))
            for q in r['rounds']:
                with self.subTest(name=name,round=q['round']):
                    made=(ROOT/q['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(name,made),scope(name,orig))
                    self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                                     sorted(tuple(f[k] for k in KEYS) for f in F))
                    self.assertNotEqual(literal_fields(made),F)
                    self.assertFalse(q['literal_omf_fixupp_equal_by_member'][name])
        for q in r['rounds']:
            exe=(ROOT/q['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
