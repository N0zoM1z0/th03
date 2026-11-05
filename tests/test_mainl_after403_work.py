"""Eight complete original NEC/IBM dispatch and DOS ABI leaf members."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after403_work import (PREFIX,WORK,MODES,NATIVE,
    NEAR_CALL_FRAME_GAPS,retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after403_work import review
from lib.pc98 import parse_mz
from lib.omf import parse_omf
MODE='eight-machine-dispatch-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalMachineDispatchLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound machine dispatch receipt absent')
    def test_full_original_pcs_and_japanese_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,560,333))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (295,163558))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(len(r['profiles']),8)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound machine dispatch receipt absent')
    def test_exact_eight_original_code_and_only_four_specific_near_frames(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),8)
        self.assertFalse(set(names)&set(carry[0][0]))
        record=json.loads(RECEIPT.read_text())
        from build_th03_mainl_after403_work import sha
        self.assertEqual(record['stdio_layout_sha256'],
                         sha((ROOT/'src/mainl/crt/stdio_layout.inc').read_bytes()))
        gaps_seen=[]
        for n in names:
            orig=original_library_member(members[NATIVE[n]['index']])
            P=payload(orig)
            self.assertEqual(len(P),NATIVE[n]['code'])
            F=literal_fields(orig)
            for row in record['rounds']:
                with self.subTest(name=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(n,made),scope(n,orig))
                    self.assertEqual(literal_fields(made)==F,n=='isatty')
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],n=='isatty')
                    of={f['site']:f for f in F}
                    mf={f['site']:f for f in literal_fields(made)}
                    self.assertEqual(set(of),set(mf))
                    for site in of:
                        if site in NEAR_CALL_FRAME_GAPS.get(n,{}):
                            self.assertEqual((of[site]['frame_method'],of[site]['frame']),
                                             (5,None))
                            self.assertEqual((mf[site]['frame_method'],mf[site]['frame']),
                                             (0,1))
                            if row['round']==1:gaps_seen.append((n,site))
                        else:
                            self.assertEqual(mf[site],of[site])
        self.assertEqual(sorted(gaps_seen),sorted([
            ('ccomwhxy',10),('ccomwhxy',22),('wherexy',3),('wherexy',22)]))
        orig=original_library_member(members[NATIVE['isatty']['index']])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
