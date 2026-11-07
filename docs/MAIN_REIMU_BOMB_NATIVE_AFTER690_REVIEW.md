# Complete Reimu Bomb/shared lifecycle: 925 original-native CODE bytes (after690)

The original `bm_reish` physical Turbo C++ source is
a complete **four-function** producer: shared non-Reimu
Bomb lifecycle, Reimu particle update, particle renderer
and the long Reimu GRCG/flash/shake/fade controller.
The original 925-CODE-byte unchanged-source control
`af688a` was compiled alongside the actual Mima/Marisa
Bomb owners before any edits, preserving the historical
native MAIN parent and original source dependencies.

Natural maintained C++ changes:

- The initial red palette ramp `frame << 2` is
  `frame * 4`; the terminal signed-byte fade
  `255-(frame<<3)` is `255-(frame*8)`
  (native proof `af690a`).
- Both odd-frame sound and alternating 80-level palette
  flash now use `static_cast<unsigned int>(frame)%2`
  instead of hand `frame&1` masks. Full physical
  object remains original equal (`af690b`).
- The long 32-slot particle update and private renderer
  use natural `if(!particle->active)` and
  `++i` for each original loop. Full original
  16-bit branch/stack layout is unchanged (`af690c`).
- TC4 now checks the actual 8-byte original particle
  stride and physical +02 X, +04 Y and +06 vertical
  velocity offsets through `sizeof` and `offsetof`.
  Source compiler-time names preserve the 32-slot
  pool/player and real 32/64/96/112 frame phases.

The original collision/particle behavior is deliberately
not sanitized: inactive slots are skipped without
compacting the array; active particles wrap Y to 384
pixels and increment signed vertical velocity. The
hardware helper's input BX value, far Pascal MRS
zero-extended argument and original signed Y
arithmetic shift remain untouched.

Final original source/OMF-COMENT-attested TC4.02/TLINK
two independent compiler rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af690e --units bm_reish
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af690e

Both native objects reproduce **all 925 CODE bytes,
104 ordered literal FIXUPPs, four PUBLIC offsets**,
entire original OMF segments, complete normal MAIN
EXE and path-normalized MAP, Japanese loaded program,
1,553 original ordered MZ relocations and independent
exact 130,882-byte original Japanese MAIN.EXE.

Retained native source/compiler evidence:
`.analysis/work/exatt-layout-af690e/report.json`,
SHA-256 `268a9ed2ad48310d5804a3723ab099c251483bf891b6a3ed7c27e70a1f2a6413`.
Only this one entire physical original project object was
freshly compiled twice. Other 98 original project
objects and libraries were reused: no full cold replay.

All bytes were already source-owned; this is natural
C++ and original layout recovery, not new canonical
Factory packed-file credit or historical raw OMF
packet-byte identity.
