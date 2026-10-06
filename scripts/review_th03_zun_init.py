#!/usr/bin/env python3
"""Whole frozen ZUNINIT payload review; cached diagnostics grant no acceptance."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import parse_launcher

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
SOURCE = "th02_zuninit.asm"
RANGES = [("start", 0x100, 3, "jmp"), ("sub_103", 0x103, 51, "iret"),
          ("sub_136", 0x136, 18, "iret"), ("sub_148", 0x148, 18, "iret"),
          ("sub_15A", 0x15a, 150, "ret"), ("sub_1F0", 0x1f0, 18, "ret"),
          ("sub_202", 0x202, 59, "ret"), ("sub_413", 0x413, 39, "ret"),
          ("start_0", 0x43a, 251, "int")]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    if len(data) != 1390:
        raise ValueError("complete initializer size differs")
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    entries = {start for _, start, _, _ in RANGES}
    boundaries, rows = set(), []
    for name, start, size, terminal in RANGES:
        body = data[start - 0x100:start - 0x100 + size]
        instructions = list(cs.disasm(body, start))
        if sum(i.size for i in instructions) != size or instructions[-1].mnemonic != terminal:
            raise ValueError("incomplete initializer procedure/terminal boundary")
        if name == "start_0" and instructions[-1].op_str != "0x21":
            raise ValueError("initializer termination interrupt differs")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic == "call":
                if not i.operands or i.operands[0].type != X86_OP_IMM:
                    raise ValueError("unexpected indirect initializer edge")
                edges.append(dict(instruction=i.address, kind=i.mnemonic, target=i.operands[0].imm))
        rows.append(dict(name=name, start=start, size=size, body_sha256=sha(body),
                         terminal=terminal, instruction_count=len(instructions), edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["target"] not in boundaries:
                raise ValueError("initializer branch enters data or instruction operand")
            if edge["kind"] == "call" and edge["target"] not in entries:
                raise ValueError("initializer call enters a procedure interior")
    return rows


def runtime_case(data, tail, resident, free_failures=()):
    """Execute genuine instructions with a limited deterministic DOS interface model."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR
    from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
                                  UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_AX,
                                  UC_X86_REG_BX, UC_X86_REG_DX, UC_X86_REG_EFLAGS)
    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(0, 0x100000)
    uc.mem_write(0x20100, data)
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        uc.reg_write(register, 0x2000)
    uc.reg_write(UC_X86_REG_SP, 0xfffc)  # wrapper's selected-option word is retained
    uc.reg_write(UC_X86_REG_EFLAGS, 2)  # dispatcher executes CLD before copying
    command = tail.encode("ascii")
    if len(command) > 126:
        raise ValueError("constructed tail exceeds PSP")
    uc.mem_write(0x20080, bytes([len(command)]) + command + b"\r")
    old = {0x59: [0x1234, 0x4567], 6: [0x2345, 0x5678], 5: [0x3456, 0x6789]}
    for vector, value in old.items():
        uc.mem_write(vector * 4, struct.pack("<HH", *value))
    if resident:
        uc.mem_write(0x30100, data)
        uc.mem_write(0x59 * 4, struct.pack("<HH", 0x103, 0x3000))
        uc.mem_write(6 * 4, struct.pack("<HH", 0x136, 0x3000))
        uc.mem_write(5 * 4, struct.pack("<HH", 0x148, 0x3000))
        for address, vector in [(0x241, 0x59), (0x245, 5), (0x249, 6)]:
            uc.mem_write(0x30000 + address, struct.pack("<HH", *old[vector]))
        uc.mem_write(0x3002c, struct.pack("<H", 0x4000))
    events, strings, errors, stop = [], [], [], {}
    def interrupt(uc, number, user):
        # ctypes callback exceptions must be captured and raised after emu_start.
        try:
            ax = uc.reg_read(UC_X86_REG_AX)
            ds, dx = uc.reg_read(UC_X86_REG_DS), uc.reg_read(UC_X86_REG_DX)
            if number != 0x21:
                raise ValueError("unexpected kernel interrupt")
            ah, al = ax >> 8, ax & 255
            if ah == 9:
                raw = bytes(uc.mem_read(ds * 16 + dx, 2048)).split(b"$", 1)
                if len(raw) != 2:
                    raise ValueError("unterminated modeled DOS output")
                strings.append(dict(offset=dx, sha256=sha(raw[0])))
                events.append(dict(kind="stdout", offset=dx))
            elif ah == 0x35:
                offset, segment = struct.unpack("<HH", uc.mem_read(al * 4, 4))
                uc.reg_write(UC_X86_REG_BX, offset)
                uc.reg_write(UC_X86_REG_ES, segment)
                events.append(dict(kind="get-vector", vector=al, value=[offset, segment]))
            elif ah == 0x25:
                uc.mem_write(al * 4, struct.pack("<HH", dx, ds))
                events.append(dict(kind="set-vector", vector=al, value=[dx, ds]))
            elif ah == 0x49:
                segment = uc.reg_read(UC_X86_REG_ES)
                failed = segment in free_failures
                flags = uc.reg_read(UC_X86_REG_EFLAGS)
                uc.reg_write(UC_X86_REG_EFLAGS, (flags | 1) if failed else (flags & ~1))
                if failed:
                    uc.reg_write(UC_X86_REG_AX, 7)
                events.append(dict(kind="free-request", segment=segment, modeled_failure=failed))
            elif ah in (0x31, 0x4c):
                stop.update(kind="tsr-request" if ah == 0x31 else "exit-request", code=al)
                if ah == 0x31:
                    stop["paragraphs"] = dx
                uc.emu_stop()
            else:
                raise ValueError("unexpected DOS model function")
        except Exception as error:
            errors.append(str(error))
            uc.emu_stop()
    uc.hook_add(UC_HOOK_INTR, interrupt)
    uc.emu_start(0x20100, 0x30000, count=10000)
    if errors or not stop:
        raise ValueError(errors[0] if errors else "initializer failed to reach bounded stop")
    vectors = {hex(v): list(struct.unpack("<HH", uc.mem_read(v * 4, 4))) for v in old}
    return dict(tail=tail, resident=resident, modeled_free_failures=list(free_failures),
                events=events, strings=strings, stop=stop, vectors=vectors,
                saved_vectors=list(struct.unpack("<6H", uc.mem_read(0x20241, 12))),
                final_sp=uc.reg_read(UC_X86_REG_SP), final_ds=uc.reg_read(UC_X86_REG_DS))


