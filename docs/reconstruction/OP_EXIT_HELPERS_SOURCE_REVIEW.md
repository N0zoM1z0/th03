# OP exit and VRAM-plane helper source proposal

This is a source-only checkpoint for three genuine, complete helper bodies.
It does not itself promote source presence, exactness, target boundaries,
native build success, runtime behavior or whole-product ownership.

| Helper | Decoded candidate extent | CODE bytes | Physical producer | GAME |
| --- | --- | ---: | --- | ---: |
| game_exit_to_dos | 0BEB:0008-0021 | 25 | th02/exit_dos.cpp | 2 |
| vram_planes_set | 0BEB:0021-004A | 41 | th01/vplanset.cpp | 1 |
| game_exit | 0BEB:0112-0155 | 67 | th03/exit.cpp | 3 |

End offsets are exclusive. These 133 bytes neither overlap each other nor the
34 existing OP source owners. The first two already have reviewed OP ledger
boundaries; the third requires a separate OP target-boundary finding before
its proposed new ledger row is installed. MAIN's game_exit acceptance is not
OP acceptance.

## Literal lineage and producer contract

The original bodies come from the pinned reference archive, revision
b6ba5b0a529edbb31efdf8c0e939263804f8ee47, archive SHA-256
9f7a4eb17f24ae2d99adaba4320f6c46f4fc8d659f9b784f6d8e5f3af99bf705.
Their original paths are th02/exit_dos.cpp, th01/hardware/vplanset.cpp and
th02/core/exit.cpp. Only quoted include paths gain the explicit compat/rec98/
prefix. Reversing that prefix recovers the original body bytes exactly.
No expression, GAME conditional, call order, pragma, ABI or byte emission is
changed. All proposed product sources and forwarding includes are ASCII,
therefore valid strict UTF-8; no encoding conversion or allowlist is required.

The actual retained Tup commands and physical source files were inspected.
All three roots are TCC C++ producers, not TASM producers. Each retains
-c -I. -O -b- -3 -Z -d -ml -DBINARY='O' and its original GAME define.
The three physical wrappers are the only translation units compiled. The
original vplanset and exit wrapper chains remain explicit; maintained body
files are included, never separately compiled as additional objects.

The maintained paths are src/op/core/exit_dos.cpp,
src/op/hardware/vram_planes_set.cpp and src/op/core/exit.cpp. The config
config/th03_op_exit_helpers_candidate.json pins source, original body and
wrapper identities, flags, objects, extents and support headers.
The stager scripts/stage_th03_op_exit_helpers.py accepts --root, --reference
and fresh --output paths. It never invokes a compiler, linker or model.

## Source-only checks

Twenty-four portable tests cover literal body provenance, distinct physical
producers, source-only deterministic staging, explicit compat forwarding,
missing/mutated source, fake compatibility stubs, changed compiler/GAME/flags,
duplicate owners, overlap, padding-credit inflation, symlink rejection,
config drift and fresh-output refusal. Both independently staged overlays
contain the same 13 files. These are source repeatability tests, not native
cold-build tests. Run tests/test_th03_op_exit_helpers.py with optional --root
and --reference arguments.

## Parent-owned native and ledger work

The ignored proposal directory .analysis/op-exit-helpers-source-proposal-v01
contains a four-phase plan: three freshly source-built owner objects and one
link. The other 24 project objects from OPFC101 are individually hash-pinned
retained link context; vendor startup and libraries remain explicit context.
Neither those objects nor this bounded link claim a new full cold graph.
The plan preserves original link response and order, and requires one CPU,
nice at least 10, headless operation, sequential 90-second phases plus
15-second owned cleanup, shared lock/poison/registry discipline, and new
execution-time source/toolchain/registry guards. It must be rebound to the
parent's clean checkpoint before execution.

Before source-presence promotion, verify fresh output and actual source
consumption for all three objects, OMF/MAP boundaries and far-cdecl ABI,
all 133 raw candidate bytes and literal relocation streams, and the new
OP game_exit target boundary. Preserve all prior global raw and ordered
negatives. Runtime, packing, full cold repeat and formal exact acceptance
remain distinct and open.

After those checks, update the two existing rows and add only game_exit.
The conditional totals are 37/42 source units and 12,569 scoped source CODE
bytes, up 133; exact credit remains zero. Do not expand the preceding
34-owner fullcold proof retroactively. Keep its frozen source composition
and evidence replay unchanged. Parent ledger integration and progress/SVG
regeneration are separate from installing this source package.

## Completed maintained-source checkpoint

The parent completed the single bounded native diagnostic at clean
`557d8cbed49abb9881115f798e5d1088bb636643`, on2026-10-22 from01:03:45 to01:04:02UTC
(Factory command `b17e8a6e479f49b8b8fbe9b6021c257b`). All three original TCC
producer phases and the unchanged OP link completed with certain exact-owned
cleanup, valid registry transitions and a released shared lock. Each phase was
headless, one CPU, nice >=10, with90 seconds work plus15 seconds owned cleanup.

- Fresh `exit_dos.obj`, `vplanset.obj` and `exit.obj` consume the maintained bodies
  and explicit compat forwarders, while retaining original physical TUs and
  `GAME=2`, `GAME=1`, `GAME=3`, respectively.
- Their complete25/41/67-byte CODE contributions have no extra DATA/BSS. Native
  OMF non-COMENT records preserve original CODE/import/public/fixup contracts;
  actual dependency comments bind the new maintained sources and includes.
- All133 bytes and literal ordered fixups equal the decoded canonical target.
  The independent target-side game_exit review establishes the new67-byte
  boundary, including23 instructions, eight fixup words and no interior entry.
- Exactly24 OPFC101 project objects are retained link context, not fresh builds
  or new source credit. Existing34 owner slices/12436 bytes retain raw bytes,
  ordered fixups, containing MAP extents and public addresses versus OPFC101.
- The EXE remains SHA-256
  `9f2e2af591645963d802489b45f9355a1e9f9b4da4b49ab0767f5be069ec204d`.
  Six whole-program target byte differences and313 global literal relocation
  ordering differences remain. Exact credit is unchanged at zero.

The earlier source-only/pending statements describe preparation history. The
candidate config remains the frozen original declaration used by staging; its
pre-review boundary annotation is superseded by the independent reviewed target
report, not silently rewritten. The current maintained replay is:

    .venv/bin/python3 scripts/replay_th03_op_exit_helpers.py

`config/op_exit_helpers/proof.json` is compact. Its ignored detailed inventory
retains896 explicit artifact pins and an `inputs` dictionary for cleanup tooling.
The replay checks all11 current maintained body/compat/config/stager/replay files
and the seven actual import/config helpers before any repository helper import.
It does not require unrelated historical tracked files to remain unchanged.
It rechecks original reference/archive provenance, source snapshots, actual OMF
lineage, all four native receipts/cleanup/registry transitions, and fresh
structural recomputation. Replay itself executes no compiler, Wine or model.

This checkpoint advances OP source presence from34/41 units and12436 CODE bytes
to37/42 and12569 CODE bytes. It does not claim a new full cold build, cold repeat,
runtime/device behavior, packing, whole-product ownership, formal source or exact
acceptance. The native runner's false acceptance flags remain unchanged.
