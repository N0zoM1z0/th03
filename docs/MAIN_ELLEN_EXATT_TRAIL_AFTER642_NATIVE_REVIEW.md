# Ellen Extra Attack: seven-point trail motion and native C++ loop recovery (after642)

The original six-function Ellen Extra Attack compiler producer owns
a complete set of per-player slot initialization, paired projectile
creation, the separate Extra Attack initializer, a four-sprite tail
renderer, the **long orbit/clip/collision/history update** and the
batch renderer. The underlying historical memory layout is
not a plain entity: each of the twelve per-player slots is 30 bytes,
with one near entity pointer and seven signed 16-bit X and Y
history coordinates.

The maintained C++ now names this physical policy and checks the
original **30-byte stride and offset +02 X-history / +10 Y-history**
with real 16-bit Turbo C++ compile-time `sizeof`/`offsetof`
assertions. It also names the orbit expansion radius 0xD00,
the 0x18 growth increment, the seven history samples and the
two-step rendering stride. Those are compiler-time constants and
introduce neither new DATA nor extra BSS ownership.

Three source-level loop recoveries compiled to the **identical native
instructions**, despite touching the large update and the renderer:

- The orbit history shift is now `for(j = 6; j > 0; --j)`,
  preserving the critical descending array-copy order.
- Completing a returning flight fills all seven history samples
  via `for(j = 0; j < 7; ++j)`, without moving the call or
  changing the original state transition.
- The render loop's original sample order 6, 4, 2, 0 is
  initialized in its own `for` statement; no history or sprite
  order was reordered.

The independent changed-source TC4 controls `af642a` and
`af642b` established the history shift and flight-fill loops.
The complete phase/slot source `af642c` then passed both genuine
Turbo C++ 4.02 compiler/TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af642c --units ex_ellen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af642c

The compiler-consumed source and original 32-byte entity header are
bound by actual OMF COMENT dependency records. Both rounds reproduce
**all 1,129 original CODE bytes, 79 literal ordered native FIXUPP
fields, six PUBLIC offsets**, complete native segments, full normal
MAIN EXE and normalized complete MAP. The loaded Japanese program,
1,553 ordered original MZ relocations and separately serialized
exact 130,882-byte Japanese MAIN.EXE all agree.

Retained receipt:
`.analysis/work/exatt-layout-af642c/report.json`,
SHA-256 `0caeb839e4fe13884c436d9e363f91661ce2d729001d47e85417a4177a57e497`.
Both original native compiler writer rounds, source overlays,
OBJ/EXE/MAP and linker responses are preserved. Only Ellen's
source owner was recompiled, not the full project.

This improves large-function C++ recovery and source-layout
verifiability over previously owned original CODE. Historic raw
vendor OMF packet equality, canonical packed-file Factory credit
and physical runtime proof are not inferred.
