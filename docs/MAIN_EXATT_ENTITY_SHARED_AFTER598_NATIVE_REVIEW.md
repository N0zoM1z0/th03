# MAIN Extra Attack shared entity layout: native source refresh after598

The maintained Yumemi (large renderer and updater) and Mima Extra Attack TUs
used to declare separate copies of the same 32-byte entity record also used
by Reimu's shared flight logic. The source now includes the existing
`src/main/player/exatt_entity.hpp` instead. This is a **source ownership /
ABI consistency** improvement, not additional target CODE credit.

The proof is an actual **scoped native build**, not a parse-only check:

- `PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af598v --units ex_yume,ex_mima`
- Two fresh Turbo C++ 4.02 rounds, then two original TLINK rounds using
  the frozen after596 project and replacing only these two OBJ slots.
- **ex_yume:** all 1,696 original CODE bytes, 87 ordered native fields,
  five PUBLIC offsets, and full OMF segment definitions equal the reference.
- **ex_mima:** all 727 original CODE bytes, 44 ordered native fields,
  four PUBLIC offsets, and full OMF segment definitions equal the reference.
- Both normal TLINK EXEs match the retained after596 EXE byte-for-byte;
  the complete MAP equals after596 after normalizing only module source paths.
  Both program images match the Japanese target, with all **1,553 ordered
  relocations**. The separate DOS MZ serializer matches the complete
  130,882-byte Japanese MAIN.EXE.
- Evidence lives at `.analysis/work/exatt-layout-af598v/report.json`,
  SHA-256 `a421865c879fc97960923d5e07c06aa958e5719240dea7626efea59d32402703`.
  Both produced OBJ, EXE, MAP and writer logs are retained beside this report.
- Original raw vendor OMF packet identity is **not** claimed; CODE, ordered
  native fields, PUBLICs and segment definitions are compared separately.
  No packed-file Factory acceptance or physical runtime validation is added.

The scoped compiler uses a **per-round header/source overlay** under the
ignored native worktree. It never overwrites the historical after596 source
snapshot, original objects or target files. The earlier after596 reader is a
historical proof tied to its original sources; the current source variant is
tested by the overlay. Failed exploratory `af598u` was traced to comparing
the after595 MAP instead of the actual after596 parent, *not* a code mismatch;
the corrected `af598v` build compares the true parent and passes both rounds.

Next source steps can reuse this driver for additional characters and for
isolated C++ expression experiments; each output must be checked without
recrediting already owned bytes.
