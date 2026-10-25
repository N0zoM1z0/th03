"""Native source/COM/BSS closure, without borrowing scoped exact ownership."""
from pathlib import Path
import csv,json,struct,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_ongchk_source import verify_outputs,SOURCE
from lib.zun_work_source import compose
from review_th03_ongchk import runtime_case
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'

@unittest.skipUnless((WORK/'ongchk/ongchk.com').is_file(),'current private native ONGCHK absent')
class OngchkSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj,cls.com,cls.map=[(WORK/('ongchk/ongchk.'+ext)).read_bytes() for ext in ('obj','com','map')]
    def test_whole_native_image_and_uninitialized_workspace_have_separate_extents(self):
        r=verify_outputs(self.obj,self.com,self.map,self.com)
        self.assertEqual((r['file_bytes'],r['code_bytes'],r['initialized_data_bytes'],r['bss_bytes']),(926,892,34,42))
        self.assertEqual(len(r['native_fields']),38);self.assertEqual(len(r['bss_publics']),7)
        self.assertFalse(r['binary_seed_consumed']);self.assertFalse(r['exact_acceptance'])
        self.assertFalse(r['original_source_identity_attested']);self.assertFalse(r['original_assembler_identity_attested'])
    def test_changed_linked_and_target_bytes_cannot_hide_native_mismatch(self):
        changed=bytearray(self.com);changed[0]^=1
        with self.assertRaisesRegex(ValueError,'complete resolved native COM bytes'):
            verify_outputs(self.obj,bytes(changed),self.map,bytes(changed))
    def test_equal_COM_bytes_do_not_prove_a_changed_BSS_extent(self):
        raw=self.obj;out=bytearray();at=0;changed=False
        while at<len(raw):
            kind=raw[at];size=int.from_bytes(raw[at+1:at+3],'little');payload=bytearray(raw[at+3:at+2+size])
            if kind==0x98 and payload[:3]==b'\x48\x2A\0':
                payload[1]=43;changed=True
            record=bytes([kind])+struct.pack('<H',size)+bytes(payload)
            out+=record+bytes([-sum(record)&255]);at+=3+size
        self.assertTrue(changed)
        with self.assertRaisesRegex(ValueError,'meaningful uninitialized workspace'):
            verify_outputs(bytes(out),self.com,self.map,self.com)
    def test_missing_BSS_public_in_either_MAP_table_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'both MAP public tables'):
            verify_outputs(self.obj,self.com,self.map.replace(b'ram_buffer',b'bad_buffer',1),self.com)
    def test_priority_reads_PSP_length_before_looking_at_tail_characters(self):
        boards=((0x188,3),(0x88,2))
        for tail,result,order in (('8',5,[3]),('x'*56,4,[2]),('8'+' '*31,4,[2])):
            r=runtime_case(self.com,tail=tail,boards=boards)
            self.assertEqual((r['result'],r['detector_order']),(result,order))
    def test_write_timeout_and_read_stall_are_distinct_terminal_contracts(self):
        r=runtime_case(self.com,boards=((0x188,3),),ram='write-timeout')
        self.assertEqual((r['stop']['kind'],r['result'],r['ram_bytes_written']),('modeled-dos-exit',3,1))
        r=runtime_case(self.com,boards=((0x188,3),),ram='read-ready-stall',instruction_budget=100000)
        self.assertEqual((r['stop']['kind'],r['phase'],r['ram_bytes_written']),('instruction-budget','read',32))
    def test_native_source_candidate_is_distinct_from_full_instruction_acceptance(self):
        publication=json.loads((ROOT/'config/zun_work/scoped_acceptance.json').read_bytes())
        self.assertFalse(publication['audit']['ongchk_source_candidate']['exact_acceptance'])
        self.assertEqual(len(publication['owner_oracles']),77)
        self.assertIn('th03-zun-decoded-ongchk',publication['owner_oracles'])
        self.assertEqual(publication['audit']['scope']['ongchk']['runtime']['executed_owner_bytes'],892)

@unittest.skipUnless((ROOT/'_reference/ReC98/.git').exists(),'private reference archive absent')
class OngchkSourceGraph(unittest.TestCase):
    def test_all_payloads_are_produced_and_only_the_declared_vendor_library_is_a_binary_input(self):
        files,maintained,context=compose(ROOT)
        self.assertNotIn('libs/kaja/ongchk.com',files)
        self.assertNotIn('ongchk/ongchk.com',files)
        self.assertEqual({n for n in files if Path(n).suffix.lower() in ('.com','.obj','.exe','.lib','.map')},{'bin/masters.lib'})
        self.assertEqual([v['path'] for v in context['vendor_inputs']],['bin/masters.lib'])
        self.assertEqual(files['ongchk/ongchk.asm'],maintained[SOURCE].replace(b'\n',b'\r\n'))

class OngchkLedger(unittest.TestCase):
    def test_recovered_source_keeps_library_origin_and_no_canonical_offset(self):
        with (ROOT/'config/units.csv').open() as f:unit=next(r for r in csv.DictReader(f) if r['id']=='th03-zun-decoded-ongchk')
        self.assertEqual((unit['state'],unit['source'],unit['origin'],unit['file_offset']),('source-present',SOURCE,'library',''))
        self.assertEqual((int(unit['size']),int(unit['compare_size'])),(926,926))
