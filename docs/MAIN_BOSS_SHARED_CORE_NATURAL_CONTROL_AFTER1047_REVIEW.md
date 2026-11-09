# TH03 MAIN shared BOSS core: natural control and arithmetic after1047

This pass extends the shared BOSS reconstruction beyond the explosion ring
into the full launch, movement, hit/death, target and pattern-selection
controllers. The maintained `src/main/boss/shared.cpp` still compiles through
its two original physical objects: `ba_sring` (348 CODE bytes) and `ba_srest`
(601 CODE bytes).

## Explosion ring

Both sprite loops are now ordinary `for` headers. Their postfix signed index
and byte-angle updates remain in the original order, and the angle updates
also accept natural `angle = angle + named_step` expressions:

```cpp
for(i = 0; i < BOSS_RING_PRIMARY_SPRITES;
    i++, angle = angle + BOSS_RING_PRIMARY_ANGLE_STEP) {
    // primary 16-sprite ring
}
for(i = 0; i < BOSS_RING_SECONDARY_SPRITES;
    i++, angle = angle + BOSS_RING_SECONDARY_ANGLE_STEP) {
    // secondary 8-sprite ring
}
```

The register-qualified byte angle, explicit `static_cast` byte truncation,
base-first `-half + polar(...)` placement, named length scale and named
secondary-radius scale all reproduce the original ring object. Constant-first
sound, PID and finish-radius comparisons are exact as well. The signed-word
compound length multiplication and binary zero-minus angle calculation remain
compiler-sensitive and are preserved in their proven forms.

## Shared controller recovery

- `boss_move_sine()` and `boss_fall()` use constant-first left/right boundary
  comparisons. The fall controller now returns early while the boss is still
  above the despawn threshold, then performs the original mode, launch-owner
  and combo transition at the threshold.
- `boss_update_start()` scopes its complete active-player path under the
  positive `GBAF_BOSS == gba_flag_active[pid_current]` guard. Its launch test
  is constant-first; the player-1 template offset uses `1 == pid_current`;
  and an already-exploding boss returns before the cleanup path. The original
  32-byte SI/DI/ES/CX `REP MOVSW` copy remains intact.
- `boss_hittest_end()` uses a register `pid_other` and returns immediately
  when HP is positive or the boss is already exploding. The remaining death,
  score, active-player and level progression order is unchanged.
- `boss_target_update()` returns immediately during DESCEND and otherwise
  writes the original target coordinates with base-first Y addition.
- `boss_pattern_next()` uses a register byte for the selected pattern and a
  positive wait-frame scope. Its random rejection is now a natural
  `do-while` loop; every rejected draw still consumes exactly one RNG
  word. The mode offset is base-first, the pattern-index postfix remains, and
  the DESCEND transition is a positive `pattern_i <= pattern_count` early
  return followed by the mode assignment.
- `boss_explosion_render()` expresses the zero-mode completion test as
  `0 == boss_mode`.

## Negative controls and compiler-sensitive boundaries

Several plausible rewrites were compiled against both complete physical
objects and rejected when they changed CODE:

- Reversing the two range comparisons in the random-pattern rejection test
  changes `ba_srest`; keep the original comparison and short-circuit order.
- Rewriting the final pattern-count test as `pattern_count < pattern_i`
  changes `ba_srest`; the accepted form is the early return on
  `pattern_i <= pattern_count`.
- Replacing the explicit player-1 template offset with either
  `&boss_character_template[pid_current]` or
  `pid_current * sizeof(boss_state_t)` changes `ba_srest`. Keep the proven
  SI initialization and conditional 32-byte increment.
- Stage af1057a replaced the fixed SI/DI/ES/CX `REP MOVSW` template copy
  with `memcpy(&boss_state, &boss_character_template[pid_current],
  sizeof(boss_state_t))`. The first complete `ba_srest` CODE comparison
  differed, so the C library copy was restored to the original inline transfer.
- Replacing the signed-word compound descent/movement updates with ordinary
  assignment changes `ba_srest`.
- Register-qualified ring X/Y scratch locals change `ba_sring`; only the byte
  angle is register-qualified.

Earlier ring negatives remain applicable: shift-based length scaling,
explicit `length = length * scale`, unary-minus angle conversion and other
byte-width substitutions are not interchangeable with the proven source.

## Complete original-owner verification

Stage `af1047k` compiled the current complete shared source through both
original physical objects in two independent original Turbo C++ 4.02 rounds.
All 949 CODE bytes, 106 ordered native fields and eight PUBLIC offsets match.
Both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations. Only `ba_sring` and `ba_srest` were rebuilt; the other
97 game objects and CRT were reused, with no full cold replay.

Protected report: `.analysis/work/exatt-layout-af1047k/report.json`

SHA-256: `a9c21a2a889b66e73466a277fb3ac6ecafdabdd4422a454e7d27d2fd3827c821`

This is a source-native improvement to already-owned original code, not new
CODE ownership, raw vendor OMF packet identity or canonical packed-game
acceptance.


## Current-source scheduler revalidation (af1056c)

The current positive wait-frame scope was re-tested with the original natural
`do-while` rejection form rather than relying only on the earlier af1025a
snapshot. The register-qualified pattern local, inclusive two-sided recent
pattern window, one-RNG-draw-per-candidate behavior, mode/frame update order
and pattern-index postfix are unchanged.

Stage `af1056c` rebuilt both shared physical owners in two independent
original TC4 4.02 rounds: `ba_sring` (348 CODE bytes, 22 ordered native fields,
1 PUBLIC) and `ba_srest` (601 CODE bytes, 84 ordered native fields, 7 PUBLICs).
Both complete normal MAIN links reproduce the Japanese loaded image and all
ordered MZ relocations. The full 949-byte shared CODE payload, 106 ordered
native fields and eight PUBLIC offsets match.

Protected current-source report: `.analysis/work/exatt-layout-af1056c/report.json`

SHA-256: `f23dfc1120fdf36091ccc6b890ac6a7382af9790b5b1662c06a830a13aa7dad5`
