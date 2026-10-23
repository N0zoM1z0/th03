"""Complete symbolic display/hardware ownership, mutable dispatch and consumed-root contracts."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/toolchain/wineprefix/drive_c/MIA02/th03_mainl.asm').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib import mainl_display_hardware_source as display_hardware
from lib.mainl_staff_source import statements

class DisplayHardwareSourceTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'config/th03_mainl_display_hardware_source.json').read_text())
        def load(row):
            raw=(ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            return raw
        self.root=load(self.config['previous_generated_root'])
        load(self.config['composer'])
        self.providers={};self.maintained={}
        for unit in self.config['units']:
            for row in unit['providers']:
                self.providers[row['name']]=load(row['provider'])
                self.maintained[row['name']]=load(row['source'])
    def test_complete_consumption_and_unchanged_statement_expansion(self):
        out=display_hardware.compose(self.root,self.providers,self.maintained)
        before=self.root;after=out['th03_mainl.asm']
        for name in display_hardware.NAMES:
            old=('include '+display_hardware.PROVIDER_PATHS[name]).encode()
            new=('include src/mainl/display_hardware/'+name+'.asm').encode()
            self.assertEqual(after.count(new),1)
            self.assertNotIn(old,after)
            before=before.replace(old,self.providers[name])
            after=after.replace(new,self.maintained[name])
        self.assertEqual(statements(before),statements(after))
        for path in (b'src/mainl/root/root.asm',b'src/mainl/formats/pi_decode.asm'):
            self.assertIn(path,after)
    def test_original_boundaries_and_no_premature_credit(self):
        c=self.config
        self.assertEqual(len(c['units']),16)
        self.assertEqual(sum(u['bytes'] for u in c['units']),2116)
        self.assertEqual(len(self.maintained),20)
        self.assertEqual(len({u['unit_id'] for u in c['units']}),16)
        for field in ('source_progress_changed','native_fragment_consumption_proven','exact_acceptance'):
            self.assertFalse(c[field])
    def test_instruction_branch_even_and_dispatch_mutations_rejected(self):
        changes=[('vsync',b'iret',b'retf'),('vsync',b'\tCLI',b'\tSTI'),('vsync',b'\tEVEN',b''),('palette_show',b'CS:PALSHOW_XORVAL',b'DS:PALSHOW_XORVAL'),('gaiji_entry_bfnt',b'jne\tshort',b'je\tshort'),('graph_copy_page',b'rep\tmovsw',b'rep\tmovsb'),('grcg_boxfill',b'\tCLI',b'\tCLD')]
        for name,old,new in changes:
            with self.subTest(name=name,old=old):
                altered=dict(self.maintained);altered[name]=altered[name].replace(old,new,1)
                self.assertNotEqual(altered[name],self.maintained[name])
                with self.assertRaises(ValueError):display_hardware.compose(self.root,self.providers,altered)
        for name in display_hardware.NAMES:
            altered=dict(self.maintained);altered[name]+=b'\ndb 90h\n'
            with self.assertRaises(ValueError):display_hardware.compose(self.root,self.providers,altered)
    def test_missing_duplicate_and_reconsumed_boundaries_rejected(self):
        for name in display_hardware.NAMES:
            marker=('include '+display_hardware.PROVIDER_PATHS[name]).encode()
            for carrier in (self.root.replace(marker,b''),self.root+b'\n'+marker):
                with self.assertRaises(ValueError):display_hardware.compose(carrier,self.providers,self.maintained)
        out=display_hardware.compose(self.root,self.providers,self.maintained)
        with self.assertRaises(ValueError):display_hardware.compose(out['th03_mainl.asm'],self.providers,self.maintained)
        missing=dict(self.maintained);missing.pop('vsync')
        with self.assertRaises(ValueError):display_hardware.compose(self.root,self.providers,missing)
    def test_no_overwrite_stage(self):
        out=display_hardware.compose(self.root,self.providers,self.maintained)
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'stage';display_hardware.stage(dest,out)
            with self.assertRaises(FileExistsError):display_hardware.stage(dest,out)
            self.assertEqual(out,{name:(dest/name).read_bytes() for name in out})
if __name__=='__main__':unittest.main()
