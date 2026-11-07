# TH03 MAIN Rikako major BOSS: original-native natural renderer mask and control gates (after726)

The complete **1,677-byte original `ba_rikak` physical TC4 source** owns
Rikako's large orbit-spread, entity-release and alternating-barage attack
procedures, the full BOSS update/collision dispatcher, the eight-sprite
main ring renderer and sixteen-sprite arrival renderer. This pass tested
natural C++ expressions **inside the complete physical BOSS**, not only
small leaves.

## Source recovery tested directly against the original Japanese object

The original renderer's two separate `static_cast<unsigned int>(i) % 4`
expressions now use the equivalent natural `i & 3`, **with the signed loop
index bounded to 0..7**. Its original pixel sprite cycle still has a
zero case separate from the nonzero 1..3 sequence; the `if(i & 3)` C++
truth test is also native-exact. The 8- and 16-sprite counts, 0x40
intro-flicker boundary and 0x64 BOSS entry transition are now explicit
named C++ enumerators, and the hit flag is naturally tested as truth.
The original BOSS intro/explosion dispatch uses its actual existing
Rikako mode enum, not duplicated magic byte values. The bit test for
odd intro flicker frames is naturally written as
`round_or_result_frame & 1` while retaining the original unsigned
16-bit frame comparison and effect/render ordering.

Actual changed-source **two-round native original Turbo C++ 4.02 / full
normal MAIN TLINK** proof:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af726d --units ba_rikak
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af726d

Both rounds reproduce **all 1,677 original CODE bytes, all 215 literal
ordered original FIXUPP fields and all 8 PUBLIC offsets**, original
segment definitions, complete full normal MAIN EXE and normalized MAP,
Japanese 124,642-byte loaded program and 1,553 ordered MZ relocations.
The separately reviewed standard MZ serializer matches every byte of
the original 130,882-byte Japanese MAIN.EXE. Only `ba_rikak` was rebuilt;
all 98 other original objects and original CRT reused, no cold replay.

### Negative original TC4 codegen controls

- `af726a` proved that just the two signed-positive-index `& 3` changes
  already matched original codegen.
- `af726b` additionally substituted prefix `++boss_spin_delta` and
  `--boss_spin_delta` for the original **mutable signed-byte** postfix
  mutations: it changed original CODE and failed. `af726c` reverted only
  these global byte mutations, retaining the simplified Boolean mask,
  and passed again. These byte-memory increment encodings must stay postfix.
- `af726e` retested the earlier historical hypothesis about original
  intro `angle = (0 - angle)` by trying natural `angle = -angle` against
  the freshly modified complete BOSS. It again **failed** CODE equality;
  the exact original two-operand subtraction expression was restored.

Failures are retained under their own ignored compiler trial stages;
none were confused with an accepted original match. The final maintained
source is the exactly reviewed `af726d` snapshot, unchanged after
restoring the failed unary-negation trial.

Proof: `.analysis/work/exatt-layout-af726d/report.json` SHA-256
`a8d269c99a3f1e90e74f33235173f59e43cbbe5d569d7819d040c240825bc2e0`.
The complete compiler object, source COMENT dependencies, original and
new linker responses, writer logs, independent full EXE/MAP/MZ results
and native reviewers are retained. These are **existing source-owned
original bytes**, not new canonical Factory packed-file credits,
historical vendor raw OMF packet identity or whole-product acceptance.
