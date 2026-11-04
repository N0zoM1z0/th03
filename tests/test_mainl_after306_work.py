"""Original Japanese Borland C++ exception subsystem and ordered MZ fixups."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after306_work import PREFIX,WORK
from review_th03_mainl_after306_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics

class OriginalCXXExceptionRuntime(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'exception-boss-build.json')).is_file(),
                         '307-source Japanese exception product vectors absent')
    def test_all_nine_exception_apis_and_original_exe_map_relocations(self):
        r=review('exception-boss')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,307,586))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (649,102964))
        p=r['profiles']['xxv']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (649,296,4))
        self.assertEqual(len(p['publics']),9)
        self.assertEqual(p['publics'][0],(0,'@terminate$qv'))
        self.assertEqual(p['publics'][-1],(571,'__ExceptInit'))
        self.assertEqual(len(p['data_publics']),15)
        self.assertEqual(p['bss_publics'],[(0,'__DestructorCountPtr')])
        self.assertEqual(len(p['imports']),5)
        self.assertEqual(len(p['relocation_sites_targets']),16)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'exception-boss-build.json')).is_file(),
                         'original exception runtime raw OBJ pairs absent')
    def test_exception_globals_256_byte_buffers_and_original_mz_order(self):
        r=json.loads((ROOT/(PREFIX+'exception-boss-build.json')).read_text())
        old=(WORK/'vendor/xxv.obj').read_bytes()
        p=payload(old)
        self.assertEqual(sum(s==1 for s,i in p),649)
        self.assertEqual(sum(s==2 for s,i in p),296)
        self.assertEqual(bytes(p[2,i] for i in range(40,296)),bytes(256))
        self.assertEqual([z for z in code_publics(old,2) if z[0] in (40,168)],
            [(40,'___exceptionNameBuff'),(168,'___ExceptStaticXbuff')])
        orig=literal_fields(old)
        self.assertEqual(len(orig),16)
        by=lambda f:(f['segment'],f['site'])
        for row in r['rounds']:
            made=(ROOT/row['outputs']['xxv']['path']).read_bytes()
            self.assertEqual(p,payload(made))
            self.assertEqual(sorted(orig,key=by),
                             sorted(literal_fields(made),key=by))
            self.assertEqual(code_publics(old,2),code_publics(made,2))
            self.assertNotEqual(orig,literal_fields(made))
            ff=literal_fields(made)
            self.assertEqual([f['site'] for f in ff if f['segment']==1
                 and f['site'] in (80,110,127)],[127,110,80])
            self.assertEqual([f['site'] for f in ff if f['segment']==2],[14,10])
            # Source-generated MZ relocation *order*, not just a sorted set,
            # is verified by the complete byte-exact EXE comparison.
            self.assertEqual((ROOT/row['outputs']['exe']['path']).read_bytes(),
                             (WORK/'bin/th03/mainl.target.exe').read_bytes())
