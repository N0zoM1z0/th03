"""Sixteen selected complete DOS/PC-98 and C++ streambuf source leaves."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after185_work import PREFIX,WORK
from review_th03_mainl_after185_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalDOSPC98CXXLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'hardware-io-leaves-build.json')).is_file(),
                         'selected 201-source original Japanese native pair unavailable')
    def test_sixteen_full_hardware_and_streambuffer_leaves(self):
        r=review('hardware-io-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,201,692))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1007,83166))
        expected={'stsetf2':106,'srbsbuf':44,'srbfreez':40,'getfat':104,
                  'pc98disk':82,'bion_key':81,'bion_prn':73,'outport':66,
                  'inport':56,'pc98key':48,'pc98prnt':32,'bioskey':41,
                  'biosdisk':62,'bios_equ':51,'dosgdate':62,'cibmsond':59}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0),n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
        self.assertEqual(r['profiles']['outport']['publics'],
                         [(0,'_outport'),(16,'_outportb'),
                          (32,'_outpw'),(48,'_outp')])
        self.assertEqual(r['profiles']['inport']['publics'],
                         [(0,'_inport'),(13,'_inportb'),
                          (28,'_inpw'),(41,'_inp')])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'hardware-io-leaves-build.json')).is_file(),
                         'selected native PC-98/DOS raw OBJ vectors absent')
    def test_exact_omf_empty_fixups_and_original_xchg_hardware_code(self):
        from lib.omf import parse_omf
        report=json.loads((ROOT/(PREFIX+'hardware-io-leaves-build.json')).read_text())
        for name in report['names']:
            old=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(literal_fields(old),[],name)
            groups=[z.data.hex() for z in parse_omf(old) if z.name=='GRPDEF']
            self.assertEqual(len(groups),1)
            for row in report['rounds']:
                out=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(old),payload(out),name)
                self.assertEqual(literal_fields(out),[],name)
                self.assertEqual([z.data.hex() for z in parse_omf(out)
                                  if z.name=='GRPDEF'],groups,name)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
        p=payload((WORK/'vendor/pc98disk.obj').read_bytes())
        data=bytes(p[1,i] for i in range(82))
        self.assertEqual((data[11:13],data[32:34],data[48:50]),
                         (bytes.fromhex('86c4'),bytes.fromhex('86d6'),
                          bytes.fromhex('86c4')))
