#!/usr/bin/env python3
"""MAINL picture/packed-pixel CPU and port observations; EGC/banks unmodeled."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_mainl_cutscene import CS, DS, Probe, REVISION, sha
from review_th03_mainl_box import describe_accesses

ROOT = Path(__file__).resolve().parents[1]
CUTSCENE_PROOF_SHA256 = "5a8afb0c78b4c2303258d8e0c8c152ccc5a62c1945807c89b227263cdc909ac4"
PROVIDERS = ("th01/hardware/egc_impl.hpp", "th02/formats/pi.h", "th03/formats/pi.hpp",
             "libs/master.lib/egc.asm", "libs/master.lib/graph_pack_put_8_noclip.asm",
             "libs/master.lib/rottbl.asm", "libs/master.lib/clip[data].asm")
HELPERS = [("egc_on", 0x724, 21, ""), ("egc_off", 0x73a, 31, ""),
           ("egc_start_end_alias", 0x75a, 43, ""),
           ("packed_clip_tail", 0x2c68, 6, "0xa"), ("packed_body", 0x2c6e, 196, "0xa")]
ON = [[0x7c, 1, 0], [0x6a, 1, 7], [0x6a, 1, 5], [0x7c, 1, 0x80], [0x6a, 1, 6]]
SETUP = [[0x4a0, 2, 0xfff0], [0x4a2, 2, 0xff], [0x4a4, 2, 0x3100],
         [0x4a8, 2, 0xffff], [0x4ac, 2, 0], [0x4ae, 2, 15]]
OFF = [[0x4a0, 2, 0xfff0], [0x4a8, 2, 0xffff], [0x6a, 1, 7],
       [0x6a, 1, 4], [0x7c, 1, 0], [0x6a, 1, 6]]


def signed(word):
    return word - 65536 if word & 0x8000 else word


def planar(packed):
    """Independent nibble/pixel-bit specification; no use of target RotTbl."""
    pixels = [nibble for byte in packed for nibble in (byte >> 4, byte & 15)]
    return [sum(((pixel >> plane) & 1) << (7 - index) for index, pixel in enumerate(pixels))
            for plane in range(4)]


def helper_analysis(image):
    rows, boundaries = [], set()
    for name, start, size, cleanup in HELPERS:
        body = image[start:start + size]
        instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, start))
        if (sum(i.size for i in instructions) != size or instructions[-1].mnemonic != "retf" or
                instructions[-1].op_str != cleanup):
            raise ValueError("picture direct helper boundary/far cleanup differs")
        boundaries.update(i.address for i in instructions)
        rows.append(dict(name=name, start=start, size=size, sha256=sha(body), instructions=len(instructions)))
    for start, size in [(0x2c6e, 196)]:
        for instruction in Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[start:start + size], start):
            if instruction.mnemonic.startswith("j"):
                destination = int(instruction.op_str, 16)
                if destination not in boundaries or not (start <= destination < start + size or destination == 0x2c68):
                    raise ValueError("packed helper edge leaves body/shared return tail")
    table = b"".join(struct.pack("<I", sum(((((byte & 15) >> plane) & 1) |
                        ((((byte >> 4) >> plane) & 1) << 1)) << (8 * plane) for plane in range(4)))
                     for byte in range(256))
    if image[0x1aaa:0x1eaa] != table or struct.unpack_from("<H", image, DS * 16 + 0x52e)[0] != 0xa800:
        raise ValueError("packed rotation table/initial clipping segment differs")
    if [image[at] for at in (0x739,0x759,0x785)] != [0x90]*3:
        raise ValueError("complete EGC provider observed EVEN bytes differ")
    return dict(helpers=rows, table_start=0x1aaa, table_size=1024, table_sha256=sha(table),
                mask_words=list(struct.unpack_from("<16H", image, DS * 16 + 0x8e2)),
                clipping_segment_initial=0xa800, ownership_acceptance=False)


def far_return_engine_control():
    """Synthetic ISA control isolates the memory-read-hook RETF defect."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ
    from unicorn.x86_const import UC_X86_REG_CS, UC_X86_REG_SS, UC_X86_REG_SP
    observations = []
    for read_hook in (False, True):
        uc = Uc(UC_ARCH_X86, UC_MODE_16)
        uc.mem_map(0, 0x100000)
        # CALL FAR 2000:0724; HLT. Callee is just RETF, no target bytes.
        uc.mem_write(0x295f0, b"\x9a\x24\x07\x00\x20\xf4")
        uc.mem_write(0x20724, b"\xcb")
        uc.reg_write(UC_X86_REG_CS, 0x295f)
        uc.reg_write(UC_X86_REG_SS, 0x4000)
        uc.reg_write(UC_X86_REG_SP, 0xfff0)
        trace, frames = [], []
        def code(cpu, address, width, user):
            trace.append(address)
            if address == 0x20724:
                frames.append(list(struct.unpack("<HH", cpu.mem_read(0x40000 + cpu.reg_read(UC_X86_REG_SP), 4))))
            if len(trace) == 3:
                cpu.emu_stop()
        uc.hook_add(UC_HOOK_CODE, code)
        if read_hook:
            uc.hook_add(UC_HOOK_MEM_READ, lambda *args: None)
        uc.emu_start(0x295f0, 0x100000, count=3)
        observations.append(dict(memory_read_hook=read_hook, trace=trace, far_return_frames=frames,
                                 expected_return_address=0x295f5, returned_correctly=trace[-1] == 0x295f5))
    if ([o["returned_correctly"] for o in observations] != [True, False] or
            any(o["far_return_frames"] != [[5, 0x295f]] for o in observations)):
        raise ValueError("far-RET memory-read-hook defect control differs; review return model before using this engine")
    return observations


