"""Twelve real DOS syscall leaf programs and the setblock vendor GROUP gap."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after407_work import (PREFIX,WORK,NATIVE,MODES,
    SOURCE_PATHS,NEAR_FRAME_GAP,retained,original_library_member,scope,
    vendor_matches_target)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after407_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz

MODE='twelve-dos-syscall-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalDosSyscallLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound twelve DOS leaf native receipt absent')
    def test_native_original_code_and_real_two_round_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,576,317))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (396,164888))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound twelve DOS leaf native receipt absent')
    def test_twelve_original_code_only_one_near_call_frame_difference(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),12)
        self.assertFalse(set(names)&set(carry[0][0]))
        report=json.loads(RECEIPT.read_text())
        self.assertEqual(report['source_paths'],SOURCE_PATHS)
        self.assertEqual(SOURCE_PATHS['setblock'],'src/mainl/crt/setblock.asm')
        original={n:original_library_member(members[NATIVE[n]['index']]) for n in names}
        for n in names:
            P=payload(original[n]);F=literal_fields(original[n])
            self.assertEqual(len(P),NATIVE[n]['code'])
            self.assertEqual(len(F),1)
            self.assertTrue(vendor_matches_target(n,(WORK/'vendor'/(n+'.obj')).read_bytes(),original[n]))
            for row in report['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(n,made),scope(n,original[n]))
                    g=literal_fields(made)
                    self.assertEqual(g==F,n!='dossetbl')
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],n!='dossetbl')
                    if n=='dossetbl':
                        self.assertEqual((F[0]['site'],F[0]['frame_method'],F[0]['frame']),
                                         (22,5,None))
                        self.assertEqual((g[0]['site'],g[0]['frame_method'],g[0]['frame']),
                                         (22,0,1))
                        self.assertEqual(NEAR_FRAME_GAP,{'dossetbl':22})
        for row in report['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound twelve DOS leaf native receipt absent')
    def test_same_named_setblock_active_target_versus_installed_vendor(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['setblock']['index']])
        vendor=(WORK/'vendor/setblock.obj').read_bytes()
        def groups(blob):
            return [r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']
        self.assertEqual(groups(orig),['08ff02ff03'])
        self.assertEqual(groups(vendor),['08ff03ff02'])
        self.assertEqual(payload(orig),payload(vendor))
        self.assertEqual(literal_fields(orig),literal_fields(vendor))
        self.assertTrue(vendor_matches_target('setblock',vendor,orig))

if __name__=='__main__':unittest.main()
