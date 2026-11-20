#!/usr/bin/env python3
"""Check linked far pointers and code writes, and screen stable address literals."""

import argparse
from bisect import bisect_right
from collections import defaultdict, deque
import json
import os
from pathlib import Path
import re
import struct

from capstone import Cs, CS_AC_WRITE, CS_ARCH_X86, CS_MODE_16, CS_GRP_CALL, CS_GRP_IRET, CS_GRP_JUMP, CS_GRP_RET
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_CS

from audit_th03_dos_pi import DRIVE, LAYOUTS, ROOT, map_rows, map_symbols, sha
from lib.pc98 import parse_mz

# Bounded straight-line and cross-branch scans adapted from TH04's PI review.
decoder = Cs(CS_ARCH_X86, CS_MODE_16)
decoder.detail = True
decoder.skipdata = True

REGISTER_FAMILIES = {
    register: names.split()[0]
    for names in ("ax eax ah al", "bx ebx bh bl", "cx ecx ch cl", "dx edx dh dl",
                  "si esi", "di edi", "bp ebp", "sp esp")
    for register in names.split()
}
SEGMENTS = {"ds", "es", "ss", "fs", "gs"}
BRANCH_GROUPS = (CS_GRP_CALL, CS_GRP_IRET, CS_GRP_JUMP, CS_GRP_RET)
ARITHMETIC = {"add", "sub", "and", "or", "shl", "shr", "sar", "inc", "dec", "neg",
              "not", "adc", "sbb"}


def stable_register_uses(code: list[bytes], origin: int) -> list[tuple]:
    """Follow literal origins through register operations and adjacent PUSH/POP.

    Clear the local state at control transfers. The results are candidates
    for source review, including possible inline data decoded as instructions.
    """
    registers = {}
    pushed = ()
    hits = []
    for instruction in decoder.disasm(code[0], origin):
        if not instruction.id:
            registers.clear()
            pushed = ()
            continue

        def family(register):
            name = instruction.reg_name(register)
            return REGISTER_FAMILIES.get(name, name)

        def seeds(register):
            return registers.get(family(register), ())

        operands = instruction.operands
        mnemonic = instruction.mnemonic
        branch = any(instruction.group(group) for group in BRANCH_GROUPS)
        literal = ()
        if (mnemonic in {"mov", "push"} and operands[-1].type == X86_OP_IMM
                and instruction.imm_size):
            begin = instruction.address - origin + instruction.imm_offset
            end = begin + instruction.imm_size
            if all(body[begin:end] == code[0][begin:end] for body in code[1:]):
                literal = ((instruction.address, operands[-1].imm,
                            f"{mnemonic} {instruction.op_str}"),)

        use = set()
        for operand in operands:
            if operand.type == X86_OP_MEM and mnemonic != "lea":
                use.update(seeds(operand.mem.base))
                use.update(seeds(operand.mem.index))
            elif branch and operand.type == X86_OP_REG:
                use.update(seeds(operand.reg))
        if mnemonic == "mov" and operands[0].type == X86_OP_REG:
            if family(operands[0].reg) in SEGMENTS and operands[1].type == X86_OP_REG:
                use.update(seeds(operands[1].reg))
        if mnemonic == "pop" and operands[0].type == X86_OP_REG:
            if family(operands[0].reg) in SEGMENTS:
                use.update(pushed)
        for address, number, producer in sorted(use):
            hits.append((address, number, producer, instruction.address,
                         f"{mnemonic} {instruction.op_str}"))

        result = ()
        if mnemonic == "mov" and operands[0].type == X86_OP_REG:
            result = literal or (seeds(operands[1].reg) if operands[1].type == X86_OP_REG else ())
            if operands[0].size == 1:
                result = tuple(set(result) | set(seeds(operands[0].reg)))
        elif mnemonic == "lea":
            result = tuple(set(seeds(operands[1].mem.base)) | set(seeds(operands[1].mem.index)))
        elif mnemonic in ARITHMETIC and operands[0].type == X86_OP_REG:
            result = seeds(operands[0].reg)
        elif mnemonic == "pop":
            result = pushed

        pushed = ()
        if mnemonic == "push":
            pushed = literal or (seeds(operands[0].reg) if operands[0].type == X86_OP_REG else ())
        for register in instruction.regs_access()[1]:
            registers.pop(family(register), None)
        if result and operands[0].type == X86_OP_REG:
            registers[family(operands[0].reg)] = result
        if branch or mnemonic.startswith("loop") or mnemonic in {"int", "int3"}:
            registers.clear()
            pushed = ()
    return hits

