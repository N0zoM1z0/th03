"""Scalar memory/event contracts for all nine actual -2 procedures.

DOS vector/free/TSR and PC-98 BIOS calls are explicit interface models. All
resident and transient instructions execute; this asserts no physical device,
kernel lifetime or out-of-domain unchecked error-table behavior.
"""

import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.x86_const import *
from review_th03_zun_init import RANGES


REG = {n: globals()["UC_X86_REG_" + n.upper()] for n in
       ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}
ENTRIES = dict(zip(("start", "error", "stop", "copy", "show", "convert", "draw", "detect", "parse"),
                   (start for _, start, _, _ in RANGES)))
OLD = {0x59: (0x1234, 0x4567), 6: (0x2345, 0x5678), 5: (0x3456, 0x6789)}
REMOTE, ENVIRONMENT, LATCH = 0x5000, 0x6000, 0x24D
TEXT = {}


def data_constants():
    resident = bytearray(b"UZPN" + bytes(13))
    transient = bytearray()

    def add(target, base, key, value):
        TEXT[key] = (base + len(target), value.encode("shift_jis"))
        target.extend(TEXT[key][1] + b"$")

    for key, value in (
        ("return", "リターンキーを押してね"), ("unknown", "なんかのエラーですぅ"),
        ("file", "ファイルがみつかんないよぉ"), ("memory", "メモリが足りないんですぅ"),
        ("batch", "バッチファイルから起動してよぉ"),
        ("score", "ハイスコアのファイルがおかしいよぅ、だからハイスコアは消えちゃったよ")):
        add(resident, 0x23D, key, value)
    for key in ("unknown", "unknown", "file", "memory", "batch", "score"):
        resident.extend(struct.pack("<H", TEXT[key][0]))
    for key, value in (
        ("stop1", "むやみにＳＴＯＰキー押したりしない"), ("stop2", "方がいいと思うの。（ゲーム中はね）"),
        ("stop3", "（ＳＴＯＰキーで戻れるよ、ねっ）　"), ("clear", "　　　　　　　　　　　　　　　　　"),
        ("copy1", "なんでＣＯＰＹキー押したりしてるの"), ("copy2", "かな〜。ふしぎ〜。　　（もう一度、"),
        ("copy3", "ＣＯＰＹキー押せば戻れるよ、ねっ）")):
        add(resident, 0x23D, key, value)
    for key, value in (
        ("banner", "\r\n\r\nINTvector set program  zuninit.com Version1.00              (c)zun 1997\r\n"),
        ("installed", "ちょこっとメモリかりるね\r\n\r\n"), ("already", "すでに常駐してるの\r\n\r\n"),
        ("removed", "メモリから消えてなくなっちゃったけど、きっとまたあえるよ、ねっ\r\n\r\n"),
        ("absent", "まだ、常駐してないわぁ\r\n\r\n"),
        ("invalid", "意味不明なオプションよぉ（オプションは -Rのみ）\r\n"),
        ("free_error", "メモリ解放エラーです。 : zuninit.com\r\n")):
        add(transient, 0x535, key, value)
    return bytes(resident), bytes(transient)


DATA1, DATA2 = data_constants()


def need(value, message):
    if not value:
        raise ValueError("ZUN init contract: " + message)


def convert(value):
    """Carry-sensitive character conversion as integer arithmetic, not decode."""
    low = value & 255
    result = (((value >> 8) * 2) & 255) * 256 + low
    carry = 0
    if low < 0x9F:
        total = result + 0xFEDF + (low < 0x80)
        result, carry = total & 65535, total > 65535
    return ((result - 0xDFFE - carry) & 65535) & 0x7F7F


def draw(text, offset, direction):
    need(len(text) % 2 == 0, "bounded doublebyte text")
    writes, position = [], offset
    step = -2 if direction else 2
    for first, second in zip(text[::2], text[1::2]):
        value = convert(first * 256 + second)
        left = ((value & 255) << 8) | (((value >> 8) - 0x20) & 255)
        for word in (left, left | 0x8000):
            writes.append((0xA0000 + position, 2, word))
            position = (position + step) & 65535
    position = offset
    for _ in range((len(text) & 65535) or 65536):
        writes.append((0xA2000 + position, 2, 0x41))
        position = (position + step) & 65535
    return writes


