# MAIN enemy formation and script VM: natural source control flow, after609

This reconstruction source refresh targets **the full `enemy.cpp`**, not
only the small leaf helper. Its original physical compiler partition consists
of `eforna`, `efornb`, `eupda`, and `eupdb`. The `efornb` source
contains the large `enemy_run()` ENEDAT script interpreter with its
move/stop/circular/sine/loop instruction dispatch; `eforna` contains
`enemy_move_and_clip()` and formation-state routines.

## C++ behavior now expressed directly

- `enemy_move_and_clip()` uses two short-circuit X/Y clipping predicates
  and explicit `EFF_FREE`/early `return true` on either clipping event,
  removing `goto clip`. X coordinates are still updated before Y; the
  mirror flag and two independent integer truncations in speed tuning
  remain exactly as in the original.
- In `enemy_run()`, the **linear**, **ordinary**, **speed-controlled**,
  **circular/plus**, and **sine-axis** movement instruction paths now
  handle clipped enemies with an early `return true`, then continue in
  the ordinary non-clipped path. This removes the inverted
  `if(!enemy_move_and_clip()) ... else ...` nesting without suppressing
  the original duplicate free-flag assignment or stop-at-player logic.
- The `__es` script pointer now adds `enemy.script_ip` in a single
  typed C++ assignment. The same segmented ES register/offset contract
  and the original unbounded script interpreter are preserved.
- Absolute and relative `EO_LOOP` instructions now express the
  taken branch as an early `continue`, then fall through to counter
  reset when the repeat count is reached. **Both original bugs remain**:
  the taken branch updates `enemy.script_ip` without updating `script`
  and advances `script` using the previously selected `op_size`.
  This is faithful source recovery, not a gameplay fix.
- The shared script-duration formula is now one natural signed-int
  arithmetic assignment using `op_duration` directly. The original
  two-division/truncation behavior and speed dependence remain intact.
  Jumps to the shared `wait_and_return` block remain because they
  represent a real common epilogue for many instruction cases.

## Native evidence — not simply a semantic assertion

Incremental scoped compiler experiments independently passed for
`eforna` (early return and flattened clip) and `efornb`
(`af609b` through `af609j`: five movement case rewrites, wait
expression, script pointer and both loop branches). Each candidate
recompiled complete native **CODE, ordered OMF relocations, PUBLIC offsets,
and segment definitions** from Turbo C++ 4.02 and linked the full MAIN
using the retained original 99-object response.

Final combined actual native build/review:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af609k --units eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af609k

Two independent compiler/TLINK rounds prove **all 3,325 original CODE
bytes**, **222 literal ordered native fixup fields** and **19 PUBLICs**,
plus all segment definitions and original source partition boundaries.
Both full linked normal MAIN EXEs and normalized MAPs match the retained
after596 source-native link; the complete Japanese MAIN program and
1,553 original ordered MZ relocations are unchanged. Separate standard
MZ serialization gives the exact 130,882-byte original Japanese MAIN.EXE.

Evidence: `.analysis/work/exatt-layout-af609k/report.json`
(SHA-256 `31d4673593de3724830c1eaf2b166b9faaa945b7409229e91788358637d21fd2`),
with all genuine compiler/linker writer logs, two native OBJ vectors,
full EXE/MAP outputs, original response files and consumed source overlays
retained. No historical receipt or original object/library was repinned
or overwritten. No whole-game cold replay was needed.

These were already counted as original game CODE. The new credit is
**more natural, ABI-accurate maintainable source with unchanged genuine
native output**, not newly accepted packed Factory bytes, original
historical vendor OMF packet identity or physical hardware runtime proof.
