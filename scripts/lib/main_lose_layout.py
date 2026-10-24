"""Recover the complete loss-animation producer without retained ASM body bytes."""

import hashlib
import re

from lib.omf import describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

BODY_SHA = "a0d21ec9d6d5c48445ed00f1f02a392daf0da9080dc7f247f5b9a29895e767da"
SYMBOL = "@player_stuff_t@lose_render$qv"


def need(value, message):
    if not value:
        raise ValueError("loss producer layout: " + message)


def detach(text):
    pattern = (r"public @PLAYER_LOSE_ANIM_RENDER\$QP14PLAYER_STUFF_T\n"
               r"@PLAYER_LOSE_ANIM_RENDER\$QP14PLAYER_STUFF_T label near\n"
               r"sub_C248\s+proc near.*?sub_C248\s+endp")
    match, = list(re.finditer(pattern, text, re.S))
    need(hashlib.sha256(match[0].encode("latin1")).hexdigest() == BODY_SHA,
         "pinned renderer body differs")
    return text[:match.start()] + "extrn " + SYMBOL + ":near" + text[match.end():]


def verify(work, target, candidate):
    raw = (work / "obj/th03/lose.obj").read_bytes()
    description = describe_omf(raw)
    need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"],
         "valid native TC4 object required")
    positive = [s for s in segment_definitions(raw) if s["size"]]
    need([(s["name"], s["class"], s["size"]) for s in positive]
         == [("PLAYER_M_TEXT", "CODE", 664)], "complete CODE or private DATA/BSS differs")
    segment = positive[0]["index"]
    need([r["size"] for r in code_bytes(raw, segment)[1]] == [664], "single complete native record required")
    publics = [(0, "@PLAYER_LOSE_ANIM_UPDATE$QP14PLAYER_STUFF_T"),
               (270, "@PLAYER_LOSE_PARTICLE_PUT$QUCUC"), (368, SYMBOL),
               (545, "@round_defeat_banners_render$qv")]
    need(code_publics(raw, segment) == publics, "complete native public set differs")
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    need(len(re.findall(r"(?m)^\s*096E:29F8\s+0298\s+C=CODE\s+S=PLAYER_M_TEXT"
                        r"\s+G=MAIN_01\s+M=src/main/player/lose\.cpp\s+ACBP=28\s*$", map_text)) == 1,
         "literal native MAP contribution differs")
    for offset, symbol in publics:
        if offset == 0:
            symbol = "player_lose_anim_update(player_stuff_t near*)"
        elif offset == 270:
            symbol = "player_lose_particle_put(unsigned char,unsigned char)"
        elif symbol == SYMBOL:
            symbol = "player_stuff_t::lose_render()"
        elif symbol == "@round_defeat_banners_render$qv":
            symbol = "round_defeat_banners_render()"
        need(len(re.findall(rf"(?m)^\s*096E:{0x29F8 + offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$",
                            map_text)) == 2, "both literal MAP public tables required")
    lo, hi = 0xC0D8, 0xC370
    need(candidate.program_image[lo:hi] == target.program_image[lo:hi], "complete linked loss CODE differs")
    vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi]
               for image in (target, candidate)]
    need(vectors[0] == vectors[1] and len(vectors[0]) == 10, "ten literal relocation pairs required")
    return dict(functions=4, code_bytes=664, code_record_sizes=[664], native_publics=4,
                literal_public_table_entries=8, ordered_relocations=10, private_data_bytes=0)
