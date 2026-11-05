"""Original PC-98 IRQ timer control, DGROUP callback and INT 1Ch."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after477_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after477_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='pc98-timer-irq-callback-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalPC98Timer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'new timer source receipt missing')
    def test_complete_member_and_two_original_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,685,208))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(162,182846))
        self.assertEqual((r['profiles']['pc98timr']['CODE_bytes'],
                          r['profiles']['pc98timr']['DATA_bytes']),(162,5))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original timer OMF missing')
    def test_native_dgroup_segment_callback_and_thirteen_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['pc98timr']['index']]
        self.assertEqual(m.name,'pc98timr')
        raw=original_library_member(m)
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),167)
        self.assertEqual(len(F),13)
        self.assertEqual(code_publics(raw,1),[(70,'_pc98timer')])
        self.assertEqual(externs(raw),[])
        self.assertEqual([r.data.hex() for r in parse_omf(raw)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual(bytes(P[2,i] for i in range(5)),bytes(5))
        fields={x['site']:x for x in F}
        self.assertEqual((fields[10]['location_type'],fields[10]['frame_method'],
                          fields[10]['target_method'],fields[10]['target']),
                         (2,5,1,1))
        self.assertEqual((fields[127]['target_method'],fields[127]['target'],
                          fields[127]['addend']),(0,1,0))
        self.assertEqual(P[1,148],0xf9) # busy wait goes to test, not STI
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['pc98timr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
