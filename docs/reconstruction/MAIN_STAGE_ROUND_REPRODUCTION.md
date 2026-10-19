# Experimental stage/round source: reproduction and status

This checkpoint preserves three complete natural functions in
`src/main/round/stage_round.cpp` and the near initializer declaration in
`src/main/round/initialize.hpp`. This is source-present research with **zero
exactness credit**. It is not integrated into the accepted build or exactness
manifests. Shared historical compiler ownership remains unproved: the combined
source is an experimental grouping, not a proved original TU boundary.

The source is byte-for-byte the explicit-a2 combined-v02 candidate. Complete
function bodies, record assertions and ordinary switches are preserved. No
fake definitions or DATA/BSS allocation have been added to resolve externals.
`MAIN_STAGE_ROUND_BINDINGS_PROPOSAL.json` records stage-side existing
storage/callee mappings; it is not completed linker integration. Additional
initializer bindings remain documented in source and the retained initializer
v04 ABI review. Original allocation ownership and all linked values are open.

See `MAIN_STAGE_ROUND_SOURCE_RESEARCH.md` for the five experiments and preserved
failures. `MAIN_STAGE_ROUND_SOURCE_EVIDENCE.json` pins their original receipts,
objects, compiler commands, source hashes and guard outcomes. The latest native
CODE is 1807 versus the target1808, with the stage-table zero still missing.
Do not update accepted byte counts or exact ledgers from this source checkpoint.

## Reproduction recipe

1. Read repository AGENTS, local th03-re skill and workflow. Run preflight and
   selected th03-main database attestation. Pin config/toolchain.toml and
   reference revision b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
2. Verify src/main/round/stage_round.cpp SHA-256:
   ccbb5c845c0b1c8d187eccf2db261283a2a64dc904a9653da7269cbdfb05e699.
   Packed historical header imports precede explicit -a2. Retain all ABI
   assertions and natural branches/tables.
3. Retained compile-only driver/profile:
   .analysis/gpt-dots-stage-round-owner-source-v02/probe-v01/probe_compile_stage_round.py
   SHA-256 fd5f8d1a8c5c6eb35de84353ad6899891428602bfbffea732696e2823f3bd3e6.
   Native flags: -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M'.
   This private retained driver freezes source/control inputs, verifies tools,
   uses oneCPU/nice10 and a bounded timeout, and checks a fresh OMF contribution
   without added DATA/BSS. Its 38 mock-only controls passed. It is a retained
   experiment artifact, not a newly versioned general-purpose build script.
4. The original receipt must not be overwritten:
   .analysis/gpt-dots-stage-round-owner-source-v02/probe-v01/compile-first-v02/receipt.json
   SHA-256 06042fb3716402e60e5a8eaf5b3bb034e2aea301d3ab462077592a1ebf083a6e.
   To repeat after this checkpoint, first independently review and refresh a
   copied driver's HEAD/source controls for the explained source-preservation
   change, stage the maintained source/header, choose a NEW run ID, and reserve
   one exclusive native writer. Old pins must fail against changed HEAD;
   never refresh them merely to suppress unexplained drift.
5. Compare complete natural CODE, real OMF fixups/tables and original ordered
   MZ relocations without patching output or excluding operands from an
   exactness assertion. Historical source/object/physical ownership, all
   original DATA/BSS bindings and reproducible cold-link Oracles remain open.

No binaries, generated objects, archives, tools or reference trees are part of
this source checkpoint. Historical failed receipts remain intact. Public
checkouts without private targets/tools can inspect source/docs and run the
portable repository tests, but cannot independently rerun private native
experiments until those separately attested inputs are supplied.
