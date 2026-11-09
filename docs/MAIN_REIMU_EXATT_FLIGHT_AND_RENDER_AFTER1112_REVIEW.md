# TH03 MAIN — Reimu Extra Attack flight, creation, collision and rendering (af1112h)

Two separate original MAIN_06 Turbo C++ 4.02 physical owners were recompiled
together: `ex_rfly` (shared flight plus Reimu creation/render/collision prefix)
and `ex_reup` (entity update and independent render pass). The first-free slot
search in both Reimu creation APIs now has a natural `for(register int i=0; …)`
header, prefix near-pointer update and an explicit eight-slot bound. Named
compile-time values express the original spawn X range, Y mask, flight-speed
bonus, orbit velocity and three-part collision stripes. The update/render
owner likewise uses typed eight-slot bounds, natural pointer advancement and
explicit first-element indexing. Two renderer sprite-offset locals initialize
at first use, after the original sprite setup.

Successive real compiler experiments `af1112a`/`b`/`c` and combined-owner
`af1112e`/`f`/`g`/final `af1112h` all reproduced their complete physical
scopes through two independent original TC4/normal MAIN links. The final
combined scope covers 1,156 original CODE bytes, 73 ordered native relocation
fields, ten PUBLIC offsets, the full Japanese MAIN loaded image and all
1,553 ordered MZ relocations. All three maintained implementation includes
are source-bound. Preserved evidence:
`.analysis/work/exatt-layout-af1112h/report.json`.

`af1112d` was an independent negative: replacing the low-level flight
transition labels with natural nested PID/edge comparisons changed original
CODE and was restored. Original register-visible flight boundaries and
entity state transitions remain. This is local source-native recovery, not
canonical Factory packed-game acceptance.
