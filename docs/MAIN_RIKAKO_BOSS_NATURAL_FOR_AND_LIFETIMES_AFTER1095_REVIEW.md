# TH03 MAIN after1095 — complete Rikako BOSS loop and local-lifetime recovery

The maintained `src/main/boss/rikako.cpp` is the complete eight-function
original physical `ba_rikak` owner. This pass rechecked the complete owner with
original Turbo C++ 4.02 rather than treating a matching leaf as sufficient.
The final source keeps all **1,677 CODE bytes, 215 ordered native fields and
eight PUBLIC offsets** exact in two independent compiler/normal-MAIN-link
rounds.

## Natural C++ loops across the complete BOSS

All five iteration sites in the current `rikako.cpp` are now natural `for`
loops; no `while` loop remains in this owner:

- `rikako_pattern_orbit_spread()` uses a signed register index declared in the
  `for` header for the full angular bullet ring. The original multiply-before-
  divide angle distribution and `bullets_add()` order are unchanged.
- `rikako_pattern_entities_and_pellets()` keeps its original shared
  function-scope register index. The entity-release loop and the four-shot
  pellet volley both use `for` headers. The four distinct RNG calls, speed
  increment and bullet emission remain ordered as before.
- `rikako_render_main()` uses a `for` header for the eight-sprite ring. Its
  iteration expression performs `++i` before the byte-angle update, matching
  the original body order. The signed index is still explicitly promoted to
  unsigned for `% 4`; removing that cast is not native-equivalent.
- `rikako_render_intro()` uses a `for` header for the sixteen-sprite ring,
  again preserving index-before-angle mutation order. The original
  `angle = (0 - angle)` form is retained; unary minus was already shown to
  change original TC4 CODE.

## Update and renderer local lifetimes

- `gba_boss_update_rikako()` keeps the direct inactive-player return, then
  declares and initializes `pid_other` at the first active-player use.
- The unused result of the frame increment is expressed as `boss_frame++`.
- `rikako_render_main()` initializes its angle local at the point where the
  orbit angle is first needed.
- `rikako_render_intro()` initializes its angle after the blink return and
  scopes the register X coordinate to the sprite loop's first assignment.

## Positive and negative native compiler experiments

Positive experiments were compiled against the complete physical owner,
including the intermediate isolated steps `af1095a`, `af1095b`, `af1095e`,
`af1095i`, `af1095j`, `af1095o`, `af1095q`, `af1095u` and `af1095v`.
The final source-bound two-round integration is `af1095w`.

The natural alternatives were tested, not assumed:

- Moving the main-render X/Y scratch into the loop or initializing X at its
  first assignment changed native CODE (`af1095c`, `af1095x`). Keep those
  locals in their current function scope.
- Initializing the intro radius at declaration changed CODE (`af1095g` /
  `af1095h`).
- Initializing the intro top coordinate at its first assignment changed CODE
  (`af1095l`).
- Initializing the intro sprite offset at its first use changed CODE
  (`af1095n`).
- Declaring the entity-release index as a new register local in the `for`
  header changed CODE (`af1095s`). The `for` conversion is exact when it keeps
  the original shared function-scope register index (`af1095v`).

These negative controls are why the final source preserves the remaining
function-scope X/Y, top, radius and sprite-offset declarations rather than
forcing every variable into the narrowest possible scope.

## Final original compiler and full-link proof

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af1095w --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1095w
```

Both independent original TC4.02/TLINK rounds reproduce all **1,677 CODE
bytes, 215 ordered native fields and eight PUBLIC offsets**. Both normal
Japanese MAIN links preserve the original loaded image and all ordered MZ
relocations. The report is
`.analysis/work/exatt-layout-af1095w/report.json`, SHA-256
`3c5a97764efebea286e22dbe72f356f99187a3a3a5354fa093653a72fda7cf8a`.
The maintained source SHA-256 is
`15d3fc54f31ad6acb7282959ee395e4d282ae54a19ad4641c12be27c44a606b9`.

Only the affected complete `ba_rikak` physical owner was rebuilt; no full cold
replay was run. This is current-source local native evidence, not a Factory
Oracle receipt, new distinct original CODE credit, or raw historical vendor
OMF packet identity.
