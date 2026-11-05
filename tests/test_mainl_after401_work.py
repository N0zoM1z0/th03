"""Original Borland stdiobuf::seekoff complete CODE and four far fixups."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after401_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after401_work import review
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
MODE='stdiobuf-seekoff-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalStdiobufSeekoff(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-linked seekoff receipt absent')
    def test_complete_seekoff_and_two_original_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,551,342))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (291,163002))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'complete original source/native OBJ pair absent')
    def test_complete_original_texta_abi_and_four_far_call_fields(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['sdbskoff']['index']]
        self.assertEqual(m.name,'sdbskoff')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),291)
        self.assertEqual([(v['name'],v['class'],v['size']) for v in segment_definitions(original)],
                         [('_TEXTA','CODE',291),('_DATA','DATA',0),('_BSS','BSS',0)])
        self.assertEqual(code_publics(original,1),[(0,'@stdiobuf@seekoff$ql12ios@seek_diri')])
        self.assertEqual(externs(original),NATIVE['sdbskoff']['imports'])
        self.assertEqual([f['site'] for f in F],[279,246,212,155])
        self.assertEqual([f['target'] for f in F],[4,2,1,3])
        self.assertEqual([f['location_type'] for f in F],[3]*4)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            b=(ROOT/row['outputs']['sdbskoff']['path']).read_bytes()
            self.assertEqual(payload(b),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(b)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(b),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['sdbskoff'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