class PictureProbe(Probe):
    """Flat memory/ports and far-RET transition model; helper operations execute."""
    def __init__(self, mz, df=False):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN, UC_MEM_WRITE
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for relocation in mz.relocations:
            at = relocation.segment * 16 + relocation.offset
            struct.pack_into("<H", image, at, (struct.unpack_from("<H", image, at)[0] + 0x2000) & 65535)
        self.uc.mem_write(0x20000, bytes(image))
        self.code, self.data, self.stack = (0x2000 + CS) * 16, (0x2000 + DS) * 16, 0x40000
        for name, value in (("CS", 0x2000 + CS), ("DS", 0x2000 + DS), ("SS", 0x4000),
                            ("ES", 0x3333), ("BP", 0x7777), ("SI", 0x1357), ("DI", 0x2468), ("EFLAGS", 0x202 | (0x400 if df else 0))):
            self.set(name, value)
        self.uc.mem_write(self.data + 0x1c60, struct.pack("<HH", 0, 0xa800))
        self.uc.mem_write(0x50000, bytes(((i * 73 + (i >> 8) * 19 + 5) & 255) for i in range(0x30000)))
        self.errors, self.ports, self.words, self.packed, self.pack_reads, self.pack_writes, self.masks = [], [], [], [], [], [], []
        self.stop, self.address = False, 0
        self.far_returns = []

        def guarded(callback):
            def invoke(*args):
                try:
                    return callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
            return invoke

        def code(uc, address, length, user):
            self.address = address
            if address == self.code + 0xff00:
                self.stop = True
                uc.emu_stop()
                return
            if address == 0x20000 + 0x2c6e:
                if self.get("CS") != 0x2000:
                    raise ValueError("packed helper segment alias")
                sp = self.get("SP")
                args = list(struct.unpack("<5H", uc.mem_read(self.stack + sp + 4, 10)))
                self.packed.append(dict(args=args, reads_start=len(self.pack_reads), writes_start=len(self.pack_writes)))
            if address in (0x20000 + 0x2d2f, 0x20000 + 0x2c6b):
                if not self.packed:
                    raise ValueError("packed return without complete helper entry")
                self.check_packed_return()
            if address in (0x20738, 0x20758, 0x20784, 0x22c6b, 0x22d2f):
                if self.get("CS") != 0x2000:
                    raise ValueError("picture far-return segment alias")
                # Unicorn 1.0.2rc4 with memory-read hooks mishandles real RETF
                # into nonzero CS despite a correct frame. Perform the declared
                # architectural stack/CS/IP transition, preserving all flags.
                cleanup = 10 if address in (0x22c6b, 0x22d2f) else 0
                opcode = b"\xca\x0a\x00" if cleanup else b"\xcb"
                if bytes(uc.mem_read(address, len(opcode))) != opcode:
                    raise ValueError("modeled far-return opcode/cleanup differs")
                sp = self.get("SP")
                offset, segment = struct.unpack("<HH", uc.mem_read(self.stack + sp, 4))
                self.far_returns.append([address, offset, segment, cleanup])
                self.set("SP", sp + 4 + cleanup)
                self.set("CS", segment)
                self.set("IP", offset)
                return
            offset = address - self.code
            root_allowed = any(start <= offset < start + size for start, size in [(0xba3, 52), (0xbd7, 117), (0xc4c, 303)])
            helper_allowed = any(0x20000 + start <= address < 0x20000 + start + size for _, start, size, _ in HELPERS)
            if not ((self.get("CS") == 0x2000 + CS and root_allowed) or (self.get("CS") == 0x2000 and helper_allowed)):
                raise ValueError(f"CPU escaped picture reviewed bodies/helpers at {address:05X}, CS={self.get('CS'):04X}")

        def memory(uc, access, address, width, value, user):
            kind = "write" if access == UC_MEM_WRITE else "read"
            if self.address - self.code in (0xc0f, 0xc21, 0xd18, 0xd21):
                self.words.append([kind, address, width])
            if 0x20000 + 0x2c6e <= self.address < 0x20000 + 0x2d32:
                if kind == "read" and 0x50000 <= address < 0x80000:
                    self.pack_reads.append([address, width])
                if kind == "write" and address >= 0xa8000:
                    self.pack_writes.append([address, width, value])

        def output(uc, port, width, value, user):
            if (port, width) not in {(0x7c, 1), (0x6a, 1), (0xa4, 1), (0xa6, 1),
                                    (0x4a0, 2), (0x4a2, 2), (0x4a4, 2), (0x4a8, 2), (0x4ac, 2), (0x4ae, 2)}:
                raise ValueError("unexpected picture port/width")
            self.ports.append([port, width, value])
            if self.address == self.code + 0xd04:
                self.masks.append(value)

        def interrupt(uc, number, user):
            raise ValueError("unexpected picture interrupt")

        def input_port(uc, port, width, user):
            self.errors.append("unexpected picture input port")
            uc.emu_stop()
            return 0

        self.uc.hook_add(UC_HOOK_CODE, guarded(code))
        self.uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, guarded(memory))
        self.uc.hook_add(UC_HOOK_INTR, guarded(interrupt))
        self.uc.hook_add(UC_HOOK_INSN, guarded(output), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, input_port, None, 1, 0, reg.UC_X86_INS_IN)

    def check_packed_return(self):
        event = self.packed[-1]
        length, pointer_offset, pointer_segment, top, left = event["args"]
        count, x = signed(length) >> 3, signed(left) >> 3
        source = pointer_offset
        if x < 0:
            count += x
            source = (source + x * 4) & 65535
            x = 0
        if count <= 0 or x >= 80:
            count = 0
        else:
            count = min(count, 80 - x)
        reads, writes = [], []
        for group in range(count):
            addresses = [pointer_segment * 16 + ((source + group * 4 + i) & 65535) for i in range(4)]
            packed = bytes(bytes(self.uc.mem_read(at, 1))[0] for at in addresses)
            reads += [[at, 1] for at in addresses]
            vo = (signed(top) * 80 + x + group) & 65535
            destinations = [0xa8000 + vo, 0xa8000 + ((vo + 0x8000) & 65535), 0xb8000 + vo, 0xe0000 + vo]
            writes += [[at, 1, value] for at, value in zip(destinations, planar(packed))]
        if self.pack_reads[event["reads_start"]:] != reads or self.pack_writes[event["writes_start"]:] != writes:
            raise ValueError("packed helper source/plane-byte conversion/clipping differs")
        event.update(output_groups=count, source_offset=source, far_offset_only_wrap=True,
                     input_reads=describe_accesses(reads), plane_writes=describe_accesses(writes),
                     df_at_return=bool(self.get("EFLAGS") & 0x400))

    def run(self, entry, args=(), far=False, budget=5000000):
        self.stop = False
        self.errors.clear()
        self.set("SP", 0xffd0)
        words = [0xff00, 0x2000 + CS] + list(args) if far else [0xff00] + list(args)
        self.uc.mem_write(self.stack + 0xffd0, struct.pack("<" + "H" * len(words), *words))
        self.set("CS", 0x2000 if far else 0x2000 + CS)
        self.uc.emu_start((0x20000 if far else self.code) + entry, 0x100000, count=budget)
        if self.errors or not self.stop:
            raise ValueError(self.errors[0] if self.errors else "picture instruction budget exhausted before return")
        if (self.get("SP") != 0xffd0 + 2 * len(words) or self.get("DS") != 0x2000 + DS or
                [self.get(r) for r in ("BP", "SI", "DI")] != [0x7777, 0x1357, 0x2468]):
            raise ValueError("picture near/far cleanup or saved DS/BP/SI/DI differs")


