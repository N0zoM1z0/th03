"""Keep natural DATA ownership, native relocation namespaces and behavior separate."""
from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.decoded_mainl_staff_data_layout import START,SIZE,DS,OBJECT,semantic_image,native_image,verify as layout
from lib.decoded_mainl_staff_data_runtime import fixture
import review_th03_mainl_staff_data_work as review
import review_th03_mainl_sound_work as sound

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/OBJECT).is_file() and (WORK/'bin/th03/mainl.target.exe').is_file(),
                     'current private MAINL DATA producer absent')
class MainlStaffDataCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,cls.cold,cls.graph,cls.files=sound.images(ROOT)

    def test_data_adds_storage_and_no_procedures(self):
        r=layout(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['code_bytes'],r['initialized_data_bytes'],r['pointer_bytes'],r['sprite_bytes'],r['mask_bytes']),
                         (0,224,96,64,64))
        self.assertEqual((r['owners'][0]['procedure_count'],len(r['owners'][0]['procedures'])),(0,0))
        self.assertEqual(len(r['ordered_native_fields']),24)
        self.assertTrue(all((f['locat'],f['fixdat'],f['frame'],f['width'])==(0xCC,0x16,2,4)
                            for f in r['ordered_native_fields']))
        self.assertFalse(r['enclosing_CODE_or_pointees_accepted'])
        self.assertFalse(r['whole_product_accepted'])

    def test_pointer_offset_and_segment_words_remain_distinct(self):
        for load in (0x1000,0x3000):
            raw=semantic_image(load)
            self.assertEqual(struct.unpack_from('<HH',raw,0),(0xB3E,load+DS))
            self.assertEqual(struct.unpack_from('<HH',raw,220),(0xC22,load+DS))
            self.assertEqual(raw[4:132],semantic_image()[4:132])

    def test_whole_data_and_literal_order_reject_drift(self):
        at=DS*16+START
        # Cover the behavior-unobserved script segment and strength-zero row,
        # as well as the final live far pointer; no semantic use is inferred.
        for off in (2,3,68,75,223):
            raw=bytearray(self.target.program_image)
            raw[at+off]^=1
            mutant=replace(self.target,program_image=bytes(raw))
            with self.assertRaises(ValueError):
                layout(self.work,mutant,self.candidate,self.graph,self.files)
        reloc=list(self.target.relocations)
        indices=[i for i,r in enumerate(reloc) if at<=r.linear<at+SIZE]
        reloc[indices[0]],reloc[indices[1]]=reloc[indices[1]],reloc[indices[0]]
        with self.assertRaisesRegex(ValueError,'ordered MZ DATA'):
            layout(self.work,replace(self.target,relocations=tuple(reloc)),self.candidate,self.graph,self.files)

    def test_actual_consumers_reject_semantic_data_corruption(self):
        for kind,p,mutation in (('flake',(0,3),(4,0)),('mask',(1,0),(76,0)),
                               ('verdict',(0,0,0),(133,7)),('ending',(21,0),(0,0))):
            fixture(kind,self.target,0x1000,p)
            with self.assertRaisesRegex(ValueError,'semantic '):
                fixture(kind,self.target,0x1000,p,mutation)

    def test_unlinked_data_rejects_a_changed_static_zero_strength_mask(self):
        raw=bytearray((self.work/OBJECT).read_bytes())
        # Change one literal initializer in the sole DATA LEDATA, then repair
        # the record checksum. Valid OMF alone cannot accept altered semantics.
        from lib.omf import parse_omf
        record,=[r for r in parse_omf(bytes(raw)) if r.name=='LEDATA' and r.data[0]==2]
        index=bytes(raw).find(record.data)
        self.assertGreater(index,0)
        raw[index+3+68]^=1
        raw[index+len(record.data)]=(raw[index+len(record.data)]+1)&255
        with self.assertRaisesRegex(ValueError,'semantic initializer'):
            native_image(bytes(raw))

    def test_current_review_binds_complete_witness(self):
        scope=review.current_scope(ROOT,self.work,self.target,self.candidate,self.cold,self.graph,self.files)
        self.assertEqual(scope['negative_controls']['count'],1712)
        self.assertEqual(scope['runtime']['cases_per_image'],236)
        self.assertFalse(scope['negative_controls']['script_segment_WORD_behavior_controls'])


if __name__=='__main__':
    unittest.main()
