"""Title's complete source-derived literal pool; no following alignment credit."""
import hashlib
import re

from lib.omf import parse_omf
from lib.op_asset_native import extent
from lib.op_title_native import DS, DATA, OBJECT, SOURCE, WRAPPER, INCLUDE, resolve
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

UNIT = 'th03-op-decoded-title-data'


def need(value, message):
    if not value:
        raise ValueError('OP title storage: ' + str(message))


def semantic_data(files):
    source = files[SOURCE].decode()
    header = files['th03/shiftjis/fns.hpp'].decode('cp932')
    macros = dict(re.findall(r'^#define\s+(BGM_MENU_MAIN_FN|MENU_MAIN_BG_FN)\s+"([^"\\]*)"\s*$', header, re.M))
    # All four pool entries in first-use order. Repeated loads reuse literals.
    operands = re.findall(r'\b(?:super_entry_bfnt|snd_load|pi_load)\((?:0,\s*)?("[^"\\]*"|BGM_MENU_MAIN_FN|MENU_MAIN_BG_FN)', source)
    texts = list(dict.fromkeys(x[1:-1] if x.startswith('"') else macros[x] for x in operands))
    need(len(texts) == 4 and len(macros) == 2, 'complete source filename/macro pool')
    data, literals = bytearray(), []
    for text in texts:
        raw = text.encode('ascii') + b'\0'
        literals.append(dict(text=text, offset=len(data), size=len(raw)))
        data.extend(raw)
    need(len(data) == 31, 'natural31-byte pool without holes')
    return bytes(data), literals


def verify(root, work, target, candidate, files):
    need(files[SOURCE] == (root / SOURCE).read_bytes() and
         all((work / name).read_bytes() == files[name] for name in
             (SOURCE, WRAPPER, INCLUDE, 'th03/shiftjis/fns.hpp')), 'actual maintained source and consumed macros')
    raw = (work / OBJECT).read_bytes()
    data, blocks = code_bytes(raw, 2)
    semantic, literals = semantic_data(files)
    need([(b['offset'], b['size']) for b in blocks] == [(0, 31)] and data == semantic and
         not code_publics(raw, 2), 'whole semantic/native literal pool')
    block = None
    for r in parse_omf(raw):
        if r.name == 'LEDATA':
            block = r.data[0]
            need(block != 3, 'no file-backed title BSS')
        elif r.name == 'FIXUPP':
            need(block == 1, 'DATA has no native pointer/segment fields')
    table = (work / 'obj/th03/op.map').read_text()
    need(len(re.findall(r'(?m)^\s*0D7F:09E2\s+001F\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=th03/op_main\.cpp\s+ACBP=48\s*$', table)) == 1,
         'whole actual title DATA allocation')
    _, fields, _ = resolve(raw, table)
    references = sorted({f['addend'] for f in fields if f['method'] == 20})
    need(references == [r['offset'] for r in literals], 'every native CODE local-DATA reference enters a complete literal')
    extent((target, candidate), data, DS, DATA, [])
    digest = hashlib.sha256(data).hexdigest()
    owner = dict(unit_id=UNIT, name='Title initialized filename pool', source=SOURCE, object=OBJECT,
        segment=DS, offset=DATA, start=DS * 16 + DATA, size=31, coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=[], procedure_count=0, procedures=[],
        code_bytes=0, initialized_data_bytes=31, private_data_bytes=31, private_bss_bytes=0,
        forwarding_chain=[WRAPPER, INCLUDE, SOURCE], abi='four NUL-terminated ASCII literals; near DGROUP offsets')
    return dict(owners=[owner], initialized_data_bytes=31, literals=literals, CODE_DATA_addends=references,
                native_DATA_fields=[], ordered_relocations=[], following_alignment_accepted=False,
                BSS_raw_byte_credit=0, whole_product_accepted=False)


if __name__ == '__main__':
    import json
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(verify(root, work, target, candidate, build.source_graph()), indent=2))
