# MAIN CPU targeting/evade update native C++ source after646

This is a new source-rooted compiler proof **outside** the previous
28 BOSS/Extra Attack/Enemy owner overlay. The full physical original
`p_cpu` compiler object contains all four CPU functions: collision
direction lookup, approaching an enemy target, the careful/approach
mode selector, and the large `player_cpu_dodge_and_aim` collision
scan with up to nine retries.

The v2 native scoped driver now supports the *actual* historical
`src/main/player/producers/cpu_native.cpp` wrapper, physical original
`p_cpu` TLINK slot and retained after596 source-native compiler path.
The real Borland OMF dependency COMMENT must identify the explicitly
staged **current modified** `cpu.cpp`, not the old copy under
`TH03WORK/src`. The original unmodified source control `af646a`
compiled the full object and reproduced MAIN in two native rounds.

Actual source recoveries:

- The long careful-mode collision scan uses a natural
  `round_or_result_frame % 4 == 0` clock check, instead of the
  original `round_or_result_frame & 3`. Turbo C++ 4.02 lowers this
  unsigned power-of-two modulo to the exact original instructions
  (`af646b`).
- The approach-target branch's one-in-four RNG bomb decision uses
  `randring1_next16() % 4 == 0`, retaining **the same actual
  random-number consumption** and comparison short-circuit. The
  original `randring1_next16() & 3` and this expression produced
  identical original CODE (`af646c`).
- The full nine-entry 3x3 direction lookup now names each row/column
  explicitly: collision **above/near/below** and player X
  **right/middle/left**. The separate three retry columns are named
  and preserved in the original nested short-circuit ternary.
  The whole compiled controller remains original-equal
  (`af646d`).

A deliberately tested `af646e` candidate simplified the signed
8-bit collision-radius loop by declaring otherwise equal-valued
enum constants for start/end/step. That **changed original native
CODE**. The final code retains the historical `64 / 2`,
`160 / 2`, and `32 / 2` expressions and their signed int8_t
loop variable. The negative result is recorded in its source comment,
without claiming that the enum version was an accepted equivalent.

The accepted full-source proof is the independently two-round
original Turbo C++ 4.02/TLINK stage:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af646f --units p_cpu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af646f

Both new physical CPU objects reproduce all **1,077 original CODE
bytes, 64 literal ordered OMF FIXUPP fields, 4 PUBLIC offsets**,
all original segment/ABI metadata and normalized complete MAPs.
Both linked normal MAIN executables reproduce the retained original
source-native parent, the full Japanese 124,642-byte loaded program,
1,553 ordered MZ relocations and independently serialized original
130,882-byte Japanese MAIN.EXE.

Retained real compiler/linker logs, source snapshots, OBJ/EXE/MAP and
response files:
`.analysis/work/exatt-layout-af646f/report.json`,
SHA-256 `d640aef37531ae1280c68756c5f4eb7170de48ac46c8d2f84b9d03b696b523b4`.
Only the one affected physical CPU object was compiled twice;
the other 98 original project objects, startup and CRT libraries
were reused. No full project cold replay or target/object patching.

The new result improves faithful C++ expression and extends the
currently source-attested compiler coverage by a separate object;
the already owned 1,077 original bytes are **not** counted again.
Raw historical vendor OMF packet equality, canonical packed-file
Factory credit and real PC-98 runtime behavior remain unproven.
