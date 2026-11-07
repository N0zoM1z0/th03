# TH03 MAIN Yumemi major BOSS timing and natural rain loop — after711

The maintained complete `src/main/boss/yumemi.cpp` reconstructs Yumemi's
substantial BOSS update dispatcher, five attack families and render paths.
This pass defined separate named **attack-specific frame gates**, retaining
strict/inclusive comparisons, original 16-bit timer arithmetic, RNG order,
explicit original sprite interrupt register encoding and the two-stage
arrival coordinate multiplication. The rain attack now uses natural `++i`
for its 12-bullet loop rather than postfix `i++`.

Attack end gates intentionally differ: aimed fire stops on `> 0x60`, cross
and rain reset on `>= 0x60`. The chase attack signals every 16th frame at
remainder 15, not remainder zero. Keeping these distinctions matters more
than normalizing all phases into a convenient common convention.

Native verification uses **only** the changed original physical `ba_yumem`
translation unit, compiled twice by genuine TC4 4.02 and linked into both
normal MAIN images with the other 98 project objects/CRT reused unchanged:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af711b --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af711b

Both rounds passed all **2,358 original CODE bytes**, **343 literal ordered
OMF fixups**, **10 PUBLIC offsets** and segment definitions, original
normal MAIN image/MAP and the Japanese loaded image with all **1,553 ordered
MZ relocations**. Original Japanese file bytes also match through separately
verified standard MZ serialization. The original real source dependency is
bound and checked from the native object (not a stale source copy).

Retained proof: `.analysis/work/exatt-layout-af711b/report.json`, SHA-256
`53c99d9bb98e2ed8d39dde8ac9125aa1302cb7b0c695fe3c95809e9c8f1671a0`,
with both full compiler/linker rounds, object, EXE, MAP, source snapshot and
writer logs. An earlier unmodified-control `af711a` was compiled after an
editing-script assertion stopped before any source change; do not confuse it
with the changed-source proof.

These bytes were already covered by prior source-native proof; this is
**natural-source recovery and a fresh source-bound validation**, not newly
accepted packed-file/canonical Factory credit or a historical vendor-OMF
packet match. Whole-product source ownership is still open.
