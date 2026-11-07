# TH03 MAIN after849: whole Combo HUD, score and BOSS/panic helpers

The maintained `src/main/player/combo.cpp` owns **two distinct original
Turbo C++ physical TUs**: `p_combo` (491 CODE, 17 ordered FIXUPPs,
2 PUBLICs) holds original **32-bit saturated Combo accumulation** and
both players' HUD score/bonus display; `p_cmbhl` (487 CODE, 40 ordered
FIXUPPs, 3 PUBLICs) owns the charged-fireball helper, BOSS launch and
Panic routes. They must retain separate original linker slots.

The four-frame blink in the substantial `combos_update_and_render()` is
now written as natural **unsigned 16-bit `% COMBO_FLASH_PERIOD`**, while
the independent render predicates remain the target's **bitwise `&`**,
not C++ `&&`. The source also gives a single meaningful decimal radix
to the two-digit HUD's tens test, tens division and remainder, without
widening the original byte-lifetime local or changing its overflow.
The original 80-frame Combo display, 32-frame reset, 99-hit visible
cap, full 8-bit defeat-screen hit maximum and 32-bit score saturation
remain separate behaviors.

## Original codegen experiments (new, actually compiled)

- `af849a`: unsigned word-clock `%4` passed original TC4/full MAIN
  TLINK twice, whole original physical `p_combo` and `p_cmbhl` exact.
- `af849b`: an alternative complete Combo HUD `while`-traversal also
  compiled byte-exact, but the original more readable `for` loop was
  retained in the final maintained source.
- `af849c`: collapsing the **32-bit** Combo bonus cap into a ternary
  assignment generated 493 initialized `p_combo` CODE bytes, rather
  than the real original 491. The original separate branch/word stores
  remain, as does the two-stage widened bonus accumulator.
- `af849d`: moving the near-pointer initialization into the `for` header
  kept the 491-byte length but **changed CODE bytes and instruction
  addresses**. Pointer initialization remains before the loop.
- `af849e`: introduced the common decimal radix and passed full
  original CODE/FIXUPP/PUBLIC and native MAIN linking in both rounds.
- `af849f`: replacing the near-segment explicit original
  `NOP; PUSH CS; CALL near fireballs_add` with an apparently ordinary
  C++ `fireballs_add()` call changed `p_cmbhl` bytes. Genuine TC4 emits
  **`9A` far CALL** instead of the original near-return-compatible
  **`90 0E E8`** sequence. The original ABI carrier was restored.
- Final `af849g`: actual current source with the accepted natural C++
  improvements and compiler/ABI notes, original dual compiler/normal
  MAIN linker rounds again match byte-for-byte.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af849g --units p_combo,p_cmbhl
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af849g
```

Both original TC4 4.02 compiler and normal TLINK rounds match **all
978 CODE bytes, 57 literal ordered OMF FIXUPP fields, five PUBLICs**,
original source/segment/ABI and full original normal MAIN EXE/MAP,
all **124,642 Japanese loaded bytes and 1,553 original MZ relocations**.
Independent standard DOS MZ serialization matches all **130,882 bytes**
of the original Japanese MAIN.EXE. **97 other original project objects
and CRT are reused unchanged**; no full cold replay, byte padding,
target substitution or old receipt modification.

Protected original-source-bound report:
`.analysis/work/exatt-layout-af849g/report.json`, SHA-256
`8593bad3f24e55c5486a1643bb09a4d4ffd98f8f966eb4346849c55fd23a802b`.
This is a new current-source native verification of historically covered
original CODE, **not** newly distinct bytes, raw vendor OMF packet identity
or canonical Factory packed-file acceptance.
