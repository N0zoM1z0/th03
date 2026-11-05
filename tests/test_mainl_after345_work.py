"""Full original Japanese Borland heap break / sbrk original-library OMF."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after345_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after345_work import review


class OriginalHeapBreakManager(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'heap-break-manager-build.json')).is_file(),
                         'local original 379-source native receipts absent')
    def test_full_heap_grow_break_brk_sbrk_and_native_link(self):
        r=review('heap-break-manager')
        p=r['profiles']['fbrk']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,379,514))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (352,125041))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (352,2,0))
        self.assertEqual(p['publics'],[(142,'__brk'),(209,'__sbrk')])
        self.assertEqual(p['imports'],NATIVE['fbrk']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),33)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),
                         (2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'heap-break-manager-build.json')).is_file(),
                         'original/source-built raw OMF pair absent')
    def test_actual_lib_vs_vendor_extdef_and_six_near_frames(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fbrk']['index']]
        self.assertEqual(m.name,'fbrk')
        original=original_library_member(m)
        vendor=(WORK/'vendor/fbrk.obj').read_bytes()
        self.assertEqual(payload(original),payload(vendor))
        self.assertNotEqual(externs(original),externs(vendor))
        self.assertEqual(set(externs(original)),set(externs(vendor)))
        group=lambda blob:[r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']
        self.assertEqual(group(original),['08ff03ff02'])
        self.assertEqual(group(vendor),['08ff02ff03'])
        def fields(blob):
            imports=externs(blob)
            return {(f['segment'],f['site']):
                dict(f, target=(imports[f['target']-1] if f['target_method']==2
                                else f['target']))
                for f in literal_fields(blob)}
        a=fields(original);b=fields(vendor)
        self.assertEqual(set(a),set(b))
        for key in a:
            aa=dict(a[key]);bb=dict(b[key])
            for f in ('frame_method','frame'):
                aa.pop(f);bb.pop(f)
            self.assertEqual(aa,bb)
        self.assertEqual({key for key in a if a[key]!=b[key]},
                         {(1,s) for s in (162,181,225,266,283,302)})
        record=json.loads((ROOT/(PREFIX+'heap-break-manager-build.json')).read_text())
        original_fields=literal_fields(original)
        self.assertEqual(len(original_fields),33)
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                built=(ROOT/row['outputs']['fbrk']['path']).read_bytes()
                self.assertEqual(payload(built),payload(original))
                self.assertEqual(literal_fields(built),original_fields)
                self.assertNotEqual(object_program_records(built),m.program_records)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fbrk'])
                self.assertFalse(row['original_program_equal_by_member']['fbrk'])
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
