"""Selected original Japanese five-segment standard C++ iostream lifecycle."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after105_work import PREFIX, WORK
from review_th03_mainl_after105_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics


class OriginalStandardIostreamLifetime(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ioststd-build.json')).is_file(),
                         'source-bound 106-source ioststd native vectors absent')
    def test_entire_original_105_to_106_source_native_product(self):
        r=review('ioststd')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,106,787))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2088,51293))
        p=r['profiles']['ioststd']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes'],
                          p['INITDATA_bytes'],p['EXITDATA_bytes']),
                         (2088,0,190,12,12))
        self.assertEqual(p['publics'],[(997,'@Iostream_delete$qv')])
        self.assertEqual(p['bss_publics'],[
            (0,'_cin'),(46,'_cout'),(90,'_cerr'),(134,'_clog'),
            (178,'___stdin_streambuf'),(182,'___stdout_streambuf'),
            (186,'___stderr_streambuf')])
        self.assertEqual(len(p['imports']),20)
        self.assertEqual(len(p['relocation_sites_targets']),148)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'ioststd-build.json')).is_file(),
                         'original 106-source ioststd OBJ receipt absent')
    def test_original_Cplusplus_RTTI_BSS_and_init_exit_relocation_frames(self):
        rep=json.loads((ROOT/(PREFIX+'ioststd-build.json')).read_text())
        original=(WORK/'vendor/ioststd.obj').read_bytes()
        origseg=segment_definitions(original)
        self.assertEqual([(x['name'],x['class'],x['size']) for x in origseg],[
            ('_TEXTA','CODE',2088),('_DATA','DATA',0),('_BSS','BSS',190),
            ('_INIT_','INITDATA',12),('_EXIT_','EXITDATA',12)])
        self.assertEqual(code_publics(original,3),[
            (0,'_cin'),(46,'_cout'),(90,'_cerr'),(134,'_clog'),
            (178,'___stdin_streambuf'),(182,'___stdout_streambuf'),
            (186,'___stderr_streambuf')])
        orig=literal_fields(original)
        self.assertEqual([len([f for f in orig if f['segment']==i])
                          for i in range(1,6)],[144,0,0,2,2])
        key=lambda f:(f['segment'],f['site'])
        bssptr=[x for x in orig if x['segment']==1 and
                x['site'] in (1291,1301,1311,1321)]
        self.assertEqual(len(bssptr),4)
        self.assertTrue(all(f['frame_method']==1 and
                            f['target_method']==0 and f['target']==3
                            for f in bssptr))
        for roundinfo in rep['rounds']:
            candidate=(ROOT/roundinfo['outputs']['ioststd']['path']).read_bytes()
            self.assertEqual(payload(original),payload(candidate))
            self.assertEqual(segment_definitions(original),
                             segment_definitions(candidate))
            fields=literal_fields(candidate)
            self.assertEqual(len(fields),148)
            self.assertEqual(sorted(fields,key=key),sorted(orig,key=key))
            self.assertNotEqual(fields,orig)
            self.assertFalse(roundinfo['literal_omf_fixupp_equal_by_member']['ioststd'])
        code=bytes(payload(original)[1,i] for i in range(2088))
        for label in (b'ostream_withassign\0',b'istream_withassign\0',
                      b'streambuf *\0',b'filebuf *\0',b'istream\0',b'ostream\0'):
            self.assertIn(label,code)
