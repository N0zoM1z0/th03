"""Complete symbolic resource ownership, semantic data and consumed-root contracts."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/toolchain/wineprefix/drive_c/MPI02/th03_mainl.asm').is_file():
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
from lib import mainl_resources_source as resources
from lib.mainl_staff_source import statements

class ResourceSourceTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'config/th03_mainl_resources_source.json').read_text())
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
        out=resources.compose(self.root,self.providers,self.maintained)
        before=self.root;after=out['th03_mainl.asm']
        for name in resources.NAMES:
            old=('include libs/master.lib/'+name+'.asm').encode()
            new=('include src/mainl/resources/'+name+'.asm').encode()
            self.assertEqual(after.count(new),1)
            self.assertNotIn(old,after)
            before=before.replace(old,self.providers[name])
            after=after.replace(new,self.maintained[name])
        self.assertEqual(statements(before),statements(after))
        for path in (b'src/mainl/root/root.asm',b'src/mainl/formats/pi_decode.asm'):
            self.assertIn(path,after)
    def test_original_boundaries_and_no_premature_credit(self):
        c=self.config
        self.assertEqual(len(c['units']),14)
        self.assertEqual(sum(u['bytes'] for u in c['units']),3475)
        self.assertEqual(len(self.maintained),23)
        self.assertEqual(len({u['unit_id'] for u in c['units']}),14)
        for field in ('source_progress_changed','native_fragment_consumption_proven','exact_acceptance'):
            self.assertFalse(c[field])
    def test_rotation_table_exhaustive_semantics(self):
        rows=statements(self.maintained['rottbl'])
        values=[]
        for row in rows:
            if b'dd' in row:
                text=b' '.join(row[row.index(b'dd')+1:]).decode()
                values.extend(int(x.strip()[:-1],16) for x in text.split(','))
        self.assertEqual(len(values),256)
        expected=[sum((((v>>b)&1)|(((v>>(b+4))&1)<<1))<<(8*b) for b in range(4)) for v in range(256)]
        self.assertEqual(values,expected)
    def test_instruction_branch_even_and_dispatch_mutations_rejected(self):
        changes=[('graph_show',b'mov\tAH,40h',b'mov\tAH,41h'),('graph_gaiji_putc',b'adc\tBP',b'add\tBP'),('graph_pack_put_8',b'jle\tshort',b'jl\tshort'),('super_put',b'org\t$-2',b'org\t$-1'),('smem_wget',b'rcr\tBX,1',b'shr\tBX,1'),('graph_gaiji_putc',b'\tEVEN',b''),('rottbl',b'00000001h',b'00000002h')]
        for name,old,new in changes:
            with self.subTest(name=name,old=old):
                altered=dict(self.maintained);altered[name]=altered[name].replace(old,new,1)
                self.assertNotEqual(altered[name],self.maintained[name])
                with self.assertRaises(ValueError):resources.compose(self.root,self.providers,altered)
        for name in resources.NAMES:
            altered=dict(self.maintained);altered[name]+=b'\ndb 90h\n'
            with self.assertRaises(ValueError):resources.compose(self.root,self.providers,altered)
    def test_missing_duplicate_and_reconsumed_boundaries_rejected(self):
        for name in resources.NAMES:
            marker=('include libs/master.lib/'+name+'.asm').encode()
            for carrier in (self.root.replace(marker,b''),self.root+b'\n'+marker):
                with self.assertRaises(ValueError):resources.compose(carrier,self.providers,self.maintained)
        out=resources.compose(self.root,self.providers,self.maintained)
        with self.assertRaises(ValueError):resources.compose(out['th03_mainl.asm'],self.providers,self.maintained)
        missing=dict(self.maintained);missing.pop('rottbl')
        with self.assertRaises(ValueError):resources.compose(self.root,self.providers,missing)
    def test_no_overwrite_stage(self):
        out=resources.compose(self.root,self.providers,self.maintained)
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'stage';resources.stage(dest,out)
            with self.assertRaises(FileExistsError):resources.stage(dest,out)
            self.assertEqual(out,{name:(dest/name).read_bytes() for name in out})
if __name__=='__main__':unittest.main()
