# TH03 MAIN Ellen Chargeshot: genuine natural SI/DI C++ renderer recovered after752

The maintained `src/main/player/chargeshot_ellen.cpp` owns **ten complete
original physical Turbo C++ functions** in `cs_ellen` (1,530 original
CODE bytes, 169 ordered literal native OMF FIXUPP fields and 10 PUBLICs).
This includes projectile reset/add, the large 32-projectile deceleration
and homing controller, Hyper attack, 16-bit collision scan, GRCG sprite
renderer and upper/side Gauge Attack bullet emitters. The source preserves
the original 12-byte projectile records, 32 slots per player, 16-bit
subpixel geometry, signed angle math and nested source ABI.

## Significant actual source recovery, not a constant-only change

The original `ellen_chargeshot_private(Subpixel x, Subpixel y)` renderer
manually manipulated `_SI`, `_DI`, `_AX`, including a casted `int16_t`
right shift, writeback and eventual `sprite16_put(_SI, _AX, ...)`.
Both source inputs now naturally use **typed C++ `register` locals**:

    register screen_x_t left = x.v;
    register screen_y_t top = y.v;
    ...
    left = playfield_fg_x_to_screen(left, pid_current) - 8;
    top = (top >> 4) + 8;
    sprite16_put(left, top, sprite_offset);

This is a genuine removal of low-level register assignments from the
maintained game source, not an inline replacement with target instruction
bytes. The real original Turbo C++ 4.02 register allocator naturally
uses SI/DI and the original AX signed shift sequence when these local
variables are declared in this precise order. `af752c` compiled this
more readable renderer together with the complete Chargeshot owner and
matched every original physical byte and relocation in two rounds.

The rest of the complete owner now naturally increments six signed
`i` loop counters with prefix `++i`, while preserving pointer postincrements
and mutable byte-memory state. Hyper and active-projectile scanning use
natural nonzero/zero checks, and target selection tests the **unsigned
byte** charge length with natural `if(!length)`. Original transition
order, zero-length vector, palette events, Gauge reload and actual RNG
and player control flow remain unchanged.

## Proven compiler-sensitivity, not guesses

A second independent `af752d` TC4 trial **reversed the order of the two
`register` local declarations**. The entire original CODE no longer
matched because of changed SI/DI register allocation. That natural-looking
alternative was rejected. The final source restored the successful order,
added the register-lifetime explanation, removed unused exploratory
enumerators and was recompiled with exact original output again at `af752e`:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af752e --units cs_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af752e

Both genuine TC4 4.02 compiler/full TLINK rounds reproduce **1,530
CODE bytes, all 169 literal ordered original OMF FIXUPPs, all 10 PUBLIC
locations**, original segment/ABI metadata and compiler-emitted source
COMENT dependencies. Full 99-project-object normal MAIN EXE and MAP,
the original Japanese **124,642-byte loaded program** and **all 1,553
ordered MZ relocation words** match. Independent standard MZ
serialization reproduces all **130,882 bytes of original Japanese
MAIN.EXE**. Only the affected `cs_ellen` was rebuilt; 98 other original
objects and original CRT reused, no cold replay or byte patches.

Current source-bound native proof:
`.analysis/work/exatt-layout-af752e/report.json` SHA-256
`f5191546579912798fc7571135d461aaa77c0ea52fe859811396ca1730aeda2d`.
The failed declaration-order experiment and both accepted source-native
compiler/linker rounds remain preserved. This is substantial maintainable
source-code recovery for already owned original bytes, **not** new
canonical Factory accepted packed-file credit, old vendor OMF raw-packet
identity or completed whole-product source ownership.
