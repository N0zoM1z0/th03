# Reimu BOSS: exact three-phase orbit and synchronized spreads

The maintained full Reimu BOSS `src/main/boss/reimu.cpp` now expresses
orbit-burst expansion, stable-radius emission and final Extra Attack
release as mutually exclusive `if/else if` phases, not independent
conditions separated by redundant returns. This preserves all three
original signed 16-bit `i * 256 / orbit_count` angle calculations,
byte-angle wrap, `polar()` sampling and the final Extra Attack call
order. Reimu's cloud orbit now commits mode completion through a
positive terminal-frame gate *after* its center and speed changes.

The two spread windows emit only on the original 16-frame global cadence
using a positive zero-remainder condition. The mirrored spread likewise
retains its unchanged two bullet calls until the 0x80 terminal frame,
when it alone resets the controller. All BOSS level-derived parameters,
original RNG draws and body-level register allocation remain untouched.

Positive original TC4/TLINK native trials `af1336a` (cloud exit),
`af1336b` (mirror exit), `af1336c` (medium spread), `af1336d`
(three orbit phases), `af1336e`/`af1336f` (unneeded final phase returns),
`af1336g`/`af1336h` (two positive volley gates) each matched the
complete BOSS owner. Final current-source `af1336i` reconstructed the
entire **2,020 initialized CODE bytes, 270 ordered native OMF fields
and nine PUBLICs**, in two independent rounds. Joint `af1336j`
recompiled Reimu, Bullet and the two shared BOSS objects: **5,654
CODE bytes, 572 ordered fields, 37 PUBLICs** matched the complete
Japanese MAIN image, normalized MAP and MZ relocation vector in both
normal links, without any whole-source cold build.

Read-only current-source check:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1336i af1336j
```

These are source-bound physical native scopes, not newly owned CODE
bytes or canonical Factory Oracle packed-file acceptance.
