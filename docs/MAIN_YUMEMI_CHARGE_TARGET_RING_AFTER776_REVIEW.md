# TH03 MAIN Yumemi Chargeshot: target acquisition, blooming ring, Gauge — after776

The complete original `cs_yume` physical Turbo C++ translation unit
has **ten functions**, not just a Chargeshot leaf: full `ellen_target_set`
formation/BOSS target acquisition, charged projectile reset/add,
movement/transition/hittest, 16-sprite polar ring renderer, substantial
64-frame multi-ring bloom and eight-entry triangular Gauge attack
controller. Its original physical OMF has **1,645 initialized CODE bytes,
133 literal ordered FIXUPP fields and 10 PUBLIC offsets**. The complete
original source also retains the MAIN_04 `PELLET_PUT` code group relation,
real 16-bit Subpixel and target record layout, and the original
TC4-generated Gauge switch's jump/value table.

Natural maintained C++ now names the byte-valued projectile lifecycle
(inactive 0, flying 1, blooming 2), retains separate frame and collision
phase clocks, uses signed register-index `++i` for the enemy target scan
and the full 16-sprite polar ring, and tests inactive state, BOSS
presence and Gauge active flags with ordinary native-exact Boolean
conditions. The original ring angle initialized as `frame * 2` can now
be expressed naturally as `frame << 1` without changing original TC4
codegen. Its mixed sin/cos coordinates, target lookup priority, selected
formation marker on fallback, bullet/ring/random order and uninitialized
Gauge switch-case behavior are all preserved as in the original game.

## Actual compiler experiments (negative results are not accepted)

- `af776a`: tried replacing the unsigned-byte Gauge launch clock
  `% 8` with a direct `& 7` as well as these natural source changes;
  original CODE shrank by **six bytes** and the full physical object
  failed byte equality. The unchanged code is not falsely accepted.
- `af776b`: reverted just the Gauge byte modulus; the rest of the
  ten-function changed source and original full MAIN link passed both
  original Turbo C++ 4.02 compiler rounds.
- `af776c`: independently changed the 16-sprite ring's angle initializer
  `frame * 2` into `frame << 1`; two actual TC4/full TLINK rounds passed.
- `af776d`: the sound effect's original byte-frame `(frame % 2) == 0`
  was challenged with the natural `!(frame & 1)`. Original compiler CODE
  changed, so this second byte-modulo form remains original.
- `af776e`: complete final current-maintained source, preserving the
  two original modulo encodings and explanatory source comments, was
  compiled **again** with two independent original TC4/TLINK rounds;
  the whole original CODE/OMF/full-Japanese-MAIN proof passed both times.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af776e --units cs_yume
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af776e

Both native rounds reproduce **all 1,645 original CODE bytes, all 133
ordered OMF FIXUPP fields, all 10 PUBLICs**, original segment/group
and emitted source COMENT dependencies. The complete normal MAIN
EXE/normalized MAP, Japanese **124,642-byte loaded program** and all
**1,553 original ordered MZ relocations** match; independent ordinary
MZ serialization reproduces the entire **130,882-byte Japanese MAIN.EXE**.
The other 98 project objects and original CRT are reused, not cold rebuilt.

Proof `.analysis/work/exatt-layout-af776e/report.json`, SHA-256
`94c4113bd8495fc92d460f17906e6056c286dfd14eb5c187e70b719940f54f64`.
Failed experiments have separate retained original compiler writer trees,
not target-byte patches or forced padding. Already owned original CODE
is not new canonical Factory accepted packed-file credit or vendor-raw
OMF packet identity; complete original source ownership remains open.
