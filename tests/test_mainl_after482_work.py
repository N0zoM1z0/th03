"""Original DOS EXEC spawn bridge with four implicit CODE SS:SP bytes."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after482_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after482_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-exec-spawn-segment-stack-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosSpawn(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native original DOS spawn receipt unavailable')
    def test_entire_original_scope_and_both_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,690,203))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(198,183737))
        self.assertEqual((r['profiles']['spawn']['CODE_bytes'],
                          r['profiles']['spawn']['DATA_bytes']),(198,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS spawn OMF missing')
    def test_implicit_real_saved_stack_and_literal_seven_fixups(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['spawn']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),194)
        self.assertEqual({i for s,i in P if s==1},set(range(4,198)))
        self.assertTrue(all((1,i) not in P for i in range(4)))
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(raw,1),[(4,'__spawn')])
        self.assertEqual(externs(raw),['__IOERROR','__psp'])
        self.assertEqual([(s['name'],s['class'],s['size'])
                          for s in segment_definitions(raw)],
                         [('_TEXT','CODE',198),('_DATA','DATA',0)])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['06ff02'])
        self.assertEqual({f['site']:(f['target_method'],f['target'],f['addend']) for f in F},
                         {92:(2,2,0),124:(2,2,0),145:(0,1,2),
                          150:(0,1,0),158:(0,1,2),163:(0,1,0),
                          182:(2,1,0)})
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            out=(ROOT/row['outputs']['spawn']['path']).read_bytes()
            self.assertEqual(payload(out),P)
            self.assertEqual(literal_fields(out),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['spawn'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
