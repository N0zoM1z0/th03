# TH03 MAIN Reimu main renderer: separate sprite phases and positive ORBIT gate (af1083h)

This review covers the complete 259-byte near-cdecl
`reimu_render_main()` at `1f1f:1fb3` (`0x211A3`). Its sole caller is
`gba_boss_render_reimu()`. The function is not treated as a handful of local
expressions: the complete 2,020-byte `ba_reimu` owner and the current
five-owner Reimu/Yumemi/Chiyuri + Reimu Extra Attack integration were rebuilt.

## Rendering sequence

The renderer derives the opponent PID, configures the main 48x48 sprite and
clip rectangle, applies the hit flash offset, transforms the boss center and
draws the main sprite. The optional orbit phase then configures the smaller
sprite, derives a separate orbit sprite offset and byte animation cel, and
draws all live orbit positions in signed-index order.

## Current source structure

The main and orbit sprite offsets have disjoint block lifetimes. The byte
animation carrier and signed orbit index are confined to the orbit phase:

```cpp
pid_t pid_other = 1 - pid_current;

sprite16_put_size.set(REIMU_RENDER_MAIN_SIZE, REIMU_RENDER_MAIN_SIZE);
if(pid_other == 0) {
    sprite16_clip.set_for_pid_0();
} else {
    sprite16_clip.set_for_pid_1();
}

{
    register sprite16_offset_t sprite_offset = boss_sprite_offset;
    if(boss_hit) {
        sprite_offset += 0x0C;
    }
    // Transform boss center and draw main sprite.
}

if(boss_render_mode == REIMU_RENDER_MODE_ORBIT) {
    sprite16_put_size.set(REIMU_RENDER_ORBIT_SIZE, REIMU_RENDER_ORBIT_SIZE);
    {
        register sprite16_offset_t sprite_offset = (boss_sprite_offset + 0xFFF4);
        unsigned char anim = (boss_frame / REIMU_RENDER_CEL_PERIOD);
        if((anim & 3) == 1) {
            sprite_offset += 6;
        } else if(anim & 3) {
            sprite_offset += (((anim & 1) * 6) + 0x780);
        }
        for(register int i = 0; i < reimu_orbit_count; ++i) {
            // Transform and draw the i-th live orbit position.
        }
    }
}
```

The current positive ORBIT branch avoids a separate negative guard and early
return. The main sprite is always drawn first. The function simply skips the
orbit phase when the render mode is not ORBIT. `pid_other == 0` is retained as
the explicit clip selection predicate. `boss_hit` uses its byte truth value.

`left` and `top` remain function-scope screen-coordinate scratches. Moving
them into the main/orbit blocks was tested at `af1082e` and changed CODE. The
orbit offset retains `boss_sprite_offset + 0xFFF4`; replacing it with
`boss_sprite_offset - 12` changed CODE at `af1082f`.

## Isolated and combined native experiments

- Declaration initialization of `pid_other` and its unparenthesized
  `1 - pid_current` expression are retained.
- Main-sprite and orbit-sprite offsets have separate block scopes.
- The ORBIT phase owns its animation byte and signed loop index.
- `if(pid_other == 0)` was verified at `af1082c`.
- The positive `if(boss_render_mode == REIMU_RENDER_MODE_ORBIT)` phase was
  verified at `af1082d`.
- Moving screen-coordinate locals into the two render blocks changed CODE
  (`af1082e`); keep them at function scope.
- Rewriting the orbit offset as subtraction changed CODE (`af1082f`); retain
  the 16-bit additive immediate `0xFFF4`.

## Original disassembly cross-check

Ghidra identifies the 259-byte function at `0x211A3` with near-cdecl calling
convention. The decompilation confirms opponent PID selection, clip setup,
hit-dependent sprite offset, main draw, the ORBIT-only sprite size and cel
selection, and the live orbit loop. The current source preserves the main
sprite before optional orbit rendering and retains the byte truncation before
the low-bit animation masks.

## Complete current-source verification

The current `ba_reimu` source was rebuilt in two independent original Turbo C++
4.02 rounds at `af1083d`. All 2,020 CODE bytes, 270 ordered native fields and
nine PUBLIC offsets match; both normal Japanese MAIN links reproduce the
original loaded image and ordered MZ relocations. The source overlay checked
the maintained C++ producer and compiler include dependency.

The later five-owner integration `af1083h` includes the current `ba_reimu`
source together with `ba_yumem`, `ba_chiyu`, `ex_rfly` and `ex_reup`.

Report: `.analysis/work/exatt-layout-af1083h/report.json`

SHA-256: `3a7cfff996b15547a5ff4f30dcc697c79cdccd3a9d2e5baf2ebf4e25cc3a74d8`

Current `ba_reimu` source SHA-256:
`a8bd4cdd9c0dfd7b98c71e1ea8593bf3ba2a16c72b721b149725925f14d4b011`

This is scoped original-toolchain source evidence, not a Factory Oracle
receipt, raw vendor OMF identity claim, or canonical packed-file acceptance.