def specification(kind, load, *, tail=b"", resident=0, vector_offset=0x103, failures=(), latch=0,
                  flags=0x246, error=2, text=b"\x82\xA0", offset=0x100, **_):
    events, writes, stores, latch_stores = [], [], [], []
    vectors = dict(OLD)
    if resident:
        vectors[0x59] = (vector_offset, REMOTE)

    def output(key): events.append(("stdout", TEXT[key][1].hex()))
    def get(v): events.append(("get", v, *vectors[v]))
    def set_(v, off, seg):
        events.append(("set", v, off, seg)); vectors[v] = (off, seg)
    def display(key, at): writes.extend(draw(TEXT[key][1], at, bool(flags & 0x400)))

    terminal, ax = None, None
    final_latch = latch
    if kind in ("start", "parse", "detect"):
        recognized = resident == 1
        remove, invalid = False, False
        if kind != "detect":
            # The PSP length byte is ignored. Only the first non-space byte and
            # one option letter are examined; all trailing text is ignored.
            for index, char in enumerate(tail + b"\r"):
                if char == 13: break
                if char in b"-/":
                    letter = (tail + b"\r")[index + 1]
                    invalid = letter <= 0x20 or (letter & 0xDF) != ord("R")
                    remove = not invalid
                    break
                if char > 0x20: break
        if invalid:
            output("invalid"); terminal = ("exit", 0)
        else:
            output("banner"); get(0x59)
            if kind == "detect": ax = int(recognized)
            elif remove:
                if not recognized: output("absent")
                else:
                    for v in (0x59, 6, 5): set_(v, *OLD[v])
                    for seg in (ENVIRONMENT, REMOTE): events.append(("free", seg, seg in failures))
                    output("free_error" if REMOTE in failures else "removed")
                terminal = ("exit", 0)
            elif recognized:
                output("already"); terminal = ("exit", 0)
            else:
                for v, at, entry in ((0x59, 0x241, 0x103), (6, 0x249, 0x136), (5, 0x245, 0x148)):
                    if v != 0x59: get(v)
                    stores.append((load * 16 + at, struct.pack("<HH", *vectors[v])))
                    set_(v, entry, load)
                output("installed"); terminal = ("tsr", 0, 0x42)
        if terminal is not None: events.append(terminal)
    elif kind == "draw": writes = draw(text, offset, bool(flags & 0x400))
    elif kind in ("error", "stop", "copy", "show"):
        if kind == "error":
            key = ("unknown", "unknown", "file", "memory", "batch", "score")[error & 0x7FFF]
            display(key, 0); display("return", 0xA0)
            events.extend((("bios", 4, 3, 0), ("bios", 4, 3, 0x10)))
        elif kind == "show" or latch == 0:
            final_latch = 0
            which = (2 if kind == "copy" else 1) if kind != "show" else latch
            if kind != "show": latch_stores.append(which)
            latch_stores.append(0)
            mask = 2 if which == 2 else 1
            events.append(("bios", 0x41))
            for key, at in zip(("copy1", "copy2", "copy3") if mask == 2 else ("stop1", "stop2", "stop3"), (0x650, 0x6F0, 0x790)):
                display(key, at)
            events.extend(("bios", 4, 12, value) for value in (mask, 0, 0, mask))
            events.append(("bios", 0x40))
            for at in (0x650, 0x6F0, 0x790): display("clear", at)
            events.append(("bios", 6))
    state_writes = [(at + delta, 2, int.from_bytes(raw[delta:delta + 2], "little"))
                    for at, raw in stores for delta in (0, 2)]
    state_writes.extend((load * 16 + LATCH, 1, value) for value in latch_stores)
    return dict(events=events, writes=writes, stores=stores, state_writes=state_writes, vectors=vectors, terminal=terminal,
                latch=final_latch, ax=ax)


