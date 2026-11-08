# TH03 — active handoff to the next reconstruction agent

> Current workflow: follow the **Highest priority** section in `AGENTS.md`.
> Prefer affected exact comparisons and useful Markdown knowledge. Ordinary
> notes do not require full CI, native replay or document-hash/pin refreshes.
> Older broad validation instructions apply only when their impact is relevant.


**Checked 2026-11-08 · current maintained-source native MAIN proof: `af935a`.**
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
- **Latest source-current native MAIN experiment: `af935a`.** Two
  independent original Turbo C++ 4.02 rounds recompiled **seven original
  physical project objects together**: the complete Marisa BOSS
  (`ba_maris`), HitCircle (`hitcirc`), all **four** Enemy source consumers
  (`eforna`, `efornb`, `eupda`, `eupdb`) and the complete Bullet engine.
  The normal complete **99-game-object MAIN TLINK** ran twice, reusing
  **92 unchanged original game objects and Borland CRT**. All **7,886 CODE
  bytes, 647 ordered native OMF FIXUPP fields, 52 PUBLICs**, source/header
  dependencies, 16-bit segment/ABI layout, complete MAIN EXE/MAP,
  **124,642 Japanese loaded bytes and all 1,553 original ordered MZ
  relocations** match. See [after935 integrated source](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER935_REVIEW.md).
  Protected report: `.analysis/work/exatt-layout-af935a/report.json`,
  SHA-256 `924fdd7943c428064b1a26d9a3a4b4b99303d4204f7c4d7bfd682965d35c3620`.
- **Independent earlier source-current experiment: `af927a`.** Two
  original compiler and normal-link rounds rebuilt five original objects,
  reusing 94 other game objects and CRT. Their **7,833 CODE bytes,
  991 ordered OMF FIXUPPs and 34 PUBLICs** remain source-current, with
  full original Japanese MAIN and 1,553 relocations matched. A separately
  reviewed standard DOS MZ serializer also matches the original
  **130,882-byte Japanese MAIN.EXE**.
- These earlier five scopes are **complete Chiyuri major BOSS** (`ba_chiyu`,
  2,654 CODE), **complete MAIN entry/round scheduler** (`entry`, 3,050),
  **full player-effects/GRCG engine** (`effects`, 628), **Chiyuri
  Chargeshot/Gauge** (`cs_chiyu`, 1,011) and **Chiyuri Bomb** (`b_chiyu`,
  490). `entry` consumes four maintained `.inl` implementations;
  edits to them must recompile the real **`entry` physical object**.
  Review [after927 integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md).
  Protected actual native writer receipt:
  `.analysis/work/exatt-layout-af927a/report.json`, SHA-256
  `3b64374f73e81bfedaf86227724544664f18d5b5ffe39ed5b381001c168ab6d5`.
- Both independent scopes are **current-source native normal MAIN proof**,
  **not** vendor packet-identical OMF, full original source ownership or
  canonical packed-file Factory acceptance. The 7,886 and 7,833 CODE bytes
  were already historically source-covered; do not award new distinct
  original CODE bytes or add these overlapping historical proof scopes.

## Independent current-source receipts versus historical snapshots

These genuine two-round native compiler/linker reports were rechecked against
the current checkout after `af935a`. They are **independent physical-object
scopes**, not one combined 99-original-source replay:

| Source-current stage | Complete physically rebuilt original owners | Original CODE bytes |
| --- | ---: | ---: |
| `af935a` | 7 | 7,886 |
| `af927a` | 5 | 7,833 |
| `af915a` | 5 | 6,059 |
| `af909a` | 5 | 7,582 |
| `af889a` | 5 | 4,191 |
| `af880h` | 2 | 1,245 |
| `af882e` | 1 | 49 |

`af921a` (`hitcirc`), `af903a` (`bullet`), `af896a` (all four physical
`enemy.cpp` consumers), `af883a` and `af881i` (`ba_maris`) no longer
bind to the changed maintained source hashes. Their original native outputs
are authentic **historical** evidence; `af935a` establishes the entire
currently changed physical scope together. These independent receipts may
have related/overlapping ownership: never add their bytes as distinct
coverage or infer whole-product source exactness.
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
- A fresh **scoped current-source MAINL Staff Roll build `af942s`** now
  recompiles the entire 19-procedure `staffdat` owner in two independent
  original TC4 rounds: **3,695 CODE + 224 DATA bytes, 342 literal ordered
  OMF FIXUPPs, six DATA PUBLICs**, with both complete normal MAINL links
  reproducing the Japanese 67,372-byte EXE and all 677 relocations. The
  other 35 original game objects and CRT were reused; no full cold replay.
  See [MAINL Staff native C++ after942](MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md).
  The old broad cold-source graph still pins the pre-edit `staff/data.cpp`;
  do not call it current or repin it just to satisfy cold-dependent tests.
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
   --stage af935a af927a af915a af909a af889a af880h af882e

# If a maintained physical source or its actual .inl changed:
# replace the examples with real original TUs and a UNIQUE unused stage.
# Shared enemy.cpp has FOUR physical consumers, even if one code path changes.
 DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
   .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
   --stage afNEWa --units eforna,efornb,eupda,eupdb
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
- [Latest seven-object source/native integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER935_REVIEW.md)
- [Earlier five-object source/native integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER927_REVIEW.md)
- [Historical source and compiler trials through after927](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Storage policy and prior safe cleanup audits](STORAGE_HANDOFF_CURRENT.md)
- [After928 applied Git/cache storage recovery](STORAGE_HANDOFF_AFTER928.md)
- [Current MAINL Staff source/native work](MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md)
- [MAINL original CRT/source recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md)
- [Generated source/acceptance progress](PROGRESS.md)