def runtime_matrix(data):
    cases = [runtime_case(data, tail, resident, failures)
             for tail, resident, failures in [
                 ("", False, ()), ("", True, ()), ("/r", True, ()),
                 ("-R", False, ()), ("/X", False, ()), ("-", False, ()),
                 ("word", False, ()), ("/R ignored", True, ()),
                 ("/R", True, (0x4000,)), ("/R", True, (0x3000,))]]
    install = cases[0]
    if (install["stop"] != dict(kind="tsr-request", code=0, paragraphs=0x42) or
            install["saved_vectors"] != [0x1234, 0x4567, 0x3456, 0x6789, 0x2345, 0x5678]):
        raise ValueError("initializer installation state differs")
    if install["vectors"] != {"0x59": [0x103, 0x2000], "0x6": [0x136, 0x2000], "0x5": [0x148, 0x2000]}:
        raise ValueError("initializer installed vector differs")
    for index in (2, 7, 8, 9):
        if cases[index]["vectors"] != {"0x59": [0x1234, 0x4567], "0x6": [0x2345, 0x5678], "0x5": [0x3456, 0x6789]}:
            raise ValueError("initializer restored vector differs")
        if [e["segment"] for e in cases[index]["events"] if e["kind"] == "free-request"] != [0x4000, 0x3000]:
            raise ValueError("initializer free request order differs")
    expected_output = [0x535, 0x5b7]
    if ([s["offset"] for s in cases[8]["strings"]] != expected_output or
            [s["offset"] for s in cases[9]["strings"]] != [0x535, 0x647]):
        raise ValueError("initializer free-failure reporting differs")
    expected_strings = [[0x535, 0x583], [0x535, 0x5a0], [0x535, 0x5b7],
                        [0x535, 0x5fa], [0x615], [0x615], [0x535, 0x583],
                        [0x535, 0x5b7], [0x535, 0x5b7], [0x535, 0x647]]
    for index, case in enumerate(cases):
        expected_stop = (dict(kind="tsr-request", code=0, paragraphs=0x42)
                         if index in (0, 6) else dict(kind="exit-request", code=0))
        if (case["stop"] != expected_stop or case["final_ds"] != 0x2000 or
                case["final_sp"] != 0xfffc or
                [s["offset"] for s in case["strings"]] != expected_strings[index]):
            raise ValueError("initializer exit/stack/segment differs")
    return cases


