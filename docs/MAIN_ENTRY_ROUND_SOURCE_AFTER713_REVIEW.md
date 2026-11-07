# TH03 MAIN large entry / round-loop source-native binding — after713

The game entry, 200+-line full per-frame round scheduler, stage preparation
and result/score-commit logic are one **3,050-byte complete original physical
TC4 translation unit**, `entry`. It is NOT a collection of arbitrarily
split leaf functions. The existing after594 original native entry proof is
historical; the current live source graph requires separately checked
compiler-consumed input provenance.

The scoped source-native overlay driver now accepts `entry`, including the
original after594 TLINK slot and four separately staged **real** implementation
files under the maintained `src/` tree:

- `src/main/core/entry.inl` — main entry and OP/MAINL transition
- `src/main/round/round_loop.inl` — original per-frame update/render,
  result/next-round routing, CPU speed/RNG cadence
- `src/main/round/stage_round.inl` — stage setup and reset logic
- `src/main/core/roundfin.inl` — score commit

The driver rewrites all four include paths to per-round private copies,
SHA-pins every current implementation, and requires actual TC4 OMF COMENT
records naming all five overridden source files. This closes the specific
stale-source include loophole that invalidated early v1 scoped proofs.

The code now expresses the **three distinct original round outcomes** as a
single natural C++ enum shared by `main()` and `round_loop()` without merging
its distinct branch/return sites: `0` returns to OP, `1` starts the next
round, `2` transitions to the ending. The frame scheduler names its 160-frame
background transition, two-win match gate, maximum speed, 64-frame speed-up,
1024-frame RNG refresh and 2000-frame CPU reset window. Natural boolean tests
on `round_quit_requested` and `stage_render_timing_flag` preserve exact
original native codegen. The original hardware I/O and important labelled
control-flow structure are intentionally not simplified.

The unchanged source control was separately validated at `af713a` to verify
new driver mapping. A first changed-source `af713b` failed at compile time
because `ROUND_SPEED_MAX` already existed in a header; it is retained as a
negative/incomplete native trial, **not proof**. The corrected live source
passed **both** independent real original TC4 4.02 compiler/full normal MAIN
TLINK rounds:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af713c --units entry
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af713c

Original `entry` CODE **3,050 bytes**, literal ordered OMF FIXUPP **433**,
PUBLIC **8**, segment definitions, full normal MAIN/MAP, Japanese original
124,642 loaded program bytes and **1,553 ordered relocations** are exact in
both rounds. Standard MZ serialization reproduces the entire Japanese
130,882-byte file. The other 98 original project objects and original CRT
were **reused**, not rebuilt; no whole cold replay took place.

Retained changed-source proof:
`.analysis/work/exatt-layout-af713c/report.json` SHA-256
`c09fae310fb93e11d0e88f0d31ab59e66d86d1d77adea4c57c224b23726bf05f`
plus both writer rounds, real source snapshots, original object payloads,
complete linker inputs, EXE/MAP, native logs and file-byte checks.

This is an additional *live source-bound scope in the current focused
verification workflow*, not additional original bytes or a fresh Factory
packed-unit acceptance. The older after594 historical proof already covered
this physical owner; do not increase cumulative distinct-owner counts without
independently deduplicating all retained source proofs.
