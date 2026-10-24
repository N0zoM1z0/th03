"""Complete CODE/DATA/BSS and tiny-model public ownership of the -3 producer."""

import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_zunsoft import RANGES, decode


SOURCE = "src/zun/zunsoft.cpp"
OBJECT = "obj/th01/zunsoft.obj"
MAP = "obj/th01/zunsoft.map"
BSS_PUBLICS = tuple(zip(
    (0, 1, 2, 3, 4, 5, 6, 8, 24, 224, 226, 234, 242, 243),
    ("_page_back", "_page_front", "_tone", "_logo_patnum", "_wave_len", "_wave_phase",
     "_wave_amp", "_circle_pos", "_star_pos", "_frame",
     "_circle_speed_x", "_circle_speed_y", "_star_angle", "_star_speed")))


def need(value, message):
    if not value:
        raise ValueError("ZUN logo layout: " + message)


def verify(work, target, candidate, payload_offset):
    need(len(target) == len(candidate) == 10096, "complete -3 COM payload")
    raw = (work / OBJECT).read_bytes()
    description = describe_omf(raw)
    need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"], "native TC4 object")
    deps = [n.replace(chr(92), "/") for n in description["dependency_paths"]]
    need("th01/zunsoft.cpp" in deps and SOURCE in deps, "actual maintained source dependency")
    need(segment_definitions(raw) == [
        dict(index=1, name="_TEXT", **{"class": "CODE"}, overlay="", size=1299),
        dict(index=2, name="_DATA", **{"class": "DATA"}, overlay="", size=15),
        dict(index=3, name="_BSS", **{"class": "BSS"}, overlay="", size=293)], "complete CODE/DATA/BSS partition")
    need([r.data[0] for r in parse_omf(raw) if r.name == "SEGDEF"] == [0x28, 0x48, 0x48],
         "BYTE CODE, WORD DATA/BSS, PUBLIC and USE16")
    need([r["size"] for r in code_bytes(raw, 1)[1]] == [1017, 282], "two complete native CODE records")
    initialized = b"touhou.dat\0\4\3\2\1"
    need(code_bytes(raw, 2)[0] == initialized and not code_publics(raw, 2), "complete initialized DATA ownership")
    need(code_publics(raw, 3) == list(BSS_PUBLICS), "complete OMF BSS public layout")
    publics = []
    text = (work / MAP).read_text().replace(chr(92), "/")
    for start, size, cls, segment, attribute in ((0x367, 1299, "CODE", "_TEXT", "28"),
            (0x21CE, 15, "DATA", "_DATA", "48"), (0x2870, 293, "BSS", "_BSS", "48")):
        pattern = (rf"(?m)^\s*0000:{start:04X}\s+{size:04X}\s+C={cls}\s+S={segment}\s+G=DGROUP"
                   rf"\s+M=th01/zunsoft\.cpp\s+ACBP={attribute}\s*$")
        need(len(re.findall(pattern, text)) == 1, "literal CODE/DATA/BSS MAP contribution")
    for offset, symbol in BSS_PUBLICS:
        need(len(re.findall(rf"(?m)^\s*0000:{0x2870 + offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$", text)) == 2,
             "both BSS MAP public tables")
    need(target[0x20CE:0x20DD] == candidate[0x20CE:0x20DD] == initialized, "complete linked DATA bytes")
    rows = []
    cursor = 0x367
    for name, start, size in RANGES:
        need(start == cursor, "complete contiguous procedure ownership")
        cursor += size
        symbol = "_main" if name == "main" else "@ZUNSOFT_VECTOR2$QRIT1UCI" if name == "zunsoft_vector2" else "@" + name + "$qv"
        publics.append((start - 0x367, symbol))
        map_public = ("_main" if name == "main" else "zunsoft_vector2(int near&,int near&,unsigned char,int)"
                      if name == "zunsoft_vector2" else name + "()")
        need(len(re.findall(rf"(?m)^\s*0000:{start:04X}\s+(?:idle\s+)?{re.escape(map_public)}\s*$", text)) == 2,
             "both CODE MAP public tables")
        a, b = target[start - 0x100:start - 0x100 + size], candidate[start - 0x100:start - 0x100 + size]
        need(len(a) == len(b) == size and a == b, "complete raw procedure extent")
        rows.append(dict(unit_id="th03-zun-decoded-logo-" + name.replace("_", "-"), source=SOURCE,
            object=OBJECT, start=start, size=size, coordinate_space="decoded-payload-com", payload_option="-3",
            payload_file_offset=start - 0x100, decoded_file_offset=payload_offset + start - 0x100,
            canonical_file_offset=None, ordered_relocations=[], format="COM",
            argument_bytes=8 if name == "zunsoft_vector2" else 0,
            callee_pop_bytes=8 if name == "zunsoft_vector2" else 0,
            target_sha256=hashlib.sha256(a).hexdigest(), candidate_sha256=hashlib.sha256(b).hexdigest()))
    need(cursor == 0x87A and code_publics(raw, 1) == publics, "complete native CODE public ownership")
    need(decode(target) == decode(candidate), "complete instruction boundaries, direct CFG and near ABI")
    return dict(owners=rows, code_bytes=1299, data_bytes=15, bss_bytes=293,
                native_code_records=[1017, 282], omf_bss_publics=14, map_public_table_entries=48,
                com_relocations=0, initialized_data_sha256=hashlib.sha256(initialized).hexdigest())
