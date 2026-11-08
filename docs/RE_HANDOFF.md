# TH03 — active handoff to the next reconstruction agent

**Checked 2026-11-08 · current maintained-source native MAIN proof: `af927a`.**
This is the **active, intentionally short handoff**. The previous 2,713-line
handoff is preserved without substantive deletion in
[RE_HANDOFF_ARCHIVE_AFTER927.md](RE_HANDOFF_ARCHIVE_AFTER927.md). Its many
historical “Latest” headings are **not current checkout claims**.
Older archives: [after709](RE_HANDOFF_ARCHIVE_AFTER709.md),
[after596](RE_HANDOFF_ARCHIVE_AFTER596.md),
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md).

## First read: what is actually proved

- Source repository is the real persistent `th03` worktree. Start with
  `git status -sb`, [AGENTS.md](../AGENTS.md),
  [RE_WORKFLOW.md](RE_WORKFLOW.md), the relevant original C++ file and
  the experiment-specific review. **Carry forward dirty work; do not
  assume another agent is concurrently editing this repository.**
- Original targets are the **pinned Japanese binaries** from
  `config/targets.toml` with `candidate-local-attested` provenance.
  Do not use translated/reference binaries as targets or alter original
  target/OBJ/compiler/CRT/linker inputs to create equality.
- **Latest source-current native MAIN experiment: `af927a`.** Two
  genuinely independent original Turbo C++ 4.02 compiler rounds rebuilt
  the **five edited original physical project objects together** and
  twice ran the actual complete **99-game-object normal MAIN TLINK**
  response, reusing **94 other original game objects and Borland CRT**.
  Source/header OMF COMENT dependencies and all 16-bit ABI/layout were
  checked. **7,833 CODE bytes, 991 literal ordered native OMF FIXUPPs,
  34 PUBLICs**, full normal MAIN EXE/MAP, **124,642 Japanese loaded
  program bytes and all 1,553 ordered original MZ relocations** match.
  A separate reviewed standard DOS MZ serializer also matches the
  original **130,882-byte Japanese MAIN.EXE**.
- The five scopes are **complete Chiyuri major BOSS** (`ba_chiyu`,
  2,654 CODE), **complete MAIN entry/round scheduler** (`entry`, 3,050),
  **full player-effects/GRCG engine** (`effects`, 628), **Chiyuri
  Chargeshot/Gauge** (`cs_chiyu`, 1,011) and **Chiyuri Bomb** (`b_chiyu`,
  490). `entry` consumes four maintained `.inl` implementations;
  edits to them must recompile the real **`entry` physical object**.
  Review [after927 integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md).
  Protected actual native writer receipt:
  `.analysis/work/exatt-layout-af927a/report.json`, SHA-256
  `3b64374f73e81bfedaf86227724544664f18d5b5ffe39ed5b381001c168ab6d5`.
- This is **current-source native normal MAIN proof**, **not** historical
  vendor raw OMF packet identity, complete original source ownership or
  **canonical packed-file Factory acceptance**. These 7,833 game CODE
  bytes were already historically source-covered: do **not** award
  7,833 additional distinct original CODE bytes for this cleanup.

## Independent current-source receipts versus historical snapshots

The following real two-round original compiler/linker receipts were
rechecked against the checkout **after** the after927 source edits;
they cover **other unchanged original physical sources** and are **not
one combined whole-project replay**:

| Source-current stage | Complete physically rebuilt original owners | Original CODE bytes |
| --- | ---: | ---: |
| `af927a` | 5 | 7,833 |
| `af921a` | 6 | 4,643 |
| `af915a` | 5 | 6,059 |
| `af909a` | 5 | 7,582 |
| `af903a` | 7 | 8,839 |
| `af896a` | 9 | 10,181 |
| `af889a` | 5 | 4,191 |
| `af883a` | 4 | 2,725 |
| `af880h` | 2 | 1,245 |
| `af881i` | 1 | 1,431 |
| `af882e` | 1 | 49 |

All of these are **independent scopes with possible historically related
ownership**, not additive distinct-coverage or product acceptance totals.
The genuine older `af877a` now **fails current maintained-source hash
binding** because both Chiyuri BOSS and Chiyuri Chargeshot changed.
`af871a` also fails after earlier Kotohime/other source changes.
`af865a`, `af859a`, `af853a`, `af847a`, `af843g`, `af842a`,
`af840a`, `af835a` and many earlier rounds are **historical evidence**,
not this checkout's source-current proof. Preserve their frozen writer
logs and reports; never rewrite old receipts or weaken binding checks.
The [after927 archive](RE_HANDOFF_ARCHIVE_AFTER927.md) and per-experiment
reviews contain the historical source/codegen trial details.

## Source-product status: avoid mixing denominators

The latest `scripts/preflight.py` (2026-11-08) reports:

