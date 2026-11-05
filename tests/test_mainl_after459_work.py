"""Original bidirectional Shift-JIS conversion, semantic DATA tables."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after459_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after459_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz

MODE='mbcs-fullwidth-mapping-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
PUBLICS=[(0,'__mbbtombc'),(59,'__mbctombb')]

class OriginalJapaneseMbtomb(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native Shift-JIS mapping receipt absent')
    def test_two_original_japanese_full_link_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,667,226))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (207,179018))
        self.assertEqual((r['profiles']['MBTOMB']['CODE_bytes'],
                          r['profiles']['MBTOMB']['DATA_bytes']),(207,432))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original table OMF absent')
    def test_five_distinct_japanese_mapping_tables_and_six_symbolic_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['MBTOMB']['index']]
        self.assertEqual(m.name,'MBTOMB')
        orig=original_library_member(m)
        P=payload(orig); F=literal_fields(orig)
        self.assertEqual(len(P),639)
        self.assertEqual(len(F),6)
        self.assertEqual(code_publics(orig,1),PUBLICS)
        self.assertEqual(externs(orig),[])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        data=bytes(P[2,i] for i in range(432))
        self.assertEqual((len(data[:190]),len(data[190:318]),
                          len(data[318:405]),len(data[405:423]),
                          len(data[423:])),(190,128,87,18,9))
        self.assertEqual(data[:4], bytes.fromhex('40814981'))
        self.assertEqual(data[405:409],bytes.fromhex('42817581'))
        self.assertEqual(data[-9:],bytes.fromhex('a1a2a3a4a5b0dedf00'))
        fixes={f['site']:f for f in F}
        self.assertEqual({s:fixes[s]['addend'] for s in fixes},
                         {27:0,51:190,126:318,147:0,181:405,189:423})
        self.assertTrue(all(f['frame_method']==1 and f['target_method']==0
                            and f['target']==2 for f in F))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['MBTOMB']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
