"""Original Borland string::contains C++ exception scope and typed RTTI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after487_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after487_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='string-contains-exception-rtti-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalStringContains(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native original contains proof absent')
    def test_full_original_code_and_both_real_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,695,198))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(200,184544))
        self.assertEqual((r['profiles']['contain']['CODE_bytes'],
                          r['profiles']['contain']['DATA_bytes']),(200,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original Borland C++ EH OMF unavailable')
    def test_real_exception_scope_local_code_and_string_rtti(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['contain']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),200)
        self.assertEqual(len(F),11)
        self.assertEqual(code_publics(original,1),[(32,'@string@contains$xqnxc')])
        self.assertEqual(externs(original),[
            '@__RefDestructorCount$qv','___InitExceptBlocks','___ExitExceptBlocks',
            '@string@$bctr$qnxc','@string@$bdtr$qv',
            '@string@find$xqmx6stringui'])
        self.assertEqual(bytes(P[1,i] for i in range(8)),
                         bytes.fromhex('000000008e000000'))
        self.assertEqual(bytes(P[1,i] for i in range(180,187)),b'string\0')
        f={x['site']:x for x in F}
        self.assertEqual(set(f),{4,18,30,41,44,47,68,90,120,131,172})
        self.assertEqual((f[4]['target_method'],f[4]['target'],f[4]['addend']),
                         (0,1,142))
        self.assertEqual((f[18]['target_method'],f[18]['target'],f[18]['addend']),
                         (0,1,0))
        self.assertEqual((f[44]['target_method'],f[44]['target'],f[44]['addend']),
                         (0,1,18))
        self.assertEqual((f[172]['target_method'],f[172]['target']), (2,5))
        expected=sorted(tuple(x[k] for k in KEYS) for x in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['contain']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(x[k] for k in KEYS)
                                    for x in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
