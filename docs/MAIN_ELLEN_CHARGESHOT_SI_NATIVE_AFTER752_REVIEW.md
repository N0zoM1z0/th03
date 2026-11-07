# TH03 MAIN Ellen charged-shot controller: natural SI/DI sprite renderer and full source-native ABI

The maintained `src/main/player/chargeshot_ellen.cpp` is the **complete
original physical `cs_ellen` Turbo C++ translation unit**, containing
**ten original PUBLIC functions**: all 64-slot reset and both 32-slot
spawn/Hyper allocators, the substantial deceleration-to-target homing
state update, sprite renderer, collision check, entire Gauge pattern
with mirrored projectile volleys, and Gauge pellet/bullet dispatchers.
The original object has **1,530 initialized CODE bytes, 169 literal
ordered OMF FIXUPP fields and 10 PUBLICs**. Existing original 12-byte
near projectile storage and 16-bit signed/subpixel semantics are intact.

## C++ recovery tested against real source-native compiler output

The reset, Hyper, update, collision and render loops now use natural
signed local prefix `++i` without altering their near pointer postfix
mutations, original 8-bit state and length decrements, or the first-active
scan. The original active/free checks and final length-zero test are
expressed as normal Boolean conditions. The implementation also replaces
an old manually assigned `_SI`/`_DI` sprite-coordinate sequence and
manual `_AX` arithmetic with ordinary C++:

    register screen_x_t left = x.v;
    register screen_y_t top = y.v;
    left = playfield_fg_x_to_screen(left, pid_current) - 8;
    top = (top >> 4) + 8;
    sprite16_put(left, top, sprite_offset);

The original **declaration order is essential**: TC4 naturally allocates
SI and DI to those two register locals in that order and generates the
original exact machine instructions. The original byte-angle sprite cel,
linked sprite-call ABI, random draws, counter mutations and Gauge
row/column fire ordering remain unchanged.

Original TC4 experiments were actually run. The modified source reached
full original object/full normal MAIN equality in earlier `af752b/c`
trials. `af752d` attempted changing the order of those register locals;
it **failed** the original CODE comparison, so this source shortcut was
rejected. The final live product source restores the original-native
allocation and explains that constraint. Its fresh **two independent
genuine Turbo C++ 4.02 compiler/full normal TLINK** rounds were validated
at `af752e`, not inferred from earlier changed-source receipts:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af752e --units cs_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af752e

Both rounds exactly reproduce all **1,530 original CODE bytes, 169 ordered
native OMF FIXUPP fields, 10 PUBLIC offsets**, original segment/group
metadata and actual current-source compiler COMENT dependencies. The
full original normal MAIN EXE/MAP, original Japanese 124,642-byte loaded
program and all 1,553 ordered MZ relocations match; independent standard
MZ serialization reproduces every byte of original Japanese 130,882-byte
MAIN.EXE. Only `cs_ellen` was rebuilt; 98 other original project objects
and original CRT were reused, with **no whole-game cold replay**.

Exact original-source current receipt:
`.analysis/work/exatt-layout-af752e/report.json`, SHA-256
`f5191546579912798fc7571135d461aaa77c0ea52fe859811396ca1730aeda2d`.
Actual source snapshots, compiler/OMF/OBJ output, complete linker response,
EXE/MAP, native writer logs and the rejected `af752d` experiment are
retained unmodified. This is natural C++ source fidelity of existing
original-owned CODE, **not** new Factory canonical accepted packed-game
byte credit, historical vendor raw OMF packet identity or complete
whole-product source reconstruction.
