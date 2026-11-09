# TH03 — active handoff (2026-11-09)

Follow [AGENTS.md](../AGENTS.md). This page records current work and evidence;
[generated progress](PROGRESS.md) provides the ledger/publication counters.
The complete pre-consolidation text is preserved in the
[after1096 archive](RE_HANDOFF_ARCHIVE_AFTER1096.md); older chronology remains
in the [after1053](RE_HANDOFF_ARCHIVE_AFTER1053.md) and
[after927](RE_HANDOFF_ARCHIVE_AFTER927.md) archives.

## Current status

The latest preflight passes target identity, tracking and current decoded
publications. OP, MAINL and ZUN retain their accepted decoded scopes; MAIN's
ledger and separate function inventory remain unchanged. Recent work improves
natural C++ while preserving original native output, so ledger totals need
not increase. The whole-game completion percentage remains unknown.

`status.py` and generated progress now select the current MAIN reports below.
The old `af1053k` composite is historical after later source changes and must
not be used as a current all-owner proof.

## Current MAIN native evidence

These five disjoint stage reports have passed read-only source/native review.
Each retains two original TC4 compiler rounds, complete physical CODE/DATA,
literal ordered native fields, PUBLICs and segment geometry, plus normal MAIN
links matching the Japanese loaded image and all ordered MZ relocations.

| Stage | Current physical owners |
| --- | --- |
| `af1092k` | Bullet, Fireball, Mima, Marisa, Ellen BOSS, Kotohime, Reimu BOSS, Yumemi, Chiyuri, both Reimu Extra Attack owners and HitCircle |
| `af1056c` | Shared BOSS providers `ba_sring`, `ba_srest` |
| `af1094e` | Ellen Extra Attack `ex_ellen` |
| `af1095w` | Rikako BOSS `ba_rikak` |
| `af1096g` | Kana BOSS `ba_kana` |

Reports live at `.analysis/work/exatt-layout-STAGE/report.json`. The current
review log is `.analysis/work/progress-review-current-main.log`. These are
separate scoped links, not a new combined build of all listed owners.
Local native proof is separate from Factory acceptance.

## Latest natural-source recovery

- **Rikako:** all five BOSS attack/render iteration sites use natural `for`
  loops; the update PID and renderer angles initialize at first use. Preserve
  the shared entity index, signed/unsigned arithmetic and RNG/emission order.
  Narrower coordinate and sprite-offset lifetimes that changed CODE remain
  rejected. See the [complete Rikako review](MAIN_RIKAKO_BOSS_NATURAL_FOR_AND_LIFETIMES_AFTER1095_REVIEW.md).
- **Kana:** the sixteen-sprite intro uses a natural `for` with its original
  shared register index. Radius, angle and X scratch initialize at first use;
  the update PID follows the inactive-player return. The zero-minus angle
  expression, wider Y/sprite-offset lifetimes and draw order remain necessary.
  See the [complete Kana review](MAIN_KANA_BOSS_NATURAL_FOR_AND_LIFETIMES_AFTER1096_REVIEW.md).
- **Ellen Extra Attack:** its separate six-function owner has natural loops
  for history shifting, initialization and spiral/render iteration, with
  first-use PID and branch/loop-local scratch. See the
  [Ellen Extra Attack review](MAIN_ELLEN_EXATT_NATIVE_HISTORY_AFTER873_REVIEW.md).
- The `af1092k` integration also retains the current Bullet/Fireball loops,
  Reimu rendering and Extra Attack, Mima/Marisa lifetimes, Ellen BOSS loops,
  Kotohime Radial, Chiyuri fans, Yumemi attacks and HitCircle cel/update work.
  Detailed attempts and earlier source bindings are in the archive and focused
  reviews; do not revive their superseded "current" claims.

## MAINL build and publication

The `af1055m` Staff/root refresh restores the current decoded publication.
Both complete decoded EXE/MAP rounds and ordered relocations match their
reference targets; the unchanged cold pair and selected providers are retained.
See the [current MAINL build review](MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md).

For a later Staff/root change, choose an unused `afNNNm` stage:

    .venv/bin/python scripts/build_th03_mainl_current.py --stage afNNNm --build
    .venv/bin/python scripts/publish_th03_mainl_work_scopes.py --stage afNNNm
    .venv/bin/python scripts/progress.py

Omit `--build` for read-only review. Other dependency changes require their
actual affected scope. Do not run the original cold builder in place over the
protected ancestor.

## Next useful work and open limits

1. Continue the Hitbox/collision family, adjacent Reimu Extra Attack creation
   and remaining rendering helpers, or select another large engine/controller.
   Inspect current source and focused evidence before choosing a function;
   recently naturalized leaves are not an unowned work queue.
2. Select genuinely unowned regions from `config/units.csv`,
   `config/evidence.csv` and focused reviews when expanding ownership.
   MAINL, OP and ZUN still have open scopes; source presence alone is not
   accepted ownership. Original ASM and library contributions remain separate
   from authored-source credit.
3. The standalone MAIN BIOS `input_s` source has a historical one-byte
   trailing-NOP link gap despite its exact 417-byte CODE owner. Preserve that
   finding; do not manufacture a NOP or call it full-link acceptance.
4. Whole-product ownership, canonical packed-unit acceptance and historical
   vendor OBJ/header-writer identity remain separate open questions.

Factory's read-only registry lists `th03`, but the accepted snapshot still
contains no OracleResults for imported claims. The earlier replay-worker
registration rejection is recorded in the archive; worker readiness was not
retested by submitting a replay here. Continue local native reconstruction and
keep Factory receipt acceptance separate.

## Minimal checks and retention

    git status -sb
    .venv/bin/python scripts/preflight.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1092k af1056c af1094e af1095w af1096g

For source changes use a fresh DOS-safe stage, compile only the affected
original physical TUs with `probe_th03_main_exatt_layout.py`, compare both
complete native rounds and normal links, then retain useful findings and
commit as `gpt-web: xxx`. No full cold replay is needed for ordinary scoped
changes. See [workflow](RE_WORKFLOW.md) and [script entry points](../scripts/README.md).

Preserve dirty/untracked work, targets, the game-specific Wine/analyzer state
and the entire active source-bound receipt DAG, including both raw rounds and
writer logs. The [current storage policy](STORAGE_HANDOFF_CURRENT.md) and
[after1024 audit](STORAGE_HANDOFF_AFTER1024.md) remain authoritative. Generic
receipt pruning and analysis deletion remain retired; cache-only cleanup is
the routine route. Finish affected checks and `git diff --check`.