def copy_words(left, top):
    return [0xa8000 + ((signed(left & 65535) // 8 + signed(top & 65535) * 80 + y * 80 + x * 2) & 65535)
            for y in range(200) for x in range(20)]


def copy_ports():
    return ON + SETUP + [[port, 1, page] for _ in range(4000) for port, page in [(0xa6, 0), (0xa6, 1)]] + OFF + [[0xa6, 1, 0]]


def copy_case(mz, left, top):
    p = PictureProbe(mz)
    p.run(0xbd7, (top & 65535, left & 65535))
    expected = [[kind, at, 2] for at in copy_words(left, top) for kind in ("read", "write")]
    if p.words != expected or p.ports != copy_ports() or p.packed:
        raise ValueError("copy geometry/port/word order differs")
    return dict(left=left, top=top, word_accesses=describe_accesses(p.words), ports=describe_accesses(p.ports),
                modeled_far_returns=describe_accesses(p.far_returns),
                bank_effects_proved=False)


def masked_case(mz, quarter, mask, initial_offset=0):
    p = PictureProbe(mz)
    p.uc.mem_write(p.data + 0x1f0e, struct.pack("<HH", initial_offset, 0x5000))
    p.run(0xc4c, (mask & 65535, quarter & 65535, 64, 160))
    offset = (initial_offset + {1:0xa0, 2:0xfa00, 3:0xfaa0}.get(quarter, 0)) & 65535
    segment, offset = (0x5000 + (offset >> 4)) & 65535, offset & 15
    expected_args, expected_masks, words = [], [], []
    for y in range(200):
        expected_args.append([320, offset, segment, 400, 0])
        offset += 320
        segment, offset = (segment + (offset >> 4)) & 65535, offset & 15
        mask_at = (0x8e2 + ((mask * 8 + (y % 4) * 2) & 65535)) & 65535
        expected_masks.append(p.word(mask_at))
        for x in range(20):
            words.extend([["read", 0xa8000 + 0x7d00 + x * 2, 2],
                          ["write", 0xa8000 + (64 + y) * 80 + 20 + x * 2, 2]])
    words += [[kind, at, 2] for at in copy_words(160, 64) for kind in ("read", "write")]
    ports = [[0xa4, 1, 1], [0xa6, 1, 0]]
    for value in expected_masks:
        ports += ON + SETUP + [[0x4a2, 2, 0xff], [0x4a4, 2, 0x3100], [0x4ae, 2, 15], [0x4a8, 2, value]] + OFF
    ports += [[0xa4, 1, 0]] + copy_ports()
    if (len(p.packed) != 200 or [e["args"] for e in p.packed] != expected_args or p.masks != expected_masks or
            p.words != words or p.ports != ports or p.word(0x1f0e) != initial_offset or p.word(0x1f10) != 0x5000):
        raise ValueError("masked picture row-pointer/mask/word/port order differs")
    return dict(quarter=quarter, mask_id=mask, initial_pointer=[initial_offset, 0x5000],
                packed_rows=p.packed, masks=expected_masks, word_accesses=describe_accesses(p.words),
                ports=describe_accesses(p.ports), first_source_pointer=expected_args[0][1:3],
                modeled_far_returns=describe_accesses(p.far_returns),
                caller_pointer_preserved=True, actual_egc_mask_pixels_proved=False)


def matrix(mz):
    copies = [copy_case(mz, left, top) for left, top in [(160,64), (0,0), (-1,-1), (638,399)]]
    masked = [masked_case(mz, q, m, off) for q, m, off in
              [(0,0,0), (1,1,0), (2,2,0), (3,3,0), (2,2,0xff80), (-1,0,0), (4,3,0), (0,-1,0), (0,4,0)]]
    packed = []
    for left, top, length, pointer, df in [(0,400,320,0x100,False), (-8,0,16,0x100,False),
            (-16,0,8,0x100,True), (632,399,64,0x100,False), (640,0,8,0x100,True),
            (0,0,0,0x100,True), (0,0,-8,0x100,True), (0,-1,8,0x100,False),
            (0,0,16,0xfffe,True)]:
        p = PictureProbe(mz, df)
        p.run(0x2c6e, (length & 65535, pointer, 0x5000, top & 65535, left & 65535), far=True)
        packed.append(dict(left=left, top=top, length=length, pointer_offset=pointer, inherited_df=df,
                           observation=p.packed[0], final_df=bool(p.get("EFLAGS") & 0x400),
                           modeled_far_returns=p.far_returns))
    p = PictureProbe(mz)
    p.run(0xba3)
    if p.ports != ON + SETUP:
        raise ValueError("standalone EGC start ports differ")
    alias = PictureProbe(mz)
    alias.run(0x75a, far=True)
    if alias.ports != ON + [row for row in SETUP if row[0] != 0x4a4] + OFF:
        raise ValueError("complete EGC START/END alias ports differ")
    return dict(copy_cases=copies, masked_cases=masked, packed_cases=packed, standalone_egc_ports=p.ports,
                library_egc_start_end_ports=alias.ports, library_egc_start_end_far_returns=alias.far_returns,
                top_level_calls=len(copies)+len(masked)+len(packed)+2,
                scope="Actual root and helper operations, far-RET transition modeled for Unicorn defect; flat memory/port logs only; EGC logic/banks/device timing unmodeled")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutscene-proof", type=Path, default=Path(".analysis/sol-mainl-cutscene-review-20261006.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT / args.cutscene_proof).read_bytes()
    if sha(raw) != CUTSCENE_PROOF_SHA256:
        raise ValueError("picture requires pinned complete cutscene diagnostic proof")
    proof = json.loads(raw)
    inputs = {**proof["inputs"], str(args.cutscene_proof): sha(raw)}
    for path in ("scripts/review_th03_mainl_picture.py", "scripts/review_th03_mainl_box.py"):
        inputs[path] = sha((ROOT / path).read_bytes())
    def verify():
        for path, digest in inputs.items():
            if sha((ROOT / path).read_bytes()) != digest:
                raise ValueError(f"picture review input changed: {path}")
    verify()
    sources = {path: subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") for path in PROVIDERS}
    table_literals = re.findall(rb"(?<![\w])([0-9a-fA-F]{8})h", sources["libs/master.lib/rottbl.asm"])
    if len(table_literals) != 256:
        raise ValueError("frozen packed table literal count differs")
    table_bytes = b"".join(struct.pack("<I", int(value,16)) for value in table_literals)
    images = [(path, parse_mz((ROOT / path).read_bytes())) for path in inputs if path.endswith("mainl.exe")]
    if len(images) != 3 or any(not mz.valid for _, mz in images):
        raise ValueError("picture target/two cached images absent/invalid")
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-mainl")
    stored = read_verified_artifact(ROOT, artifact)
    if sha(stored) != proof["stored_sha256"]:
        raise ValueError("canonical MAINL differs from guarded proof")
    engine_control = far_return_engine_control()
    observations = []
    for path, mz in images:
        if "th03-diet" not in path:
            tree = Path(path).parents[2]
            for source, original in sources.items():
                cached_path = str(tree / source)
                cached = (ROOT / cached_path).read_bytes()
                if cached != (original.replace(b"\n", b"\r\n") if source.endswith(".asm") else original):
                    raise ValueError("picture cached provider association differs")
                inputs[cached_path] = sha(cached)
            map_path = next(p for p in inputs if str(tree) in p and p.endswith("mainl.map"))
            map_text = (ROOT / map_path).read_text(encoding="ascii")
            if set(re.findall(r"(?m)^\s*0000:075A(?: idle)?\s+(EGC_(?:START|END))\s*$", map_text)) != {"EGC_START","EGC_END"}:
                raise ValueError("cached EGC START/END public alias association differs")
        if mz.program_image[0x1aaa:0x1eaa] != table_bytes:
            raise ValueError("frozen packed rotation table differs from target/candidate")
        analysis = helper_analysis(mz.program_image)
        analysis["original_segment_relocation_sites"] = [r.segment * 16 + r.offset for r in mz.relocations
            if any(start <= r.segment * 16 + r.offset < start + size for _, start, size, _ in HELPERS)
            or 0x1aaa <= r.segment * 16 + r.offset < 0x1eaa]
        if analysis["original_segment_relocation_sites"]:
            raise ValueError("direct picture helpers/table unexpectedly contain MZ segment relocation sites")
        observations.append(dict(path=path, analysis=analysis, runtime=matrix(mz)))
        print(f"PASS picture image {len(observations)}/3", flush=True)
    if any((o["analysis"],o["runtime"]) != (observations[0]["analysis"],observations[0]["runtime"]) for o in observations[1:]):
        raise ValueError("picture helper/CPU observations differ across target/candidates")
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical MAINL changed")
    for source, raw_source in sources.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{source}"], cwd=ROOT / "_reference/ReC98") != raw_source:
            raise ValueError("frozen picture provider changed")
    result = dict(kind="th03-mainl-picture-cpu-flat-memory-port-diagnostics", observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, providers={p:sha(d) for p,d in sources.items()}, observations=observations,
                  total_top_level_calls=sum(o["runtime"]["top_level_calls"] for o in observations),
                  synthetic_engine_far_return_control=engine_control,
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  diagnostic_checks_pass=True, physical_egc_pixels_proved=False, page_banks_proved=False,
                  fresh_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(f"PASS {result['total_top_level_calls']} picture/packed CPU calls; physical EGC/banks unproved: {args.output}")


if __name__ == "__main__":
    main()
