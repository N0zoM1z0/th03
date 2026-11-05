"""Eleven complete Borland formatted I/O, scanner and conio CRT leaves."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after434_work import (PREFIX,WORK,MODES,NATIVE,
    NEAR_FRAME_GAPS,retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after434_work import review
from lib.pc98 import parse_mz
MODE='eleven-format-scan-console-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalFormatScanConio(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound 11 CRT leaf receipt absent')
    def test_all_original_members_and_two_whole_japanese_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,642,251))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(515,173421))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(len(r['profiles']),11)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound eleven member OMF vectors absent')
    def test_exact_43_relocation_sites_only_15_attested_near_frame_gaps(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),11)
        self.assertFalse(set(names)&set(carry[0][0]))
        self.assertEqual(NEAR_FRAME_GAPS,{
            'cprintf':{24:1},'vcprintf':{23:1},'vprintf':{24:2},
            'vfprintf':{25:1},'fprintf':{26:2},
            'cscanf':{29:3},'vcscanf':{30:3},
            'clreol':{9:3,24:3,41:2},
            'insline':{10:3,31:2,46:3,67:2},'window':{18:2}})
        record=json.loads(RECEIPT.read_text())
        self.assertEqual(sum(NATIVE[n]['code'] for n in names),515)
        self.assertEqual(sum(NATIVE[n]['fields'] for n in names),43)
        self.assertEqual(sum(len(x) for x in NEAR_FRAME_GAPS.values()),15)
        observed=[]
        for n in names:
            m=members[NATIVE[n]['index']]
            self.assertEqual(m.name,n)
            orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
            self.assertEqual(len(P),NATIVE[n]['code'])
            self.assertEqual(len(F),NATIVE[n]['fields'])
            fo={(f['segment'],f['site']):f for f in F}
            for row in record['rounds']:
                with self.subTest(name=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    G=literal_fields(made)
                    go={(f['segment'],f['site']):f for f in G}
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(n,made),scope(n,orig))
                    self.assertEqual(set(fo),set(go))
                    self.assertNotEqual(G,F)  # chronological Borland/TASM records
                    self.assertFalse(row['literal_omf_fixupp_equal_by_member'][n])
                    for key in fo:
                        a,b=fo[key],go[key]
                        if key[1] in NEAR_FRAME_GAPS.get(n,{}):
                            self.assertEqual((a['frame_method'],a['frame']),(5,None))
                            self.assertEqual((b['frame_method'],b['frame']),(0,1))
                            self.assertEqual((a['target_method'],a['target'],a['addend']),
                                             (2,NEAR_FRAME_GAPS[n][key[1]],0))
                            self.assertEqual((b['target_method'],b['target'],b['addend']),
                                             (2,NEAR_FRAME_GAPS[n][key[1]],0))
                            if row['round']==1:observed.append((n,key[1]))
                        else:
                            self.assertEqual(a,b)
        self.assertEqual(sorted(observed),sorted((n,site) for n,gs in
                         NEAR_FRAME_GAPS.items() for site in gs))
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