def interrupt_case(data, entry, latch, direction_set=False):
    """A synthetic interrupt frame and keyboard responses, never a BIOS Oracle."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR, UC_HOOK_CODE
    from unicorn import x86_const as registers
    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(0, 0x100000)
    uc.mem_write(0x20100, data)
    initial = dict(CS=0x2000, SS=0x2000, DS=0x1111, ES=0x9999, AX=2,
                   BX=0x3344, CX=0x5566, DX=0x7788, SI=0x2323, DI=0xabcd, BP=0x9898)
    for name, value in initial.items():
        uc.reg_write(getattr(registers, "UC_X86_REG_" + name), value)
    uc.reg_write(registers.UC_X86_REG_SP, 0xfff6)
    restored_flags = 0x646 if direction_set else 0x246
    uc.reg_write(registers.UC_X86_REG_EFLAGS, 0x402 if direction_set else 2)
    uc.mem_write(0x2fff6, struct.pack("<HHH", 0xffff, 0x2000, restored_flags))
    uc.mem_write(0x2024d, bytes([latch]))
    responses = ([0, 0x10] if entry == 0x103 else
                 ([1, 0, 0, 1] if entry == 0x136 else [2, 0, 0, 2]))
    events, errors, stopped = [], [], []
    def interrupt(uc, number, user):
        try:
            ax = uc.reg_read(registers.UC_X86_REG_AX)
            if number != 0x18:
                raise ValueError("unexpected non-BIOS modeled interrupt")
            event = dict(ax=ax)
            if ax >> 8 == 4:
                if not responses:
                    raise ValueError("constructed keyboard responses exhausted")
                event["returned_ah"] = responses.pop(0)
                uc.reg_write(registers.UC_X86_REG_AX, event["returned_ah"] * 256 + (ax & 255))
            elif ax >> 8 not in (0x41, 0x40, 6):
                raise ValueError("unexpected BIOS model function")
            events.append(event)
        except Exception as error:
            errors.append(str(error))
            uc.emu_stop()
    def code(uc, address, size, user):
        if address == 0x2ffff:
            stopped.append(True)
            uc.emu_stop()
    uc.hook_add(UC_HOOK_INTR, interrupt)
    uc.hook_add(UC_HOOK_CODE, code)
    uc.emu_start(0x20000 + entry, 0x30000, count=10000)
    final = {name: uc.reg_read(getattr(registers, "UC_X86_REG_" + name)) for name in initial}
    final_latch = uc.mem_read(0x2024d, 1)[0]
    if (errors or not stopped or final != initial or
            uc.reg_read(registers.UC_X86_REG_SP) != 0xfffc or
            uc.reg_read(registers.UC_X86_REG_EFLAGS) != restored_flags):
        raise ValueError(errors[0] if errors else "interrupt return/register/frame differs")
    suppressed = entry != 0x103 and latch != 0
    if (suppressed and (events or final_latch != latch)) or (not suppressed and final_latch != 0):
        raise ValueError("resident latch behavior differs")
    return dict(entry=entry, initial_latch=latch, final_latch=final_latch, bios_events=events,
                direction_flag_set=direction_set,
                registers_preserved=final, restored_flags=restored_flags, final_sp=0xfffc,
                text_plane_sha256=sha(bytes(uc.mem_read(0xa0000, 0x1000))),
                attribute_plane_sha256=sha(bytes(uc.mem_read(0xa2000, 0x1000))))


def interrupt_matrix(data):
    cases = [interrupt_case(data, entry, latch, direction) for entry, latch, direction in
             [(0x103, 0, False), (0x136, 0, False), (0x148, 0, False),
              (0x136, 2, False), (0x148, 1, False), (0x103, 0, True), (0x136, 0, True)]]
    for normal, reversed_case in [(cases[0], cases[5]), (cases[1], cases[6])]:
        if (normal["text_plane_sha256"] == reversed_case["text_plane_sha256"] or
                normal["attribute_plane_sha256"] == reversed_case["attribute_plane_sha256"]):
            raise ValueError("reviewed inherited-DF drawing differs")
    return cases


def empty_draw_case(data):
    """Construct a dollar-only string to expose the unguarded CX decrement."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
    from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_SS, UC_X86_REG_SP,
                                  UC_X86_REG_AX, UC_X86_REG_DX, UC_X86_REG_EFLAGS)
    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(0, 0x100000)
    uc.mem_write(0x20100, data)
    uc.mem_write(0x21800, b"$")
    uc.mem_write(0xa2000, b"\xa5" * 65536)
    uc.mem_write(0x2fffc, struct.pack("<H", 0xffff))
    uc.reg_write(UC_X86_REG_CS, 0x2000)
    uc.reg_write(UC_X86_REG_SS, 0x2000)
    uc.reg_write(UC_X86_REG_SP, 0xfffc)
    uc.reg_write(UC_X86_REG_AX, 0x100)
    uc.reg_write(UC_X86_REG_DX, 0x1800)
    uc.reg_write(UC_X86_REG_EFLAGS, 2)
    stopped, writes = [], []
    def code(uc, address, size, user):
        if address == 0x2ffff:
            stopped.append(True)
            uc.emu_stop()
    def write(uc, access, address, size, value, user):
        if 0xa2000 <= address < 0xb2000:
            writes.append((size, value))
    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(0x20202, 0x30000, count=300000)
    memory = bytes(uc.mem_read(0xa2000, 65536))
    if not stopped or len(writes) != 65536 or set(writes) != {(2, 0x41)} or memory != b"A\0" * 32768:
        raise ValueError("empty-string attribute loop differs")
    return dict(constructed_string="$", attribute_word_writes=len(writes),
                attribute_segment_bytes_changed=65536, final_attribute_sha256=sha(memory),
                scope="Constructed empty string; no valid caller currently proved to pass one")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frozen = {}
    def read(path):
        frozen[path] = (ROOT / path).read_bytes()
        return frozen[path]
    config = tomllib.loads(read("config/th03_zun_launcher.toml").decode())
    diet = tomllib.loads(read("config/th03_diet.toml").decode())
    for path in ("config/targets.toml", "scripts/review_th03_zun_init.py", "scripts/lib/zun.py", "scripts/lib/targets.py"):
        read(path)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun")
    stored = read_verified_artifact(ROOT, artifact)
    decoded = read(config["decoded_path"])
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    restoration = json.loads(read(config["diet_receipt"]))
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    if (config["reference_revision"] != REVISION or sha(decoded) != expected["decoded_sha256"] or
            sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"]):
        raise ValueError("initializer decoded restoration lineage differs")
    source = subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98")
    cold = json.loads(read(config["cold_receipt"]))
    if (sha(frozen[config["cold_receipt"]]) != config["cold_receipt_sha256"] or
            cold["reference_revision"] != REVISION or not cold["pass"] or not cold["all_products_equal"]):
        raise ValueError("cached scaffold receipt identity/state differs")
    text = source.decode("shift_jis")
    names = re.findall(r"^(\w+)\s+proc\s+(?:near|far)\s*$", text, re.M)
    if names != [name for name, *_ in RANGES]:
        raise ValueError("complete frozen procedure catalogue differs")
    payload = parse_launcher(decoded, 223)["payloads"][1]
    target = decoded[payload["decoded_file_offset"]:payload["decoded_file_offset"] + payload["size"]]
    source_md5 = re.search(r"Input\s+MD5\s*:\s*([0-9A-Fa-f]{32})", text)[1].lower()
    if hashlib.md5(target).hexdigest() != source_md5:
        raise ValueError("initializer upstream original input MD5 differs")
    target_rows, target_cases = decode(target), runtime_matrix(target)
    target_interrupt_cases = interrupt_matrix(target)
    target_empty_draw_case = empty_draw_case(target)
    pin = next(p for p in config["payloads"] if p["option"] == "-2")
    rounds = []
    for path in pin["cold_paths"]:
        candidate = read(path)
        cached_source_path = str(Path(path).parents[2] / SOURCE)
        cached_source = read(cached_source_path)
        if b"\r" in source or cached_source != source.replace(b"\n", b"\r\n"):
            raise ValueError("cached initializer compiler source differs from frozen candidate")
        if sha(candidate) != pin["sha256"] or candidate != target:
            raise ValueError("complete cached initializer raw bytes differ")
        rows, cases = decode(candidate), runtime_matrix(candidate)
        interrupt_cases = interrupt_matrix(candidate)
        empty_case = empty_draw_case(candidate)
        if (rows != target_rows or cases != target_cases or interrupt_cases != target_interrupt_cases or
                empty_case != target_empty_draw_case):
            raise ValueError("cached initializer diagnostic observations differ")
        rounds.append(dict(path=path, sha256=sha(candidate), complete_raw_equal=True,
                           cached_source_path=cached_source_path, cached_source_exact_text_match=True,
                           cached_source_byte_equal=False, cached_source_transform="LF to CRLF only",
                           procedures=rows, runtime_cases=cases, interrupt_cases=interrupt_cases,
                           empty_draw_case=empty_case))
    for path, data in frozen.items():
        if (ROOT / path).read_bytes() != data:
            raise ValueError("initializer diagnostic input changed")
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical ZUN changed")
    if subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98") != source:
        raise ValueError("frozen initializer source changed")
    result = dict(kind="th03-zun-init-complete-candidate-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, source=SOURCE, source_sha256=sha(source), source_input_md5=source_md5,
                  stored_sha256=sha(stored), decoded_sha256=sha(decoded), initializer_sha256=sha(target),
                  payload=payload, target_procedures=target_rows, target_runtime_cases=target_cases, rounds=rounds,
                  target_interrupt_cases=target_interrupt_cases,
                  target_empty_draw_case=target_empty_draw_case,
                  byte_accounting=dict(procedure_bodies=607, resident_data=470, transient_strings=313),
                  runtime_scope="Constructed DOS interface model; no actual kernel/free/TSR/BIOS/game execution",
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  inputs={p: sha(d) for p, d in frozen.items()}, diagnostic_checks_pass=True,
                  fresh_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS complete 1390-byte cached equality, nine procedures, 54 bounded CPU/model cases; no acceptance: {args.output}")


if __name__ == "__main__":
    main()