class Machine:
    def __init__(self, image, load):
        need(len(image) == 1390 and image[0x13D:0x313] == DATA1 and image[0x435:] == DATA2,
             "complete semantic initialized DATA")
        self.image, self.load, self.base = image, load, load * 16
        self.uc = Uc(UC_ARCH_X86, UC_MODE_16); self.uc.mem_map(0, 1 << 20)
        self.initial = bytearray(b"\xA5" * (1 << 20))
        self.initial[self.base + 0x100:self.base + 0x100 + len(image)] = image
        self.instructions = {}
        for _, start, size, _ in RANGES:
            rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[start - 0x100:start - 0x100 + size], start))
            need(sum(i.size for i in rows) == size, "complete instruction boundaries")
            self.instructions.update({i.address: i.size for i in rows})
        self.covered, self.maximum_stack = set(), 0
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE, self.code), self.uc.hook_add(UC_HOOK_INTR, self.interrupt),
                      self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write)]

    def close(self):
        for hook in self.hooks: self.uc.hook_del(hook)
        self.hooks = []; self.uc = None

    def r(self, name): return self.uc.reg_read(REG[name])
    def fail(self, error): self.error = str(error); self.uc.emu_stop()

    def code(self, uc, address, size, _):
        try:
            if address == self.base + 0xFFFF:
                self.stopped = True; uc.emu_stop(); return
            ip = address - self.base
            need(self.instructions.get(ip) == size, "execution outside owned instructions")
            self.covered.update(range(ip, ip + size))
        except Exception as error: self.fail(error)

    def write(self, uc, access, address, size, value, _):
        try:
            need(self.kind != "convert", "conversion must not write memory")
            if self.base + self.stack - 80 <= address and address + size <= self.base + self.stack:
                self.maximum_stack = max(self.maximum_stack, self.base + self.stack - address)
                return
            if 0xA0000 <= address < 0xB2000:
                item = (address, size, value)
                need(self.video_index < len(self.expected["writes"]) and item == self.expected["writes"][self.video_index],
                     "independent ordered character/attribute stores")
                self.video_index += 1
            else:
                need((self.kind in ("start", "parse") and self.base + 0x241 <= address
                      and address + size <= self.base + 0x24D)
                     or (address == self.base + LATCH and size == 1), "write outside owned state/stack/video")
                need(self.state_index < len(self.expected["state_writes"])
                     and (address, size, value) == self.expected["state_writes"][self.state_index],
                     "independent ordered saved-vector/latch stores")
                self.state_index += 1
        except Exception as error: self.fail(error)

    def interrupt(self, uc, number, _):
        try:
            ax, dx, ds, es = (self.r(n) for n in ("ax", "dx", "ds", "es"))
            ah, al = ax >> 8, ax & 255
            if number == 0x18:
                if ah == 4:
                    reply = self.expected["events"][len(self.events)][3]
                    event = ("bios", ah, al, reply)
                    uc.reg_write(REG["ax"], reply * 256 + al)
                else:
                    need(ah in (0x41, 0x40, 6), "bounded BIOS function")
                    event = ("bios", ah)
            elif number == 0x21:
                if ah == 9:
                    text = bytes(uc.mem_read(ds * 16 + dx, 1024)).split(b"$", 1)
                    need(len(text) == 2, "bounded terminated DOS string")
                    event = ("stdout", text[0].hex())
                elif ah == 0x35:
                    off, seg = self.vectors[al]
                    uc.reg_write(REG["bx"], off); uc.reg_write(REG["es"], seg)
                    event = ("get", al, off, seg)
                elif ah == 0x25:
                    if ds == self.load:
                        need(self.state_index == {0x59: 2, 6: 4, 5: 6}[al], "save old vector before publishing handler")
                    self.vectors[al] = (dx, ds)
                    uc.mem_write(al * 4, struct.pack("<HH", dx, ds))
                    event = ("set", al, dx, ds)
                elif ah == 0x49:
                    failed = es in self.failures
                    flags = uc.reg_read(UC_X86_REG_EFLAGS)
                    uc.reg_write(UC_X86_REG_EFLAGS, (flags | 1) if failed else flags & ~1)
                    if failed: uc.reg_write(REG["ax"], 7)
                    event = ("free", es, failed)
                elif ah in (0x31, 0x4C):
                    event = ("tsr", al, dx) if ah == 0x31 else ("exit", al)
                    self.stopped = True; uc.emu_stop()
                else: raise ValueError("unexpected DOS interface")
            else: raise ValueError("unexpected guest interrupt")
            self.events.append(event)
            need(self.events == self.expected["events"][:len(self.events)], "independent DOS/BIOS event contract")
        except Exception as error: self.fail(error)

    def run(self, kind, *, tail=b"", resident=0, vector_offset=0x103, failures=(), latch=0,
            flags=0x246, error=2, text=b"\x82\xA0", offset=0x100, stack=0xF800, pattern=0):
        need(kind in ENTRIES and kind != "convert" and len(tail) <= 125, "bounded entry/tail fixture")
        need(not flags & 0x400 or kind not in ("start", "parse"), "wrapper supplies cleared DF")
        self.kind, self.stack, self.failures = kind, stack, failures
        self.expected = specification(kind, self.load, tail=tail, resident=resident, vector_offset=vector_offset,
            failures=failures, latch=latch, flags=flags, error=error, text=text, offset=offset)
        self.events, self.video_index, self.state_index, self.error, self.stopped = [], 0, 0, None, False
        self.uc.mem_write(0, bytes(self.initial))
        self.vectors = dict(OLD)
        if resident:
            self.uc.mem_write(REMOTE * 16 + 0x100, self.image)
            for at, v in ((0x241, 0x59), (0x245, 5), (0x249, 6)):
                self.uc.mem_write(REMOTE * 16 + at, struct.pack("<HH", *OLD[v]))
            self.uc.mem_write(REMOTE * 16 + 0x2C, struct.pack("<H", ENVIRONMENT))
            if resident in (2, 3): self.uc.mem_write(REMOTE * 16 + 0x23D + 2 * (resident - 2), b"XX")
            self.vectors[0x59] = (vector_offset, REMOTE)
        for v, value in self.vectors.items(): self.uc.mem_write(v * 4, struct.pack("<HH", *value))
        self.uc.mem_write(self.base + LATCH, bytes((latch,)))
        self.uc.mem_write(self.base + 0x80, bytes((0,)) + tail + b"\r")  # deliberately wrong PSP length
        self.uc.mem_write(self.base + 0x1800, text + b"$")
        irq = kind in ("error", "stop", "copy")
        frame = struct.pack("<HHH", 0xFFFF, self.load, flags) if irq else struct.pack("<H", 0xFFFF)
        self.uc.mem_write(self.base + stack, frame)
        initial = bytes(self.uc.mem_read(0, 1 << 20))
        registers = dict(ax=error if kind == "error" else offset, bx=0x3344 ^ pattern, cx=0x5566 ^ pattern,
                         dx=0x1800, si=0x2323 ^ pattern, di=0xABCD ^ pattern, bp=0x9898 ^ pattern,
                         cs=self.load, ds=self.load if kind in ("start", "parse", "detect") else 0x1111,
                         ss=self.load, es=self.load if kind in ("start", "parse", "detect") else 0x7777, sp=stack)
        for n, value in registers.items(): self.uc.reg_write(REG[n], value)
        self.uc.reg_write(UC_X86_REG_EFLAGS, flags & ~0x200 if irq else flags)
        try: self.uc.emu_start(self.base + ENTRIES[kind], self.base + 0x10000, count=350000)
        except UcError as error_: raise ValueError("ZUN init contract: guest execution failed") from error_
        need(self.error is None, self.error or "guest error")
        need(self.stopped and self.events == self.expected["events"] and self.video_index == len(self.expected["writes"])
             and self.state_index == len(self.expected["state_writes"]),
             "complete bounded return/events/stores")
        expected_sp = stack if self.expected["terminal"] else stack + (6 if irq else 2)
        need(self.r("sp") == expected_sp, "real near/IRET/terminal stack shape")
        preserved = (("cs", "ds", "ss", "si", "di", "bp") if kind == "detect" else ("cs", "ds", "ss", "di", "bp")) if kind in ("start", "parse", "detect") else (
            tuple(n for n in registers if n != "sp") if kind in ("error", "stop", "copy", "show") else ("cs", "ds", "ss", "si", "bp"))
        need(all(self.r(n) == registers[n] for n in preserved), "full declared register preservation")
        if self.expected["ax"] is not None: need(self.r("ax") == self.expected["ax"], "fixed-offset signature result")
        if irq or kind == "show":
            need(self.uc.reg_read(UC_X86_REG_EFLAGS) & 0xED7 == flags & 0xED7, "complete restored interrupt/PUSHF flags")
        else:
            need(self.uc.reg_read(UC_X86_REG_EFLAGS) & 0x600 == flags & 0x600, "inherited IF/DF")
        expected = bytearray(initial)
        expected[self.base + LATCH] = self.expected["latch"]
        for address, raw in self.expected["stores"]: expected[address:address + len(raw)] = raw
        for v, value in self.expected["vectors"].items(): expected[v * 4:v * 4 + 4] = struct.pack("<HH", *value)
        for address, size, value in self.expected["writes"]: expected[address:address + size] = value.to_bytes(size, "little")
        actual = bytes(self.uc.mem_read(0, 1 << 20))
        lo, hi = self.base + stack - 80, self.base + stack
        expected[lo:hi] = actual[lo:hi]
        need(actual == expected, "whole physical memory outside bounded stack")
        video_hash = hashlib.sha256()
        for row in self.expected["writes"]: video_hash.update(struct.pack("<IHH", *row))
        return dict(events=self.events, ordered_video_sha256=video_hash.hexdigest(), video_word_writes=self.video_index,
                    ordered_state_stores=self.expected["state_writes"],
                    terminal=self.expected["terminal"], final_latch=self.expected["latch"])

    def conversions(self, values):
        """No guest writes are permitted; avoid copying 1 MiB for each scalar."""
        self.kind, self.stack = "convert", 0xF800
        self.uc.mem_write(0, bytes(self.initial)); self.uc.mem_write(self.base + self.stack, b"\xFF\xFF")
        registers = dict(bx=0xBEEF, cx=0xABCD, dx=0x1234, si=0x9876, di=0x4321, bp=0x6789,
                         cs=self.load, ds=0x1111, ss=self.load, es=0x7777)
        for n, value in registers.items(): self.uc.reg_write(REG[n], value)
        trace = hashlib.sha256(); count = 0
        for count, value in enumerate(values, 1):
            self.error, self.stopped = None, False
            flags = (2, 0x203, 0x402, 0x603)[value & 3]
            self.uc.reg_write(REG["ax"], value); self.uc.reg_write(REG["sp"], self.stack)
            self.uc.reg_write(UC_X86_REG_EFLAGS, flags)
            self.uc.emu_start(self.base + ENTRIES["convert"], self.base + 0x10000, count=30)
            need(not self.error and self.stopped and self.r("ax") == convert(value), "independent scalar conversion")
            need(self.r("sp") == self.stack + 2 and all(self.r(n) == v for n, v in registers.items()), "conversion registers/near return")
            need(self.uc.reg_read(UC_X86_REG_EFLAGS) & 0x600 == flags & 0x600, "conversion inherited IF/DF")
            trace.update(struct.pack("<HH", value, self.r("ax")))
        return dict(cases=count, trace_sha256=trace.hexdigest())


