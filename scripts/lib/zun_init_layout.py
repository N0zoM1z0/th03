"""Complete original-ASM -2 ownership, native fixups and source lineage."""

import hashlib
import json
from pathlib import Path
import re
import subprocess

from lib.omf import parse_omf
from verify_th03_zun_init_standalone import verify_outputs, parse_object

ROOT = Path(__file__).resolve().parents[2]
SOURCE, OBJECT, MAP = "src/zun/init.asm", "init/init.obj", "init/init.map"
NAMES = ("start", "error_interrupt", "stop_interrupt", "copy_interrupt", "show_key_message",
         "convert_character_word", "draw_doublebyte_text", "print_banner_and_detect_resident", "parse_install_or_remove")


def need(value, message):
    if not value:
        raise ValueError("ZUN init layout: " + message)


def tokens(text, inverse):
    rows = []
    for line in text.splitlines():
        # All maintained literals use single quotes; semicolons inside them are
        # data, never comments. Tokenize first, then recognize comment starts.
        words = re.findall(r"'[^']*'|[A-Za-z_@][A-Za-z_0-9@]*|[^\s]", line)
        words = words[:words.index(";")] if ";" in words else words
        if words: rows.append([inverse.get(word, word) for word in words])
    return rows


def lineage(root=ROOT):
    reference = subprocess.check_output(["git", "show", "b6ba5b0a529edbb31efdf8c0e939263804f8ee47:th02_zuninit.asm"],
                                        cwd=root / "_reference/ReC98")
    need(hashlib.sha256(reference).hexdigest() == "72281210345c697384157bb46216a0f313cf99893b6b4aa21026481462fa93e5", "pinned original ASM identity")
    labels = json.loads((root / "config/th03_zun_init_labels.json").read_bytes())
    need(len(labels) == len(set(labels.values())) == 59, "complete bijective label map")
    need(tokens(reference.decode("shift_jis"), {}) == tokens((root / SOURCE).read_text(), {v: k for k, v in labels.items()}),
         "complete original instruction/data/directive token lineage")
    return dict(origin="original-asm", reference_sha256=hashlib.sha256(reference).hexdigest(), labels=59,
                only_labels_comments_encoding_changed=True, newly_authored_bytes=0)


def verify(work, target, candidate, payload_offset):
    raw = (work / OBJECT).read_bytes()
    review = verify_outputs(raw, candidate, (work / MAP).read_bytes(), target)
    obj = parse_object(raw)
    blocks = []
    for record in parse_omf(raw):
        if record.name == "LEDATA":
            blocks.append([int.from_bytes(record.data[1:3], "little"), len(record.data) - 3])
    need(blocks == [[0x100, 1000], [0x4E8, 390]], "complete native ordered mixed CODE/DATA records")
    owner = dict(unit_id="th03-zun-decoded-init", source=SOURCE, object=OBJECT, start=0x100, size=1390,
                 origin="original-asm", code_bytes=607, data_bytes=783, procedures=9,
                 coordinate_space="decoded-payload-com", payload_option="-2", payload_file_offset=0,
                 decoded_file_offset=payload_offset, canonical_file_offset=None, ordered_relocations=[], format="COM",
                 abi="PSP entry, near helpers, three IRET handlers; caller interrupt stack",
                 target_sha256=hashlib.sha256(target).hexdigest(), candidate_sha256=hashlib.sha256(candidate).hexdigest())
    procedures = [dict(name=name, start=row["start"], size=row["size"], terminal=row["terminal"])
                  for name, row in zip(NAMES, review["procedures"])]
    review["map"]["allocations"] = [list(row) for row in review["map"]["allocations"]]
    return dict(owners=[owner], code_bytes=607, data_bytes=783, bss_bytes=0, procedure_count=9,
                procedures=procedures, native_records=blocks, ordered_native_fixups=obj["fixups"],
                map=review["map"], com_relocations=0, source_lineage=lineage())
