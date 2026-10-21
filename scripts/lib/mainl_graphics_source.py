"""Source-only MAINL graphics composition. No OMF or executable edits."""
from pathlib import Path
import hashlib

def replace_once(raw, old, new):
    if raw.count(old) != 1:
        raise ValueError("source boundary is not unique: " + repr(old))
    return raw.replace(old, new, 1)

def generate(root_asm, maintained):
    # Work with byte-preserving source text: assembly may contain Shift-JIS.
    raw = root_asm.replace(b"\r\n", b"\n")
    code = maintained.replace(b"\r\n", b"\n")
    original_group = b"group_01 group CFG_LRES_TEXT, MAINL_SC_TEXT, CUTSCENE_TEXT, SCOREDAT_TEXT, REGIST_TEXT, STAFF_TEXT, mainl_03_TEXT"
    raw = replace_once(raw, original_group, original_group + b", MAINL_SNOW_TEXT, MAINL_DISSOLVE_TEXT, MAINL_STAFF_TEXT")
    begin = b"mainl_03_TEXT segment byte public 'CODE' use16\ninclude th03/formats/cdg_unput_upwards.asm"
    newbegin = b"""mainl_03_TEXT segment byte public 'CODE' use16
 extern CDG_UNPUT_FOR_UPWARDS_MOTION_E_8:near
 extern _mainl_clear_blue:near
mainl_03_TEXT ends
MAINL_SNOW_TEXT segment byte public 'CODE' use16"""
    raw = replace_once(raw, begin, newbegin)
    start = raw.index(b"sub_BB51\tproc near")
    end = raw.index(b"sub_BB51\tendp", start) + len(b"sub_BB51\tendp")
    raw = raw[:start] + raw[end:]
    raw = raw.replace(b"sub_BB51", b"_mainl_clear_blue")
    marker = b"include th03/formats/cdg_put_dissolve.asm"
    replacement = b"""MAINL_SNOW_TEXT ends
MAINL_DISSOLVE_TEXT segment byte public 'CODE' use16
 extern CDG_PUT_DISSOLVE_E_8:near
MAINL_DISSOLVE_TEXT ends
MAINL_STAFF_TEXT segment byte public 'CODE' use16"""
    raw = replace_once(raw, marker, replacement)
    raw = replace_once(raw, b"mainl_03_TEXT\tends", b"MAINL_STAFF_TEXT ends")
    for old, alias in [(b"byte_10BC7\tdb ?", b"_mainl_dissolve_alpha_enabled"),
                       (b"byte_10BB5\tdb ?", b"_mainl_dissolve_alpha_requested")]:
        raw = replace_once(raw, old, b"public " + alias + b"\n" + alias + b" label byte\n" + old)
    old = b"include th03/formats/cdg_put_dissolve[data].asm"
    raw = replace_once(raw, old, b"public _mainl_dissolve_pattern\n_mainl_dissolve_pattern label word\n" + old)
    # Near CALL takes a FAR pointer: original PUSH DWORD memory then CALL.
    raw = replace_once(raw, b"\t\tcall\t@cutscene_script_load$qnxc pascal, [off_EE4E]", b"\t\tpush\tdword ptr [off_EE4E]\n\t\tcall\t@cutscene_script_load$qnxc")
    unput = code.index(b'extern "C" void near pascal cdg_unput_for_upwards_motion_e_8(')
    dissolve = code.index(b'extern "C" void near pascal cdg_put_dissolve_e_8(')
    header = code[:unput]
    prefix = code[:dissolve]
    effect = header + code[dissolve:]
    effect = replace_once(effect, b'#pragma option -zCMAINL_03_TEXT', b'#pragma option -zCMAINL_DISSOLVE_TEXT')
    return {"th03_mainl.asm": raw.replace(b"\n", b"\r\n"),
            "gfxpre.cpp": prefix.replace(b"\n", b"\r\n"),
            "gfxdis.cpp": effect.replace(b"\n", b"\r\n")}
