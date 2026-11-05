"""Original strstreambuf::init and console clear, precise 27h OMF gap."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after429_work import PREFIX,WORK,NATIVE,MODES,retained,original_library_member,scope
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after429_work import review
from lib.pc98 import parse_mz
MODE='strstreambuf-init-and-console-clear'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalStrstreamInitConsoleClear(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original native receipt absent')
    def test_full_init_and_clear_source_link_original_japanese_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,626,267))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(272,171599))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound complete original source members absent')
    def test_all_twelve_fields_only_single_attested_scroll_frame_difference(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(names,('srbinit','clrscr'))
        self.assertFalse(set(names)&set(carry[0][0]))
        original={n:original_library_member(members[NATIVE[n]['index']]) for n in names}
        for n in names:
            self.assertEqual(len(payload(original[n])),NATIVE[n]['code'])
            self.assertEqual(len(literal_fields(original[n])),NATIVE[n]['fields'])
        self.assertEqual([f['site'] for f in literal_fields(original['srbinit'])],
                         [189,120,83,27])
        original_scroll=next(f for f in literal_fields(original['clrscr']) if f['site']==27)
        self.assertEqual((original_scroll['frame_method'],original_scroll['frame'],
                          original_scroll['target_method'],original_scroll['target']),
                         (5,None,2,2))
        r=json.loads(RECEIPT.read_text())
        for q in r['rounds']:
            for n in names:
                blob=(ROOT/q['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(blob),payload(original[n]))
                self.assertEqual(scope(n,blob),scope(n,original[n]))
                self.assertFalse(q['literal_omf_fixupp_equal_by_member'][n])
                FF={f['site']:f for f in literal_fields(original[n])}
                GG={f['site']:f for f in literal_fields(blob)}
                self.assertEqual(set(FF),set(GG))
                for site in FF:
                    if n=='clrscr' and site==27:
                        self.assertEqual((GG[site]['frame_method'],GG[site]['frame']),(0,1))
                        self.assertEqual((FF[site]['target'],GG[site]['target']), (2,2))
                    else:
                        self.assertEqual(GG[site],FF[site])
            exe=(ROOT/q['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