ALU = ARITHMETIC | {"xor", "rol", "ror"}
MAX_INSTRUCTIONS = 96


def branch_register_uses(bodies, origin):
    code = bodies[0]
    decoded = {i.address: i for i in decoder.disasm(code, origin) if i.id}
    for start in decoded.values():
        m = start.mnemonic
        ops = start.operands
        if m not in ALU | {"mov", "push"} or not start.imm_size:
            continue
        if ops[-1].type != X86_OP_IMM or (m != "push" and
                                         (ops[0].type != X86_OP_REG or ops[0].size < 2)):
            continue
        immediate = start.address - origin + start.imm_offset
        end = immediate + start.imm_size
        if any(body[immediate:end] != code[immediate:end] for body in bodies[1:]):
            continue

        def reg(number):
            n = decoder.reg_name(number)
            return REGISTER_FAMILIES.get(n, n)

        regs = frozenset() if m == "push" else frozenset({reg(ops[0].reg)})
        pending = deque([(start.address + start.size, regs, int(m == "push"), False, 1)])
        seen, hits = set(), set()
        while pending:
            address, regs, stack_slot, crossed, depth = pending.popleft()
            if depth > MAX_INSTRUCTIONS or not (regs or stack_slot):
                continue
            key = (address, regs, stack_slot, crossed)
            if key in seen or address not in decoded:
                continue
            seen.add(key)
            i = decoded[address]
            insn, ops = i.mnemonic, i.operands
            branch = i.group(CS_GRP_JUMP) or insn.startswith("loop")
            call = i.group(CS_GRP_CALL)
            use = any(
                (o.type == X86_OP_MEM and insn != "lea" and
                 (reg(o.mem.base) in regs or reg(o.mem.index) in regs)) or
                (o.type == X86_OP_REG and (branch or call) and reg(o.reg) in regs)
                for o in ops
            )
            if insn in {"mov", "pop"} and ops[0].type == X86_OP_REG and reg(ops[0].reg) in SEGMENTS:
                use |= (stack_slot == 1 if insn == "pop" else
                        ops[1].type == X86_OP_REG and reg(ops[1].reg) in regs)
            if use and (crossed or m in ALU) and address not in hits:
                hits.add(address)
                yield (start.address, start.operands[-1].imm, f"{m} {start.op_str}",
                       address, f"{insn} {i.op_str}")

            if call or i.group(CS_GRP_RET) or i.group(CS_GRP_IRET) or insn in {"int", "int3", "into"}:
                continue
            next_address = address + i.size
            if branch:
                if len(ops) == 1 and ops[0].type == X86_OP_IMM:
                    pending.append((ops[0].imm & 65535, regs, stack_slot, True, depth + 1))
                if insn not in {"jmp", "ljmp"}:
                    pending.append((next_address, regs, stack_slot, True, depth + 1))
                continue

            dest = reg(ops[0].reg) if ops and ops[0].type == X86_OP_REG else None
            writes = {reg(r) for r in i.regs_access()[1]}
            out = regs - writes
            copy = False
            if insn == "mov" and dest:
                copy = ops[1].type == X86_OP_REG and reg(ops[1].reg) in regs
            elif insn == "lea" and dest:
                copy = reg(ops[1].mem.base) in regs or reg(ops[1].mem.index) in regs
            elif insn in ALU and dest:
                clears = (insn in {"sub", "xor"} and len(ops) == 2 and
                          ops[1].type == X86_OP_REG and ops[1].reg == ops[0].reg)
                copy = not clears and (dest in regs or
                                       any(o.type == X86_OP_REG and reg(o.reg) in regs for o in ops[1:]))
            elif insn == "xchg" and all(o.type == X86_OP_REG for o in ops):
                first, second = (reg(o.reg) for o in ops)
                if first in regs:
                    out |= {second}
                if second in regs:
                    out |= {first}
            elif insn == "pop":
                copy = stack_slot == 1
                stack_slot = max(0, stack_slot - 1)
            elif insn == "push":
                if ops[0].type == X86_OP_REG and reg(ops[0].reg) in regs:
                    stack_slot = 1
                elif stack_slot:
                    stack_slot += 1
            elif "sp" in writes:
                stack_slot = 0
            if dest and (copy or (ops[0].size == 1 and dest in regs and dest in writes)):
                out |= {dest}
            pending.append((next_address, out, stack_slot, crossed, depth + 1))



