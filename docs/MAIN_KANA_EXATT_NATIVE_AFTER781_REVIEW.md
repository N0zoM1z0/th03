# TH03 MAIN Kana Extra Attack: eight-slot state machine and native sprite timer — after781

The original complete `ex_kana` Turbo C++ physical source contains
**five functions**: eight-slot normal and special projectile creation,
original sprite animation leaf, the substantial eight-slot accelerating
projectile/bullet generation and collision update, and active-entity
renderer. Its original OMF has **663 initialized CODE bytes, 44 literal
ordered native FIXUPP fields and 5 PUBLICs** in `P_EXATT_TEXT`. All
five functions are checked together as one original physical object,
not independently cherry-picked source fragments.

The maintained game now uses compile-time names for the original
byte-valued free/active/flying states, appearing-end frame 0x1C,
eight original slots and the 16-frame bullet emission interval.
All four signed local slot loops naturally use `++i` while preserving
near-pointer postincrements, original RNG and BOSS player ownership.
Inactive/active entity checks use natural byte truthiness. The original
accelerating bullet type, Y acceleration, special sprite offset, clip,
frame and speed byte-memory postincrements and original collision path
remain identical to the original Japanese code.

## Actual original Turbo C++ compiler experiments

- `af781a`: initial full natural lifecycle and loop recovery matched
  complete original 663-byte CODE and whole normal MAIN link in two
  original compiler rounds.
- `af781b`: attempted to replace the unsigned-byte shot `frame % 16`
  equality with a direct bit mask `frame & 15`. Original CODE changed.
- `af781c`: attempted to combine the sprite animation's
  `(frame / 4) % 4` as `((frame >> 2) & 3)`. Original CODE differed.
- `af781d`: preserved the original `% 4` but changed `/ 4` to `>> 2`;
  still different native CODE. Rejected.
- `af781e`: preserved `/ 4` but changed the resulting `% 4` into a
  direct `& 3` mask; also different original CODE. Rejected.
- `af781f`: the final live source retains the original byte `/4`, `%4`
  and `%16` encodings and the native-exact named state/loop recovery.
  **Both independent original TC4 4.02 compiler/full normal MAIN
  TLINK rounds** matched complete original CODE/OMF/MZ again.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af781f --units ex_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af781f

Both actual native compiler rounds reproduce all **663 original CODE
bytes, 44 literal ordered OMF FIXUPP fields, 5 PUBLIC offsets**, original
segment/ABI metadata and source COMENT dependencies. Both complete
normal 99-object MAIN EXE/normalized MAP, Japanese **124,642-byte
loaded program** and **1,553 original ordered MZ relocations** match;
independent normal DOS MZ serialization reproduces the complete
**130,882-byte Japanese MAIN.EXE**. The 98 other original game objects
and Borland CRT were reused, not cold-recompiled; no binary patching,
NOP padding or synthetic OMF was used.

Final current-source proof:
`.analysis/work/exatt-layout-af781f/report.json`, SHA-256
`adc6b0646000448821e3766f2eb10ca639e85b309506b7ac1e405a60877e0470`.
All failed native writer trees remain preserved as negative experiments;
they are not accepted. This is natural maintainable C++ recovery for
**previously owned original bytes**, not additional canonical Factory
packed-file credit, raw vendor OMF identity or complete game acceptance.
