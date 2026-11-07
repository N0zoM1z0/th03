# TH03 MAIN after876 — original PC-98 VRAM shutdown leaf and register effects

The complete original `exit` Turbo C++ 4.02 physical SHARED translation
unit contains one **67-CODE-byte `void far __cdecl game_exit()`**.
It closes the original archive, selects display page one before one
clear, selects page zero before another clear, **selects display page
zero again**, then switches access page zero, ending with the original
VSYNC, memory, text, joystick and EGC shutdown sequence. The real
PC-98 DX ports are **0xA6** for display and **0xA4** for access; these
are separate hardware registers, not ordinary host-memory variables.

The current maintained C++ names the actual one-byte display page one
and zero values as compile-time enumerators while preserving all four
physical `out dx, al` instructions and every original `_DX`/`_AL`
assignment. It also uses actual TC4-compatible file-scope `typedef
char[...]` declarations to check the original **16-bit unsigned port
word** and **8-bit page value**, without allocating new DATA/BSS or
adding code. No C++ hardware abstraction or erased repeated OUT can
be assumed to be original-native without a real compiler test.

## Genuine original compiler experiments and rejected cleanup

- `af876a`: both physical page values became meaningful C++ constants,
  and the entire original unit and full normal MAIN TLINK matched
  in two independent genuine original TC4 rounds.
- `af876b`: treated the **third repeated page-zero selection** as
  redundant, removing its original DX/AL assignments but retaining the
  `out` instruction. The genuine compiler emitted **62** CODE bytes
  instead of the original **67**, first mismatch CODE offset 30.
  Those two register writes were restored. Removing them is not an
  original-exact 'optimization' and might also change actual hardware
  behavior after a graphics library call.
- `af876c`: replaced the direct `_AL = PAGE_1` with a local C++
  `const unsigned char display_front = PAGE_1; _AL = display_front;`.
  This changed TC4 register/stack code generation to **72** initialized
  CODE bytes; the direct enum-valued hardware assignment was restored.
- Final `af876d`: preserves the four real OUTs, all original DX/AL
  operations and the natural page enums, with source comments and
  legacy compile-time width checks. Both independent original compiler
  and complete normal MAIN TLINK rounds were byte-exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af876d --units exit
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af876d
```

Both actual original TC4 and normal MAIN TLINK rounds reproduce all
**67 original CODE bytes, 8 literal ordered native OMF FIXUPP fields,
one PUBLIC offset**, original SHARED segment/ABI/source dependencies,
complete normal MAIN EXE and normalized MAP, **124,642 loaded Japanese
program bytes and all 1,553 original MZ relocations**. The independently
reviewed standard DOS MZ writer reproduces all **130,882 original
Japanese MAIN.EXE bytes**, not implying original vendor direct
header-byte serialization. The **98 other original project objects and
Borland CRT were reused**, without full-project cold replay, source
substitution, byte padding or OBJ/target patches.

Protected real compiler/source/OBJ/EXE/MAP two-round proof:
`.analysis/work/exatt-layout-af876d/report.json`, SHA-256
`58c3ff62542496cbc428b3ed385a6f64a462d2b3c6f76be778e227445d906e63`.
This was already a historically source-owned original leaf. Its
improved native C++/ABI proof is **not additional distinct original
CODE byte credit, vendor raw OMF packet identity or canonical Factory
packed-file acceptance**.
