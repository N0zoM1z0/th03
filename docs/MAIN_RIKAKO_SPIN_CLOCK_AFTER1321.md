# Rikako BOSS: exact independent spin clocks and renderer angles

The complete `ba_rikak` controller now separates its signed spin-delta
limit from the unsigned 16-bit eight-frame cadence in all three attack
families. This retains the original upper/lower bounds, byte mutations,
first-frame RNG consumption and pattern dispatch. The intro renderer also
expresses its early 0x40-frame gate and global odd-frame flicker as
independent tests. Both sprite-loop byte angles now use natural compound
`+=` in their for headers, preserving original 8-bit wrap and register
assignment ordering.

Source-native TC4/TLINK stage `af1321h` reproduced the full 1,677-byte
BOSS object, 215 ordered native fixup fields and eight PUBLICs in two
rounds, including the complete Japanese MAIN image and ordered MZ
relocations. The dependent Bullet-engine join `af1321i` reproduced
4,362 CODE bytes, 411 ordered fields and 28 PUBLICs, again with both
complete normal links exact. Only the affected owners were compiled.

Two rejected trials define the compiler-sensitive boundaries. `af1321d`
replaced the four alternating burst equality tests with a C++ `switch`;
TC4 emitted a jump table and grew the owner to 1,699 CODE bytes and 229
fixup fields. `af1321e` changed the signed spin steering expression into
separate `++`/`--` branches; this shortened CODE to 1,673 bytes. Both were
reverted; the original ordered OR tests and signed ternary remain.

Current scoped check:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1321h
```

## 2026-11-11: signed spin boundaries with explicit independent cadence

All three physical attack families now express their spin steering as
one ordered short-circuit predicate. The orbit spread checks the signed
positive limit before the unsigned-word eight-frame modulo, and only
then increments the signed byte. The entity/pellet family checks its
negative limit before the same clock and decrements. The alternating
burst checks for the neutral spin state before the cadence and retains
the original conditional signed delta `+=` rather than substituting two
separate increment/decrement statements. No frame or RNG draw moves
across the existing mutually exclusive warning/fire/terminal dispatch.

`rikako_render_intro()` now uses a single short-circuit predicate to
suppress its sixteen arrival sprites on odd global frames before its
original flicker deadline. The frame/angle calculations and sprite
emission order remain intact.

Stages `af1352j` (positive/negative spin), `af1352k` (neutral spin) and
`af1352l` (intro flicker) each recompiled the entire BOSS owner in two
independent original TC4 rounds. The final current-source `af1352l`
reproduces **1,677 CODE bytes, 215 ordered native fields, eight PUBLICs**
and both normal Japanese MAIN links and relocations. A separate negative
trial `af1352m` cached the repeated renderer `% 4` in an unsigned local;
TC4 allocated a different temporary and emitted **1,680 CODE bytes**,
so that rewrite was rejected.

The joint source check `af1352n` recompiled Rikako, the Bullet engine,
both shared BOSS objects and Rikako Extra Attack together. Both original
compiler/linker rounds reproduce **6,013 CODE bytes, 563 native fields,
41 PUBLICs** and the full original normal MAIN image and MZ relocations.

Rikako proof: `.analysis/work/exatt-layout-af1352l/report.json`, SHA-256
`4b14c198f019058a67dad79cc8217cbfdb4c47cc3f2741d1f99a33bb0d69f52e`.
Joint proof: `.analysis/work/exatt-layout-af1352n/report.json`, SHA-256
`86f7cafc19d0dd8c919548ea43bcce8c27dae520974ffd9cb9b3304fba6d0e31`.
