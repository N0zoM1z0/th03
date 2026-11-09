# TH03 MAIN — Yumemi BOSS natural update, renderer and RNG geometry (af1106d)

The original complete `ba_yumem` owner spans all 2,358 bytes of original
CODE: ring/aimed/cross/chase/rain attacks, frame and collision controller,
main visual effects, multi-phase entrance raster and render dispatch.
The update's unsigned 16-bit frame uses `++boss_frame`, and the original
two-frame aimed-shot cadence uses natural `%` without changing RNG order.
The rendering entry checks inactive players via early return. The five
aimed-volley bullet groups are indexed with `sizeof(yumemi_groups)`,
retaining the same original one-RNG-word draw and five physical bytes.
The effect renderer has natural `!boss_effect_radius && !boss_render_frame`
exit logic and keeps its two separate animation state values.

Genuine native stages `af1106a` (frame/dispatcher and aimed-shot clock),
`af1106c` (type-sized group selector), and final `af1106d` (effect guard)
all passed two original TC4/full normal MAIN TLINK rounds. The complete
2,358-byte CODE owner, 343 ordered native fields, ten PUBLICs, full Japanese
MAIN image and all 1,553 ordered MZ relocations match. Current source proof:
`.analysis/work/exatt-layout-af1106d/report.json`.

The `af1106b` attempt to replace the original center-only player view with
`src/main/player/stuff.hpp` failed TC4 compilation because transitive
unprotected collision-map declarations were included twice; no header or ABI
patch was made to conceal it. Separately, `af1106e` narrowed line-effect
target coordinate lifetimes and `af1106f` narrowed the overlay sprite offset;
both changed original CODE and were rejected. Full source-native exactness and
whole-product canonical Factory credit remain separate.
