"""Original FAR strtok state machine, 4-byte BSS and twelve true FIXUPPs."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after472_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after472_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='far-tokenizer-persistent-bss-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalFarStrtok(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound far tokenizer proof absent')
    def test_complete_source_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,680,213))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(203,182030))
        self.assertEqual((r['profiles']['fstrtok']['CODE_bytes'],
                          r['profiles']['fstrtok']['DATA_bytes'],
                          r['profiles']['fstrtok']['BSS_bytes']),(203,0,4))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original far tokenizer OMF unavailable')
    def test_real_bss_far_cursor_all_twelve_relocations_and_flow(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['fstrtok']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),203)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(raw,1),[(0,'__fstrtok')])
        self.assertEqual(externs(raw),[])
        segs=segment_definitions(raw)
        self.assertEqual((segs[2]['name'],segs[2]['size']),('_BSS',4))
        self.assertTrue(all(f['segment']==1 and f['target_method']==0
                            and f['target']==3 and f['frame_method']==1 for f in F))
        self.assertEqual({f['site']:f['addend'] for f in F},
                         {24:2,27:0,53:0,83:0,87:0,97:0,
                          113:2,116:0,148:0,161:0,179:0,183:0})
        self.assertEqual(P[1,80],0x0e) # true skip-to-second-empty-check
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fstrtok']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