class Image:
    def __init__(self, path, product, exe_hash, map_hash):
        self.exe = parse_mz((path / f"{product}.exe").read_bytes())
        mapping = path / f"{product}.map"
        if not self.exe.valid or sha(self.exe.raw) != exe_hash or sha(mapping.read_bytes()) != map_hash:
            raise ValueError(f"layout image identity drift: {path.name}/{product}")
        self.code = self.exe.program_image
        self.rows = sorted((r for r in map_rows(mapping) if r.size), key=lambda row: row.start)
        self.starts = [r.start for r in self.rows]
        self.sites = [r.linear for r in self.exe.relocations]
        self.symbols = map_symbols(mapping)

    def owner(self, address, width=1):
        index = bisect_right(self.starts, address) - 1
        if index >= 0:
            row = self.rows[index]
            if address + width <= row.start + row.size:
                return index, address - row.start
        return None

    def word(self, at):
        return int.from_bytes(self.code[at:at + 2], "little")

    def far_address(self, at):
        return self.word(at) * 16 + self.word(at - 2)


def paired_owners(images):
    shifted = []
    for image in images[1:]:
        owners = defaultdict(deque)
        for index, row in enumerate(image.rows):
            owners[row.owner].append(index)
        shifted.append(owners)
    mapping = []
    for index, row in enumerate(images[0].rows):
        paired = [index, *(owners[row.owner].popleft() for owners in shifted)]
        if any(image.rows[ordinal].size != row.size for image, ordinal in zip(images, paired, strict=True)):
            raise ValueError(f"changed extent for {row.owner}")
        mapping.append(paired)
    return mapping


def far_data(images, mapping):
    baseline = images[0]
    sites = set(baseline.sites)
    checked, other = 0, []
    for old_site in baseline.sites:
        owner, relative = baseline.owner(old_site, 2)
        source = baseline.rows[owner]
        if source.kind == "CODE":
            continue
        if relative < 2 or any(old_site + offset in sites for offset in (-3, -2, -1, 1, 2, 3)):
            other.append([source.module, relative, "segment-only field"])
            continue
        target = baseline.owner(baseline.far_address(old_site))
        if target is None:
            other.append([source.module, relative, "no mapped far target"])
            continue
        index, displacement = target
        observed = [
            image.owner(image.far_address(image.rows[ordinal].start + relative))
            for image, ordinal in zip(images, mapping[owner], strict=True)
        ]
        expected = [(ordinal, displacement) for ordinal in mapping[index]]
        if observed == expected:
            checked += 1
        else:
            other.append([source.module, relative, baseline.rows[index].module, observed, expected])
    return checked, other


def entry_frames(image):
    frames = defaultdict(set)
    for site in image.sites:
        if site >= 3 and image.code[site - 3] in (0x9A, 0xEA):
            target = image.owner(image.far_address(site))
            if target is not None and image.rows[target[0]].kind == "CODE":
                frames[target[0]].add(image.word(site))
    return frames


