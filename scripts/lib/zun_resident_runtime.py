"""Independent scalar/state/event contracts for the actual maintained -5 root.

The two owned procedures and native N_SCOPY execute. Foreign allocation, DOS,
text and graph services are bounded Pascal interfaces, not hardware acceptance.
Every service sees its real stack arguments and clobbers caller-saved registers.
"""

import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.x86_const import *

from lib.zun_resident_layout import DATA, DEFAULTS, IDENTIFIER, MESSAGES


ENTRIES = {"cfg_init": (0x367, 97), "main": (0x3C8, 225)}
SERVICES = {0x4AA: ("clear", 0), 0x4CE: ("exist", 6), 0x516: ("create", 6),
            0x58C: ("free", 2), 0x59C: ("open", 4), 0x5B2: ("file_create", 4),
            0x5C6: ("print", 2), 0x5EE: ("close", 2), 0x604: ("write", 8), 0x61E: ("seek", 8)}
REG = {n: globals()["UC_X86_REG_" + n.upper()] for n in
       ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}


def need(value, message):
    if not value:
        raise ValueError("ZUN resident contract: " + message)


def s16(n):
    return (n & 0x7FFF) - (n & 0x8000)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def specification(kind, *, argc=2, argument=b"/D", existing=0, allocated=0x800,
                  opened=5, created=7, debug=0, segment=0xBEEF, reply=0xFFF9, **_):
    """Reference uses values/strings only, never guest instructions or addresses."""
    events = []

    def cfg(seg):
        events.append(("open", 0x3D02, b"yume.cfg".hex()))
        handle = opened
        if s16(handle) > 0:
            events.append(("seek", handle, 5, 0))
        else:
            handle = created
            events.append(("file_create", b"yume.cfg".hex(), 0x20))
            events.append(("write", handle, DEFAULTS.hex()))
        events.extend((("write", handle, struct.pack("<H", seg).hex()),
                       ("write", handle, bytes((debug,)).hex()), ("close", handle)))

    changed = None
    if kind == "cfg_init":
        cfg(segment)
        return dict(events=events, ax=reply, debug=debug, resident=None, df_cleared=True)
    events.extend((("exist", IDENTIFIER[:-1].hex(), 10, 16),
                   ("print", MESSAGES[0].encode("cp932").hex()), ("clear",)))
    result = None
    if argc == 2:
        prefix, letter = argument[0], argument[1]
        if prefix in b"-/" and letter in b"Rr":
            if existing:
                events.extend((("free", existing), ("print", MESSAGES[2].encode("cp932").hex())))
                result = 0
            else:
                events.append(("print", MESSAGES[1].encode("cp932").hex()))
                result = 1
        elif prefix in b"-/" and letter in b"Dd":
            debug = 1
        else:
            events.append(("print", MESSAGES[3].encode("cp932").hex()))
            result = 1
    if result is None:
        if existing:
            events.append(("print", MESSAGES[4].encode("cp932").hex()))
            result = 1
        else:
            events.append(("create", IDENTIFIER[:-1].hex(), 10, 16))
            if not allocated:
                events.append(("print", MESSAGES[5].encode("cp932").hex()))
                result = 1
            else:
                events.append(("print", MESSAGES[6].encode("cp932").hex()))
                changed = allocated
                cfg(allocated)
                result = 0
    return dict(events=events, ax=result, debug=debug, resident=changed, df_cleared=changed is not None)


