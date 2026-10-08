"""No runtime tools; negative controls for the compiler-generated HUD stitch."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.tc4_omf_bridge import _record
from lib.omf import parse_omf
from lib.hud_tc4_bridge import (
    stitch_hud_compiler_asm,
    reverse_hud_fixupp_order,
    validate_hud_stitch_recipe,
)


class HudStitchControls(unittest.TestCase):
    def synthetic_compiler(self, name):
        # Three CODE segments: zero-byte declaration, actual function and
        # zero-byte segment footer, the exact compiler layout required.
        seg=b"PLAYER_M_TEXT\tsegment byte public use16 'CODE'\r\n"
        end=b"PLAYER_M_TEXT\tends\r\n"
        first=b"\t.386p\r\n"+seg+end
        head=b"DGROUP\tgroup\t_DATA,_BSS\r\nMAIN_01\tgroup\tPLAYER_M_TEXT\r\n"
        body=(b"PUBLIC "+name+b"\r\n"+name+b"\tproc near\r\n"
              +b'\r\n'.join((f'@1@{i}'.encode()+b':\t nop'
                             for i in range(9)))+b"\r\n"
              +name+b"\tendp\r\n")
        return first+head+seg+body+end+seg+end+b"\tpublic\t"+name+b"\r\n\tend\r\n"

    def setUp(self):
        self.state=self.synthetic_compiler(b"_hud_start_anim_update")
        self.render=self.synthetic_compiler(b"_hud_start_anim_render")
        self.low=(b".386\nPLAYER_M_TEXT segment byte public 'CODE' use16\n"
                  b"HUD_START_SPRITE_STRIP_PUT proc near\n"
                  b" ret 8\nHUD_START_SPRITE_STRIP_PUT endp\n"
                  b"HUD_START_PARTICLE_PIXEL_PUT proc near\n"
                  b" ret 4\nHUD_START_PARTICLE_PIXEL_PUT endp\n"
                  b"PLAYER_M_TEXT ends\nend\n")

    def test_stitch_has_all_semantic_producers_and_one_end(self):
        asm=stitch_hud_compiler_asm(self.state,self.render,self.low)
        self.assertIn(b"HUD_START_SPRITE_STRIP_PUT proc near",asm)
        self.assertIn(b"HUD_START_PARTICLE_PIXEL_PUT proc near",asm)
        self.assertIn(b"_hud_start_anim_update\tproc near",asm)
        self.assertIn(b"_hud_start_anim_render\tproc near",asm)
        self.assertIn(b"HUDR_L_0",asm)
        self.assertNotIn(b"@1@0",asm[asm.index(b"_hud_start_anim_render\tproc near"):])
        self.assertEqual(asm.count(b"\tend\r\n"),1)

    def test_truncated_synthetic_source_refused(self):
        for data in (b"",self.state.replace(b"\t.386p",b""),self.state.replace(b"_hud_start_anim_update",b"other")):
            with self.subTest(data=data[:28]),self.assertRaises(ValueError):
                stitch_hud_compiler_asm(data,self.render,self.low)
        with self.assertRaises(ValueError):
            stitch_hud_compiler_asm(self.state,self.render,self.low.replace(b"PARTICLE_PIXEL_PUT",b"OTHER"))

    def fake_omf(self):
        hdr=_record(0x80,b"\x08h_stitch")
        part0=_record(0xa0,b"\x01\x00\x00"+b"\x90"*1007)
        part1=_record(0xa0,b"\x01\xef\x03"+b"\x90"*471)
        def fixups(count):
            arr=[]
            for i in range(count):
                location=8+i*6
                arr.append(bytes((0xC4+(location>>8),location&255,0x16,1,7)))
            return _record(0x9c,b"".join(arr))
        return hdr+part0+fixups(87)+part1+fixups(57)+_record(0x8a,b"\0")

    def test_exact_records_reverse_without_mutating_code_or_targets(self):
        native=self.fake_omf()
        changed=reverse_hud_fixupp_order(native)
        r=parse_omf(native);c=parse_omf(changed)
        self.assertEqual(len(r),len(c))
        for a,b in zip(r,c):
            if a.record_type not in (0x9c,):
                self.assertEqual(a.data,b.data)
        self.assertNotEqual(r[2].data,c[2].data)
        self.assertEqual(r[2].data[:5],c[2].data[-5:])
        with self.assertRaises(ValueError):
            reverse_hud_fixupp_order(changed)

    def test_missing_record_and_bad_fixup_fail(self):
        native=self.fake_omf()
        records=list(parse_omf(native))
        missing=native.replace(b"\x01\xef\x03",b"\x01\xf0\x03",1)
        with self.assertRaises(ValueError):
            reverse_hud_fixupp_order(missing)
        bad=bytearray(records[2].data)
        bad[2]=0x99
        patched=b"".join(_record(x.record_type,bytes(bad) if i==2 else x.data)
                         for i,x in enumerate(records))
        with self.assertRaises(ValueError):
            reverse_hud_fixupp_order(patched)

    def test_exact_recipe_only(self):
        info=dict(object="h_stitch",object_path="obj/th03/h_stitch.obj",
                  wrapper="th03/h_stitch.asm",
                  source="src/main/hud/start_anim.cpp",
                  translator_comment="Turbo Assembler  Version 5.0",
                  wrapper_prefix="",hud_tc4_stitch="hud-roundintro-1478")
        self.assertEqual(validate_hud_stitch_recipe(info),info["wrapper"])
        for edit in ({"hud_tc4_stitch":"arbitrary"}, {"object":"h_other"},
                     {"wrapper":"../escape.asm"},{"source":"src/unknown.asm"}):
            with self.subTest(edit=edit),self.assertRaises(ValueError):
                validate_hud_stitch_recipe({**info,**edit})


if __name__ == "__main__":
    unittest.main()
