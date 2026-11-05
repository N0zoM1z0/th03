"""Ten small original CRT ABI programs, complete localeconv and true frame gaps."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after398_work import (PREFIX,WORK,NATIVE,MODES,
    NEAR_VIDEO_FRAME_GAPS,retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after398_work import review
from lib.pc98 import parse_mz

MODE='ten-abi-video-locale-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalTenAbiLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound ten-leaf native receipt absent')
    def test_original_native_link_with_all_source_abi_leaves(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,548,345))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (126,162203))
        self.assertEqual(r['profiles']['cconv']['DATA_bytes'],59)
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound ten-leaf native receipt absent')
    def test_each_complete_member_and_exactly_three_near_video_frame_gaps(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),10)
        self.assertFalse(set(names)&set(carry[0][0]))
        r=json.loads(RECEIPT.read_text())
        original={n:original_library_member(members[NATIVE[n]['index']]) for n in names}
        literal_exact=set(names)-set(NEAR_VIDEO_FRAME_GAPS)-{'cconv'}
        self.assertEqual(len(literal_exact),6)
        for n in names:
            q=original[n]
            if n=='cconv':
                p=payload(q)
                self.assertEqual(len(p),69)
                self.assertEqual(bytes(p[2,i] for i in range(40,48)),b'\x7f'*8)
                self.assertEqual(bytes(p[2,i] for i in range(48,59)),b'.'+b'\0'*10)
                self.assertEqual(NATIVE[n]['data_publics'],[(0,'__localeconvention')])
            for row in r['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(q))
                    self.assertEqual(scope(n,made),scope(n,q))
                    of=literal_fields(q);mf=literal_fields(made)
                    self.assertEqual(mf==of,n in literal_exact)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],n in literal_exact)
                    if n in NEAR_VIDEO_FRAME_GAPS:
                        self.assertEqual(len(of),1)
                        self.assertEqual((of[0]['site'],of[0]['frame_method'],of[0]['frame']),
                                         (NEAR_VIDEO_FRAME_GAPS[n],5,None))
                        self.assertEqual((mf[0]['site'],mf[0]['frame_method'],mf[0]['frame']),
                                         (NEAR_VIDEO_FRAME_GAPS[n],0,1))
        for row in r['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
