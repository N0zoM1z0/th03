# MAINL Staff Roll: natural score, verdict and transition C++

The maintained `src/mainl/staff/data.cpp` is the **complete 19-procedure
original `staffdat` owner**, not a small snow-only helper. Its original
Turbo C++ object has **3,695 CODE bytes, 224 initialized DATA bytes, six
DATA PUBLICs and 342 literal ordered OMF FIXUPP fields**. The current
source keeps that entire owner and all six initialized data exports intact.

This source pass gives the large Staff Roll and its smaller rendering and
snow leaves clearer semantic names without changing the original TC4 output:

- `mainl_snow_spawn()` now uses the natural `!flake->alive` byte predicate.
- `mainl_staff_verdict()` names the character, rank, score and skill text
  coordinates instead of repeating screen-layout literals.
- `mainl_staff_roll()` names the score rank digits, rank thresholds, bonus
  amounts and 100-point cap. The original case-3 fallthrough into case 4 is
  retained explicitly. TC4 emitted a shorter, non-original direct-memory
  `ADD` for `skill += ENUM`; the exact source uses
  `skill = skill + ENUM`, which retains the original load/add/store sequence.
- `mainl_staff_leave()`, `mainl_staff_gallery()` and `mainl_staff_pair()` name
  the distinct final transition/dissolve frame boundaries. The fast and
  normal center positions shared by `mainl_staff_single()`, `pair()` and
  `hold()` are now named layout constants. The underlying page selection,
  frame clocks, snow calls and rendering order are unchanged.

The failed `af937s` TC4 experiment is retained. Replacing the final
`mainl_verdict_skill += 15` with a named enum compound assignment caused
**3,692 CODE bytes and 341 OMF fields** instead of the original 3,695/342.
The explicit assignment spelling in `af938s` restored the complete object;
`af942s` is the final source-current round after the additional transition,
layout and score-digit naming.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/build_th03_mainl_staff_native_probe.py --stage af942s
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_mainl_staff_native_probe.py --stage af942s
```

Two independent genuine original Turbo C++ 4.02 compiler rounds rebuilt the
complete `staffdat.obj`; each then ran the complete original normal MAINL
TLINK response with this object in its original slot. Both reproduce all
**3,695 CODE bytes, 224 initialized DATA bytes, 19 CODE PUBLIC functions,
six DATA PUBLIC names, 342 literal ordered FIXUPP fields**, exact segment
geometry and ABI, the full **67,372-byte Japanese decoded MAINL EXE** and
all **677 ordered MZ relocations**. The other **35 original project objects
and the original C0/CRT library were reused**. No full cold replay was run.

Protected native build report:
`.analysis/work/mainl-staff-af942s-native-build.json`, SHA-256
`08d53f8f332aadba836ac13e57bbdb8e4417b584d1f48fdfd09123eac021c1ba`.
The read-only reviewer report is
`.analysis/work/mainl-staff-af942s-native-review.json`.

The stage-specific builder and reviewer preserve fresh source snapshots,
original compiler/linker responses, both objects, complete EXE/MAP outputs
and writer logs. The existing after575 and earlier stages remain immutable
historical snapshots. The cold MAINL source graph still pins the pre-edit
`staff/data.cpp`; a cold-dependent `test_mainl_snow_current` stops at that
stale source hash. That graph and its historical receipt were not rewritten
or refreshed, consistent with the scoped no-cold-replay workflow.

This is a current-source **scoped native object and normal-link result**.
It does not change the current decoded MAINL accepted-unit count (still
0/259), create canonical Factory acceptance, prove raw vendor OMF packet
identity or close whole-product source ownership.
