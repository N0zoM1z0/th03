# TH03 MAIN — complete Ellen BOSS timed attacks and template recovery (af1111e)

The full nine-function original `ba_ellen` Turbo C++ 4.02 owner includes
all spread, radial Extra Attack and pellet patterns, the live update/collision
controller and the strip/main/intro renderers. Both 16-bit two-frame spread
clocks now use natural `% ELLEN_SPREAD_PERIOD`, and the Extra Attack warning,
first burst and final burst use independent `if` branches after original
returns. This preserves every sound, random angle and far projectile emission
in the original order. Template mode and rendering mode now use the meaningful
`ELLEN_MODE_INTRO` and `ELLEN_RENDER_MODE_NORMAL` values.

Progressive native stages `af1111a` (two spread clocks), `af1111d` (extra
phase guards), and final `af1111e` (template state) were each rebuilt in two
independent original TC4/normal MAIN TLINK rounds. The complete 1,675-byte
CODE owner, all 213 ordered native fields, nine PUBLIC offsets, complete
Japanese MAIN image and its 1,553 ordered relocations matched twice. Current
source-linked receipt: `.analysis/work/exatt-layout-af1111e/report.json`.

Two compiler-specific negative controls: `af1111b` moved the radial `register
int i` into its `for` header and changed CODE; `af1111f` replaced a byte
`boss_render_frame = boss_render_frame + STEP` with compound `+=`, also
changing CODE. Both were restored. The two byte-angle/radial signed division
operations and strip progression are retained. These local results do not
establish canonical Factory packed-file credit.
