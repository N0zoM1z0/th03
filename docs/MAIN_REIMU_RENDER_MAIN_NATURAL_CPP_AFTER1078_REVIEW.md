# TH03 MAIN Reimu main renderer: disjoint sprite lifetimes and loop-local orbit index (af1078r)

This pass recovers the complete 259-byte near-cdecl `reimu_render_main()`
function. The original Ghidra function is `FUN_1f1f_1fb3` at `1f1f:1fb3`
(address `0x211A3`). Its one caller is `gba_boss_render_reimu()`.

## Original rendering phases

The renderer first derives the opposite-player PID, configures the 48x48 main
sprite and clip rectangle, adjusts the boss sprite offset when `boss_hit` is
nonzero, converts the boss center to screen coordinates and draws the main
sprite. If `boss_render_mode` is not ORBIT, it returns.

The ORBIT phase sets the smaller sprite size, derives a second sprite offset
from `boss_sprite_offset + 0xFFF4`, computes the byte animation cel from the
16-bit boss frame divided by the cel period, applies the phase mask and
optional alternate bank, then draws `reimu_orbit_count` live orbit positions
in signed-index order.

## Current natural C++ lifetimes

The current source keeps the PID local initialized at declaration and splits
the two non-overlapping sprite-offset lifetimes:

```cpp
pid_t pid_other = 1 - pid_current;

sprite16_put_size.set(REIMU_RENDER_MAIN_SIZE, REIMU_RENDER_MAIN_SIZE);
if(!pid_other) {
    sprite16_clip.set_for_pid_0();
} else {
    sprite16_clip.set_for_pid_1();
}

{
    register sprite16_offset_t sprite_offset = boss_sprite_offset;
    if(boss_hit) {
        sprite_offset += 0x0C;
    }
    left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - REIMU_RENDER_MAIN_LEFT_MARGIN);
    top = ((boss_center_y >> 4) - REIMU_RENDER_MAIN_TOP_MARGIN);
    sprite16_put(left, top, sprite_offset);
}

if(boss_render_mode != REIMU_RENDER_MODE_ORBIT) {
    return;
}

sprite16_put_size.set(REIMU_RENDER_ORBIT_SIZE, REIMU_RENDER_ORBIT_SIZE);
{
    register sprite16_offset_t sprite_offset = (boss_sprite_offset + 0xFFF4);
    unsigned char anim = (boss_frame / REIMU_RENDER_CEL_PERIOD);
    // Original byte-cel phase selection remains mask-based.
    if((anim & 3) == 1) {
        sprite_offset += 6;
    } else if(anim & 3) {
        sprite_offset += (((anim & 1) * 6) + 0x780);
    }
    for(register int i = 0; i < reimu_orbit_count; ++i) {
        // transform and draw the i-th live orbit position
    }
}
```

The main-sprite and orbit-sprite offsets are now separate register locals in
their own scopes. The byte animation cel is declared only in the ORBIT phase,
and the signed orbit index lives in the `for` initializer. `pid_other` is
initialized at first declaration. The `boss_hit` byte uses a truth test.

## Isolated experiments

- Moving `pid_other` initialization into its declaration preserves the full
  original owner (`af1078h`); removing the redundant parentheses around
  `1 - pid_current` also preserves it (`af1078i`).
- Moving `anim` into the ORBIT block and initializing it from the frame
  division preserves the owner (`af1078j`).
- Moving the signed register index into the `for` initializer preserves the
  owner (`af1078k`).
- Splitting the main and ORBIT sprite offsets into two disjoint block locals
  preserves the owner (`af1078m` / formatted source `af1078n`).
- Replacing `if(boss_hit != 0)` with `if(boss_hit)` preserves the owner
  (`af1078p`).
- Replacing the ORBIT offset `boss_sprite_offset + 0xFFF4` with the seemingly
  equivalent `boss_sprite_offset - 12` changes CODE (`af1078o`). Keep the
  original 16-bit additive form; the signed arithmetic rewrite is not accepted.

## Original disassembly cross-check

The Ghidra decompilation and instruction stream confirm the local PID byte,
clip range, hit-dependent main sprite offset, screen coordinate conversions,
main draw and early return, followed by the orbit-only size/offset/animation
setup and signed-index loop. The original orbit offset uses an ADD with the
16-bit immediate `0xFFF4`; this is why the source retains that additive form
rather than rewriting it as subtraction. The byte animation cel is stored
before the `& 3` and `& 1` masks; the current source preserves this byte
truncation and mask ordering.

## Complete original-owner verification

Stage `af1078q` rebuilt the complete `ba_reimu` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The source
overlay independently checked the current `reimu.cpp` dependency.

Report: `.analysis/work/exatt-layout-af1078q/report.json`

SHA-256: `7f4c3948ab74f6209ea40b44065300229c7b7e76a30444cec4b1fb41fbaaca2c`

## Current five-owner integration

Stage `af1078r` rebuilt `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and
`ex_reup` together in two independent original TC4 rounds: 8,188 CODE bytes,
1,067 ordered native fields and 40 PUBLIC offsets match. Both complete normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations.

Report: `.analysis/work/exatt-layout-af1078r/report.json`

SHA-256: `e5aa2a5f4a4efc2075db8509f1e16d5ea43ca872e658f7c34cc15a404b2812ff`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
