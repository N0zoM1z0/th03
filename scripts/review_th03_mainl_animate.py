#!/usr/bin/env python3
"""Execute complete MAINL interpreter loop paths with explicit input/font models."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_mainl_cutscene import CS, DS, Probe, RANGES, REVISION, sha
from review_th03_mainl_box import PLANES, SIZE, coordinates, describe_accesses, seed

ROOT = Path(__file__).resolve().parents[1]
BOX_PROOF_SHA256 = "aa6cdd31012a2b9d2e27f34f5e6597e4cc15b10818b72f742af4da02c748bdfa"
PROVIDERS = ("th03/hardware/input.h", "th01/hardware/grppsafx.h", "th02/hardware/frmdelay.h")
IMPORTS = {(0, 0x21ae): ("allocate", 2, 2), (0, 0x22b2): ("free", 2, 2),
           (0, 0x3641): ("tolower", 2, 0), (0xc7e, 0xdc2): ("input", 0, 0),
           (0xc7e, 0x9b7): ("font", 10, 10), (0xc7e, 0x372): ("delay", 2, 2),
           (0xc7e, 0xee5): ("wait", 2, 2)}


class AnimateProbe(Probe):
    """Root instructions are real; foreign input/font/timing/allocation are models."""
    def __init__(self, mz, keys=(0,), frame_limit=None):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN, UC_MEM_WRITE
        from unicorn import x86_const as reg
        if not keys or any(not 0 <= k <= 65535 for k in keys):
            raise ValueError("invalid constructed input sequence")
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
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
        self.events, self.ports, self.errors, self.accesses, self.reads = [], [], [], [], []
        self.keys, self.key_index, self.delays, self.waits, self.glyphs = keys, 0, [], [], []
        self.glyph_inputs = []
        self.stop = False
        self.frame_limit = frame_limit
        self.model_stopped = False
        self.offset = 0
        for i, segment in enumerate(PLANES):
            self.uc.mem_write(self.data + 0x1c60 + i * 4, struct.pack("<HH", 0, segment))
        self.import_at = {(0x2000 + segment) * 16 + offset: (segment, name, count, cleanup)
                          for (segment, offset), (name, count, cleanup) in IMPORTS.items()}

        def guarded(callback):
            def invoke(*args):
                try:
                    return callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
            return invoke

        def code(uc, address, length, user):
            if address == self.code + 0xff00:
                self.stop = True
                uc.emu_stop()
                return
            if address in self.import_at:
                segment, name, count, cleanup = self.import_at[address]
                if self.get("CS") != 0x2000 + segment:
                    raise ValueError("animate import segment alias")
                sp = self.get("SP")
                words = list(struct.unpack("<" + "H" * ((count + 4) // 2), uc.mem_read(self.stack + sp, count + 4)))
                args = words[2:]
                event = dict(name=name, args=args)
                if name == "allocate":
                    if args != [SIZE]:
                        raise ValueError("animate box allocation size differs")
                    self.set("AX", 0x6000)
                elif name == "tolower":
                    self.set("AX", args[0] + 32 if 65 <= args[0] <= 90 else args[0])
                elif name == "input":
                    key = keys[min(self.key_index, len(keys) - 1)]
                    self.word(0x1d0c, key)
                    event["key"] = key
                    self.key_index += 1
                    self.set("AX", 0xffff)
                elif name == "font":
                    offset, pointer_segment, fx, top, left = args
                    glyph = bytes(uc.mem_read(pointer_segment * 16 + offset, 3))
                    page = self.ports[-1][1]
                    if page == 1:
                        self.glyph_inputs.append(self.word(0x1d0c))
                    self.glyphs.append(dict(bytes=list(glyph), left=left, top=top, fx=fx, page=page))
                    # Constructed marker in one cell of each flat plane. This
                    # deliberately does not emulate font ROM or PC-98 rendering.
                    vo = ((left >> 3) + top * 80) & 65535
                    for plane in PLANES:
                        uc.mem_write(plane * 16 + vo, b"\x5a\xa5")
                    self.set("AX", 0xffff)
                elif name == "delay":
                    self.delays.append(args[0])
                    if self.frame_limit is not None and len(self.delays) >= self.frame_limit:
                        self.model_stopped = True
                        uc.emu_stop()
                        return
                    self.set("AX", 0xffff)
                elif name == "wait":
                    self.waits.append(args[0])
                    self.set("AX", 0xffff)
                else:
                    self.set("AX", 0xffff)
                    self.set("EFLAGS", self.get("EFLAGS") | 1)
                self.events.append(event)
                self.set("SP", sp + 4 + cleanup)
                self.set("CS", words[1])
                self.set("IP", words[0])
                return
            offset = address - self.code
            if self.get("CS") != 0x2000 + CS or not any(start <= offset < start + size for _, start, size, _ in RANGES):
                raise ValueError("CPU escaped animate reviewed bodies/interfaces")

        def memory(uc, access, address, width, value, user):
            if access != UC_MEM_WRITE and 0x50000 <= address < 0x60000:
                self.reads.append([address - 0x50000, width])
            if (any(segment * 16 <= address < segment * 16 + 0x8000 for segment in PLANES) or
                    0x60000 <= address < 0x60000 + SIZE):
                self.accesses.append(["write" if access == UC_MEM_WRITE else "read", address, width])

        def interrupt(uc, number, user):
            raise ValueError("unexpected animate kernel interrupt")

        def output(uc, port, width, value, user):
            if port != 0xa6 or width != 1:
                raise ValueError("unexpected animate port/width")
            self.ports.append([port, value])

        def input_port(uc, port, width, user):
            self.errors.append("unexpected animate input port")
            uc.emu_stop()
            return 0

        self.uc.hook_add(UC_HOOK_CODE, guarded(code))
        self.uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, guarded(memory))
        self.uc.hook_add(UC_HOOK_INTR, guarded(interrupt))
        self.uc.hook_add(UC_HOOK_INSN, guarded(output), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, input_port, None, 1, 0, reg.UC_X86_INS_IN)

    def execute(self, raw, offset=0, budget=5000000, *, expect_terminal=True):
        self.stop = False
        self.model_stopped = False
        self.errors.clear()
        self.script(raw, offset)
        self.offset = offset
        self.set("SP", 0xfff0)
        self.uc.mem_write(self.stack + 0xfff0, struct.pack("<H", 0xff00))
        self.uc.emu_start(self.code + 0x167e, 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if expect_terminal != self.stop or self.model_stopped:
            raise ValueError("animate terminal contract differs or substituted delay stopped execution")
        if self.stop and (self.get("SP") != 0xfff2 or [self.get(r) for r in ("BP", "SI", "DI")] != [0x7777, 0x1357, 0x2468]):
            raise ValueError("animate near cleanup/callee-saved contract differs")


def expected_glyphs(glyphs, fx=0x2f):
    result, x, y, boxes = [], 80, 320, 0
    for index, glyph in enumerate(glyphs):
        effect = fx[index] if isinstance(fx, list) else fx
        for page in (1, 0):
            result.append(dict(bytes=list(glyph) + [0], left=x, top=y, fx=effect, page=page))
        x += 16
        if x == 560:
            x, y = 144, y + 16
        if y == 384:
            x, y = 80, 320
            boxes += 1
    return result, [x, y], boxes


def case(mz, name, raw, glyphs, delays, keys=(0,), fx=0x2f, offset=0):
    p = AnimateProbe(mz, keys)
    original, backup = seed(p)
    p.execute(raw, offset)
    expected, cursor, boxes = expected_glyphs(glyphs, fx)
    expected_waits = [0] * boxes if not keys[-1] & 0x1000 else []
    cycle = bytes(p.uc.mem_read(p.stack + 0xffec, 1))[0]
    expected_cycle = sum(bool(key) and not key & 0x1000 for key in p.glyph_inputs) & 255
    expected_ports = [[0xa6, 0]]
    for glyph in expected:
        expected_ports.append([0xa6, glyph["page"]])
        if glyph["page"] == 0 and glyph["left"] == 544 and glyph["top"] == 368:
            expected_ports.extend([[0xa6, 1], [0xa6, 0]])
    if (p.glyphs != expected or p.delays != delays or [p.word(0x21e0), p.word(0x21e2)] != cursor or
            [p.word(0x21d6), p.word(0x21d8)] != [(offset + len(raw)) & 65535, 0x5000] or
            p.word(0x21da) or p.word(0x21dc) or p.events[-1]["name"] != "free" or p.waits != expected_waits or
            cycle != expected_cycle or p.ports != expected_ports):
        raise ValueError(f"animate {name}: glyph/delay/cursor/pointer/cleanup differs")
    for segment, plane in zip(PLANES, original):
        if bytes(p.uc.mem_read(segment * 16, 0x8000)) != plane:
            raise ValueError(f"animate {name}: final backup restore failed or outside rectangle changed")
    # Actual snapshot + full-box dual restores + exit single restore.
    expected_accesses = []
    for index, address in enumerate(coordinates()):
        expected_accesses.extend([["read", address, 2], ["write", 0x60000 + index * 2, 2]])
    for _ in range(boxes * 2 + 1):
        for index, address in enumerate(coordinates()):
            expected_accesses.extend([["read", 0x60000 + index * 2, 2], ["write", address, 2]])
    if p.accesses != expected_accesses:
        raise ValueError(f"animate {name}: snapshot/restore ordered transfers differ")
    return dict(name=name, script_hex=raw.hex(), initial_offset=offset, input_sequence=keys,
                input_calls=p.key_index, glyphs=p.glyphs, delays=p.delays, waits=p.waits,
                glyph_input_words=p.glyph_inputs, speedup_cycle_byte=cycle,
                final_cursor=cursor, final_script_offset=p.word(0x21d6), ports=p.ports,
                events=p.events, transfers=describe_accesses(p.accesses), backup_sha256=sha(backup),
                final_sp=p.get("SP"), terminal=True)


def matrix(mz):
    cases = [case(mz, "explicit-stop-empty", b"\\$", [], []),
             case(mz, "control-space-skip", b"\0 \t\r\nAB\\$", [b"AB"], [1]),
             case(mz, "NUL-second-byte", b"A\0\\$", [b"A\0"], [1]),
             case(mz, "backslash-second-byte", b"A\\\\$", [b"A\\"], [1]),
             case(mz, "far-offset-wrap", b"AB\\$", [b"AB"], [1], offset=0xfffc),
             case(mz, "cancel-release", b"ABCD\\$", [b"AB", b"CD"], [1], keys=(0x1000, 0, 0)),
             case(mz, "mixed-key-cycles", b"ABCDEF\\$", [b"AB", b"CD", b"EF"], [1, 1], keys=(1, 0, 1, 0)),
             case(mz, "cancel-does-not-advance-cycle", b"ABCDEFGH\\$", [b"AB", b"CD", b"EF", b"GH"], [1], keys=(1, 0x1000, 1, 1, 0))]
    for key in (0, 1, 0x20, 0x2000, 0x1000, 0x3000):
        cases.append(case(mz, f"default-input-{key:04x}", b"ABCD\\$", [b"AB", b"CD"],
                          [1, 1] if not key else ([] if key & 0x1000 else [1]), keys=(key,)))
    for interval in (0, 1, 2, 3, 4, 999):
        for key in (0, 1):
            delays = [interval, interval] if not key else ([interval // 3] * 2 if interval >= 3 else [1])
            cases.append(case(mz, f"interval-{interval}-key-{key}", f"\\v{interval}ABCD\\$".encode(),
                              [b"AB", b"CD"], delays, keys=(key,)))
    cases.append(case(mz, "color-weight-truncation", b"\\c260\\b1AB\\b3CD\\b9EF\\b0GH\\$",
                      [b"AB", b"CD", b"EF", b"GH"], [1] * 4, fx=[0x14, 0x34, 0x34, 4]))
    for count, key in ((110, 0), (257, 1), (110, 0x1000)):
        cases.append(case(mz, f"glyphs-{count}-input-{key:04x}", b"AB" * count + b"\\$", [b"AB"] * count,
                          [1] * count if not key else ([] if key & 0x1000 else [1] * (count // 2)), keys=(key,)))
    p = AnimateProbe(mz)
    seed(p)
    p.execute(b"AB", budget=500000, expect_terminal=False)
    if p.stop or p.model_stopped or p.word(0x21dc) != 0x6000 or any(e["name"] == "free" for e in p.events) or len(p.glyphs) != 2:
        raise ValueError("missing STOP unexpectedly terminates/cleans up or renders NUL as text")
    nonterminal = dict(script_hex="4142", instruction_budget=500000, input_calls=p.key_index,
                       final_script_offset=p.word(0x21d6), script_segment=p.word(0x21d8),
                       backup_pointer=[p.word(0x21da), p.word(0x21dc)],
                       glyph_calls=len(p.glyphs), terminal=False, model_stopped=False,
                       script_reads=describe_accesses(p.reads))
    return dict(terminal_cases=cases, nonterminal=nonterminal,
                scope="Complete animate body on selected scripts; real box/params/cursor/script-op branches; font/input/timing/free/allocation models, flat planes only")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--box-proof", type=Path, default=Path(".analysis/sol-mainl-box-review-20261006.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT / args.box_proof).read_bytes()
    if sha(raw) != BOX_PROOF_SHA256:
        raise ValueError("box diagnostic proof differs from reviewed pin")
    proof = json.loads(raw)
    if proof["kind"] != "th03-mainl-box-cpu-flat-memory-diagnostics" or not proof["diagnostic_checks_pass"] or proof["exact_acceptance"]:
        raise ValueError("animate requires verified box diagnostic proof")
    inputs = {**proof["inputs"], str(args.box_proof): sha(raw)}
    inputs["scripts/review_th03_mainl_animate.py"] = sha(Path(__file__).read_bytes())
    def verify():
        for path, digest in inputs.items():
            if sha((ROOT / path).read_bytes()) != digest:
                raise ValueError(f"animate review input changed: {path}")
    verify()
    frozen = {path: subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") for path in PROVIDERS}
    images = [(path, parse_mz((ROOT / path).read_bytes())) for path in inputs if path.endswith("mainl.exe")]
    if len(images) != 3 or any(not mz.valid for _, mz in images):
        raise ValueError("animate target/two cached images absent/invalid")
    for path, _ in images:
        if "th03-diet" in path:
            continue
        tree = Path(path).parents[2]
        for source, expected in frozen.items():
            cached_path = str(tree / source)
            data = (ROOT / cached_path).read_bytes()
            if data != expected:
                raise ValueError("animate header/provider association differs")
            inputs[cached_path] = sha(data)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-mainl")
    stored = read_verified_artifact(ROOT, artifact)
    base = json.loads((ROOT / ".analysis/sol-mainl-cutscene-review-20261006.json").read_bytes())
    if sha(stored) != base["stored_sha256"]:
        raise ValueError("canonical MAINL differs from guarded cutscene proof")
    observations = [dict(path=path, runtime=matrix(mz)) for path, mz in images]
    if any(o["runtime"] != observations[0]["runtime"] for o in observations[1:]):
        raise ValueError("animate target/cached CPU observations differ")
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical MAINL changed")
    for path, data in frozen.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") != data:
            raise ValueError("frozen animate provider changed")
    result = dict(kind="th03-mainl-animate-cpu-interface-diagnostics", observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, providers={p: sha(d) for p, d in frozen.items()}, observations=observations,
                  terminal_calls=sum(len(o["runtime"]["terminal_cases"]) for o in observations), nonterminal_cases=len(observations),
                  tools=dict(unicorn_distribution=version("unicorn")), diagnostic_checks_pass=True,
                  whole_interpreter_devices_proved=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS {result['terminal_calls']} complete-loop CPU/model calls and {result['nonterminal_cases']} missing-STOP budget observations: {args.output}")


if __name__ == "__main__":
    main()
