# Large explosion collision/hit chain: original-native C++ after611

This is a **real source-rooted** recovery of the 630-byte
`explosions_hittest()` function in `src/main/enemy/expl.cpp`, not a
review of a cached original build. The function scans the complete effect
pool, intersects hitboxes, increments collision-chain hits with 8-bit
saturation, adjusts scores and gauge charges, and dispatches fireballs
and boss attacks. No collision branch, score order or original unchecked
input behavior is suppressed.

The repaired native builder now forces the actual Turbo C++ 4.02 wrapper
to include `probe/af611g/rN/src/main/enemy/expl.cpp` and verifies that
path in the compiler's own OMF `COMENT` dependencies. An intentionally
invalid source field caused the expected real TC4 error (`af611a`), while
unmodified original source rebuilt byte-exact as a separate control
(`af611c`). This addresses the earlier v1 source-binding flaw.

From that proven baseline, **four incremental true source tests**
recovered natural Turbo C++ without changing the complete original CODE:

- `af611d`: replace the misleading three-statement
  `chain_hits_inc_and_clamp` macro with direct `chains.hits` load,
  saturating increment and store.
- `af611e`: remove macro aliases that reused the `hits` byte and
  `charge_fireball_p` pointer for the separate pellet/fireball charge.
  The original source's shared storage lifetime is preserved explicitly.
- `af611f`: replace the union between a byte and an enum with a single
  clearly typed `uint8_t against2`; keep the original category codes and
  exact byte arithmetic.
- `af611g`: express the radius-then-diameter local union as a single
  `Subpixel extent` with the same lifetime, offset and arithmetic.

Negative control `af611b` additionally demonstrates that introducing two
independent locals instead of reusing the original stack storage changes
the function prologue from `ENTER 0x0e` to `ENTER 0x12` and increases
CODE to 634 bytes. That attractive but incorrect source was rejected,
not passed by altering a receipt.

The actual v2 native command and read-only source-bound verification are:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af611g --units e_expl
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af611g

Both independent genuine source compiler/link rounds exactly reproduce
all **630 original CODE bytes**, 49 ordered native fields, one PUBLIC
function, the original segment layout, the entire normal 99-object
MAIN EXE and normalized MAP, all 1,553 ordered Japanese MZ relocations
and exact file after standard-MZ serialization. Actual consumed-source
OMF dependency, compiler writer logs and all OBJ/EXE/MAP outputs are
retained under `.analysis/work/exatt-layout-af611g/report.json`, SHA-256
`9d3e3a9989ccc347ab6a608dcef1826f7051845d83c1d351923306ee2f72810e`.

`src/main/player/exatt_entity.hpp` changed separately after this
Explosion-only stage; it is **not a compiler input to Explosion**. The
read-only reviewer verifies the retained header snapshot and only demands
live header identity when the compiled TU actually consumed it.

No raw vendor OMF packet identity, new packed Factory acceptance or
physical hardware runtime claim is made, and the 630 bytes already had
historical authored ownership; this is a genuinely verified natural C++
**large collision routine** improvement.
