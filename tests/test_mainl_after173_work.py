"""Original C++ fstream destructor, own far jump adjustors and RTTI."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after173_work import PREFIX,WORK
from review_th03_mainl_after173_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFstreamDestructor(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'fstream-destructor-build.json')).is_file(),
                         '174-source original Japanese fstream destructor vectors absent')
    def test_full_native_fstream_destructor_and_original_product(self):
        r=review('fstream-destructor')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,174,719))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (735,76670))
        p=r['profiles']['iofsdtr']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (735,36,0))
        self.assertEqual(p['publics'],[(0,'@fstream@$bdtr$qv')])
        self.assertEqual((len(p['imports']),len(p['relocation_sites_targets'])),
                         (9,36))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'fstream-destructor-build.json')).is_file(),
                         'native original fstream destructor raw OBJ unavailable')
    def test_three_self_referential_far_jumps_and_36_original_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'fstream-destructor-build.json')).read_text())
        old=(WORK/'vendor/iofsdtr.obj').read_bytes()
        p=payload(old)
        self.assertEqual(len([k for k in p if k[0]==1]),735)
        self.assertEqual(len([k for k in p if k[0]==2]),36)
        code=bytes(p[1,i] for i in range(735))
        instr=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[145:181],145))
        self.assertEqual([z.address for z in instr if z.mnemonic=='ljmp'],
                         [152,164,176])
        self.assertTrue(all(code[i]==0xEA for i in (152,164,176)))
        original=literal_fields(old)
        self.assertEqual(len(original),36)
        self.assertEqual(len([f for f in original if f['segment']==2]),5)
        for site in (153,165,177):
            f=next(f for f in original if f['segment']==1 and f['site']==site)
            self.assertEqual((f['target_method'],f['target'],f['addend']),
                             (0,1,0))
        by=lambda f:(f['segment'],f['site'])
        for row in r['rounds']:
            new=(ROOT/row['outputs']['iofsdtr']['path']).read_bytes()
            self.assertEqual(p,payload(new))
            fields=literal_fields(new)
            self.assertEqual(sorted(original,key=by),sorted(fields,key=by))
            self.assertNotEqual(original,fields)
