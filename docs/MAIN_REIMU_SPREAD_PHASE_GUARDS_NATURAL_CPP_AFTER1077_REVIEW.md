# TH03 MAIN Reimu spread leaves: positive cadence guards and typed angles (af1077k)

This review covers the complete 118-byte `reimu_pattern_spreads()` and
98-byte `reimu_pattern_mirrored_spread()` functions. These were present as
uncommitted working-tree changes when this pass began. They were not discarded
or assumed correct: I checked their control flow against the original Ghidra
decompilation and rebuilt the complete `ba_reimu` physical owner before
retaining them.

## Two-stage spread controller (118 bytes)

The original controller has three frame regions after `boss_move_sine()` and
bullet-template setup:

- `boss_frame < 0x40`: on the global 16-frame cadence, add the two narrow
  bullets at angles `0x20` and `0x60`; always return from this phase.
- `boss_frame < 0x64`: on the same cadence, add one medium bullet at angle
  `0x40`; always return from this phase.
- `boss_frame >= 0x64`: return to `REIMU_MODE_SELECT` and reset `boss_frame`.

The source now makes the cadence-positive branch explicit while preserving
phase returns:

```cpp
if(boss_frame < REIMU_SPREAD_NARROW_END) {
    if(!round_frame_mod16) {
        bullet_template.angle = 0x20;
        bullet_template.group = BG_3_SPREAD_NARROW;
        bullets_add();
        bullet_template.angle = 0x60;
        bullets_add();
    }
    return;
}

if(boss_frame < REIMU_SPREAD_MEDIUM_END) {
    if(!round_frame_mod16) {
        bullet_template.group = BG_5_SPREAD_MEDIUM;
        bullet_template.angle = 0x40;
        bullets_add();
    }
    return;
}
```

This avoids the old negative cadence guard with an early return nested inside
each phase. The first `!round_frame_mod16` replacement was tested alone at
`af1077h`; the second was tested alone at `af1077i`. Both preserve the entire
original 2,020-byte owner in two original TC4 rounds. The phase boundaries,
angle values, bullet groups, call counts and selector reset remain unchanged.

## Mirrored spread (98 bytes)

The mirrored spread retains its 16-frame firing cadence and 0x80 completion:

```cpp
if(boss_frame < REIMU_MIRROR_FINISH_FRAME) {
    if((boss_frame & (REIMU_MIRROR_FIRE_PERIOD - 1)) != 0) {
        return;
    }
    // prepare template and emit two mirrored bullets
    bullet_template.angle = static_cast<unsigned char>(boss_frame);
    bullets_add();
    bullet_template.angle = (
        REIMU_MIRROR_OPPOSITE_ANGLE - static_cast<unsigned char>(boss_frame)
    );
    bullets_add();
    return;
}

boss_mode = REIMU_MODE_SELECT;
boss_frame = 0;
```

Both original C-style byte casts were replaced by explicit
`static_cast<unsigned char>` expressions. The two casts preserve the byte
truncation before the opposite-angle subtraction. This is verified as part of
the complete `ba_reimu` owner; no assumption is made that dropping the cast or
moving the conversion after subtraction is equivalent.

## Original disassembly cross-check

The read-only Ghidra view identifies the original functions at
`1f1f:1bb0` (118 bytes) and `1f1f:1de1` (98 bytes). The spread decompilation
confirms the `< 0x40` and `< 100` phase tests, a zero test of the global
16-frame cadence, two narrow bullet additions, one medium addition, and the
final selector/frame reset. The mirrored decompilation confirms the `< 0x80`
range, `(frame & 0x0f) == 0` cadence, two byte-angle emissions and the final
selector/frame reset. The current C++ keeps those operations and their order.

## Complete original-owner verification

Stage `af1077g` rebuilt the complete `ba_reimu` owner in two independent
original Turbo C++ 4.02 rounds: all 2,020 CODE bytes, 270 ordered native fields
and nine PUBLIC offsets match. The normal Japanese MAIN image and ordered MZ
relocations also match, and the source overlay checked the live `reimu.cpp`
producer dependency.

Report: `.analysis/work/exatt-layout-af1077g/report.json`

SHA-256: `d7580e60c1484d5d9afcbd44404256b5aec726eecfdc2fc8dcaca576f14a2de8`

The two cadence-only negative/positive-guard experiments are retained as
separate full-owner proofs:

- `af1077h`: narrow spread `if(!round_frame_mod16)`;
  report SHA-256 `ab87e8f517296a0bb61b115f6601fee3109756ef08e1273639f31e81ee5369c4`.
- `af1077i`: medium spread `if(!round_frame_mod16)`;
  report SHA-256 `4df60c632a522ae4efaee989674033287dc99d351fb54f4b9bc9d58422d87bc2`.

## Current five-owner integration

Stage `af1077k` rebuilt `ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly` and
`ex_reup` together in two independent original TC4 rounds: 8,188 CODE bytes,
1,067 ordered native fields and 40 PUBLIC offsets match. Both complete normal
Japanese MAIN links reproduce the original loaded image and ordered MZ
relocations. This includes the two spread leaves, the full Reimu BOSS owner,
Yumemi and Chiyuri BOSS owners, and both physical Reimu Extra Attack owners.

Report: `.analysis/work/exatt-layout-af1077k/report.json`

SHA-256: `ac71f4eff35a78362537d81d8d01b1d306c8a86d4dfa137830c0775de65742b8`

This is scoped original-toolchain evidence, not a Factory Oracle receipt,
raw vendor OMF identity claim, or canonical packed-file acceptance.