def cs_stores(image, row, frames):
    stores = {}
    for instruction in decoder.disasm(image.code[row.start:row.start + row.size], row.offset):
        if not instruction.id:
            continue
        for operand in instruction.operands:
            if (operand.type != X86_OP_MEM or not operand.access & CS_AC_WRITE
                    or operand.mem.segment != X86_REG_CS):
                continue
            displacement = operand.mem.disp & 0xFFFF
            targets = tuple(sorted(frame * 16 + displacement - row.start for frame in frames))
            if operand.mem.base or operand.mem.index:
                targets = None
            stores[instruction.address - row.offset] = (operand.size, targets)
    return stores


def vector_targets(image):
    """Check VSYNC, CRT BIOS and archive INT 21h installation in linked CS."""
    vectors = {}
    setvect_frame, setvect_offset = image.symbols["DOS_SETVECT"]
    frame, offset = image.symbols["VSYNC_START"]
    start = frame * 16 + offset
    body = image.code[start:start + 126]
    patterns = (
        (0x0A, rb"\xb0\x0a", rb"\x50\x1e\xb8..\x8e\xd8"),
        (0x18, rb"\xb8\x18\x00", rb"\x9c\x2e\xff\x1e..\xe6\x64\xcf"),
    )
    for vector, setup, signature in patterns:
        (call,) = re.finditer(setup + rb"\x50\x0e\xb8(..)\x50\x90?\x0e\xe8(..)", body, re.S)
        (handler,) = re.finditer(signature, body, re.S)
        offset_word = int.from_bytes(call[1], "little")
        near_target = (offset + call.end() + int.from_bytes(call[2], "little", signed=True)) & 65535
        if offset_word != offset + handler.start() or frame * 16 + near_target != setvect_frame * 16 + setvect_offset:
            raise ValueError(f"wrong destination for INT {vector:02X}")
        vectors[vector] = handler.start()

    frame, offset = image.symbols["PFSTART"]
    start = frame * 16 + offset
    body = image.code[start:start + 270]
    (install,) = re.finditer(rb"\x0e\x1f\xba(..)\xb8\x21\x25\xcd\x21", body, re.S)
    (handler,) = re.finditer(rb"\x2e\x80\x3e..\x00\x74\x05\x2e\xff\x2e", body, re.S)
    if int.from_bytes(install[1], "little") != offset + handler.start():
        raise ValueError("wrong destination for archive INT 21h")
    vectors[0x21] = handler.start()
    return vectors


def bullet_switches(image, frames):
    """Compare the compiler's two near jump tables in MAIN's caller CS."""
    (index,) = (index for index, row in enumerate(image.rows)
                if row.kind == "CODE" and row.name == "BULLET_TEXT"
                and row.module.replace("\\", "/").endswith("/bullet.cpp"))
    row = image.rows[index]
    checked_frames = frames[index]
    if checked_frames != {row.frame}:
        raise ValueError("bullet far caller frame differs from the MAP")
    instructions = list(decoder.disasm(image.code[row.start:row.start + row.size], row.offset))
    switches = []
    for ordinal, instruction in enumerate(instructions):
        if instruction.mnemonic != "jmp":
            continue
        operand = instruction.operands[0]
        if operand.type != X86_OP_MEM or operand.mem.segment != X86_REG_CS:
            continue
        limits = [item.operands[1].imm for item in instructions[max(0, ordinal - 8):ordinal]
                  if item.mnemonic == "cmp" and item.operands[1].type == X86_OP_IMM]
        if not limits or not 0 <= limits[-1] < 64:
            raise ValueError("bullet switch bound requires source review")
        count = limits[-1] + 1
        table = row.frame * 16 + (operand.mem.disp & 0xffff)
        targets = [row.frame * 16 + image.word(table + 2 * i) - row.start for i in range(count)]
        if image.owner(table, 2 * count) != (index, table - row.start) or not all(0 <= t < row.size for t in targets):
            raise ValueError("bullet switch table or target left the emitting contribution")
        switches.append([instruction.address - row.offset, table - row.start, targets])
    if len(switches) != 2:
        raise ValueError("expected both MAIN bullet switches")
    return switches


