"""Original Borland TMP filename generation, real BSS and DOS attribute retry."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after492_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after492_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-temp-name-counter-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDOSFilename(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native tmpname source receipt missing')
    def test_original_two_complete_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,700,193))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(188,185353))
        self.assertEqual((r['profiles']['mkname']['CODE_bytes'],
                          r['profiles']['mkname']['DATA_bytes'],
                          r['profiles']['mkname']['BSS_bytes']),(188,9,13))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original filename BSS OMF absent')
    def test_real_typed_prefix_suffix_buffer_and_seven_site_audit(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['mkname']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),197)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(original,1),
                         [(0,'__MKNAME'),(97,'__TMPNAM')])
        self.assertEqual(externs(original),['__UTOA','_strcat',
                                            '__stpcpy','__dos_getfileattr'])
        self.assertEqual(bytes(P[2,i] for i in range(9)),b'TMP\0.$$$\0')
        segs=segment_definitions(original)
        self.assertEqual((segs[2]['name'],segs[2]['size']),('_BSS',13))
        self.assertEqual(NEAR_FRAME_GAPS,{'mkname':{64:1}})
        original_by_site={f['site']:f for f in F}
        self.assertEqual(set(original_by_site),{19,35,54,64,68,78,163})
        self.assertEqual((original_by_site[19]['target_method'],
                          original_by_site[19]['target']),(0,3))
        self.assertEqual((original_by_site[35]['target_method'],
                          original_by_site[35]['target']),(0,2))
        self.assertEqual((original_by_site[163]['target_method'],
                          original_by_site[163]['target']),(2,4))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['mkname']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            fields={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(fields),set(original_by_site))
            for site,old in original_by_site.items():
                new=fields[site]
                if site==64:
                    self.assertEqual((old['frame_method'],old['frame']),(5,None))
                    self.assertEqual((new['frame_method'],new['frame']),(0,1))
                    keys=set(old)-{'frame_method','frame'}
                    self.assertEqual({k:old[k] for k in keys},{k:new[k] for k in keys})
                else:self.assertEqual(old,new)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
