"""Original Japanese C++ conbuf/constream CRT and RTTI owner proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after104_work import PREFIX, WORK
from review_th03_mainl_after104_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalConsoleStreamCplusplusBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'constrea-build.json')).is_file(),
                         '105-source original C++ console native rounds absent')
    def test_complete_17_function_CPP_console_and_original_link(self):
        r=review('constrea')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,105,788))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (3241,49205))
        q=r['profiles']['constrea']
        self.assertEqual((q['CODE_bytes'],q['DATA_bytes'],q['BSS_bytes']),
                         (3241,92,0))
        self.assertEqual(len(q['publics']),17)
        self.assertEqual(q['publics'][0],(0,'@conbuf@$bctr$qv'))
        self.assertEqual(q['publics'][1],(107,'@conbuf@overflow$qi'))
        self.assertEqual(q['publics'][-1],(2544,'@setclr$qi'))
        self.assertEqual(q['data_publics'],
                         [(0,'@conbuf@current'),(4,'@constream@isCon_')])
        self.assertEqual(len(q['imports']),35)
        self.assertEqual(len(q['relocation_sites_targets']),152)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'constrea-build.json')).is_file(),
                         'original C++ RTTI OBJ vector not retained')
    def test_typed_original_cpp_RTTI_and_all_152_literal_site_frames(self):
        receipt=json.loads((ROOT/(PREFIX+'constrea-build.json')).read_text())
        original=(WORK/'vendor/constrea.obj').read_bytes()
        made=(ROOT/receipt['rounds'][0]['outputs']['constrea']['path']).read_bytes()
        p,q=payload(original),payload(made)
        self.assertEqual(p,q)
        self.assertEqual(len([f for f in p if f[0]==1]),3241)
        self.assertEqual(len([f for f in p if f[0]==2]),92)
        origbytes=bytes(p[1,i] for i in range(3241))
        for off,string in [(2689,b'conbuf\x00\x00'),(2755,b'constream\x00'),
                           (3099,b'ios\x00'),(3153,b'ostream\x00'),
                           (3219,b'streambuf\x00')]:
            self.assertEqual(origbytes[off:off+len(string)],string)
        a,b=literal_fields(original),literal_fields(made)
        self.assertEqual((len(a),len(b)),(152,152))
        self.assertEqual(len([f for f in a if f['segment']==1]),134)
        self.assertEqual(len([f for f in a if f['segment']==2]),18)
        key=lambda f:(f['segment'],f['site'])
        self.assertEqual(sorted(a,key=key),sorted(b,key=key))
        self.assertNotEqual(a,b)
        self.assertEqual(receipt['rounds'][0]['literal_omf_fixupp_equal_by_member'],
                         {'constrea':False})