def cdg_replay(image, public, load):
    """Run the linked MAINL blitter with a two-row, four-plane sprite."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INSN, UC_HOOK_MEM_WRITE
    from unicorn.x86_const import (
        UC_X86_INS_IN, UC_X86_INS_OUT, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SP, UC_X86_REG_SS,
    )

    frame, entry = image.symbols[public]
    data_frame, slot = image.symbols["_cdg_slots"]
    cs, ds, ss = load + frame, load + data_frame, 0x9000
    draw_start = cs * 16 + entry
    alpha, colors = 0x8000, 0x8100
    payload = bytes(range(1, 65))
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    cpu.mem_write(load * 16, image.exe.relocated_program_image(load))
    cpu.mem_write(colors * 16, payload)
    # Slot zero, bottom row offset 80, two dwords wide.
    cpu.mem_write(ds * 16 + slot, struct.pack("<8H", 0, 0, 0, 80, 2, 0, alpha, colors))
    for register, value in ((UC_X86_REG_CS, cs), (UC_X86_REG_DS, ds),
                            (UC_X86_REG_SS, ss), (UC_X86_REG_SP, 0xff00)):
        cpu.reg_write(register, value)
    cpu.mem_write(ss * 16 + 0xff00, struct.pack("<5H", 0, 0x9100, 0, 3, 8))
    patches = []
    returned = False

    def watch(uc, address, size, _):
        nonlocal returned
        if address == 0x91000:
            returned = True
            uc.emu_stop()

    def store(uc, access, address, size, value, _):
        if load * 16 <= address < load * 16 + len(image.code):
            patches.append((address - draw_start, size, value))

    cpu.hook_add(UC_HOOK_CODE, watch)
    cpu.hook_add(UC_HOOK_MEM_WRITE, store)
    cpu.hook_add(UC_HOOK_INSN, lambda *_: None, None, 1, 0, UC_X86_INS_OUT)
    cpu.hook_add(UC_HOOK_INSN, lambda *_: 0, None, 1, 0, UC_X86_INS_IN)
    cpu.emu_start(draw_start, 0xa0000, count=10000)
    if not returned or cpu.reg_read(UC_X86_REG_SP) != 0xff0a or cpu.reg_read(UC_X86_REG_DS) != ds:
        raise ValueError(f"{public}: incorrect far return at load {load:04x}")
    for plane, address in enumerate((0xa8000, 0xb0000, 0xb8000, 0xe0000)):
        actual = bytes(cpu.mem_read(address + 321, 8) + cpu.mem_read(address + 241, 8))
        if actual != payload[plane * 16:(plane + 1) * 16]:
            raise ValueError(f"{public}: plane {plane} differs at load {load:04x}")
    expected_patches = [120, 113, 99, 125, 95] if public == "CDG_PUT_8" else [71]
    if [(relative, size) for relative, size, _ in patches] != [(relative, 2) for relative in expected_patches]:
        raise ValueError(f"{public}: write to unexpected instruction fields")
    return patches


def collision_edge(image, with_contact):
    """Execute the actual 2P collision scan for Demo 1's first differing input."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_BX, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_SP

    load, ss = 0x2000, 0x8300
    frame, entry = image.symbols["player_hittest(int)"]
    data_frame, bitmap = image.symbols["_collmap"]
    start = frame * 16 + entry
    (test,) = (instruction.address for instruction in decoder.disasm(image.code[start:start + 224], entry)
               if instruction.bytes == b"\x84\x2f")
    cs, ds = load + frame, load + data_frame
    player = image.symbols["_players"][1] + 128
    cpu = Uc(UC_ARCH_X86, UC_MODE_16)
    cpu.mem_map(0, 0x100000)
    cpu.mem_write(load * 16, image.exe.relocated_program_image(load))
    cpu.mem_write(ds * 16 + player, struct.pack("<HH", 480, 3936) + bytes(124))
    cpu.mem_write(ds * 16 + image.symbols["_player_cur"][1], struct.pack("<H", player))
    cpu.mem_write(ds * 16 + image.symbols["_pid"][1], b"\x01")
    # The first visible column starts at tile row (3936 / 32) - (32 / 2).
    width = 18 * 184
    cpu.mem_write(ds * 16 + bitmap, bytes(2 * width))
    if with_contact:
        cpu.mem_write(ds * 16 + bitmap + width + 107, b"\x80")
    for register, value in ((UC_X86_REG_CS, cs), (UC_X86_REG_DS, ds),
                            (UC_X86_REG_SS, ss), (UC_X86_REG_SP, 0xff00)):
        cpu.reg_write(register, value)
    cpu.mem_write(ss * 16 + 0xff00, struct.pack("<HH", 0xfff0, 32))
    reads = []
    returned = False

    def trace(uc, address, size, _):
        nonlocal returned
        if address == cs * 16 + test:
            reads.append(uc.reg_read(UC_X86_REG_BX) - bitmap - width)
        elif address == cs * 16 + 0xfff0:
            returned = True
            uc.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, trace)
    cpu.emu_start(cs * 16 + entry, 0xa0000, count=10000)
    if not returned or not reads or cpu.reg_read(UC_X86_REG_SP) != 0xff04:
        raise ValueError("collision fixture missed the complete scan and near return")
    flags = bytes(cpu.mem_read(ds * 16 + player + 4, 1))
    coords = bytes(cpu.mem_read(ds * 16 + image.symbols["_player_hittest_collision_top"][1], 4))
    return {"reads_from_bitmap_2p": reads, "first_ds": bitmap + width + reads[0],
            "within_2p_bitmap": all(0 <= word < width for word in reads),
            "hit": flags[0], "collision_xy": list(struct.unpack("<HH", coords))}


