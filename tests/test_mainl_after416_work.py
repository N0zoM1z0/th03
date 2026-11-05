"""Twelve complete DOS/NEC/IBM/MBCS/ios leaves and exact bounded ABI gaps."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after416_work import (PREFIX,WORK,NATIVE,MODES,
    NEAR_FRAME_GAPS,retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after416_work import review
from lib.pc98 import parse_mz

MODE='twelve-drive-video-mbcs-ios-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalTwelveDosVideoLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'twelve-source native receipt absent')
    def test_inherited_source_chain_and_full_native_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,603,290))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (640,167323))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(len(r['profiles']),12)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound twelve DOS and MBCS member receipts absent')
    def test_all_twelve_complete_code_and_only_five_attested_near_frame_gaps(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),12)
        self.assertFalse(set(names)&set(carry[0][0]))
        self.assertEqual(NEAR_FRAME_GAPS,{
            'ccomscrl':{35:1,57:2},'ccomscrn':{32:1,51:2},'cputs':{30:2}})
        record=json.loads(RECEIPT.read_text())
        literal_exact={'dosgdriv','MBSBTYPE','FMBSBTYP','fgetpos'}
        observed=[]
        for n in names:
            orig=original_library_member(members[NATIVE[n]['index']])
            P=payload(orig);F=literal_fields(orig)
            self.assertEqual(len(P),NATIVE[n]['code'])
            self.assertEqual(members[NATIVE[n]['index']].name,n)
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    G=literal_fields(made)
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(n,made),scope(n,orig))
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],n in literal_exact)
                    self.assertEqual(G==F,n in literal_exact)
                    self.assertEqual({f['site'] for f in G},{f['site'] for f in F})
                    fo={f['site']:f for f in F};go={f['site']:f for f in G}
                    for site in fo:
                        orig_f=fo[site];native_f=go[site]
                        if site in NEAR_FRAME_GAPS.get(n,{}):
                            self.assertEqual((orig_f['frame_method'],orig_f['frame']),(5,None))
                            self.assertEqual((native_f['frame_method'],native_f['frame']),(0,1))
                            self.assertEqual(orig_f['target'],NEAR_FRAME_GAPS[n][site])
                            self.assertEqual(native_f['target'],orig_f['target'])
                            self.assertEqual(orig_f['addend'],native_f['addend'])
                            self.assertEqual(orig_f['location_type'],native_f['location_type'])
                            if row['round']==1:observed.append((n,site))
                        else:
                            self.assertEqual(native_f,orig_f)
        self.assertEqual(sorted(observed),sorted([
            ('ccomscrl',35),('ccomscrl',57),('ccomscrn',32),('ccomscrn',51),
            ('cputs',30)]))
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