def cases():
    for tail in (b"", b"word", b"  -r ignored", b"/R", b"-R", b"/x", b"-", b"\t /r", b"/ ", b"/rignored"):
        for resident in (0, 1, 2, 3):
            for failures in ((), (ENVIRONMENT,), (REMOTE,), (ENVIRONMENT, REMOTE)):
                yield "start", dict(tail=tail, resident=resident, failures=failures)
    for value in range(256):
        yield "parse", dict(tail=b"/" + bytes((value,)), resident=value & 1)
    for resident in (0, 1, 2, 3):
        for flags in (0x246, 0x646):
            yield "detect", dict(resident=resident, vector_offset=0x880, flags=flags)
    for kind in ("stop", "copy"):
        for latch in range(256):
            for flags in (0x246, 0x646): yield kind, dict(latch=latch, flags=flags)
    for error in (*range(6), *range(0x8000, 0x8006)):
        for flags in (0x46, 0x246, 0x446, 0x646): yield "error", dict(error=error, flags=flags)
    for latch in (0, 1, 2, 0xFF):
        for flags in (0x246, 0x646): yield "show", dict(latch=latch, flags=flags)
    for text in (b"\x82\xA0", b"\x81\x7F\x81\x80\x81\x9E\x81\x9F", b""):
        for offset in (0, 1, 0xFFFE):
            for flags in (0x246, 0x646): yield "draw", dict(text=text, offset=offset, flags=flags)


