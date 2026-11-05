"""Original DOS read/write/seek, file date/time, memory and TSR CRT APIs."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after333_work import PREFIX, WORK, NATIVE, original_library_member, retained
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import parse_omf
from lib.borland_library import object_program_records
from review_th03_mainl_after333_work import review

SIZES = {'dosread':40,'doswrite':40,'dosseek':45,'dosgftim':39,
         'dossftim':33,'dosfree':26,'dosalloc':40,'doskeep':24}
FRAME_GAPS = {'dosseek','dosgftim','dossftim','dosfree'}


class OriginalBorlandDOSLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-file-memory-leaves-build.json')).is_file(),
                         'local 352-source Japanese native receipts absent')
    def test_eight_complete_original_code_and_full_native_product(self):
        r=review('dos-file-memory-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,352,541))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (287,114907))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for name,size in SIZES.items():
            with self.subTest(member=name):
                p=r['profiles'][name]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[name]['publics'])
                self.assertEqual(p['imports'],NATIVE[name]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),1)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'dos-file-memory-leaves-build.json')).is_file(),
                         'raw original and native source OBJ pairs unavailable')
    def test_original_logical_fixups_and_exact_frame_status_each_member(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'dos-file-memory-leaves-build.json')).read_text())
        keys=('segment','site','location_type','width','segment_relative',
              'target_method','target','addend')
        identity=lambda fields:sorted(tuple(f[k] for k in keys) for f in fields)
        for name in SIZES:
            original=original_library_member(members[NATIVE[name]['index']])
            want=literal_fields(original)
            self.assertEqual(len(want),1)
            for row in receipt['rounds']:
                with self.subTest(member=name,round=row['round']):
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    fields=literal_fields(made)
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(identity(want),identity(fields))
                    self.assertEqual(fields==want,name not in FRAME_GAPS)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][name],
                                     name not in FRAME_GAPS)
                    self.assertEqual(row['original_program_equal_by_member'][name],
                        object_program_records(made)==
                        members[NATIVE[name]['index']].program_records)
                    self.assertEqual([r.data.hex() for r in parse_omf(made)
                                      if r.name=='GRPDEF'],[NATIVE[name]['group']])
        # These BCC near imports use TARGET frame, while TASM uses CODE frame.
        original=original_library_member(members[NATIVE['dosseek']['index']])
        made=(ROOT/receipt['rounds'][0]['outputs']['dosseek']['path']).read_bytes()
        self.assertEqual(literal_fields(original)[0]['frame_method'],5)
        self.assertEqual(literal_fields(made)[0]['frame_method'],0)
        # Original DOS read/write near imports do not have that mismatch.
        original=original_library_member(members[NATIVE['dosread']['index']])
        made=(ROOT/receipt['rounds'][0]['outputs']['dosread']['path']).read_bytes()
        self.assertEqual(literal_fields(original),literal_fields(made))


if __name__=='__main__':
    unittest.main()
