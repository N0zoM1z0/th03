"""Four complete original Borland fstreambase 16-bit constructors."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after252_work import PREFIX,WORK
from review_th03_mainl_after252_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFstreambaseConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'fstreambase-constructors-build.json')).is_file(),
                         '256-source Japanese native vectors unavailable')
    def test_four_complete_constructors_and_full_original_product(self):
        r=review('fstreambase-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,256,637))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1722,95192))
        cases={'fsctr1':(421,18,'@fstreambase@$bctr$qv'),
               'fsctr2':(444,19,'@fstreambase@$bctr$qnxcii'),
               'fsctr3':(424,18,'@fstreambase@$bctr$qi'),
               'fsctr4':(433,18,'@fstreambase@$bctr$qinci')}
        for name,(size,nfix,public) in cases.items():
            p=r['profiles'][name]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,20,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['relocation_sites_targets']),nfix)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'fstreambase-constructors-build.json')).is_file(),
                         'selected fstreambase OBJ vectors unavailable')
    def test_native_executable_adjustors_and_all_73_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'fstreambase-constructors-build.json')).read_text())
        cuts=dict(fsctr1=153,fsctr2=176,fsctr3=156,fsctr4=165)
        key=lambda f:(f['segment'],f['site'])
        for name,cut in cuts.items():
            orig=(WORK/'vendor'/(name+'.obj')).read_bytes()
            p=payload(orig)
            c=bytes(p[1,i] for i in range(max(j for s,j in p if s==1)+1))
            for st in (b'fstreambase\0',b'filebuf\0',b'ios\0',b'streambuf\0'):
                self.assertIn(st,c)
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[cut:cut+12],cut))
            self.assertEqual([x.mnemonic for x in ins],['mov','add','ljmp'])
            self.assertEqual(c[cut+7],0xea)
            f=literal_fields(orig)
            self.assertEqual(len([x for x in f if x['segment']==2]),3)
            for row in receipt['rounds']:
                compiled=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(orig),payload(compiled))
                self.assertEqual(sorted(f,key=key),
                                 sorted(literal_fields(compiled),key=key))
                self.assertNotEqual(f,literal_fields(compiled))