- **MAIN:** real source-native normal linker comparisons above, but
  **no claim of complete game-source exactness or canonical packed-game
  acceptance**. Parent and selected original project OBJ/CRT are reused;
  a verified normal EXE does not automatically establish the vendor
  linker’s own MZ-header serialization or packet-identical OMF.
- **MAINL (ending):** current decoded source **accepted units 0/259**,
  zero current authored/library decoded acceptance and Factory
  acceptance **false**. The after587 historical original-native link
  did reproduce the **67,372-byte Japanese MAINL executable and 677
  relocations at that historic source snapshot**, but its old broad
  source publication guard no longer matches this checkout. Recertify
  current source and ownership before calling that result current.
  Historical older “0/250” uses a *different tracking population*;
  do not substitute it for the current preflight **0/259**.
- **OP:** current decoded source acceptance **60 extents / 92
  procedures / 14,985 bytes** (13,221 CODE + 1,764 DATA), with a
  validated source-only cold pair and native ownership/ABI. This is
  separate from canonical packed-file acceptance or whole-game exactness.
- **ZUN:** current decoded source acceptance **77 extents**, with
  2,179 authored, 1,390 original-ASM and 5,066 library bytes;
  canonical packed-unit credit and complete source ownership remain open.
- Whole-game completion percentage is **unknown**. Use
  [the generated progress](PROGRESS.md) and **current preflight**,
  not old claimed percentages or summed CODE extents.

## Important unresolved issues and best next work

1. **Pursue new distinct original source ownership**, not only another
   refactor of already historically source-covered CODE. Attack real
   large BOSS/engine functions and small leaves together; use original
   codegen to confirm natural C/C++, but count new bytes only after
   formal acceptance. The newest work provides repeatable examples.
2. **`input_s` historical single-NOP parent normal-link gap** remains
   unresolved. Do not insert a synthetic NOP, alter an original OBJ or
   claim full normal MAIN acceptance for that owner. See the read-only
   `scripts/review_th03_input_s_link_gap_after744.py` diagnostic.
3. **MAINL decoded publication and source binding** require fresh
   recertification against current source and the preserved after587
   ancestry; 0/259 current accepted. The historical linker equality
   is useful evidence but **not** a current broad-source acceptance.
4. **Vendor OMF packet identity and raw MZ-header writer identity**
   remain separate from CODE, ordered FIXUPP, PUBLIC and independently
   serialized Japanese EXE equality. **Factory canonical packed-file
   acceptance remains open.** Preserve this distinction in every report.
5. **Storage:** `.analysis` includes the Wine/Borland toolchain,
   original inputs and successful two-round OBJ/EXE/MAP/writer logs.
   Never bulk-remove source-bound stages or prune by age. Only audited
   unreferenced failed trials and official regenerable caches may be
   removed. The latest bounded safe repack/cache cleanup reclaimed
   about 23.77 MiB **without deleting proof trees**; see
   [after928 applied storage audit](STORAGE_HANDOFF_AFTER928.md) and
   [current storage policy](STORAGE_HANDOFF_CURRENT.md).

## Minimal repeatable commands (no full cold replay)

```sh
# At session start; read-only, modest checks
 git status -sb
 .venv/bin/python scripts/preflight.py
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/review_th03_main_source_overlay.py \
   --stage af927a af921a af915a af909a af903a af896a af889a af883a af880h af881i af882e

# If a maintained physical source or its actual .inl changed:
# replace the examples with real original TUs and a UNIQUE unused stage.
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
   --stage afNEWa --units ba_chiyu,entry
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/review_th03_main_source_overlay.py --stage afNEWa

# Ordinary completion checks
 .venv/bin/python -m unittest discover -s tests \
   -p test_main_source_overlay_inline_contract.py -q
 .venv/bin/python scripts/validate_tracking.py
 .venv/bin/python scripts/progress.py --check
 git diff --check
```

Use an actually unused DOS-safe `afNNNx` stage, **not** the literal
`afNEWa` example. Probe **only edited original physical TUs**, preserving
all other original game objects and CRT, and require two actual original
TC4 rounds plus two complete **normal** MAIN TLINKs. No routine full
cold replay. Do not edit another agent's reference toolchain or original
target. Preserve dirty source changes and commit meaningful progress as
`gpt-web: xxx` (local commits; no push unless asked).

## Reference map

- [Workflow](RE_WORKFLOW.md) · [Architecture](ARCHITECTURE.md) ·
  [Original fixed targets](../config/targets.toml)
- [Latest source/native integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md)
- [Historical source and compiler trials through after927](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Storage policy and prior safe cleanup audits](STORAGE_HANDOFF_CURRENT.md)
- [After928 applied Git/cache storage recovery](STORAGE_HANDOFF_AFTER928.md)
- [MAINL original CRT/source recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md)
- [Generated source/acceptance progress](PROGRESS.md)