def verify(target, candidate):
    observations = []
    for image in (target, candidate):
        loads = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            try:
                values = range(65536) if load == 0x1000 else (high * 256 + low for high in range(256) for low in (0, 0x7F, 0x80, 0x9E, 0x9F, 0xFF))
                scalars = machine.conversions(values)
                trace = hashlib.sha256()
                for count, (kind, options) in enumerate(cases(), 1):
                    row = machine.run(kind, stack=0xF800 if count & 1 else 0xE800, pattern=0 if count & 1 else 0xFFFF, **options)
                    trace.update(json.dumps(row, sort_keys=True).encode())
                need(len(machine.covered) == 607, "all 607 owned instruction bytes execute")
                loads.append(dict(load_segment=load, scenario_cases=count, conversions=scalars,
                                  covered_owner_bytes=len(machine.covered), maximum_observed_stack_depth=machine.maximum_stack,
                                  trace_sha256=trace.hexdigest()))
            finally: machine.close()
        observations.append(loads)
    need(observations[0] == observations[1], "target/candidate independent observations")
    return dict(images=2, functions=9, code_bytes=607, data_bytes=783, executed_owner_bytes=607,
                cases_per_image=sum(o["scenario_cases"] + o["conversions"]["cases"] for o in observations[0]),
                observations=observations[0], empty_string_attribute_word_writes=65536,
                interfaces="bounded DOS/PC-98 BIOS; wrapper entry requires DF clear; no real device or DOS lifetime claim")


