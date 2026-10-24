"""Complete native ownership of the maintained -5 root, in COM coordinates."""

import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_zun_resident import decode


SOURCE = "src/zun/res_yume.cpp"
OBJECT = "obj/th03/res_yume.obj"
MAP = "obj/th03/res_yume.map"
OWNERS = (("cfg-init", 0x367, 97, "@cfg_init$qur10resident_t", "cfg_init(resident_t _seg *)"),
          ("main", 0x3C8, 225, "_main", "_main"))
MESSAGES = (
    "\n\n東方夢時空用　 常駐プログラム　RES_YUME.com Version1.00       (c)zun 1997\n",
    "わたし、まだいませんよぉ\n\n", "さよなら、また会えたらいいな\n\n",
    "そんなオプション付けられても、困るんですけど\n\n", "わたし、すでにいますよぉ\n\n",
    "作れません、わたしの居場所がないの！\n\n", "それでは、よろしくお願いします\n\n")
DEFAULTS = bytes((1, 0, 1, 0, 0))
IDENTIFIER = b"YUMEConfig\0"
DATA = b"\0" + DEFAULTS + b"yume.cfg\0" + IDENTIFIER + b"".join(s.encode("cp932") + b"\0" for s in MESSAGES)


def need(value, message):
    if not value:
        raise ValueError("ZUN resident layout: " + message)


def verify(work, target, candidate, payload_offset):
    need(len(target) == len(candidate) == 5618, "complete -5 payload")
    raw = (work / OBJECT).read_bytes()
    description = describe_omf(raw)
    need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"], "native TC4 object")
    deps = [n.replace(chr(92), "/") for n in description["dependency_paths"]]
    need(all(n in deps for n in ("th03/res_yume.cpp", SOURCE, "src/zun/cfg_init.inl", "src/zun/res_init.inl")),
         "complete maintained source dependencies")
    need(segment_definitions(raw) == [
        dict(index=1, name="_TEXT", **{"class": "CODE"}, overlay="", size=322),
        dict(index=2, name="_DATA", **{"class": "DATA"}, overlay="", size=307),
        dict(index=3, name="_BSS", **{"class": "BSS"}, overlay="", size=0)], "complete segment ownership")
    need([r.data[0] for r in parse_omf(raw) if r.name == "SEGDEF"] == [0x28, 0x48, 0x48],
         "BYTE CODE, WORD DATA/BSS, PUBLIC USE16")
    need([r["size"] for r in code_bytes(raw, 1)[1]] == [322], "complete native CODE record")
    need(code_bytes(raw, 2)[0] == DATA and len(DATA) == 307, "complete semantic initialized DATA")
    need(code_publics(raw, 1) == [(start - 0x367, public) for _, start, _, public, _ in OWNERS]
         and code_publics(raw, 2) == [(0, "_debug")] and not code_publics(raw, 3), "complete OMF publics")
    text = (work / MAP).read_text().replace(chr(92), "/")
    for start, size, cls, seg, attr in ((0x367, 322, "CODE", "_TEXT", "28"),
                                      (0x131E, 307, "DATA", "_DATA", "48"), (0x16F4, 0, "BSS", "_BSS", "48")):
        pattern = (rf"(?m)^\s*0000:{start:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+G=DGROUP"
                   rf"\s+M=th03/res_yume\.cpp\s+ACBP={attr}\s*$")
        need(len(re.findall(pattern, text)) == 1, "literal complete MAP contribution")
    for start, public in [(start, name) for _, start, _, _, name in OWNERS] + [(0x131E, "_debug")]:
        need(len(re.findall(rf"(?m)^\s*0000:{start:04X}\s+(?:idle\s+)?{re.escape(public)}\s*$", text)) == 2,
             "both MAP public tables")
    need(target[0x121E:0x1351] == candidate[0x121E:0x1351] == DATA, "complete linked DATA bytes")
    rows = []
    for name, start, size, _, _ in OWNERS:
        a, b = target[start - 0x100:start - 0x100 + size], candidate[start - 0x100:start - 0x100 + size]
        need(len(a) == len(b) == size and a == b, "complete raw procedure")
        rows.append(dict(unit_id="th03-zun-decoded-resident-" + name, source=SOURCE, object=OBJECT,
            start=start, size=size, coordinate_space="decoded-payload-com", payload_option="-5",
            payload_file_offset=start - 0x100, decoded_file_offset=payload_offset + start - 0x100,
            canonical_file_offset=None, ordered_relocations=[], format="COM",
            argument_bytes=2 if name == "cfg-init" else 4, callee_pop_bytes=0,
            target_sha256=hashlib.sha256(a).hexdigest(), candidate_sha256=hashlib.sha256(b).hexdigest()))
    need(decode(target) == decode(candidate), "complete decode, direct CFG and near cdecl ABI")
    return dict(owners=rows, code_bytes=322, data_bytes=307, bss_bytes=0, native_code_records=[322],
                map_public_table_entries=6, com_relocations=0, initialized_data_sha256=hashlib.sha256(DATA).hexdigest())
