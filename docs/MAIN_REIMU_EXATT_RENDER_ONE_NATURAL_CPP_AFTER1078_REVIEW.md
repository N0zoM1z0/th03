# TH03 MAIN Reimu Extra Attack renderer: branch-local sprite state and typed word access (af1078g)

This pass recovers the complete 205-byte `reimu_exatt_render_one()` helper in
the `ex_rfly` physical owner. The function is near cdecl and has one original
caller, `exatt_render_reimu()`. Its rendering behavior was checked against the
read-only Ghidra decompilation and the full 825-byte original physical owner.

## Original rendering sequence

The original function obtains the current entity from `exatt_entity_p`,
converts its X coordinate to screen space using the entity PID, converts Y
from subpixels to pixels and adds the 16-pixel render offset. It configures a
48x48 sprite and selects the opposite player's clip region based on
`pid_current`.

For an ACTIVE entity, the renderer derives the sprite base from
`pid.so_attack + 0x280`, divides the frame byte by four, and selects one of
three sprite offsets using the low two phase bits:

- phase low bits equal one: add six;
- another nonzero phase: add `0x780` plus six for odd phase;
- zero phase: retain the base offset.

It draws the active sprite and returns. FLYING entities call
`exatt_render_state2()` with the adjacent 16-bit word beginning at `p->frame`;
other states call `exatt_render_state_other()` with the 16-bit word beginning
at `p->state`.

## Current natural C++ form

The coordinate locals are initialized at declaration. The sprite offset and
phase scratch now exist only in the ACTIVE branch, where they are used:

```cpp
register exatt_entity_t near *p = exatt_entity_p;
screen_x_t left = playfield_fg_x_to_screen(p->x, p->pid);
screen_y_t top = (p->y >> 4) + 16;
sprite16_put_size.set(48, 48);

if(p->state == REIMU_FLY_STATE_ACTIVE) {
    register sprite16_offset_t sprite_offset;
    sprite_offset = pid.so_attack + 0x280;
    unsigned char phase = (p->frame / 4);
    if((phase & 3) == 1) {
        sprite_offset += 6;
    } else if(phase & 3) {
        sprite_offset += 0x780 + ((phase & 1) * 6);
    }
    sprite16_put(left - 24, top - 24, sprite_offset);
    return;
}
if(p->state == REIMU_FLY_STATE_FLYING) {
    exatt_render_state2(
        left, top, *reinterpret_cast<unsigned int near *>(&p->frame)
    );
} else {
    exatt_render_state_other(
        left, top, *reinterpret_cast<unsigned int near *>(&p->state)
    );
}
```

The reinterpret casts make the intentional 16-bit field loads explicit and
preserve the adjacent byte used by the original near-Pascal helpers. They are
not equivalent to passing only `p->frame` or `p->state` as a byte.

## Isolated compiler experiments

The following transformations individually reproduce the complete original
`ex_rfly` owner:

- `sprite_offset` is declared inside the ACTIVE branch (`af1077m`).
- `phase` is declared and initialized inside the ACTIVE branch (`af1077n`).
- The ACTIVE phase's nonzero test uses `else if(phase & 3)` (`af1077q`).
- The sprite base assignment omits redundant outer parentheses (`af1077r`).
- The X/Y screen coordinates are initialized at declaration (`af1077s`).
- The frame-word access uses `reinterpret_cast` (`af1077t`).
- The state-word access uses `reinterpret_cast` (`af1077u`).
- The secondary sprite-offset addition omits redundant outer parentheses
  (`af1078d`).
- The Y pixel initializer omits redundant grouping parentheses (`af1078e`).

Negative controls:

- Removing `register` from the entity pointer changes CODE (`af1077o`); retain
  the register-qualified near pointer.
- Replacing the original `/ 4` phase division with `>> 2` changes CODE
  (`af1077p`); retain division despite the equivalent nonnegative arithmetic.

## Original disassembly cross-check

Ghidra identifies the function at `28fe:13e4`, address `0x2A3C4`, with 205
bytes and near-cdecl calling convention. The decompilation and disassembly
confirm the coordinate calculations, 48x48 size, PID-dependent clip range,
ACTIVE phase selection, early return after active drawing, and the two
16-bit helper arguments. The current C++ preserves their order and width.

## Complete original-owner verification

Stage `af1078f` rebuilt the complete `ex_rfly` physical owner in two
independent original Turbo C++ 4.02 rounds. All 825 CODE bytes, 51 ordered
native fields and eight PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay independently checked the current `exatt_reimu_prefix.inl` dependency.

Report: `.analysis/work/exatt-layout-af1078f/report.json`

SHA-256: `e488e39f94c085314d7270397fbeb08dac3f54ff0cf721a14b6c64f7185407d7`

## Current five-owner integration

Stage `af1078g` rebuilt `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and
`ex_reup` together in two independent original TC4 rounds: 8,188 CODE bytes,
1,067 ordered native fields and 40 PUBLIC offsets match. Both complete normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations.

Report: `.analysis/work/exatt-layout-af1078g/report.json`

SHA-256: `72099aefd64f188f12591c77ad74fb72761fce80e0920c849255e0b645172838`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
