"""Original Borland BCD x87 emulation FIXUPPs and typed extended constants."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after460_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after460_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz

MODE='bcd-x87-emulation-conversion-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
PUBLICS=[(89,'__BCD_TOBINARY'),(145,'__BCD_TODECIMAL'),
         (264,'__BCD_LOG10'),(305,'__BCD_POW10')]
IMPORTS=['FIDRQQ','FIERQQ','FIWRQQ']

class OriginalBcdEmulator(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound native BCD receipt absent')
    def test_whole_original_bcd_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,668,225))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (398,179416))
        self.assertEqual((r['profiles']['bcd1']['CODE_bytes'],
                          r['profiles']['bcd1']['DATA_bytes']),(398,140))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original x87 OMF absent')
    def test_true_emulated_fpu_fixups_and_original_extended_constants(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['bcd1']['index']]
        self.assertEqual(m.name,'bcd1')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),538)
        self.assertEqual(len(F),23)
        self.assertEqual(code_publics(orig,1),PUBLICS)
        self.assertEqual(externs(orig),IMPORTS)
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        data=bytes(P[2,i] for i in range(140))
        self.assertEqual([int.from_bytes(data[i:i+4],'little') for i in range(0,32,4)],
                         [1,10,100,1000,10000,100000,1000000,10000000])
        self.assertEqual(len(data[32:132]),100)  # ten true 80-bit powers
        self.assertEqual(data[32:42],bytes.fromhex('000000000020bcbe1940'))
        self.assertEqual(data[122:132],bytes.fromhex('9b97208a025260c42575'))
        self.assertEqual(data[132:140],bytes.fromhex('0000807f0000c07f'))
        sites={f['site']:f for f in F}
        for site,target,addend in [(40,1,56219),(97,2,9883),(256,3,39824),
                                   (297,3,39824)]:
            f=sites[site]
            self.assertEqual((f['target_method'],f['target'],f['addend']),
                             (2,target,addend))
        self.assertEqual((sites[38]['target_method'],sites[38]['target'],
                          sites[38]['addend']),(0,2,0))
        self.assertEqual((sites[48]['target_method'],sites[48]['target'],
                          sites[48]['addend']),(0,2,32))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['bcd1']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(code_publics(made,1),PUBLICS)
            self.assertEqual(externs(made),IMPORTS)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
