"""Original harderr: four public entries and interrupt-state relocation scope."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after390_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after390_work import review

class OriginalCriticalError(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-critical-error-boss-build.json')).is_file(),
                         'source-linked INT24h native receipt absent')
    def test_four_original_critical_error_apis_and_full_link(self):
        r=review('dos-critical-error-boss')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,513,380))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (300,159721))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(r['profiles']['harderr']['BSS_bytes'],12)
        self.assertEqual(r['profiles']['harderr']['publics'],
                         [(84,'___harderr'),(132,'__harderr'),
                          (180,'__hardresume'),(207,'__hardretn')])

    @unittest.skipUnless((ROOT/(PREFIX+'dos-critical-error-boss-build.json')).is_file(),
                         'source-linked INT24h native receipt absent')
    def test_bss_first_dgroup_interrupt_trampoline_and_all_twenty_fixups(self):
        _,_,_,members,_,_=retained()
        o=original_library_member(members[NATIVE['harderr']['index']]);P=payload(o);F=literal_fields(o)
        self.assertEqual(len(P),300)
        self.assertEqual([x.data.hex() for x in parse_omf(o) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual([(x['name'],x['class'],x['size']) for x in segment_definitions(o)],
                         [('_TEXT','CODE',300),('_DATA','DATA',0),('_BSS','BSS',12)])
        self.assertEqual(code_publics(o,1),NATIVE['harderr']['publics'])
        self.assertEqual(len(F),20)
        self.assertEqual([(f['site'],f['location_type'],f['target_method'],f['target'])
                          for f in F if f['site'] in (10,109,113,157,161)],
                         [(10,2,1,1),(109,2,0,1),(113,1,0,1),
                          (157,2,0,1),(161,1,0,1)])
        record=json.loads((ROOT/(PREFIX+'dos-critical-error-boss-build.json')).read_text())
        keys=('segment','site','location_type','width','segment_relative',
              'frame_method','frame','target_method','target','addend')
        expected=sorted(tuple(f[k] for k in keys) for f in F)
        for row in record['rounds']:
            b=(ROOT/row['outputs']['harderr']['path']).read_bytes()
            self.assertEqual(payload(b),P)
            self.assertEqual([x.data.hex() for x in parse_omf(b) if x.name=='GRPDEF'],
                             ['08ff03ff02'])
            self.assertEqual(sorted(tuple(f[k] for k in keys)
                                    for f in literal_fields(b)),expected)
            self.assertNotEqual(literal_fields(b),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['harderr'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
