# Chiyuri full BOSS: four real native C++ fan volleys and sprite geometry after680

The original full eleven-function Chiyuri BOSS physical source
owns 2,654 original CODE bytes, 381 literal ordered native
FIXUPP fields and 11 PUBLICs. Its large `chiyuri_pattern_fans`
emits separate horizontal and vertical pellet fans, each with
ascending and descending speed passes. The update, ring renderer
and full sprite renderer remain in the same complete source unit.

In all **four** fan-pass loops, the original subpixel
coordinate calculation
`(((i * 0x70) / chiyuri_fan_count) << 4)`
is now natural, exact compiler-generated C++:
`(((i * 0x70) / chiyuri_fan_count) * 16)`.
Both original-TC4 rounds of `af680a` proved that the
two forms produce exactly identical native instructions.
**The integer division must occur before this multiplication**
because moving the scale inside a quotient would change
rounding and the actual bullet geometry.

Four additional fan angle expressions use natural
`(i * 64) / chiyuri_fan_count` rather than
`(i << 6) / chiyuri_fan_count`. The genuine
original-byte-exact test `af680b` includes all
four complete emission loops and both mirrored shots.

Three other owner contexts now use natural C++ scaling
instead of explicit authored shifts: `boss_move_phase * 16`
for the original palette pulse in the large BOSS update,
`boss_effect_radius * 16` for the entire sixteen-sprite
ring radius and `boss_render_frame * 4` in **two**
distinct ring/main sprite offsets. Stage `af680c`
recompiled the complete physical BOSS object in two genuine
original Turbo C++ 4.02 compiler/TLINK rounds and reproduced
all original CODE and fixup bytes.

Final source/header-OMF-dependency-attested native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af680d --units ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af680d

Both new objects reproduce **2,654 original CODE bytes,
381 literal ordered FIXUPPs, 11 PUBLIC offsets**, all
OMF segments and 16-bit ABI metadata. Both full normal
MAIN EXEs and path-normalized complete MAPs equal the
retained source-native parent. Japanese program image,
all 1,553 literal ordered original MZ relocations and
independently serialized 130,882-byte original Japanese
MAIN.EXE remain exact in both rounds.

Native evidence: `.analysis/work/exatt-layout-af680d/report.json`,
SHA-256 `408b42e4d0e9866b9508ffb18ecf1d63dcacdc442dc3bec7db304d2b8e71da3f`.
Both genuine modified source/compiler inputs, packed
BOSS state header dependencies, raw objects and full
compiler/linker writer logs are retained. Only this one
complete physical BOSS TU was recompiled; the other 98
original objects and CRT/library sources were reused
without full cold replay.

These game CODE bytes were previously source-owned;
the result is original-byte-exact maintained C++ and
is not new canonical Factory packed-file acceptance,
raw historical vendor OMF packet identity or actual
PC-98 device behavior proof.
