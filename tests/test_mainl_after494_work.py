"""Original Borland CRT exit lifecycle, three FAR callbacks and MZ order."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after494_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after494_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='crt-exit-atexit-lifecycle-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalExitRuntime(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native CRT exit source receipt absent')
    def test_two_original_full_links_after_symbolic_data_order_fix(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,702,191))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (170,185687))
        self.assertEqual((r['profiles']['exit']['CODE_bytes'],
                          r['profiles']['exit']['DATA_bytes']),(170,12))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS CRT exit OMF absent')
    def test_three_live_far_exit_callbacks_reverse_fixup_sequence(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['exit']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),182)
        self.assertEqual(len(F),14)
        self.assertEqual(code_publics(orig,1),
                         [(95,'_exit'),(114,'__exit'),(136,'__cexit'),
                          (154,'__c_exit')])
        self.assertEqual(code_publics(orig,2),
                         [(0,'__exitbuf'),(4,'__exitfopen'),(8,'__exitopen')])
        self.assertEqual(externs(orig),['__atexitcnt','__atexittbl',
                                       '__terminate','__cleanup',
                                       '__checknull','__restorezero'])
        self.assertEqual(bytes(P[2,i] for i in range(12)),bytes(12))
        self.assertEqual([f['site'] for f in F if f['segment']==2],[8,4,0])
        self.assertTrue(all(f['target_method']==0 and f['target']==1
                            for f in F if f['segment']==2))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['exit']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(code_publics(made,2),code_publics(orig,2))
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertEqual([f['site'] for f in literal_fields(made)
                              if f['segment']==2],[8,4,0])
            self.assertEqual([(int.from_bytes(rec.data[1:3],'little'),
                               len(rec.data[3:]))
                              for rec in parse_omf(made)
                              if rec.name=='LEDATA' and rec.data[0]==2],
                             [(8,4),(4,4),(0,4)])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
