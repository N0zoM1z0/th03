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
