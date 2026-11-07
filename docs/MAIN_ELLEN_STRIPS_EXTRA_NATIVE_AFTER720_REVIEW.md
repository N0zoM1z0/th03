# TH03 MAIN Ellen major-BOSS radial extra and strip renderer C++ — after720

The complete original `ba_ellen` TC4 BOSS source contains three attack
patterns, a full BOSS update/collision controller, the three rotating
96-pixel display strips and the large 4×8 sprite entrance renderer.

This pass reconstructed **natural prefix C++ loop/register mutations** in
both mirrored radial Extra Attack volleys (`++i` while independently
stepping the original 8-bit angle by 256/count), and all four descending
strip-index decrements in `ellen_render_main()` and `ellen_render_intro()`
(`--i` instead of the postfix `i--` statement). These exact same local
signed-register semantics retain the original three-strip draw order and
index wrap from -1 to 8. The nested 4×8 entrance loop and original signed
sprite Y-coordinate register shift are unchanged. The impact of the BOSS
hit flag and the original 2-frame intro blink are now represented by
natural Boolean tests, while entry/explosion mode checks use existing
byte mode enumeration.

The **first** native trial of these modified expressions, `af720a`,
compiled two real original Turbo C++ 4.02 objects and linked each into
the complete source-native MAIN. **All 1,675 original CODE bytes, 213
literal ordered native FIXUPP fields and 9 PUBLIC offsets** matched,
including segment definitions, full original TLINK MAIN/MAP, Japanese
loaded program and 1,553 original relocations. Independent standard MZ
serialization reproduced the complete Japanese MAIN.EXE in both rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af720a --units ba_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af720a

A separate **negative** `af720b` trial combined the first `--i` with its
signed `if(i < 0)` wrap test into `if(--i < 0)`. Despite equivalent source
semantics, native CODE differed. The combined statement was discarded and
the current source matches `af720a` exactly; the negative writer stage is
retained for later codegen analysis. This independently confirms that the
old historical warning about branch/codegen shape should not be blindly
optimized away.

Receipt: `.analysis/work/exatt-layout-af720a/report.json`, SHA-256
`7c215e839ea3f251740b916b14428ce8c643902d5bf9909ade6cb25b718a0b0e`.
Both real writer rounds, all source dependencies and actual OBJ/EXE/MAP
are retained. Only one full BOSS object was recompiled; the other 98
original objects and CRT reused. This is natural C++ recovery, not
canonical packed-file Factory unit credit or historical raw OMF identity.
