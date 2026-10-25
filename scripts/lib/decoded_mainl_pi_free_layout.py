"""Complete PI release in the maintained root, without enclosing heap ownership."""
import hashlib
import re
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from lib.decoded_mainl_root_helpers_layout import CODE_BASE, OBJECT, WRAPPER, native
from probe_th03_main_boss_marisa_cpp import code_publics

SOURCE = 'src/mainl/resources/graph_pi_free.asm'
START, SIZE, HEAP = 0xFEC, 76, 0x22B2
CALLS = ((0xFFD, 0x1002), (0x1016, 0x101B), (0x102F, 0x1034))


def need(value, message):
    if not value:
        raise ValueError('MAINL PI free layout: ' + message)


def native_body(raw):
    # The existing root parser checks the complete segment geometry, alignment,
    # producer identity and literal unthreaded field grammar, including context.
    _, description = native(raw)
    start, end = START - CODE_BASE, START - CODE_BASE + SIZE
    body = bytearray(SIZE)
    seen = set()
    block = None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = (record.data[0], int.from_bytes(record.data[1:3], 'little'))
            if block[0] != 1:
                continue
            for at in range(max(start, block[1]), min(end, block[1] + len(record.data) - 3)):
                need(at not in seen, 'nonoverlapping owner LEDATA')
                seen.add(at)
                body[at - start] = record.data[3 + at - block[1]]
        elif record.name == 'FIXUPP' and block and block[0] == 1:
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                if method & ~3 in (0x04, 0x14):
                    at += 1
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = {1: 2, 2: 2, 3: 4}[loc >> 2 & 15]
                need(not (site < end and site + width > start), 'empty complete ordered owner OMF field vector')
    need(seen == set(range(start, end)), 'complete file-backed native coverage')
    return bytes(body), description


def verify(work, target, candidate, graph, files):
    root = Path(__file__).resolve().parents[2]
    raw = (work / OBJECT).read_bytes()
    body, description = native_body(raw)
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['wrapper'], row['source'], row['game'], row['binary'], row['first_binary'])
         == (WRAPPER, WRAPPER, 3, 'L', 'mainl'), 'actual GAME3/L root producer')
    need(SOURCE in description['dependency_paths'] and
         files[WRAPPER].decode('cp932').count('include ' + SOURCE) == 1,
         'one real maintained source include and native dependency')
    need(files[SOURCE] == (work / SOURCE).read_bytes() and
         files[SOURCE].replace(b'\r\n', b'\n') == (root / SOURCE).read_bytes().replace(b'\r\n', b'\n'),
         'current maintained source transport')
    text = (work / 'obj/th03/mainl.map').read_text().replace(chr(92), '/')
    need(text.count('0000:0272 2AC0 C=CODE   S=_TEXT          G=(none)  M=th03_mainl.asm ACBP=48') == 1,
         'literal containing root MAP allocation')
    for symbol, address in (('GRAPH_PI_FREE', START), ('HMEM_FREE', HEAP)):
        need((address - CODE_BASE, symbol) in code_publics(raw, 1), 'real root public ' + symbol)
        need(len(re.findall(rf'(?m)^\s*0000:{address:04X}\s+(?:idle\s+)?{symbol}\s*$', text)) == 2,
             'both MAP public tables ' + symbol)
    need(body == target.program_image[START:START + SIZE] == candidate.program_image[START:START + SIZE],
         'complete unmodified native function bytes')
    instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, START))
    need(sum(i.size for i in instructions) == SIZE and instructions[-1].mnemonic == 'retf'
         and instructions[-1].op_str == '8', 'complete instruction scope and far Pascal pop-eight')
    for nop, continuation in CALLS:
        at = nop - START
        displacement = (HEAP - continuation) & 65535
        need(body[at:at + 5] == b'\x90\x0e\xe8' + displacement.to_bytes(2, 'little'),
             'original symbolic nopcall macro and actual same-root destination')
    for image in (target, candidate):
        need(not any(r.linear < START + SIZE and r.linear + 2 > START for r in image.relocations),
             'empty complete ordered MZ relocation vector')
    digest = hashlib.sha256(body).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-pi-decoder-free', name='GRAPH_PI_FREE', source=SOURCE,
                 object=OBJECT, segment=0, offset=START, start=START, size=SIZE,
                 coordinate_space='decoded-load', canonical_file_offset=None,
                 target_sha256=digest, candidate_sha256=digest, ordered_relocations=[],
                 argument_bytes=8, callee_pop_bytes=8, return_address_bytes=4,
                 private_data_bytes=0, private_bss_bytes=0,
                 abi='far Pascal; two far pointers; native nopcall frames; HMEM_FREE is a bounded interface')
    return dict(owners=[owner], functions=1, code_bytes=SIZE, ordered_native_fields=[], ordered_relocations=[],
                native_nopcall_sites=[n for n, _ in CALLS], heap_entry=HEAP,
                containing_producer_accepted=False, heap_body_accepted=False, whole_product_accepted=False)
