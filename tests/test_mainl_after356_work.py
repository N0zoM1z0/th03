"""Original static TCharMask, string hash APIs, typed RTTI and INITDATA."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after356_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after356_work import review

PUBLICS=[(0,'@TCharMask@$bctr$qv'),(96,'@string@hash$xqv'),
         (207,'@string@hash_case$xqv')]

class OriginalStringHashBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-hash-static-boss-build.json')).is_file(),
                         'native 408-source Japanese hash receipts absent')
    def test_complete_original_three_methods_static_state_and_two_native_links(self):
        r=review('string-hash-static-boss')
        p=r['profiles']['hash']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,408,485))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (421,131776))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes'],p['INITDATA_bytes']),
                         (50,371,421,0,4,6))
        self.assertEqual(p['publics'],PUBLICS)
        self.assertEqual(p['imports'],NATIVE['hash']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),17)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-hash-static-boss-build.json')).is_file(),
                         'original native source OBJ/INIT/EXE pairs absent')
    def test_actual_bss_init_and_exact_original_ordered_relocs(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['hash']['index']]
        self.assertEqual(m.name,'hash')
        orig=original_library_member(m)
        old=payload(orig)
        self.assertEqual(len(old),427)
        self.assertEqual([i for i in range(4) if (3,i) in old],[])
        self.assertEqual(bytes(old[5,i] for i in range(6)),
                         bytes.fromhex('01 20 21 00 00 00'))
        fields=literal_fields(orig)
        self.assertEqual(len(fields),17)
        self.assertEqual([f['site'] for f in fields if f['segment']==1],
                         [41,37,31,5])
        self.assertEqual([f['site'] for f in fields if f['segment']==4],
                         [343,295,196,185,168,155,129,117,111,108,105,21])
        self.assertEqual([(f['segment'],f['site']) for f in fields[-1:]],[(5,2)])
        at={(f['segment'],f['site']):f for f in fields}
        self.assertEqual((at[4,295]['target_method'],at[4,295]['target'],
                          at[4,295]['frame_method']), (0,3,1))
        self.assertEqual((at[4,117]['target_method'],at[4,117]['target'],
                          at[4,117]['frame_method']), (2,6,1))
        self.assertEqual((at[5,2]['target_method'],at[5,2]['target'],
                          at[5,2]['addend']), (0,1,33))
        self.assertEqual([q.data.hex() for q in parse_omf(orig)
                          if q.name=='GRPDEF'],['0cff02ff03'])
        rec=json.loads((ROOT/(PREFIX+'string-hash-static-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(native_round=row['round']):
                made=(ROOT/row['outputs']['hash']['path']).read_bytes()
                self.assertEqual(payload(made),old)
                self.assertEqual(literal_fields(made),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['hash'])
                self.assertFalse(row['original_program_equal_by_member']['hash'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
