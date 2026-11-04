"""Original Japanese Borland filebuf/stdiobuf and istream buffer algorithms."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after177_work import PREFIX,WORK
from review_th03_mainl_after177_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFileAndInputStreamMethods(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'file-stream-methods-build.json')).is_file(),
                         '185-source native file stream methods absent')
    def test_eight_full_native_buffer_algorithms_and_original_product(self):
        r=review('file-stream-methods')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,185,708))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (3076,82159))
        expected=dict(fsbskoff=(434,4),fsbuflow=(440,5),fsbsync=(415,6),
                      sdbuflow=(416,5),istgbuf=(369,3),istebuf=(361,2),
                      istechp=(355,3),sdbsync=(286,4))
        for n,(size,fields) in expected.items():
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,0,0),n)
            self.assertEqual(len(p['relocation_sites_targets']),fields,n)
            self.assertEqual(len(p['publics']),1,n)
            self.assertEqual(p['publics'][0][0],0,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'file-stream-methods-build.json')).is_file(),
                         'original file/istream method vectors absent')
    def test_32_original_omf_site_frames_and_far_virtual_opcodes(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'file-stream-methods-build.json')).read_text())
        by=lambda f:(f['segment'],f['site'])
        for name in receipt['names']:
            original=(WORK/'vendor'/(name+'.obj')).read_bytes();p=payload(original)
            fields=literal_fields(original)
            for rd in receipt['rounds']:
                new=(ROOT/rd['outputs'][name]['path']).read_bytes()
                self.assertEqual(p,payload(new),name)
                g=literal_fields(new)
                self.assertEqual(sorted(fields,key=by),sorted(g,key=by),name)
                self.assertNotEqual(fields,g,name)
        for name,code_sites in [('fsbuflow',{114:'ff5f24'}),
                                ('sdbuflow',{126:'ff5f18'}),
                                ('istgbuf',{69:'ff5f18',178:'ff5f0c',259:'ff5f0c'}),
                                ('istebuf',{68:'ff5f18',178:'ff5f0c',259:'ff5f0c'}),
                                ('istechp',{145:'ff5f0c',231:'ff5f0c'}),
                                ('sdbsync',{58:'ff5f18'})]:
            raw=(WORK/'vendor'/(name+'.obj')).read_bytes();p=payload(raw)
            size=max(i for seg,i in p if seg==1)+1
            c=bytes(p[1,i] for i in range(size))
            ins={x.address:x.bytes.hex() for x in Cs(CS_ARCH_X86,CS_MODE_16).disasm(c,0)}
            self.assertEqual({k:ins[k] for k in code_sites},code_sites,name)
