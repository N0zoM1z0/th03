# TH03 MAIN Reimu intro renderer: polar loop and local scratch lifetimes (af1083h)

This review covers the complete 259-byte near-Pascal
`reimu_render_intro(unsigned char angle, int length)` at `1f1f:20b6`
(`0x212A6`). It is called by `gba_boss_render_reimu()` and emits eight polar
sprites during the intro sequence.

## Original state and rendering flow

The function derives the opposite PID and first applies the intro flash gate:
when `round_frame_mod2` is set and the boss frame is before
`REIMU_INTRO_FLASH_END_FRAME` (`0x40`), it returns without drawing. Otherwise
it configures the 48x48 sprite and opposite-player clip rectangle, computes
the attack sprite cel, then emits eight sprites around the boss center.

For each sprite, the current angle indexes `CosTable8` and `SinTable8`; the
resulting X/Y positions are transformed to screen coordinates and drawn. The
angle advances by `REIMU_INTRO_ANGLE_STEP` (`0x20`) after each draw, while the
signed index advances once per iteration.

## Current source structure

```cpp
void near pascal reimu_render_intro(unsigned char angle, int length)
{
    screen_y_t top;
    int i;
    unsigned char anim;
    pid_t pid_other = 1 - pid_current;

    if(round_frame_mod2 && (boss_frame < REIMU_INTRO_FLASH_END_FRAME)) {
        return;
    }

    sprite16_put_size.set(REIMU_RENDER_ORBIT_SIZE, REIMU_RENDER_ORBIT_SIZE);
    if(pid_current) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }

    register sprite16_offset_t sprite_offset = (pid.so_attack + 0x280);
    anim = (boss_frame / REIMU_RENDER_CEL_PERIOD);
    if((anim & 3) == 1) {
        sprite_offset += 6;
    } else if(anim & 3) {
        sprite_offset += (((anim & 1) * 6) + 0x780);
    }

    for(i = 0; i < REIMU_INTRO_SPRITE_COUNT; i++, angle += REIMU_INTRO_ANGLE_STEP) {
        register screen_x_t left = polar(boss_center_x, length, CosTable8[angle]);
        top = polar(boss_center_y, length, SinTable8[angle]);
        left = (playfield_fg_x_to_screen(left, pid_other) - REIMU_RENDER_ORBIT_LEFT_MARGIN);
        top = ((top >> 4) - REIMU_RENDER_ORBIT_TOP_MARGIN);
        sprite16_put(left, top, sprite_offset);
    }
}
```

The opposite PID and sprite offset are initialized at declaration. The X
coordinate is a register local inside the loop body, initialized directly by
its polar calculation. The Y coordinate remains function-scope because
moving it into the loop body changed CODE. The animation byte remains
function-scope and is assigned after sprite-offset setup: making it a
first-use initializer changed CODE. The signed index also remains
function-scope: moving it into the `for` initializer changed CODE.

## Isolated native experiments

- `pid_other = 1 - pid_current` moved to its declaration and passed as part of
  the complete current-source rebuild.
- The sprite offset is initialized at its first use after clip setup.
- The X polar coordinate is declared and initialized inside the loop body.
- Replacing prefix `++i` with postfix `i++` in the loop header preserves the
  complete owner (`af1083f`). The current source uses postfix form; angle
  advancement remains the second comma-expression operation.
- Initializing `anim` at its first use changed CODE (`af1083a`); keep the
  declaration and later assignment.
- Moving `i` into the `for` initializer changed CODE (`af1083e`); keep its
  function-scope declaration.
- Moving `top` into the loop body changed CODE (`af1083g`); keep it at
  function scope.

The loop retains eight iterations and byte-angle advancement by 0x20. The
`anim` value remains a byte before its `& 3` and `& 1` phase masks; do not
rewrite the byte mask sequence as a remainder expression without a separate
full-owner experiment.

## Original disassembly cross-check

Ghidra identifies the function at `0x212A6` with near-Pascal calling
convention. Its decompilation and instruction stream confirm the `0x40`
flash threshold, PID-dependent clip range, `boss_frame >> 2` animation
calculation, eight-iteration word index, two polar calls per iteration, the
screen transforms, the sprite draw, and `angle += 0x20` after the draw. The
current C++ preserves this ordering and the 16-bit coordinate/angle behavior.

## Complete current-source verification

Stage `af1083d` rebuilt the complete current `ba_reimu` source in two
independent original Turbo C++ 4.02 rounds: 2,020 CODE bytes, 270 ordered
native fields and nine PUBLIC offsets match, and both normal Japanese MAIN
links reproduce the original loaded image and ordered MZ relocations. The
source overlay checked the maintained C++ source and compiler dependencies.

Stage `af1083h` then rebuilt the current five-owner set
`ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and `ex_reup` in two independent
original TC4 rounds: 8,188 CODE bytes, 1,067 ordered native fields and 40
PUBLIC offsets match. Both normal Japanese MAIN links reproduce the original
loaded image and ordered MZ relocations.

Report: `.analysis/work/exatt-layout-af1083h/report.json`

SHA-256: `3a7cfff996b15547a5ff4f30dcc697c79cdccd3a9d2e5baf2ebf4e25cc3a74d8`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