def named_reference(product, image):
    """Check one game-specific data reference in each linked layout."""
    def linear(name):
        frame, offset = image.symbols[name]
        return frame * 16 + offset

    if product == "main":
        frame, ring = image.symbols["_randring"]
        cursor_frame, cursor = image.symbols["_randring_p"]
        at = linear("randring1_next16()")
        expected = (b"\x32\xff\x8a\x1e" + struct.pack("<H", cursor)
                    + b"\x81\xc3" + struct.pack("<H", ring) + b"\xfe\x06" + struct.pack("<H", cursor))
        if frame != cursor_frame or cursor - ring != 256 or not image.code[at:].startswith(expected):
            raise ValueError("MAIN's ring accessor or adjacent cursor binding diverged")
        return [frame, ring, cursor]

    if product == "op":
        frame, offset = image.symbols["_resident"]
        start = linear("start_demo()")
        end = linear("wait_for_input_or_start_demo_the()")
        body = image.code[start:end]
        references = [instruction for instruction in decoder.disasm(body, 0)
                      if instruction.mnemonic == "les" and instruction.operands[1].type == X86_OP_MEM
                      and not instruction.operands[1].mem.base and not instruction.operands[1].mem.index]
        if frame != image.word(1) or not references or any(ins.operands[1].mem.disp != offset
                                                           for ins in references):
            raise ValueError("OP's attract routine lost the resident pointer")
        return [frame, offset, len(references)]

    field = linear("_mainl_ending_script")
    target = linear("_mainl_ending_template")
    if field + 2 not in image.sites or image.far_address(field + 2) != target:
        raise ValueError("MAINL's initialized ending script pointer lost its template")
    return list(image.symbols["_mainl_ending_template"])


