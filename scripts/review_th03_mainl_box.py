#!/usr/bin/env python3
"""Execute MAINL box/cursor instructions with explicit flat plane/interface models."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_mainl_cutscene import CS, DS, Probe, RANGES, sha

ROOT = Path(__file__).resolve().parents[1]
PLANES = (0xa800, 0xb000, 0xb800, 0xe000)
BOX_POINTER = 0x21da
SIZE = 0x3c00
CUTSCENE_PROOF_SHA256 = "5a8afb0c78b4c2303258d8e0c8c152ccc5a62c1945807c89b227263cdc909ac4"


def coordinates():
    """Independent rectangle/planar layout specification, not a device model."""
    return [segment * 16 + y * 80 + x // 8
            for y in range(320, 384) for x in range(80, 560, 16) for segment in PLANES]


def describe_accesses(accesses):
    return dict(count=len(accesses), sha256=sha(json.dumps(accesses, separators=(",", ":")).encode()),
                first=accesses[:4], last=accesses[-4:])


class BoxProbe(Probe):
    """Own hooks: allocator/free/wait/tolower models; no font, EGC or page banks."""
    def __init__(self, mz, allocation=0x6000):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN, UC_MEM_WRITE
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.events, self.ports, self.errors = [], [], []
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for relocation in mz.relocations:
            at = relocation.segment * 16 + relocation.offset
            struct.pack_into("<H", image, at, (struct.unpack_from("<H", image, at)[0] + 0x2000) & 65535)
        self.uc.mem_write(0x20000, bytes(image))
        self.code, self.data, self.stack = (0x2000 + CS) * 16, (0x2000 + DS) * 16, 0x40000
        for name, value in (("CS", 0x2000 + CS), ("DS", 0x2000 + DS), ("SS", 0x4000),
                            ("ES", 0x3333), ("BP", 0x7777), ("SI", 0x1357), ("DI", 0x2468), ("EFLAGS", 0x202)):
            self.set(name, value)
        self.word(0x21e0, 80)
        self.word(0x21e2, 320)
        self.accesses = []
        self.calls = 0
        self.backup_base = allocation * 16
        self.waits = []
        for index, segment in enumerate(PLANES):
            self.uc.mem_write(self.data + 0x1c60 + index * 4, struct.pack("<HH", 0, segment))
        models = {0x221ae: ("HMEM_ALLOCBYTE", 2, 2), 0x222b2: ("HMEM_FREE", 2, 2),
                  (0x2000 + 0xc7e) * 16 + 0xee5: ("input_wait_for_change", 2, 2),
                  0x23641: ("tolower", 2, 0)}

        def guarded(callback):
            def call(*args):
                try:
                    callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
            return call

        def code(uc, address, length, user):
            if address == self.code + 0xff00:
                self.stop = True
                uc.emu_stop()
                return
            if address in models:
                name, count, cleanup = models[address]
                expected_segment = 0x2c7e if name == "input_wait_for_change" else 0x2000
                if self.get("CS") != expected_segment:
                    raise ValueError("box import segment alias")
                sp = self.get("SP")
                words = list(struct.unpack("<" + "H" * ((count + 4) // 2), uc.mem_read(self.stack + sp, count + 4)))
                args = words[2:]
                event = dict(name=name, args=args, box_pointer=[self.word(BOX_POINTER), self.word(BOX_POINTER + 2)])
                if name == "HMEM_ALLOCBYTE":
                    self.set("AX", allocation)
                elif name == "tolower":
                    self.set("AX", args[0] + 32 if 65 <= args[0] <= 90 else args[0])
                else:
                    # Constructed failed free / completed wait, not actual DOS semantics.
                    self.set("AX", 0xffff)
                    self.set("EFLAGS", self.get("EFLAGS") | 1)
                    if name == "input_wait_for_change":
                        self.waits.append(args[0])
                event["returned_ax"] = self.get("AX")
                event["returned_cf"] = self.get("EFLAGS") & 1
                self.events.append(event)
                self.set("SP", sp + 4 + cleanup)
                self.set("CS", words[1])
                self.set("IP", words[0])
                return
            offset = address - self.code
            allowed = {"box_allocate_snap", "box_free", "box_put", "cursor_advance", "script_op", "number_first", "number_second"}
            if self.get("CS") != 0x2000 + CS or not any(name in allowed and start <= offset < start + size for name, start, size, _ in RANGES):
                raise ValueError("CPU escaped box reviewed bodies/interfaces")

        def memory(uc, access, address, width, value, user):
            if (any(segment * 16 <= address < segment * 16 + 0x8000 for segment in PLANES) or
                    self.backup_base <= address < self.backup_base + 0x10000):
                self.accesses.append(["write" if access == UC_MEM_WRITE else "read", address, width])

        def interrupt(uc, number, user):
            raise ValueError("unexpected box kernel interrupt")

        def output(uc, port, width, value, user):
            if port != 0xa6 or width != 1:
                raise ValueError("unexpected box port/width")
            self.ports.append([port, value])

        def input_port(uc, port, width, user):
            # IN never occurs in these owned bodies; reject rather than model it.
            self.errors.append("unexpected box input port")
            self.uc.emu_stop()
            return 0

        self.uc.hook_add(UC_HOOK_CODE, guarded(code))
        self.uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, guarded(memory))
        self.uc.hook_add(UC_HOOK_INTR, guarded(interrupt))
        self.uc.hook_add(UC_HOOK_INSN, guarded(output), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, input_port, None, 1, 0, reg.UC_X86_INS_IN)

    def pointer(self, offset, segment):
        self.word(BOX_POINTER, offset)
        self.word(BOX_POINTER + 2, segment)
        self.backup_base = segment * 16

    def run(self, entry, args=(), budget=800000):
        self.stop = False
        self.errors.clear()
        self.set("SP", 0xfff0)
        self.uc.mem_write(self.stack + 0xfff0, struct.pack("<" + "H" * (1 + len(args)), 0xff00, *args))
        self.uc.emu_start(self.code + entry, 0x100000, count=budget)
        if self.errors or not self.stop:
            raise ValueError(self.errors[0] if self.errors else "box scope exhausted instruction budget before return")
        if self.get("SP") != 0xfff2 + 2 * len(args) or [self.get(r) for r in ("BP", "SI", "DI")] != [0x7777, 0x1357, 0x2468]:
            raise ValueError("box near cleanup/callee-saved contract differs")
        self.calls += 1


def seed(p):
    raw = []
    for plane, segment in enumerate(PLANES):
        data = b"".join(struct.pack("<H", (i * 37 + plane * 0x1111) & 65535) for i in range(0x4000))
        p.uc.mem_write(segment * 16, data)
        raw.append(data)
    backup = b"".join(raw[plane][y * 80 + x // 8:y * 80 + x // 8 + 2]
                      for y in range(320, 384) for x in range(80, 560, 16) for plane in range(4))
    return raw, backup


def expect_copy(p, *, snapshot, segment, offset=0, repeats=1):
    expected = []
    for _ in range(repeats):
        for i, address in enumerate(coordinates()):
            backup = segment * 16 + ((offset + i * 2) & 65535)
            expected.extend([["read", address if snapshot else backup, 2],
                             ["write", backup if snapshot else address, 2]])
    if p.accesses != expected:
        raise ValueError("box ordered word/plane/offset transfer differs")


def matrix(mz):
    cases, calls = [], 0
    for allocation in (0x6000, 0):
        for old in ((0, 0), (7, 0x6100)):
            p = BoxProbe(mz, allocation)
            original, backup = seed(p)
            p.pointer(*old)
            p.backup_base = allocation * 16
            p.run(0xd7b)
            expect_copy(p, snapshot=True, segment=allocation)
            if (p.uc.mem_read(allocation * 16, SIZE) != backup or
                    [p.word(BOX_POINTER), p.word(BOX_POINTER + 2)] != [0, allocation] or
                    p.ports != [[0xa6, 0]] or p.events[-1]["args"] != [SIZE] or p.events[-1]["box_pointer"] != [0, 0] or
                    [e["name"] for e in p.events] != (["HMEM_FREE"] if old != (0, 0) else []) + ["HMEM_ALLOCBYTE"]):
                raise ValueError("box unchecked allocation/snapshot contract differs")
            transfer = describe_accesses(p.accesses)
            p.run(0xe4c)
            if p.word(BOX_POINTER) or p.word(BOX_POINTER + 2):
                raise ValueError("box pointer not cleared after modeled failed free")
            if allocation and p.events[-1]["name"] != "HMEM_FREE":
                raise ValueError("allocated box free omitted")
            if not allocation and p.events[-1]["name"] != "HMEM_ALLOCBYTE":
                raise ValueError("NULL pointer wrongly freed")
            cases.append(dict(kind="snapshot_then_free", allocation_segment=allocation, old_pointer=old,
                              backup_sha256=sha(backup), transfers=transfer, ports=p.ports, events=p.events))
            calls += p.calls
    for offset, segment in ((0, 0x6000), (0xff00, 0x6000), (0, 0)):
        p = BoxProbe(mz)
        original, backup = seed(p)
        p.pointer(offset, segment)
        for i in range(0, SIZE, 2):
            p.uc.mem_write(segment * 16 + ((offset + i) & 65535), backup[i:i + 2])
        for plane in PLANES:
            p.uc.mem_write(plane * 16, b"\xa5" * 0x8000)
        p.run(0xe6b)
        expect_copy(p, snapshot=False, segment=segment, offset=offset)
        if [p.word(BOX_POINTER), p.word(BOX_POINTER + 2)] != [offset, segment]:
            raise ValueError("restore mutated its far backup pointer")
        for plane, data in zip(PLANES, original):
            expected = bytearray(b"\xa5" * 0x8000)
            for y in range(320, 384):
                start = y * 80 + 10
                expected[start:start + 60] = data[start:start + 60]
            if p.uc.mem_read(plane * 16, 0x8000) != expected:
                raise ValueError("box restored rectangle/outside guard differs")
        cases.append(dict(kind="restore", pointer=[offset, segment], transfers=describe_accesses(p.accesses),
                          null_pointer_reads_low_memory=segment == 0, far_offset_only_wrap=offset == 0xff00))
        calls += p.calls
    for pointer in ((0, 0), (7, 0), (17, 0x6100)):
        p = BoxProbe(mz)
        p.pointer(*pointer)
        p.run(0xe4c)
        if (len(p.events) != int(pointer != (0, 0)) or p.word(BOX_POINTER) or p.word(BOX_POINTER + 2) or
                (p.events and p.events[0]["args"] != [pointer[1]])):
            raise ValueError("box full-far-pointer test/segment-only failed free differs")
        cases.append(dict(kind="free", pointer=pointer, events=p.events))
        calls += p.calls
    cursor_cases = [(528, 320, 0, [544, 320], 0), (544, 352, 0, [144, 368], 0),
                    (544, 368, 0, [80, 320], 2), (544, 368, 1, [80, 320], 2),
                    (0xffff, 368, 0, [15, 368], 0), (0x7fff, 368, 0, [0x800f, 368], 0)]
    commands = [("n", "7!", 0, [7]), ("s", "-!", 0, []), ("s", "12!", 0, [12]), ("s", "12!", 1, [])]
    for case in cursor_cases + commands:
        p = BoxProbe(mz)
        seed(p)
        p.pointer(0, 0x6000)
        p.uc.mem_write(0x60000, b"\x5a\xa5" * (SIZE // 2))
        if isinstance(case[0], int):
            x, y, fast, expected_cursor, copies = case
            p.word(0x21e0, x)
            p.word(0x21e2, y)
            expected_waits = [0] if copies and not fast else []
            entry, args = 0x100c, ()
            description = dict(kind="cursor", initial=[x, y], fast_forward=fast)
        else:
            command, tail, fast, expected_waits = case
            p.word(0x21e2, 368)
            p.script(tail.encode())
            expected_cursor, copies = [80, 320], 2
            entry, args = 0x105d, (ord(command),)
            description = dict(kind="script_box_change", command=command, tail=tail, fast_forward=fast)
        p.uc.mem_write(p.data + 0x21de, bytes([fast]))
        p.run(entry, args)
        expect_copy(p, snapshot=False, segment=0x6000, repeats=copies)
        if ([p.word(0x21e0), p.word(0x21e2)] != expected_cursor or p.waits != expected_waits or
                p.ports != ([[0xa6, 1], [0xa6, 0]] if copies else [])):
            raise ValueError("cursor/script wait/reset/dual-restore contract differs")
        cases.append(dict(**description, final_cursor=expected_cursor, waits=p.waits, ports=p.ports,
                          transfers=describe_accesses(p.accesses), events=p.events))
        calls += p.calls
    return dict(cases=cases, top_level_calls=calls,
                model="Four initialized flat 32KiB plane regions; page port logged, banks/device effects unmodeled; allocator/free/wait/tolower substituted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutscene-proof", type=Path, default=Path(".analysis/sol-mainl-cutscene-review-20261006.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proof_raw = (ROOT / args.cutscene_proof).read_bytes()
    if sha(proof_raw) != CUTSCENE_PROOF_SHA256:
        raise ValueError("cutscene diagnostic proof differs from reviewed pin")
    proof = json.loads(proof_raw)
    if proof["kind"] != "th03-mainl-whole-cutscene-candidate-analysis" or not proof["diagnostic_checks_pass"] or proof["exact_acceptance"]:
        raise ValueError("box review requires guarded diagnostic cutscene proof")
    inputs = {**proof["inputs"], str(args.cutscene_proof): sha(proof_raw)}
    for path in ("scripts/review_th03_mainl_box.py",):
        inputs[path] = sha((ROOT / path).read_bytes())
    def verify():
        for path, digest in inputs.items():
            if sha((ROOT / path).read_bytes()) != digest:
                raise ValueError(f"box review input changed: {path}")
    verify()
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-mainl")
    stored = read_verified_artifact(ROOT, artifact)
    if sha(stored) != proof["stored_sha256"]:
        raise ValueError("canonical MAINL differs from cutscene proof")
    images = [(path, parse_mz((ROOT / path).read_bytes())) for path in inputs if path.endswith("mainl.exe")]
    if len(images) != 3 or any(not mz.valid for _, mz in images):
        raise ValueError("box target/two cached images absent or invalid")
    observations = [dict(path=path, runtime=matrix(mz)) for path, mz in images]
    if any(item["runtime"] != observations[0]["runtime"] for item in observations[1:]):
        raise ValueError("box CPU contracts differ between target/cached images")
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical MAINL changed")
    result = dict(kind="th03-mainl-box-cpu-flat-memory-diagnostics", observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, observations=observations, total_top_level_calls=sum(o["runtime"]["top_level_calls"] for o in observations),
                  diagnostic_checks_pass=True, page_banks_proved=False, whole_runtime_proved=False,
                  tools=dict(unicorn_distribution=version("unicorn")),
                  source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS {result['total_top_level_calls']} box/cursor/script CPU calls; flat memory only: {args.output}")


if __name__ == "__main__":
    main()
