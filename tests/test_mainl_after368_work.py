"""Complete original Japanese Borland 10-API multibyte byte classifier."""
import json
import sys
import unittest
# Python 3.12: bootstrap setuptools' distutils shim before the long inherited
# CRT driver imports Unicorn, whose legacy runtime imports distutils.sysconfig.
import setuptools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after368_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after368_work import review

PUBS=[(0,'__ismbbkalpha'),(24,'__ismbbkpunct'),(48,'__ismbbkana'),
      (72,'__ismbbalpha'),(117,'__ismbbpunct'),(162,'__ismbbalnum'),
      (207,'__ismbbprint'),(252,'__ismbbgraph'),(297,'__ismbblead'),
      (321,'__ismbbtrail')]
SITES=[335,311,281,268,236,223,191,178,146,133,101,88,62,38,14]

class OriginalMBBISFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'mbbis-ten-classifiers-build.json')).is_file(),
                         'native original 444-member Japanese receipt absent')
    def test_complete_ten_api_mbbis_and_full_japanese_link(self):
        r=review('mbbis-ten-classifiers')
        p=r['profiles']['MBBIS']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,444,449))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (345,140928))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (345,0,0))
        self.assertEqual(p['publics'],PUBS)
        self.assertEqual(p['imports'],['__ctype','__mbctype'])
        self.assertEqual(len(p['relocation_sites_targets']),15)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'mbbis-ten-classifiers-build.json')).is_file(),
                         'native original/source OMF and MZ rounds absent')
    def test_original_byte_table_fixupp_order_and_all_public_offsets(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['MBBIS']['index']])
        F=literal_fields(original)
        self.assertEqual(code_publics(original,1),PUBS)
        self.assertEqual([f['site'] for f in F],SITES)
        self.assertEqual(len(payload(original)),345)
        self.assertTrue(all(f['location_type']==1 and f['target_method']==2
                            and f['frame_method']==1 and f['frame']==1
                            and f['addend']==1 for f in F))
        self.assertEqual([f['target'] for f in F].count(2),10)
        self.assertEqual([f['target'] for f in F].count(1),5)
        rec=json.loads((ROOT/(PREFIX+'mbbis-ten-classifiers-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['MBBIS']['path']).read_bytes()
                self.assertEqual(payload(made),payload(original))
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['MBBIS'])
                self.assertFalse(row['original_program_equal_by_member']['MBBIS'])
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['MBBIS']['index']].program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
