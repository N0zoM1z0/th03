# TH03 MAIN original PMD sound-effect arbitration: source-native after727

The physical original `snd_se` translation unit is separate from the
`reset`/PMD bridge producers. It owns the original pair of routines
`snd_se_play()` and `snd_se_update()` in a three-segment OMF layout
(`SHARED` CODE 120 bytes, zero DATA and BSS), with 18 ordered original
fixup fields and two original PUBLICs.

We extended the actual original-source scoped TC4/TLINK compiler to select
`src/main/sound/se.cpp` and replace the **real** `obj/th03/snd_se.obj` in the
99-object normal MAIN link. The baseline original-source `af727a` proof
matched the entire original object and full executable, rather than assuming
that the existing source was exact.

The original priority arbiter has now been simplified into **natural C++**:
`register int se = new_se` directly handles the source parameter and the
priority/timeout lookup arrays are indexed directly by `snd_se_playing`
instead of a redundant `for_current()` helper. The byte sentinel
`SE_NONE=0xFF`, conditional priority preemption, original frame reset on
preemption, PMD playback (`AH=PMD_SE_PLAY`, `AL=se`, INT 60h), and explicit
original frame-expiration ordering are all preserved.

`af727b` proved the direct-source simplifications compiled original-exact.
`af727c` added natural `if(!snd_se_frame)` and changed the mutable **global
8-bit** frame counter from `snd_se_frame++` to prefix `++snd_se_frame`;
that changed original CODE and failed, despite equivalent C++ state results.
`af727d` restored the original postfix byte mutation, **keeping the
natural zero condition**, and both full original-source compiler/link
rounds passed. The failed `af727c` native scratch stage is retained, not
counted as exact.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af727d --units snd_se
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af727d

Each genuine TC4 4.02 / TLINK round matched **all 120 original CODE bytes,
18 ordered literal native FIXUPP fields, 2 PUBLICs**, complete OMF segments,
normal full MAIN EXE and normalized MAP, Japanese 124,642-byte loaded game
and all 1,553 ordered MZ relocations. Independent standard MZ serialization
reproduces the entire original 130,882-byte Japanese MAIN.EXE. Only
`snd_se` was recompiled; 98 original other project objects and original
CRT were reused, not a full cold replay.

Proof: `.analysis/work/exatt-layout-af727d/report.json`, SHA-256
`629696f575585ddfa45e7ad6e6dbd3e4e6c72191ace02f9cebbcfa7d894d5f2d`.
Two rounds of current-source snapshots, real OMF dependency comments,
compiler logs, OBJ/EXE/MAP, full linker responses and independent MZ
file comparisons remain preserved. This is a newly directly proven
physical sound-source producer in the focused workflow; it does **not**
represent new Factory canonical packed acceptance, original vendor raw
OMF packet identity or whole-project source completion.
