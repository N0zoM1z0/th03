"""Bounded header, digit alphabet and semantic DATA ownership, excluding reserves.

The restricted declaration reader maps source labels to emitted OMF bytes; it
does not infer ownership from matching target runs. Native relocation records
are resolved separately. Behavioral contracts use independent message/table
specifications and execute consumers against the unmodified initial image.
"""
import hashlib
import re

from lib.zun_driver_layout import review, resolve_native, public_contract
from stage_th03_zun_driver import dos_text

SOURCE = 'src/zun/driver_data.inl'
RANGES = (
    ('header', 0x100, 12, 'src/zun/driver.asm', 2),
    ('digit-alphabet', 0x8DC, 16, 'src/zun/driver.asm', 0),
    ('state-and-tables', 0xC80, 1261, SOURCE, 0),
    ('switch-strings', 0x1170, 7, SOURCE, 0),
)
OPTION_TARGETS = (0xFF0, 0x243, 0xFF3, 0x2AD, 0xFF6, 0x1D7, 0xFF9, 0x1DE,
                  0x1002, 0x5D0, 0x1009, 0x5A4, 0x1010, 0x610, 0x1015, 0x201)
SERVICE_TARGETS = (0x520, 0x540, 0x364, 0x340, 0x346, 0x34C, 0x352, 0x358, 0x35E)


def need(value, message):
    if not value:
        raise ValueError('ZUN DATA layout: ' + message)


def declarations(source):
    """Only the maintained DB/DW/label grammar; no includes or byte injection."""
    labels, statements, cursor = {}, [], 0xC80
    for line in source.splitlines():
        line = line.split(';', 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'(?:(sprite16_\w+)\s+)?(db|dw|label)\s+(.+)', line)
        need(match, 'bounded declaration grammar')
        name, kind, body = match.groups()
        if name:
            need(name not in labels, 'unique source label')
            labels[name] = cursor
        if kind == 'label':
            need(body == 'byte', 'BYTE boundary label')
            continue
        parts = re.findall(r"'[^']*'|[^,]+", body)
        atoms = []
        for part in parts:
            part = part.strip()
            if part.startswith("'"):
                need(kind == 'db' and part.endswith("'"), 'DB string literal')
                atoms.append(part[1:-1].encode('shift_jis'))
            elif re.fullmatch(r'(?:[0-9]+|[0-9A-Fa-f]+h) dup\(0\)', part):
                count = part.split()[0]
                count = int(count[:-1], 16) if count.endswith('h') else int(count)
                atoms.append(bytes(count * (1 if kind == 'db' else 2)))
            elif re.match(r'offset\s', part):
                need(kind == 'dw' and re.fullmatch(r'offset\s+sprite16_\w+', part), 'near symbolic pointer')
                atoms.append(part.split()[1])
            else:
                need(re.fullmatch(r'[0-9]+|[0-9A-Fa-f]+h', part), 'literal integer')
                value = int(part[:-1], 16) if part.endswith('h') else int(part)
                atoms.append(value.to_bytes(1 if kind == 'db' else 2, 'little'))
        statements.append((cursor, atoms))
        cursor += sum(2 if isinstance(a, str) else len(a) for a in atoms)
    need(cursor == 0x1180, 'complete DATA declaration length')
    symbols = dict(public_contract(), **labels)
    output, fixups = bytearray(), []
    for start, atoms in statements:
        need(start == 0xC80 + len(output), 'contiguous source declarations')
        for atom in atoms:
            if isinstance(atom, str):
                need(atom in symbols, 'known declared pointer target')
                value = symbols[atom]
                fixups.append((0xC80 + len(output), value))
                output.extend(value.to_bytes(2, 'little'))
            else:
                output.extend(atom)
    return bytes(output), labels, fixups


def verify(work, target, candidate, at, files, maintained):
    obj = (work / 'driver/driver.obj').read_bytes()
    physical = review(obj, (work / 'driver/driver.map').read_bytes())
    image, fixups, blocks = resolve_native(obj)
    need(image == target == candidate and len(image) == 4224, 'whole native driver equality')
    source = maintained[SOURCE].decode()
    need(files['driver/data.inc'] == dos_text(source) == (work / 'driver/data.inc').read_bytes(),
         'actual whole maintained DATA include')
    need(files['driver/driver.asm'].count(b'include data.inc\r\n') == 1, 'single consumed DATA slot')
    data, labels, declared = declarations(source)
    need(data == image[0xC80-256:], 'all declarations, widths, order and packed offsets')
    selected = [f for f in fixups if f['address'] >= 0xC80]
    literal = list(zip(range(0x101C, 0x103C, 2), OPTION_TARGETS))
    literal += list(zip(range(0x103E, 0x1050, 2), SERVICE_TARGETS))
    need(declared == literal == [(f['address'], f['target_address']) for f in selected]
         and all(f['width'] == 2 and not f['self_relative'] for f in selected),
         '25 ordered native WORD pointers, with untouched zero sentinel')
    root = maintained['src/zun/driver.asm'].decode()
    need('start:\n    jmp short sprite16_entry\nsprite16_signature db \'SPRITE16\',0\nsprite16_version db 4\n' in root,
         'complete semantic startup header')
    need("sprite16_hex_digits db '0123456789ABCDEF'\n" in root,
         'nonterminated digit alphabet source')
    need(image[:12] == b'\xEB\x0ASPRITE16\0\x04' and image[0x8DC-256:0x8EC-256] == b'0123456789ABCDEF',
         'header transfer, signature/version and hexadecimal alphabet')
    need(labels['sprite16_startup_stack'] == 0xD38 and labels['sprite16_startup_stack_top'] == 0xF38
         and labels['sprite16_reserved_before_switches'] == 0x116D
         and labels['sprite16_reserved_tail'] == 0x1177, 'stack and explicitly excluded boundaries')
    owners = []
    for name, start, size, path, code in RANGES:
        raw = image[start-256:start-256+size]
        digest = hashlib.sha256(raw).hexdigest()
        owners.append(dict(unit_id='th03-zun-decoded-driver-data-' + name, source=path,
            object='driver/driver.obj', include='driver/data.inc' if path == SOURCE else 'driver/driver.asm',
            start=start, size=size, origin='library', coordinate_space='decoded-payload-com', payload_option='-4',
            payload_file_offset=start-256, decoded_file_offset=at+start-256, canonical_file_offset=None,
            format='COM', code_bytes=code, data_bytes=size-code, private_data_bytes=size-code, private_bss_bytes=0,
            abi='tiny DGROUP, packed little-endian WORD state/pointers; COM header JMP and 512-byte startup stack',
            argument_bytes=0, callee_pop_bytes=0, ordered_relocations=[],
            ordered_native_fixups=[f for f in selected if start <= f['address'] < start+size],
            target_sha256=digest, candidate_sha256=digest))
    return dict(owners=owners, code_bytes=2, data_bytes=1294, functions=0, native_layout=physical,
        native_records=blocks, ordered_native_fixups=selected, source_labels=labels, startup_stack_bytes=512,
        excluded_reserved_spans=[dict(start=0x116D,size=3),dict(start=0x1177,size=9)],
        enclosing_driver_accepted=False, reserved_spans_owned=False, original_assembler_identified=False)
