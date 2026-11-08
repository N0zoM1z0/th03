# MAINL root controller: named story outcomes, win timing and shot extension

The maintained `src/mainl/root/complete_data.cpp` is the complete original
**11-function `rootdata` controller**, not a small wrapper. This source pass
names the story-dispatch return protocol and its three terminal story-stage
values, then uses those result names in the large `main()` controller. The
six measure/tick values in `mainl_win_animate()` now have named timing
constants; the repeated decimal-character threshold is named and shared by
the stage intro, story path and shot loader. The small `mainl_shot_pair()`
leaf names the two original filename-extension bytes (`e`, `x`). These are
compile-time C++ values; no new initialized DATA, BSS or callbacks are added.

The original entry's inline `cmp outcome, 4 / je story_cutscene` is retained.
The natural `if(outcome == 4) goto story_cutscene` candidate in `af940r`
compiled as an inverted conditional plus an unconditional jump, adding two
CODE bytes. A switch/goto alternative in `af941r` also failed the complete
object comparison. No source or original assembler bytes were patched to
force equality. The original branch remains explicit until a natural form
can produce the same short conditional jump.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/build_th03_mainl_root_native_probe.py --stage af944r
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_mainl_root_native_probe.py --stage af944r
```

Two independent genuine original Turbo C++ 4.02 rounds rebuilt the entire
original root object: **2,458 CODE bytes, 112 initialized DATA bytes,
186 BSS bytes, 278 literal ordered OMF FIXUPP fields and all 17 original
PUBLICs** (11 CODE, 3 DATA and 3 BSS). Both complete normal MAINL links
reproduce the **67,372-byte Japanese decoded MAINL EXE** and all **677
ordered MZ relocations**. The other **35 original game objects and original
C0/CRT** were reused; no full cold replay.

The source-current report is
`.analysis/work/mainl-root-af944r-native-build.json`, SHA-256
`fc78af376962b40134ec5005658d2b4de6a557bfe827a544e7fd93c2a0151c96`.
The new stage-specific driver/reviewer bind the actual maintained source and
producer wrapper. They intentionally do not compare the edited source to
the stale pre-edit `WORK/rootdata.cpp` copy embedded in the historical
`after580` recipe; all original target, object, parent-link, ABI and native
output checks remain in force. The unchanged-source baseline `af942r`
also passed, confirming the new driver before source edits.

The older `after580` receipt is retained as authentic historical source
snapshot evidence, not current source binding. This scoped normal-link proof
does not change decoded MAINL accepted units (still 0/259), canonical Factory
acceptance, vendor raw OMF packet identity or whole-product source ownership.
