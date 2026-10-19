# Central round-loop experiment: reproduction and retention

The maintained experimental source is byte-identical to the final reviewed
helper experiment:

- src/main/round/round_loop.cpp:
  18dcaf6e1ad0068aa04ea4654192953374e5ef8551239a841318701cd2d56035
- src/main/round/round_loop.hpp:
  dff1d902226f6c0536d65e7b3d7441f19b231a922e8391819a982d7408a8bb31

These are source-present research, not accepted exact owners. The source body
has four explicit loop returns, but the compiler still folds two exits into one.
Do not count the emitted helper as an additional exact function.

## Retained experiments

Keep these complete private receipt trees intact:

1. .analysis/gpt-dots-round-loop-source-v01/probe-v01/compile-first-v01
2. .analysis/gpt-dots-round-loop-source-v02/probe-v01/compile-first-v02
3. .analysis/gpt-dots-round-loop-helper-source-v01/probe-v01/compile-first-v01

Their receipt/object hashes, actual CODE sizes and limits are recorded in
MAIN_ROUND_LOOP_SOURCE_EVIDENCE.json. Preserve the original driver controls,
frozen source, compiler logs, reference archives and fresh OMF outputs. Do not
overwrite receipts or refresh old control pins to conceal a changed HEAD.

## Bounded reproduction recipe

1. Read AGENTS.md, the local th03-re skill and reconstruction workflow. Use
   TH03 Factory only. Run preflight and a fresh read-only th03-main attestation.
   Verify target SHA f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.
2. Verify the two source hashes above and pinned reference revision
   b6ba5b0a529edbb31efdf8c0e939263804f8ee47. Reference is corroboration/scaffold,
   not immutable target authority or proof of original source ownership.
3. Review the retained driver:
   .analysis/gpt-dots-round-loop-helper-source-v01/probe-v01/probe_compile_round_loop.py
   SHA 6e12ac77c0faf61ebd320142fdf3223dacb3d8ab7c131bb9e5fdefc336f33267.
   Its 37 mock-only controls passed before the one native experiment.
4. For an authorized new run, copy the reviewed driver to a normal sibling
   ignored layout, preserve its ROOT derivation, stage the maintained source and
   source-specific header, and independently refresh explained HEAD/content/mode
   guards. Use a NEW run ID. Reserve one native writer. Never silently reuse an
   object from a previous run.
5. Fixed flags are -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M'.
   The driver uses one CPU/nice10, at most 120 seconds (default90), a game-local
   Wine prefix and identity-bound cleanup of only its owned processes.
6. Require exact public identities as a set: _round_loop and
   ROUND_SCORE_STORE_WINNER. Offset-sorted order must be loop then helper in
   the same MAIN_01_TEXT/MAIN_01 CODE contribution, with no DATA/BSS/common
   allocation. Total933 and individual862/71 are target diagnostics, not size
   gates. No artificial gap is inserted into the packed object.
7. Decode complete bodies, real fixups and all returns. Compare all bytes and
   original ordered relocations only after legitimate full-link integration;
   excluding operands/branches never establishes exactness.

The already-tested local-helper ownership hypothesis was negative. A repeat is
not a reason for source permutations, fake aliases, empty inline barriers,
volatile side effects, assembly returns, output patching or compiler-flag sweeps.
A new experiment requires a new target-supported hypothesis. Original physical
ownership, outside-scope preservation and complete cold-link acceptance remain
open. No accepted manifest, exact ledger or aggregate count changes belong to
this checkpoint.
