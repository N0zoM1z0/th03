"""Scalar release contract for actual PI_FREE instructions and native call frames.

HMEM_FREE is an explicit unowned interface: it preserves BX/CX/DX/SI/DI/BP,
DS/ES/SS, GPR high halves and IF/DF, returns AX/arithmetic flags, and pops one
WORD argument. Heap storage and its internal stack writes are outside this
interface model. No actual heap execution or allocator correctness is claimed.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *
from lib.decoded_mainl_pi_free_layout import START, SIZE, HEAP, CALLS
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical

REPLIES = ((0, 0x44), (0xFFFF, 0x895), (0xA55A, 0x90))
TEST_FLAGS = 0xEC7  # TEST leaves AF undefined; retain the defined flags and IF/DF.


def need(value, message):
    if not value:
        raise ValueError('MAINL PI free contract: ' + str(message))


def address(segment, offset, displacement=0):
    # Each effective WORD offset wraps before the segment is added. A WORD at
    # offset FFFF still has its second physical byte at the next linear address.
    return segment * 16 + ((offset + displacement) & 65535)


def specification(memory, regs, flags, replies):
    """Release comment, then machine info, then image; observe live aliasing."""
    out = dict(regs)
    events = []
    stack, ss = regs['sp'], regs['ss']

    def word(at):
        return int.from_bytes(memory[at:at + 2], 'little')

    def store(at, value):
        events.append(('store', at, 2, value))
        memory[at:at + 2] = struct.pack('<H', value)

    store(address(ss, stack - 2), regs['bp'])
    out.update(bp=stack - 2, cx=0)
    header_offset = word(address(ss, stack + 8))
    header_segment = word(address(ss, stack + 10))
    out.update(bx=header_offset, es=header_segment)
    calls = 0
    mask = 0x8C5
    for index, (segment_field, clear_fields) in enumerate(((2, (4, 2, 0)), (18, (14, 18, 16)), (None, ()))):
        segment = word(address(ss, stack + 6)) if segment_field is None else word(address(header_segment, header_offset, segment_field))
        out['ax'] = segment
        flags = (flags & 0x600) | 2 | logical(segment, 16)
        mask = 0x8C5
        if not segment:
            continue
        continuation = CALLS[index][1]
        store(address(ss, stack - 4), segment)
        store(address(ss, stack - 6), regs['cs'])
        store(address(ss, stack - 8), continuation)
        request = dict(out, sp=stack - 8)
        reply = replies[calls]
        events.append(('heap', segment, continuation, request, flags & TEST_FLAGS, reply))
        out['ax'] = reply[0]
        flags = (flags & 0x600) | (reply[1] & 0x8D5) | 2
        mask = 0x8D5
        calls += 1
        for field in clear_fields:
            store(address(header_segment, header_offset, field), 0)
    out.update(bp=word(address(ss, stack - 2)), sp=stack + 12)
    return out, flags, mask, events, calls


class Machine:
    def __init__(self, image, load):
        need(image.valid, 'valid decoded image')
        self.load, self.base = load, load * 16
        self.u = Uc(UC_ARCH_X86, UC_MODE_16)
        self.u.mem_map(0, 1 << 20)
        initial = bytearray(b'\xA5' * (1 << 20))
        raw = image.relocated_program_image(load)
        initial[self.base:self.base + len(raw)] = raw
        self.initial = bytes(initial)
        instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image.program_image[START:START + SIZE], START))
        need(sum(i.size for i in instructions) == SIZE, 'complete instruction boundaries')
        self.instructions = {i.address: i.size for i in instructions}
        self.covered = set()
        self.hooks = [self.u.hook_add(UC_HOOK_CODE, self.code), self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)]

    def close(self):
        for hook in self.hooks:
            self.u.hook_del(hook)
        self.hooks = []
        self.u = None

    def regs(self):
        return {name: self.u.reg_read(REG[name]) & 65535 for name in REG if name != 'ip'}

    def check_registers(self, expected):
        need(self.regs() == expected, 'all WORD/segment registers ' + str((self.regs(), expected)))
        need(all(self.u.reg_read(GPRS[n]) == self.high[n] | expected[n] for n in GPRS),
             'all DWORD high halves including ESP')

    def event(self, event):
        need(self.index < len(self.events) and self.events[self.index] == event,
             f'ordered event {self.index}: {event}; expected {self.events[self.index:self.index + 1]}')
        self.index += 1
        self.observed.append(event)

    def fail(self, error):
        self.error = str(error)
        self.u.emu_stop()

    def code(self, u, at, size, _):
        try:
            if at == self.base + 0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            if at == self.base + HEAP:
                sp, ss = u.reg_read(REG['sp']), u.reg_read(REG['ss'])
                frame = bytes(u.mem_read(address(ss, sp), 6))
                continuation, cs, segment = struct.unpack('<3H', frame)
                need(cs == self.load, 'real pushed CS on the same native frame')
                reply = self.replies[self.calls]
                event = ('heap', segment, continuation, self.regs(), u.reg_read(UC_X86_REG_EFLAGS) & TEST_FLAGS, reply)
                self.event(event)
                self.check_registers(event[3])
                u.reg_write(REG['ax'], reply[0])
                u.reg_write(UC_X86_REG_EFLAGS, (event[4] & 0x600) | (reply[1] & 0x8D5) | 2)
                u.reg_write(REG['sp'], sp + 6)
                u.reg_write(REG['cs'], cs)
                u.reg_write(REG['ip'], continuation)
                self.calls += 1
                return
            offset = at - self.base
            need(self.instructions.get(offset) == size, 'only selected native owner instructions or declared heap entry')
            self.covered.update(range(offset, offset + size))
        except Exception as error:
            self.fail(error)

    def write(self, u, access, at, size, value, _):
        try:
            self.event(('store', at, size, value))
        except Exception as error:
            self.fail(error)

    def run(self, *, segments=(0x1111, 0x2222, 0x3333), image_offset=0xFFFF,
            header_offset=0x1234, ss=0x7000, stack=0xF800, flags=0x202,
            seed=0x1357, foreign_ds=False, alias_frame=False, replies=REPLIES):
        need(len(segments) == len(replies) == 3 and all(0 <= x <= 65535 for x in (*segments, image_offset, header_offset)), 'WORD fixture')
        need(all(0 <= a <= 65535 and 0 <= f <= 0xFFFF for a, f in replies), 'bounded heap replies')
        need(ss in (0x7000, 0x8000) and stack in (0x80, 0xF800) and flags in (2, 0x202, 0x402, 0xED7), 'bounded foreign SS/flags')
        hseg = ss if alias_frame else 0x5000
        hoff = stack + 4 if alias_frame else header_offset
        memory = bytearray(self.initial)
        for offset in range(72):
            memory[address(hseg, hoff, offset)] = (seed + offset * 37) & 255
        for offset, segment in zip((2, 18), segments[:2]):
            at = address(hseg, hoff, offset)
            memory[at:at + 2] = struct.pack('<H', segment)
        frame = struct.pack('<6H', 0xFFFF, self.load, image_offset, segments[2], hoff, hseg)
        memory[address(ss, stack):address(ss, stack) + len(frame)] = frame
        self.u.mem_write(0, bytes(memory))
        regs = {n: (seed + i * 0x231) & 65535 for i, n in enumerate(GPRS)}
        regs.update(sp=stack, cs=self.load, ds=0x6000 if foreign_ds else self.load + 0xE3F, es=seed, ss=ss)
        self.high = {n: ((seed ^ 0x5AA5) << 16) for n in GPRS}
        for name in GPRS:
            self.u.reg_write(GPRS[name], self.high[name] | regs[name])
        for name in ('cs', 'ds', 'es', 'ss'):
            self.u.reg_write(REG[name], regs[name])
        self.u.reg_write(UC_X86_REG_EFLAGS, flags)
        expected, final, mask, self.events, calls = specification(memory, regs, flags, replies)
        self.replies, self.calls = replies, 0
        self.index, self.error, self.returned, self.observed = 0, None, False, []
        try:
            self.u.emu_start(self.base + START, 1 << 20, count=1000)
        except UcError as error:
            raise ValueError('MAINL PI free contract: guest fault') from error
        need(self.error is None, self.error or 'guest error')
        need(self.returned and self.index == len(self.events) and self.calls == calls, 'complete native return and events')
        self.check_registers(expected)
        actual_flags = self.u.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags & (mask | 0x600) == final & (mask | 0x600), 'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0, 1 << 20)) == memory, 'whole physical memory including every stack and caller byte')
        return dict(registers=expected, flags=actual_flags & (mask | 0x600), events=self.observed,
                    heap_calls=calls, stack_depth=8 if calls else 2, header_segment=hseg, header_offset=hoff)


def cases():
    # Both byte lanes of every tested WORD segment, with other allocations live.
    for field in range(3):
        for shift in (0, 8):
            for value in range(256):
                segments = [0x1111, 0x2222, 0x3333]
                segments[field] = value << shift
                yield dict(segments=tuple(segments))
    for active in range(8):
        segments = tuple(0xFFFF if active & (1 << i) else 0 for i in range(3))
        for offset, ss, flags, foreign in itertools.product((0, 1, 0xFFED, 0xFFFE, 0xFFFF), (0x7000, 0x8000), (2, 0x202, 0x402, 0xED7), (False, True)):
            yield dict(segments=segments, header_offset=offset, ss=ss, flags=flags, foreign_ds=foreign)
        for ss, flags in itertools.product((0x7000, 0x8000), (2, 0x202, 0x402, 0xED7)):
            yield dict(segments=segments, alias_frame=True, ss=ss, flags=flags)
    for shift in (0, 8):
        for value in range(256):
            yield dict(image_offset=value << shift)
    for replies in itertools.product(REPLIES, repeat=3):
        yield dict(segments=(0xABCD,) * 3, replies=replies)


def verify(target, candidate):
    results = []
    for image in (target, candidate):
        rows = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            trace = hashlib.sha256()
            calls = set()
            try:
                for count, parameters in enumerate(cases(), 1):
                    p = dict(seed=0x1357 if count & 1 else 0xECA8, stack=0x80 if count & 1 else 0xF800)
                    p.update(parameters)
                    result = machine.run(**p)
                    calls.add(result['heap_calls'])
                    trace.update(json.dumps(result, sort_keys=True).encode())
                need(machine.covered == set(range(START, START + SIZE)), 'all 76 owner bytes execute')
                rows.append(dict(load_segment=load, cases=count, executed_owner_bytes=len(machine.covered),
                                 heap_call_counts=sorted(calls), maximum_owner_stack_depth=8, trace_sha256=trace.hexdigest()))
            finally:
                machine.close()
        results.append(rows)
    need(results[0] == results[1], 'complete independent target/candidate observations')
    return dict(images=2, functions=1, code_bytes=SIZE, executed_owner_bytes=SIZE,
                cases_per_image=sum(r['cases'] for r in results[0]), observations=results[0],
                exhaustive_segment_byte_lanes=256, ignored_stack_bytes=0,
                heap_body_executed=False, physical_allocator_proved=False)


def negative_controls(target):
    controls = (
        ('clear-CX', 0xFF0, 1, {}), ('header-far-pointer-slot', 0xFF3, 2, {}),
        ('comment-segment-field', 0xFF7, 2, {}), ('comment-WORD-test', 0xFF8, 1, dict(segments=(0x100, 0, 0))),
        ('comment-zero-branch', 0xFFB, 1, dict(segments=(0, 0, 0))),
        ('comment-call-destination', 0x1000, 1, {}), ('comment-length-clear', 0x1005, 2, {}),
        ('comment-segment-clear', 0x1009, 2, {}), ('comment-offset-clear', 0x100C, 1, {}),
        ('machine-segment-field', 0x1010, 2, {}), ('machine-zero-branch', 0x1014, 1, dict(segments=(0, 0, 0))),
        ('machine-call-destination', 0x1019, 1, {}), ('machine-length-clear', 0x101E, 2, {}),
        ('machine-segment-clear', 0x1022, 2, {}), ('machine-offset-clear', 0x1026, 2, {}),
        ('image-segment-not-offset', 0x1029, 2, {}), ('image-WORD-test', 0x102A, 1, dict(segments=(0, 0, 0x100))),
        ('image-zero-branch', 0x102D, 1, dict(segments=(0, 0, 0))),
        ('image-call-destination', 0x1032, 1, {}), ('far-Pascal-pop-eight', 0x1036, 2, {}))
    rejected = []
    for name, at, xor, parameters in controls:
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        machine = None
        try:
            machine = Machine(replace(target, program_image=bytes(raw)), 0x1000)
            machine.run(**parameters)
        except (ValueError, UcError):
            rejected.append(name)
        else:
            raise ValueError('PI free instruction mutation escaped: ' + name)
        finally:
            if machine:
                machine.close()
    return dict(count=len(rejected), rejected=rejected, actual_guest_instruction_mutations=True,
                nop_mutations_counted=False)