class Machine:
    def __init__(self, image, load):
        need(len(image) == 5618, "complete COM image")
        self.load, self.base = load, load * 16
        self.uc = Uc(UC_ARCH_X86, UC_MODE_16)
        self.uc.mem_map(0, 1 << 20)
        self.initial = bytearray(b"\xA5" * (1 << 20))
        self.initial[self.base + 0x100:self.base + 0x100 + len(image)] = image
        need(image[0x121E:0x1351] == DATA, "semantic owned DATA")
        self.instructions, self.owner_bytes = {}, set()
        for start, size in (*ENTRIES.values(), (0x7CA, 28)):
            decoded = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[start - 0x100:start - 0x100 + size], start))
            need(sum(i.size for i in decoded) == size, "complete instruction boundaries")
            self.instructions.update({i.address: i.size for i in decoded})
            if start != 0x7CA:
                self.owner_bytes.update(range(start, start + size))
        self.covered, self.maximum_stack = set(), 0
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE, self.code),
                      self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write),
                      self.uc.hook_add(UC_HOOK_INTR, self.interrupt)]

    def close(self):
        for hook in self.hooks:
            self.uc.hook_del(hook)
        self.hooks = []
        self.uc = None

    def r(self, name):
        return self.uc.reg_read(REG[name])

    def word(self, address):
        return struct.unpack("<H", self.uc.mem_read(address, 2))[0]

    def text(self, segment, offset):
        return bytes(self.uc.mem_read(segment * 16 + offset, 512)).split(b"\0", 1)[0]

    def fail(self, error):
        self.error = str(error)
        self.uc.emu_stop()

    def interrupt(self, uc, number, _):
        self.fail("unexpected guest interrupt " + str(number))

    def write(self, uc, access, address, size, value, _):
        try:
            stack = self.base + self.stack - 80 <= address and address + size <= self.base + self.stack
            debug = address == self.base + 0x131E and size == 1
            resident = self.expected["resident"]
            owned = resident is not None and resident * 16 + 11 <= address and address + size <= resident * 16 + 256
            need(stack or debug or owned, "write outside owned stack/debug/resident tail")
            if stack:
                self.maximum_stack = max(self.maximum_stack, self.base + self.stack - address)
        except Exception as error:
            self.fail(error)

    def code(self, uc, address, size, _):
        try:
            ip = address - self.base
            if ip == 0xFFFF:
                self.stopped = True
                uc.emu_stop()
                return
            if ip in SERVICES:
                name, count = SERVICES[ip]
                frame = self.base + self.r("sp")
                arg = lambda offset: self.word(frame + offset)
                reply = self.options["reply"]
                if name in ("exist", "create"):
                    event = (name, self.text(self.load, arg(6)).hex(), arg(4), arg(2))
                    reply = self.options["existing" if name == "exist" else "allocated"]
                elif name == "print": event = (name, self.text(self.load, arg(2)).hex())
                elif name == "clear": event = (name,)
                elif name in ("close", "free"): event = (name, arg(2))
                elif name == "open":
                    event = (name, arg(4), self.text(self.load, arg(2)).hex())
                    reply = self.options["opened"]
                elif name == "file_create":
                    event = (name, self.text(self.load, arg(4)).hex(), arg(2))
                    reply = self.options["created"]
                elif name == "seek": event = (name, arg(8), arg(4) + (arg(6) << 16), arg(2))
                elif name == "write":
                    need(arg(2) <= 5, "bounded write length")
                    event = (name, arg(8), bytes(uc.mem_read(arg(6) * 16 + arg(4), arg(2))).hex())
                self.events.append(event)
                need(self.events == self.expected["events"][:len(self.events)], "independent ordered service/argument contract")
                return_ip = arg(0)
                for register, value in (("ax", reply), ("bx", 0xC713), ("cx", 0xFDA6), ("dx", 0x9E31), ("es", 0x6000)):
                    uc.reg_write(REG[register], value)
                uc.reg_write(REG["sp"], self.r("sp") + 2 + count)
                uc.reg_write(REG["ip"], return_ip)
                return
            need(self.instructions.get(ip) == size, "execution outside owned instructions/helper/services")
            if ip in self.owner_bytes:
                self.covered.update(range(ip, ip + size))
        except Exception as error:
            self.fail(error)

    def run(self, kind, *, argc=2, argument=b"/D", existing=0, allocated=0x800,
            opened=5, created=7, debug=0, segment=0xBEEF, reply=0xFFF9,
            flags=0x602, stack=0xFC00, pattern=0):
        need(kind in ENTRIES and len(argument) >= 2, "bounded entry/argument fixture")
        self.options = dict(argc=argc, argument=argument, existing=existing, allocated=allocated,
                            opened=opened, created=created, debug=debug, segment=segment, reply=reply)
        self.expected = specification(kind, **self.options)
        self.stack, self.events, self.error, self.stopped = stack, [], None, False
        self.uc.mem_write(0, bytes(self.initial))
        self.uc.mem_write(self.base + 0x131E, bytes((debug,)))
        # Ten ID characters and their terminator precede 245 nonzero bytes.
        if allocated:
            need(0x800 <= allocated <= 0x900, "disjoint bounded allocation fixture")
            self.uc.mem_write(allocated * 16, IDENTIFIER + b"\xD7" * (256 - len(IDENTIFIER)))
        self.uc.mem_write(self.base + 0x1900, argument + b"\0")
        self.uc.mem_write(self.base + 0x1800, struct.pack("<HH", 0x1920, 0x1900))
        args = (segment,) if kind == "cfg_init" else (argc, 0x1800)
        caller = struct.pack("<" + "H" * (1 + len(args)), 0xFFFF, *args)
        self.uc.mem_write(self.base + stack, caller)
        initial = bytes(self.uc.mem_read(0, 1 << 20))
        registers = dict(si=(0xABBA ^ pattern), di=(0xCDDA ^ pattern), bp=(0x1234 ^ pattern),
                         sp=stack, cs=self.load, ds=self.load, es=0x6000, ss=self.load,
                         ax=0xA117 ^ pattern, bx=0xB223 ^ pattern, cx=0xC331 ^ pattern, dx=0xD441 ^ pattern)
        for name, value in registers.items(): self.uc.reg_write(REG[name], value)
        self.uc.reg_write(UC_X86_REG_EFLAGS, flags)
        try:
            self.uc.emu_start(self.base + ENTRIES[kind][0], self.base + 0x10000, count=20000)
        except UcError as error:
            raise ValueError("ZUN resident contract: guest execution failed") from error
        need(self.error is None, self.error or "guest error")
        need(self.stopped and self.events == self.expected["events"], "complete bounded return/events")
        need(self.r("ax") == self.expected["ax"], "independent return AX")
        need(all(self.r(n) == registers[n] for n in ("si", "di", "bp", "cs", "ds", "ss"))
             and self.r("sp") == stack + 2, "near cdecl frame/register preservation")
        expected_flags = flags & ~0x400 if self.expected["df_cleared"] else flags
        need(self.uc.reg_read(UC_X86_REG_EFLAGS) & 0x600 == expected_flags & 0x600, "IF/DF helper boundary")
        need(bytes(self.uc.mem_read(self.base + stack, len(caller))) == caller, "unchanged caller argument frame")
        expected = bytearray(initial)
        expected[self.base + 0x131E] = self.expected["debug"]
        resident = self.expected["resident"]
        if resident is not None:
            expected[resident * 16 + 11:resident * 16 + 256] = bytes(245)
        actual = bytes(self.uc.mem_read(0, 1 << 20))
        lo, hi = self.base + stack - 80, self.base + stack
        expected[lo:hi] = actual[lo:hi]
        need(actual == expected, "whole physical memory outside bounded owned stack")
        return dict(events=self.events, ax=self.r("ax"), debug=self.expected["debug"],
                    resident_tail_cleared=resident is not None, df_cleared=self.expected["df_cleared"])


