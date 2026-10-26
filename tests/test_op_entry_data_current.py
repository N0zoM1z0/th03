"""Initialized OP storage must not become invented CODE or file-backed BSS."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_entry_data_layout import DS,START,SIZE,semantic_image,verify as layout
from lib.op_entry_data_runtime import fixture
from review_th03_op_cfg_work import images
import review_th03_op_entry_data_work as review


@unittest.skipUnless((ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpEntryDataCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)

    def test_entire_semantic_initializer_and_non_file_backed_BSS_boundary(self):
        result=layout(ROOT,self.work,self.target,self.candidate)
        self.assertEqual((len(semantic_image()),len(result['publics']),len(result['declarations'])),(487,27,46))
        self.assertEqual((result['functions'],result['code_bytes'],result['initialized_data_bytes'],result['bss_bytes']),(0,0,487,0))
        self.assertEqual(result['ordered_relocations'],[])
        self.assertEqual(len(self.target.program_image),DS*16+0x118A)
        self.assertFalse(result['BSS_file_backed'])

    def test_equal_mutated_unused_storage_cannot_inherit_native_ownership(self):
        raw=bytearray(self.target.program_image)
        raw[DS*16+START+173]^=1
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'initialized DATA equality'):
            layout(ROOT,self.work,bad,bad)
        # The unused type-string array has no behavior-mutation credit.
        _,read=fixture(self.target,0x3000,'render',('main',dict(selection=0)),(173,0))
        self.assertNotIn(173,read)
        # A noncanonical true encoding still follows the same native bool branch.
        _,read=fixture(self.target,0x3000,'main',None,(211,7))
        self.assertIn(211,read)

    def test_added_or_straddling_DATA_relocation_is_rejected(self):
        for offset in (START-1,START+1):
            relocation=replace(self.target.relocations[0],segment=DS,offset=offset)
            bad=replace(self.target,relocations=(*self.target.relocations,relocation))
            with self.assertRaisesRegex(ValueError,'empty ordered MZ vector'):
                layout(ROOT,self.work,bad,bad)

    def test_actual_CRT_observes_zero_template_bytes_later_overwritten(self):
        with self.assertRaisesRegex(ValueError,'semantic actual CRT zero-template stack output'):
            fixture(self.target,0x3000,'startup',{},(1,0))

    def test_unnamed_string_is_still_read_through_unchecked_story_index(self):
        for character,offset,held in ((221,126,True),(229,130,False)):
            row,read=fixture(self.target,0x3000,'story',('alias',character))
            self.assertEqual(row['result']['nonterminal'],held)
            self.assertIn(offset,read)

    def test_numeric_high_bit_is_checked_at_the_real_native_register_transfer(self):
        with self.assertRaisesRegex(ValueError,'semantic native numeric register transfer'):
            fixture(self.target,0x3000,'story',1,(16,7))

    def test_demo_BYTE_wrap_reads_real_neighboring_VS_and_pairing_data(self):
        row,read=fixture(self.target,0x3000,'demo',255)
        events=row['result']['events']
        self.assertIn(('store',0x60031+0xC,1,0x8F),events)
        self.assertIn(('store',0x60031+0x10,4,0x05090B07),events)
        self.assertTrue({50,51,56,57,58,59}<=read)

    def test_witness_cannot_turn_DATA_or_static_bits_into_new_procedures(self):
        scope=json.loads(review.REPORT.read_bytes())['scope']
        review.witness(scope)
        for path,value in ((('layout','functions'),1),(('layout','BSS_file_backed'),True),
                           (('runtime','observations',0,'initialized_bytes_read'),487),
                           (('negative_controls','actual_initializer_bit_mutations'),3896)):
            bad=deepcopy(scope)
            at=bad
            for key in path[:-1]:at=at[key]
            at[path[-1]]=value
            with self.assertRaises(ValueError):review.witness(bad)

    def test_all_prior_32_owner_and_scope_observations_remain_identical(self):
        path='config/op_work/scoped_acceptance.json'
        old=json.loads(subprocess.check_output(['git','show',review.BASELINE+':'+path],cwd=ROOT))['audit']['scope']
        current=json.loads((ROOT/path).read_bytes())['audit']['scope']
        by_id={o['unit_id']:o for o in current['owners']}
        self.assertTrue(all(by_id[o['unit_id']]==o for o in old['owners']))
        self.assertEqual({k:v for k,v in old.items() if k!='owners'},
                         {k:v for k,v in current.items() if k not in ('owners','entry_data')})


if __name__=='__main__':unittest.main()
