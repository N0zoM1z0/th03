# TH03 MAIN Reimu BOSS: full attack/render native C++ recovery (after728)

The **complete 2,020-byte original physical `ba_reimu`** contains the
cloud spiral, two-wave radial spreads, orbit/ring/Extra Attack release,
mirrored spread and the entire BOSS controller/collision dispatcher,
plus the main and eight-sprite entrance renderers. This recovery is not
limited to a small leaf or a synthetic code fragment.

Both renderer paths now use natural low-bit animation expressions:
`anim & 3` for the four-frame sprite cycle, `anim & 1` for the palette
variant, and an ordinary `if(anim & 3)` for the nonzero case. These
operate on the original **unsigned byte** derived from the 16-bit BOSS
frame, keeping the original 4-frame cadence, sprite offsets and
low/upper-byte behavior. The source uses the actual BOSS mode enums for
entry/explosion routing, natural hit/clip/intro-blink truth tests and
named intro finish/flicker frames and sprite counts.

The substantial attack controllers' original unsigned frame gates now
naturally test the byte `round_frame_mod16` as Boolean, the cloud speed
tick uses `!(boss_frame & 1)`, and the mirror volley uses
`boss_frame & 15`. The original BOSS movement, spawn/randring order,
subpixel polar arithmetic, all four radial loops and hitbox handling
remain intact. No attempt was made to remove a known original gameplay
quirk or add defensive behavior.

Both original Turbo C++ 4.02 and full normal TLINK rounds for the
changed full original `ba_reimu` source passed:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af728b --units ba_reimu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af728b

**Every original 2,020 CODE byte, all 270 literal ordered OMF FIXUPP
fields, all 9 PUBLIC offsets and OMF segment declarations** matched in
each fresh native compiler round. Full normal MAIN EXE/normalized MAP,
Japanese 124,642-byte loaded image and all 1,553 original MZ relocations
matched. Independent standard MZ serialization reproduced the entire
130,882-byte Japanese MAIN.EXE. The other 98 original project objects
and original CRT were reused (no cold replay).

An earlier `af728a` native trial already proved the two renderers' mask
expressions exact. The later `af728b` additionally proved the attack
state machine and intro gates. We independently **retested** the previous
historical hypothesis about the mutable global `reimu_cloud_speed++` by
substituting `++reimu_cloud_speed` into the complete currently modified
source (`af728c`). That altered original CODE, so the original postfix
byte mutation was restored. The final live source is again exactly the
independently reviewed `af728b` source. The negative attempt remains
retained, not credited as exact.

Primary proof: `.analysis/work/exatt-layout-af728b/report.json`
SHA-256 `f2774bc5b388169980c640ffdcb7533404ab6bd7ba47bc23cc251a8f2bc5caf1`.
Both real source/writer rounds, compiler OBJ/EXE/MAP, COMENT input evidence,
link responses and independent source reviews are retained. This is
**more natural original C++**, not new canonical Factory packed-file
accepted bytes, old vendor raw OMF packet identity, or completed 99-TU
whole-game source ownership.
