# TH03 shared BOSS ring renderer and seven controller helpers: original-native after708

The original shared BOSS producer is physically split into **two**
complete 16-bit Turbo C++ translation units, selected from one
maintained `src/main/boss/shared.cpp`:
`ba_sring` contributes the complete two-ring 16+8-sprite BOSS
explosion renderer, and `ba_srest` the seven shared BOSS
movement, descent, activation, hit-test, next-pattern and
explosion-controller helpers. They together own **949 original
CODE bytes, 106 literal ordered OMF FIXUPP fields, 8 PUBLIC
offsets**. Original 32-byte packed BOSS state layout and
original register/segment copy calling convention remain intact.

Source-level recoveries proven with the genuine original TC4:
- Both sixteen-sprite inner ring and eight-sprite outer ring
  loops naturally use `++i` for the loop index instead of
  postfix `i++`. Their angular step and each original
  call to the sprite renderer stay in original order
  (two-round `af708a`).
- The shared end-of-BOSS explosion update naturally uses
  `if(!boss_mode)` for the zero state, reproducing the
  original unsigned byte comparison in `af708e`.

Three negative controls prevent a false natural-source claim:
- Prefix `++boss_angle` in the sine movement helper changed
  original native CODE (`af708b`).
- Prefix `++boss_pattern_i` in the complex repeat-rejecting
  next-pattern RNG state machine likewise changed original
  machine CODE (`af708c`).
- Shortening two player-specific `pid_current == 1`
  checks into `if(pid_current)` changed CODE in the ring
  renderer (`af708d`).

All original postfix fields and explicit `==1` comparisons
remain in the final physical source. The shared controller's
original inline REP MOVSW BOSS-state copy, fixed 32-byte
packed layout, RNG rejection loop and original far
palette/score call boundaries were preserved.

Final genuine modified-source/packed-template-OMF-COMENT-attested
original Turbo C++ 4.02/full normal MAIN TLINK two-round proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af708f --units ba_sring,ba_srest
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af708f

Both native compiler rounds reproduce **all 949 CODE bytes,
106 literal ordered original FIXUPPs, eight PUBLICs** and
complete original OMF segment definitions. Both full normal
MAIN executables and path-normalized MAPs match the retained
source-native parent. The Japanese loaded image and all 1,553
original ordered MZ relocations agree; independent serialization
reproduces the complete original 130,882-byte Japanese MAIN.EXE.

Retained source, compiler/OBJ/MAP/EXE and writer receipt:
`.analysis/work/exatt-layout-af708f/report.json`.
Only the two affected complete original physical shared-BOSS
producers were compiled twice, reusing the other 97 original
project objects and CRT. No full cold replay, target-object
patching or new canonical Factory packed-game CODE credit.