def scan(product, images, pi_collision=False):
    mapping = paired_owners(images)
    named = [named_reference(product, image) for image in images]
    baseline = images[0]
    frames = [entry_frames(image) for image in images]
    vectors = [vector_targets(image) for image in images]
    if any(value != vectors[0] for value in vectors[1:]):
        raise ValueError("interrupt handlers moved relative to their providers")
    switches, collision = [], []
    if product == "main":
        switches = [bullet_switches(image, observed) for image, observed in zip(images, frames, strict=True)]
        if any(value != switches[0] for value in switches[1:]):
            raise ValueError("MAIN bullet switches changed their targets")
        for contact in (False, True):
            attempts = [collision_edge(image, contact) for image in images]
            collision.append(attempts)
            if pi_collision and any(not row["within_2p_bitmap"] or row["hit"] != int(contact)
                                    or row["reads_from_bitmap_2p"] != attempts[0]["reads_from_bitmap_2p"]
                                    or row["collision_xy"] != attempts[0]["collision_xy"]
                                    for row in attempts):
                raise ValueError("PI collision scan depends on link layout")
    cdg_runs = 0
    if product == "mainl":
        for public in ("CDG_PUT_8", "CDG_PUT_NOALPHA_8"):
            results = [cdg_replay(image, public, load) for image in images for load in (0x2000, 0x6000)]
            if any(result != results[0] for result in results[1:]):
                raise ValueError(f"{public}: patch values changed with layout")
            cdg_runs += len(results)
    pointers, other_data = far_data(images, mapping)
    candidates, store_review = [], []
    code_size = stores_checked = 0
    for row, indexes in zip(baseline.rows, mapping, strict=True):
        if row.kind != "CODE" or not row.module.lower().endswith((".asm", ".c", ".cpp", ".inc")):
            continue
        counterparts = [image.rows[index] for image, index in zip(images, indexes, strict=True)]
        bodies = [image.code[owner.start:owner.start + row.size]
                  for image, owner in zip(images, counterparts, strict=True)]
        code_size += row.size
        uses = set(stable_register_uses(bodies, row.offset))
        uses.update(branch_register_uses(bodies, row.offset))
        for address, number, producer, sink_ip, sink in sorted(uses):
            candidates.append([row.module, f"{row.frame:04X}:{address:04X}", number, producer,
                               f"{row.frame:04X}:{sink_ip:04X}", sink])

        stores = [cs_stores(image, owner, observed.get(index) or {owner.frame})
                  for image, owner, index, observed in zip(images, counterparts, indexes, frames, strict=True)]
        for address in sorted(set().union(*stores)):
            values = [variant.get(address) for variant in stores]
            first = values[0]
            if (first is not None and values.count(first) == len(values) and first[1] is not None
                    and all(0 <= target <= row.size - first[0] for target in first[1])):
                stores_checked += 1
            else:
                store_review.append([row.module, f"{row.frame:04X}:{row.offset + address:04X}", values])
    return dict(named_reference=named, collision_edge=collision, vectors=len(vectors[0]), cdg_runs=cdg_runs, bullet_switches=len(switches[0]) if switches else 0,
                code_bytes=code_size, far_data_pointers=pointers, other_data=other_data,
                cs_stores=stores_checked, cs_store_review=store_review, register_candidates=candidates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"af[0-9]+[a-z]", args.stage):
        parser.error("expected a retained PI stage")
    output = args.output.resolve()
    if output.exists() or not output.is_relative_to(ROOT / ".analysis"):
        parser.error("expected a fresh private output")
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    stage = DRIVE / "TH03PI" / args.stage
    result = {}
    for product, row in json.loads((stage / "layout.json").read_bytes()).items():
        images = [Image(stage / "control", product, row["baseline_sha256"], row["baseline_map_sha256"])]
        for layout in LAYOUTS:
            pin = row["layouts"][layout]
            images.append(Image(stage / layout, product, pin["exe_sha256"], pin["map_sha256"]))
        result[product] = scan(product, images, (stage / "pi-core.json").is_file())
        print(product, {key: len(value) if isinstance(value, list) else value
                        for key, value in result[product].items()}, flush=True)
    output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