def cases():
    # Every second option byte, both valid prefixes and a foreign prefix; only
    # argc == 2 parses argv[1]. Trailing bytes are intentionally not checked.
    for prefix in (b"/", b"-", b"X"):
        for letter in range(256):
            for existing in (0, 0x900):
                yield "main", dict(argument=prefix + bytes((letter,)) + b"ignored", existing=existing)
    for argc in (0, 1, 3, 0x7FFF, 0x8000, 0xFFFF):
        for existing, allocated in ((0, 0), (0, 0x800), (0x900, 0x800)):
            yield "main", dict(argc=argc, argument=b"/R", existing=existing, allocated=allocated, debug=0xA7)
    for argument in (b"/D", b"-d", b"/R", b"-r", b"/X", b"XX"):
        for flags in (2, 0x202, 0x402, 0x602):
            yield "main", dict(argument=argument, allocated=0, flags=flags, debug=0xFF)
    for flags in (2, 0x202, 0x402, 0x602):
        for reply in (0, 0x7FFF, 0x8000, 0xFFFF):
            yield "main", dict(argc=1, opened=0xFFFF, created=0xFFFF, allocated=0x900,
                               flags=flags, reply=reply, debug=0x80)
    for opened in (0, 1, 0x7FFF, 0x8000, 0xFFFF):
        for created in (0, 7, 0xFFFF):
            for index, debug in enumerate((0, 1, 0x80, 0xFF)):
                for segment in (0, 0x800, 0xFFFF):
                    yield "cfg_init", dict(opened=opened, created=created, debug=debug, segment=segment,
                                           flags=(2, 0x202, 0x402, 0x602)[index], reply=created)


