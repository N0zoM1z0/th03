"""Native metadata ownership, compressed OMF storage and actual reader controls."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun import parse_launcher
from lib.zun_directory_source import compose_native_launcher
from lib.zun_directory_layout import native,verify,specification
from lib.zun_directory_runtime import negative_controls
from review_th03_zun_format_work import images
from review_th03_zun_directory_work import witness
from test_main_enemy_layout import mutate_record

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'


@unittest.skipUnless((WORK/'wrapper/meta.obj').is_file(),'private native directory absent')
class Directory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = (WORK/'product/zun.target.com').read_bytes()
        cls.obj = (WORK/'wrapper/meta.obj').read_bytes()
        cls.linked = (WORK/'wrapper/meta.com').read_bytes()
        cls.map = (WORK/'wrapper/meta.map').read_bytes()

    def test_complete_semantic_DATA_owner_and_outer_public_rebasing(self):
        work,_,_,_,files,maintained,cold = images(ROOT)
        r = verify(work,self.image,(work/'product/zun.com').read_bytes(),files,maintained,json.loads(cold))
        self.assertEqual((r['code_bytes'],r['data_bytes'],r['functions']),(0,324,0))
        self.assertEqual(r['outer_publics'],dict(directory_count=0x1DF,directory_names=0x1E1,directory_entries=0x2E1,directory_end=0x323))
        self.assertEqual(r['semantic']['ordered_payload_boundaries'],[0x326,0x6C4,0xC32,0x33A2,0x4422,0x5A14])
        self.assertIsNone(r['owners'][0]['canonical_file_offset'])
        self.assertFalse(r['original_generation_tool_identified'])

    def test_native_iterated_records_supply_only_unused_name_and_entry_slots(self):
        r = native(self.obj,self.linked,self.map)
        repeats = [b for b in r['native_records'] if b['kind'] == 'LIDATA']
        self.assertEqual([(b['start'],b['size']) for b in repeats],[(0x12A,216),(0x20E,54)])
        self.assertEqual(sum(b['size'] for b in r['native_records']),324)
        self.assertEqual(r['ordered_native_fixups'],[])

    def test_malformed_repetition_and_MAP_alignment_are_rejected(self):
        changed = mutate_record(self.obj,lambda r:r.name == 'LIDATA',lambda d:d[:3]+b'\xFF\xFF'+d[5:])
        with self.assertRaises(ValueError):
            native(changed,self.linked,self.map)
        with self.assertRaises(ValueError):
            native(self.obj,self.linked,self.map.replace(b'ACBP=48',b'ACBP=68',1))

    def test_seven_actual_native_length_definitions_bind_each_cold_round(self):
        work,_,_,_,files,maintained,cold = images(ROOT)
        changed = json.loads(cold)
        changed['rounds'][1]['directory_definitions']['ONGCHK_BYTES'] -= 1
        with self.assertRaisesRegex(ValueError,'actual linked-length'):
            verify(work,self.image,(work/'product/zun.com').read_bytes(),files,maintained,changed)

    def test_compositor_consumes_and_validates_the_complete_native_directory(self):
        d = parse_launcher(self.image,223)
        payloads = [self.image[p['decoded_file_offset']:p['decoded_file_offset']+p['size']] for p in d['payloads']]
        args = (self.image[:223],self.image[547:550],self.image[-8:],[p['name'] for p in d['payloads']],payloads)
        self.assertEqual(compose_native_launcher(*args,directory_bytes=self.linked),self.image)
        with self.assertRaisesRegex(ValueError,'native directory'):
            compose_native_launcher(*args,directory_bytes=self.linked[:-1])

    def test_all_static_DATA_and_actual_name_boundary_reader_mutations_fail(self):
        r = negative_controls(self.image)
        self.assertEqual((r['initial_DATA_byte_mutations_rejected'],r['actual_reader_DATA_mutation_count']),(324,11))
        self.assertEqual(r['instruction_mutations'],0)
        self.assertFalse(r['static_mutations_have_execution_credit'])

    def test_wrong_capacity_source_controls_emit_314_and_334_bytes(self):
        r = json.loads((ROOT/'.analysis/work/zun-build.json').read_bytes())['directory_source_controls']
        self.assertEqual([(c['capacity'],c['bytes']) for c in r['controls']],[(31,314),(33,334)])
        self.assertTrue(all(c['byte_exact_rejected'] and c['changed_source_declarations'] == ['DIRECTORY_CAPACITY'] for c in r['controls']))

    def test_unused_slots_are_semantic_format_fields_without_execution_credit(self):
        for offset in (265,546):
            changed = bytearray(self.image)
            changed[offset] ^= 1
            with self.assertRaises(ValueError):
                specification(changed)

    @unittest.skipUnless((ROOT/'.analysis/work/zun-directory-build.json').is_file(),'complete directory witness absent')
    def test_partial_readers_and_unused_slot_execution_cannot_borrow_witness(self):
        scope = json.loads((ROOT/'.analysis/work/zun-directory-build.json').read_bytes())['scope']
        for key,value in (('cases_per_image',21),('unused_slots_have_execution_credit',True)):
            changed = deepcopy(scope)
            changed['runtime'][key] = value
            with self.assertRaises(ValueError):
                witness(changed)
