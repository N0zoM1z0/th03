"""Bounded command ownership, malformed input and actual guest mutations."""
from pathlib import Path
import shutil
import struct
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun import parse_launcher
from lib.zun_driver_command_layout import verify, RANGES
from lib.zun_driver_command_runtime import Machine, negative_controls, COUNT, VECTOR, CURSOR
from lib.zun_work_source import compose

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'


@unittest.skipUnless((WORK/'product/zun.target.com').is_file(),'private current native ZUN absent')
class CurrentCommand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(WORK/'product/zun.target.com').read_bytes();child=parse_launcher(raw,223)['payloads'][3]
        cls.offset=child['decoded_file_offset'];cls.target=raw[cls.offset:cls.offset+child['size']]
        cls.candidate=(WORK/'driver/driver.com').read_bytes();cls.files,cls.maintained,_=compose(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_whole_native_contribution_has_nine_owners_and_thirty_ordered_fixups(self):
        result=verify(WORK,self.target,self.candidate,self.offset,self.files,self.maintained)
        self.assertEqual((result['functions'],result['code_bytes']),(9,361))
        self.assertEqual((result['private_data_bytes'],result['private_bss_bytes']),(0,0))
        fixups=result['ordered_native_fixups'];self.assertEqual(len(fixups),30)
        self.assertEqual(sum(f['self_relative'] for f in fixups),7)
        self.assertEqual({o['origin'] for o in result['owners']},{'library'})
        self.assertFalse(result['reserved_spans_owned']);self.assertFalse(result['enclosing_driver_accepted'])
        self.assertTrue(all(o['canonical_file_offset'] is None for o in result['owners']))
    def test_changed_actual_include_cannot_borrow_current_ownership(self):
        with TemporaryDirectory() as name:
            work=Path(name);shutil.copytree(WORK/'driver',work/'driver')
            path=next(p for p in (work/'driver/procs').glob('*.inc') if b'public sprite16_tokenize_command\r\n' in p.read_bytes())
            path.write_bytes(path.read_bytes().replace(b'push\tax',b'push\tbx',1))
            with self.assertRaisesRegex(ValueError,'consumed command include'):
                verify(work,self.target,self.candidate,self.offset,self.files,self.maintained)
    def test_quote_tail_is_skipped_and_semicolon_only_terminates_at_token_start(self):
        m=self.machine();text=b'"a,b"suffix next;part ;ignored'
        m.run('tokenize_command',text=text,flags=0xED7)
        count=int.from_bytes(m.uc.mem_read(m.base+COUNT,2),'little');self.assertEqual(count,2)
        pointers=struct.unpack('<2H',bytes(m.uc.mem_read(m.base+VECTOR,4)))
        self.assertEqual(pointers,(0x3002,0x3001+text.index(b'next')))
        self.assertEqual(m.uc.mem_read(m.base+0x3001+text.index(b';ignored'),1),b'\0')
    def test_sixty_fifth_token_overwrites_cursor_without_capacity_check(self):
        m=self.machine();m.run('tokenize_command',text=b' '.join([b'x']*65))
        self.assertEqual(int.from_bytes(m.uc.mem_read(m.base+COUNT,2),'little'),65)
        self.assertEqual(int.from_bytes(m.uc.mem_read(m.base+CURSOR,2),'little'),0x3081)
    def test_optional_number_keeps_the_inverted_legacy_branch(self):
        m=self.machine()
        row=m.run('optional_number_legacy',arguments=(b'garbage',),flags=0xED7)
        self.assertEqual((row['registers']['ax'],row['result_flags']&1),(0,0))
        row=m.run('optional_number_legacy',text=b'ffh',remaining=0)
        self.assertEqual((row['registers']['ax'],row['result_flags']&1),(255,0))
        self.assertEqual([w[2] for w in row['writes']],[0,ord('h')])
    def test_error_print_helper_uses_ss_and_terminal_status_one(self):
        m=self.machine();row=m.run('tokenize_command',text=b'"open',split_stack=True)
        self.assertTrue(row['exit']);self.assertEqual(row['registers']['ax'],0x4C01)
        self.assertEqual(bytes(row['output']),b'foreign SS quote\r\n')
        self.assertEqual(m.r('sp'),0xF800-12)
    def test_dispatch_zero_count_still_advances_and_reads_the_vector(self):
        m=self.machine();row=m.run('dispatch_options',arguments=(),flags=0xED7)
        self.assertEqual(row['registers']['si'],0xDEAD);self.assertEqual(row['callbacks'],[])
        self.assertEqual(row['writes'],[(m.base+CURSOR,2,VECTOR),(m.base+CURSOR,2,VECTOR+2)])
    def test_real_option_targets_and_callback_argument_consumption(self):
        m=self.machine();row=m.run('dispatch_options',arguments=(b'-r',b'123',b'/Z',b'456'),callback_consume=True,flags=0xED7)
        self.assertEqual(row['callbacks'],[0x2AD,0x243])
        self.assertEqual(row['registers']['es'],0x3000)
        self.assertEqual(row['registers']['si'],0xDEAD)
        self.assertFalse(row['exit'])
    def test_cursor_wrap_carry_and_scanner_flags(self):
        m=self.machine()
        for kind in ('require_argument','optional_argument'):
            row=m.run(kind,cursor=0xFFFF,flags=0xED7)
            self.assertEqual(row['result_flags']&1,int(kind=='require_argument'))
            self.assertEqual(row['registers']['si'],0x4001)
        for kind in ('skip_separators','find_token_end','find_quote_end'):
            m.run(kind,text=b' \t,abc\r',flags=0xED7,split_stack=True)
    def test_nineteen_actual_guest_changes_fail_independent_contracts(self):
        self.assertEqual(negative_controls(self.target)['count'],19)