def verify(target, candidate):
    observations = []
    for image in (target, candidate):
        per_load = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            try:
                trace = hashlib.sha256()
                count = 0
                for count, (kind, options) in enumerate(cases(), 1):
                    row = machine.run(kind, stack=0xFC00 if count & 1 else 0xE800,
                                      pattern=0 if count & 1 else 0xFFFF, **options)
                    trace.update(json.dumps(row, sort_keys=True).encode())
                need(len(machine.covered) == 322, "every owned instruction byte executes")
                per_load.append(dict(load_segment=load, cases=count, covered_owner_bytes=len(machine.covered),
                                     maximum_observed_stack_depth=machine.maximum_stack, trace_sha256=trace.hexdigest()))
            finally:
                machine.close()
        observations.append(per_load)
    need(observations[0] == observations[1], "target/candidate independent observations")
    return dict(images=2, cases_per_image=sum(o["cases"] for o in observations[0]), functions=2,
                executed_owner_bytes=322, data_bytes=307, bss_bytes=0, observations=observations[0],
                bounded_interfaces="Pascal services preserve IF/DF and callee-saved registers; DOS/device bodies unowned",
                actual_compiler_helper="N_SCOPY@ 28 bytes executes; clears DF; no source credit")


def negative_controls(target):
    # Each changed operand/condition runs as actual guest code against the scalar
    # contract. No raw equality comparison is used to reject these controls.
    controls = (
        ("signed-positive-handle", 0x38A, b"\x76", "cfg_init", dict(opened=0xFFFF)),
        ("zero-handle-create", 0x38A, b"\x7C", "cfg_init", dict(opened=0)),
        ("seek-five-byte-options", 0x390, b"\x04", "cfg_init", {}),
        ("create-archive-attribute", 0x39A, b"\x21", "cfg_init", dict(opened=0)),
        ("segment-word-width", 0x3B2, b"\x01", "cfg_init", {}),
        ("debug-byte-width", 0x3BC, b"\x02", "cfg_init", {}),
        ("argc-equals-two", 0x3EE, b"\x03", "main", dict(argc=3, argument=b"/R")),
        ("remove-lowercase", 0x40A, b"\x73", "main", dict(argument=b"/r", existing=0x900)),
        ("remove-free-segment", 0x416, b"\x56", "main", dict(argument=b"/R", existing=0x900)),
        ("debug-one", 0x443, b"\x02", "main", dict(argument=b"/D")),
        ("create-paragraph-count", 0x460, b"\x0F", "main", dict(argc=1)),
        ("preserve-id-terminator", 0x486, b"\x0A", "main", dict(argc=1)),
        ("clear-last-byte", 0x49A, b"\xFF\x00", "main", dict(argc=1)),
        ("failed-return-one", 0x471, b"\x02", "main", dict(argument=b"/X")),
        ("cfg-caller-cleanup", 0x4A2, b"\x90", "main", dict(argc=1)),
        ("actual-copy-helper-clears-df", 0x7D6, b"\xFD", "cfg_init", dict(flags=0x602)),
    )
    rejected = []
    for name, address, replacement, kind, options in controls:
        image = bytearray(target)
        image[address - 0x100:address - 0x100 + len(replacement)] = replacement
        machine = Machine(bytes(image), 0x3000)
        try:
            try: machine.run(kind, **options)
            except ValueError: rejected.append(name)
            else: raise ValueError("ZUN resident mutation escaped: " + name)
        finally:
            machine.close()
    return dict(count=len(rejected), rejected=rejected)
