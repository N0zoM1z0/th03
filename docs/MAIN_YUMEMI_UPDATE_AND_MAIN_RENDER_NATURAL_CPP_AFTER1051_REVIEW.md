# TH03 MAIN Yumemi update and main renderer: natural C++ after1051

This pass attacks the 368-byte `gba_boss_update_yumemi()` controller and the
333-byte `yumemi_render_main()` renderer, rather than limiting the work to
small pattern leaves. Both are part of the complete ten-function
`ba_yumem` physical owner.

## Full update controller

The level-parameter initialization now uses an explicit nonzero return test:

```cpp
if(0 != boss_update_start()) {
    // six original level-derived attack parameters
}
```

The active-player controller is expressed as a direct mismatch return. The
original active body then proceeds without an enclosing PID `if`:

```cpp
if(pid_current != gba_boss_launched_by) {
    return;
}
pid_other = 1 - pid_current;
bullet_template.pid = pid_other;
boss_target_update();
boss_frame += 1;
```

The order of PID assignment, target update, frame increment, origin
calculation, mode dispatch, effect countdown, collision-map update and
hitbox/HP tail is unchanged. `pid_other` is register-qualified; the origin Y
calculation is now base-first. The 16-bit frame counter accepts compound
`+= 1`, but not ordinary `frame = frame + 1`.

The switch still covers INTRO, SELECT, all five attack families, DESCEND and
EXPLODE. The INTRO sound checks precede its finish/return test. EXPLODE
continues to return before countdown and collision work.

## Main renderer

All five local values in `yumemi_render_main()` are register-qualified:
`sprite_offset`, `target_left`, `target_top`, `pid_other`, `left` and `top`.
The full main sprite and effect geometry uses natural base-first coordinate
expressions. Both effect-origin Y values put the named bias first. The
render-mode and alternate-mode tests are constant-first; hit rendering uses
`0 != boss_hit`. The effect/hit sprite-offset arithmetic no longer carries
redundant parentheses.

The two independent effect-state counters now use an explicit conjunction
of zero comparisons before the early return. The circle/line selection uses
`0 == boss_render_frame` for the circle branch. The existing clip selection,
EGC/GRCG transitions, sprite order, line/circle calls and clip restoration
remain unchanged.

## Negative controls

The following source forms were compiled and rejected against the complete
original Yumemi owner:

- Reversing the circle/line branches so the nonzero line case comes first
  changes CODE; retain the original circle-first branch.
- Replacing `sprite_offset += YUMEMI_RENDER_EFFECT_ALT_OFF` with ordinary
  `sprite_offset = sprite_offset + ...` changes CODE.
- Replacing `boss_hp -= boss_hit` with ordinary subtraction assignment
  changes CODE.
- Replacing `boss_frame += 1` with `boss_frame = boss_frame + 1` changes CODE.
- Replacing the byte `boss_render_frame--` with `boss_render_frame -= 1`
  changes CODE; keep the original postfix decrement.
- Reversing the PID comparison operands changes ordered native fields; keep
  `pid_current != gba_boss_launched_by`.

The `register` locals, base-first coordinate calculations, explicit zero
predicates, direct mismatch return, `pid_other = 1 - pid_current`, and
`boss_frame += 1` all passed complete-owner verification.

## Complete original-owner verification

Stage `af1051j` rebuilt the complete 2,358-byte `ba_yumem` physical object in
two independent original Turbo C++ 4.02 rounds. All 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The other 98
original game objects and CRT were reused; no full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1051j/report.json`

SHA-256: `1923796b0f778511e0a6ae91741ba0d7dcded19e1a6d3c9f304e48e2e15c6063`

This is natural-C++ recovery inside the already source-owned original Yumemi
object, not new unique CODE ownership, raw vendor OMF packet identity or
canonical packed-game acceptance.
