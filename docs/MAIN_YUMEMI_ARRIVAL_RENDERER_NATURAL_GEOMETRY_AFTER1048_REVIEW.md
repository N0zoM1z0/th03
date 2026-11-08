# TH03 MAIN Yumemi arrival renderer: natural geometry and registers after1048

This pass advances the complete ten-function Yumemi BOSS owner through its
404-byte `yumemi_render_arrival()` and 83-byte far render dispatcher. The
four-stage entrance raster remains the same original PC-98 sprite/overlap
operation, now with additional natural C++ geometry and local-lifetime
recovery.

## Four-phase entrance geometry

All four unsigned BOSS-frame boundaries now use constant-first comparisons.
The original two-stage signed scale is expressed with named C++ scale values:

```cpp
((value * YUMEMI_ARRIVAL_POS_LOW_SCALE) *
    YUMEMI_ARRIVAL_POS_HIGH_SCALE)
```

The two stages must remain separate. Genuine original TC4 4.02 emits the
original CODE for `value * 8` followed by `* 16`; folding the scales into
`value * 128` changes CODE. The four existing raster `for` loops keep their
original inclusive left/right tests, signed step direction and compound
step updates.

The renderer also now uses register locals for its Y coordinate, opposite
PID and byte phase. Its left/right coordinates remain register-qualified.
The Y origin uses base-first `-YUMEMI_RENDER_MAIN_TOP_OFFSET +
(boss_center_y >> 4)`, and the three phase-byte assignments no longer carry
redundant parentheses around their subtraction.

## Far render dispatcher

`gba_boss_render_yumemi()` now scopes its active path under the positive
`pid_current == gba_boss_launched_by` guard. Its `pid_other` is register-
qualified, and INTRO/EXPLODE mode checks are constant-first. The original
arrival/main/explosion dispatch and return order is unchanged.

## Negative controls

The complete original owner was used to reject several superficially
interchangeable alternatives:

- Folding the two scale stages into `value * 128` changes CODE.
- Reversing raster comparison operands (`left <= right` to `right >= left`,
  or `left >= right` to `right <= left`) changes CODE. Keep the original
  inclusive operand order in all four loops.
- Replacing `left += step` / `left -= step` with ordinary assignment changes
  CODE; keep compound raster updates.
- Reordering the first phase's `value - TO_SP(104)` as
  `-TO_SP(104) + value` changes CODE.
- Reversing the far-render PID inequality operands preserves CODE bytes but
  changes ordered native fields. Keep `pid_current != gba_boss_launched_by`.

The original `asm { xor dx, dx }`, hardware interrupt sequence, clipping and
final overlap-clear protocol remain intact.

## Complete-owner verification

Stage `af1048t` rebuilt the entire original `ba_yumem` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,358 CODE bytes, 343 ordered
native fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. Only this
physical BOSS owner was rebuilt; the other 98 game objects and CRT were
reused. No full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1048t/report.json`

SHA-256: `5483fece57ab643cb3f8b2ffcd2696974d5af9827cab20adfa5a8c4cbfd2395b`

This is natural-source recovery for historically owned CODE, not new unique
CODE ownership, raw vendor OMF packet identity or canonical packed-game
acceptance.
