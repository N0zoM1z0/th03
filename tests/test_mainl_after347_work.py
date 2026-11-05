"""Complete original Borland operator new: typed C++ RTTI, INIT/EXIT and OMF."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after347_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after347_work import review


class OriginalNewOperatorBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'new-operator-exception-boss-build.json')).exists(),
                         'native 390-source original Java? no, Japanese CRT receipts absent')
    def test_complete_new_exception_and_full_original_native_link(self):
        r=review('new-operator-exception-boss')
        p=r['profiles']['new']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,390,503))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (754,126150))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (754,24,0))
        self.assertEqual((p['INITDATA_bytes'],p['EXITDATA_bytes']),(6,6))
        self.assertEqual(p['DATA_implicit_sites'],list(range(6)))
        self.assertEqual(p['publics'],NATIVE['new']['publics'])
        self.assertEqual(p['data_publics'],NATIVE['new']['data_publics'])
        self.assertEqual(p['imports'],NATIVE['new']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),49)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'new-operator-exception-boss-build.json')).exists(),
                         'both native 390-source OBJ and complete Japanese linker outputs absent')
    def test_original_sparse_data_real_init_exit_and_literal_49_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['new']['index']]
        self.assertEqual(m.name,'new')
        original=original_library_member(m)
        p=payload(original)
        self.assertEqual(len(p),784) # 754 CODE, 18 initialized DATA, 6 INIT, 6 EXIT
        self.assertEqual([i for i in range(24) if (2,i) not in p],list(range(6)))
        self.assertEqual(bytes(p[2,i] for i in range(6,24)),
                         b'\x1c\0\0\0Out of memory\0')
        self.assertEqual(bytes(p[4,i] for i in range(6)),b'\x01\x20\x6f\x01\0\0')
        self.assertEqual(bytes(p[5,i] for i in range(6)),b'\x01\x20\xca\x01\0\0')
        fields=literal_fields(original)
        self.assertEqual(len(fields),49)
        self.assertEqual({(f['segment'],f['site'],f['target'],f['addend'])
                          for f in fields if f['segment'] in (2,4,5)},
                         {(2,6,1,28),(4,2,1,367),(5,2,1,458)})
        self.assertEqual([f['site'] for f in fields if f['segment']==1],
                         sorted((f['site'] for f in fields if f['segment']==1),reverse=True))
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['0cff02ff03'])
        record=json.loads((ROOT/(PREFIX+'new-operator-exception-boss-build.json')).read_text())
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                compiled=(ROOT/row['outputs']['new']['path']).read_bytes()
                self.assertEqual(payload(compiled),p)
                self.assertEqual(literal_fields(compiled),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['new'])
                self.assertFalse(row['original_program_equal_by_member']['new'])
                self.assertNotEqual(object_program_records(compiled),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
