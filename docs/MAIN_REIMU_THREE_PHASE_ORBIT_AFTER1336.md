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

## 2026-11-11: source-exact Reimu windows and stable-ring cadence

Reimu's large spread controller now expresses the first two firing windows
with their own direct off-cadence returns; the narrow two-volley pattern
and medium five-way volley remain tied to the global 16-frame clock. In
the stable-radius phase of `reimu_pattern_orbit_burst()`, each frame still
recomputes all original orbit coordinates and advances the byte angle,
while a positive `round_frame_mod16 == 0` condition controls the random
ring release. No RNG is consumed on off-cadence frames. The cloud BOSS
pattern also uses explicit zero-remainder gates for its variable launch
interval and two-frame byte-speed increment. The original unsigned word
modulo and signed polar math are unchanged.

Individual whole-owner native trials `af1352a` (narrow window),
`af1352b` (orbit maintenance), `af1352c` (cloud zero remainder) and
`af1352f` (medium window) all reproduced the original. A negative
`af1352d` trial inverted and lifted the mirrored spread terminal
condition; it retained the same **2,020-byte total CODE length** but
changed 62 actual code byte locations. The original mirror branch layout
was restored rather than accepting merely equal length.

Current source-rooted `af1352h` compiles the complete **2,020-byte** Reimu
BOSS object twice in the original TC4 and reproduces all **270 ordered
native fields, nine PUBLICs**, both normal Japanese MAIN links and the
ordered MZ relocations. Joint current-source `af1352g` rebuilds Reimu
and the independently owned VSYNC frame-delay leaf together (**2,041
CODE bytes, 272 fields, ten PUBLICs**) with exact normal links.

Reimu receipt: `.analysis/work/exatt-layout-af1352h/report.json`, SHA-256
`bb173522c5f977217f5a3d588c79c9b0c76ac8427892940acf2c39c5bd275ce3`.
Joint receipt: `.analysis/work/exatt-layout-af1352g/report.json`, SHA-256
`5fb6bb72198312554484112c9a1528d3e9a61d2688ab5c56949603c2c80cefb1`.