def negative_controls(target):
    controls = (
        ("tsr-retention-paragraphs", 0x4C0, b"\x03", "start", {}),
        ("second-signature-word", 0x42D, b"\x51", "detect", dict(resident=1)),
        ("restore-vector-order", 0x4F3, b"\x06", "start", dict(tail=b"/R", resident=1)),
        ("second-free-carry", 0x50A, b"\x72", "start", dict(tail=b"/R", resident=1, failures=(REMOTE,))),
        ("exit-success-code", 0x531, b"\x01", "start", dict(tail=b"/X")),
        ("conversion-carry-constant", 0x1FA, b"\xDE", "draw", dict(text=b"\x82\x7F")),
        ("attribute-value", 0x234, b"\x42", "draw", {}),
        ("character-CS-override", 0x211, b"\x3E", "draw", dict(flags=0x646)),
        ("stop-latch-nonzero", 0x13C, b"\x74", "stop", dict(latch=3)),
        ("stop-latch-before-bios", 0x143, b"\x00", "stop", {}),
        ("copy-latch-kind", 0x155, b"\x01", "copy", {}),
        ("error-key-mask", 0x12A, b"\x20", "error", {}),
        ("iret-preserves-frame", 0x135, b"\xC3", "error", {}),
    )
    rejected = []
    for name, at, replacement, kind, options in controls:
        raw = bytearray(target); raw[at - 0x100:at - 0x100 + len(replacement)] = replacement
        machine = Machine(bytes(raw), 0x3000)
        try:
            try: machine.run(kind, **options)
            except (ValueError, UcError): rejected.append(name)
            else: raise ValueError("ZUN init mutation escaped: " + name)
        finally: machine.close()
    return dict(count=len(rejected), rejected=rejected)
