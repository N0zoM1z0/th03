# MAIN frame scheduler: unsigned-word cadence and VSync predicates

The full 3,050-byte `entry` physical owner includes the stage setup,
round reset and main frame scheduler. The latter's unsigned-word periodic
updates now use natural `%64` and `%1024` checks rather than literal masks.
Both render-skip checks use a named two-frame period; the shot-damage
recovery cap is named. The two busy VSync waits use an equivalent natural
less-than predicate, retaining their distinct state-update order. Hardware
page flip and the three separate match/round return paths are untouched.

Source-bound original Turbo C++ 4.02/TLINK stages `af1126a`, `af1126b` and
final `af1126c` each matched 3,050 original CODE bytes, 433 native ordered
fields, eight PUBLICs and the full Japanese MAIN image and relocations in
two independent rounds. Final receipt:
`.analysis/work/exatt-layout-af1126c/report.json`.

The byte-valued `round_frame_mod16` and `round_speed` updates retain their
original mask/postfix codegen; these results are specific to the *word-sized*
clock and do not generalize to byte arithmetic.
