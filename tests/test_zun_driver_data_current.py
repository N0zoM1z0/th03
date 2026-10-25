"""Reject wrong widths, pointer order, stale raw defaults and reserve ownership."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_driver_data_layout import declarations, verify
from lib.zun_driver_data_runtime import Machine, specification, negative_controls
from review_th03_zun_data_work import witness
from review_th03_zun_format_work import images

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'


@unittest.skipUnless((WORK/'driver/driver.com').is_file(),'private current driver absent')
class DataOwnership(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = (WORK/'driver/driver.com').read_bytes()

    def test_omf_fields_and_owned_spans_exclude_both_reserved_runs(self):
        work,target,candidate,at,files,maintained,cold = images(ROOT)
        result = verify(work,target,candidate,at,files,maintained)
        self.assertEqual((result['code_bytes'],result['data_bytes'],len(result['ordered_native_fixups'])),(2,1294,25))
        owned = {a for o in result['owners'] for a in range(o['start'],o['start']+o['size'])}
        self.assertEqual(len(owned),1296)
        self.assertFalse(owned & (set(range(0x116D,0x1170)) | set(range(0x1177,0x1180))))
        self.assertFalse(result['enclosing_driver_accepted'])

    def test_source_WORD_width_and_nonterminated_alphabet_are_not_interchangeable(self):
        work,target,candidate,at,files,maintained,cold = images(ROOT)
        changed = dict(maintained)
        changed['src/zun/driver_data.inl'] = changed['src/zun/driver_data.inl'].replace(
            b'sprite16_interrupt_number\tdb 42h',b'sprite16_interrupt_number\tdw 42h')
        with self.assertRaises(ValueError):
            declarations(changed['src/zun/driver_data.inl'].decode())
        changed = dict(maintained)
        changed['src/zun/driver.asm'] = changed['src/zun/driver.asm'].replace(
            b"db '0123456789ABCDEF'",b"db '0123456789ABCDEF',0")
        with self.assertRaisesRegex(ValueError,'alphabet source'):
            verify(work,target,candidate,at,files,changed)

    def test_every_semantic_DATA_byte_mutation_and_actual_consumers_reject(self):
        result = negative_controls(self.image)
        self.assertEqual(result['data_byte_mutations_rejected'],1294)
        self.assertEqual((result['header_instruction_mutations'],result['consumed_data_mutations']),(1,6))
        self.assertFalse(result['data_mutations_are_instruction_execution'])

    def test_raw_defaults_are_checked_without_replacing_them_with_fixtures(self):
        for load in (0x1000,0x3000):
            machine = Machine(self.image,load)
            try:
                result = machine.contracts()
                self.assertEqual(result['cases'],142)
                self.assertTrue(result['raw_data_preserved_on_load'])
            finally:
                machine.close()

    def test_reserve_changes_have_no_semantic_DATA_ownership_credit(self):
        before = specification(self.image)
        changed = bytearray(self.image)
        for address in (*range(0x116D,0x1170),*range(0x1177,0x1180)):
            changed[address-256] = 0xA5
        self.assertEqual(specification(changed),before)

    @unittest.skipUnless((ROOT/'.analysis/work/zun-data-build.json').is_file(),'complete DATA witness absent')
    def test_fixtured_defaults_and_reserved_ownership_cannot_borrow_new_witness(self):
        scope = json.loads((ROOT/'.analysis/work/zun-data-build.json').read_bytes())['scope']
        for section,key,value in (('runtime','default_state_replaced',True),
                                  ('layout','reserved_spans_owned',True),
                                  ('runtime','cases_per_image',142)):
            changed = deepcopy(scope)
            changed[section][key] = value
            with self.assertRaises(ValueError):
                witness(changed)
