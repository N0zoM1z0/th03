"""Original complete Borland C++ string::assign and 24 ordered FIXUPPs."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
# Deep historical source-bound parent import chain: Python dataclasses may
# exceed its default recursion depth while importing entirely unchanged
# legacy drivers. Adjust only this independent test process' import stack.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after369_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after369_work import review

class OriginalStringAssignBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-assign-boss-build.json')).is_file(),
                         'original native 445-source Japanese receipts absent')
    def test_complete_assign_exception_metadata_and_original_link(self):
        r=review('string-assign-boss')
        p=r['profiles']['assign']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,445,448))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(791,141719))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(126,665,791,0,0))
        self.assertEqual(p['publics'],[(0,'@string@assign$qmx6stringuiui')])
        self.assertEqual(p['imports'],NATIVE['assign']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),24)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-assign-boss-build.json')).is_file(),
                         'raw original/TASM OBJ and EXE/MAP vectors absent')
    def test_literal_original_fixups_typed_rtti_and_japanese_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['assign']['index']]
        self.assertEqual(m.name,'assign')
        original=original_library_member(m)
        old=payload(original)
        self.assertEqual(len(old),791)
        self.assertEqual(code_publics(original,4),[(0,'@string@assign$qmx6stringuiui')])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['0aff02ff03'])
        fields=literal_fields(original)
        self.assertEqual(len(fields),24)
        for segment,count in ((1,7),(4,17)):
            sites=[f['site'] for f in fields if f['segment']==segment]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for offset,bs in ((414,b'TStringRef *\0'),(465,b'xalloc\0\0'),
                          (531,b'xmsg\0\0'),(587,b'TStringRef\0\0'),
                          (645,b'TReference\0\0')):
            self.assertEqual(bytes(old[4,i] for i in range(offset,offset+len(bs))),bs)
        rec=json.loads((ROOT/(PREFIX+'string-assign-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['assign']['path']).read_bytes()
                self.assertEqual(payload(made),old)
                self.assertEqual(literal_fields(made),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['assign'])
                self.assertFalse(row['original_program_equal_by_member']['assign'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
