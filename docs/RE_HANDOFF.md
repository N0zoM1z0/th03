# TH03 reconstruction — agent handoff (updated 2026-11-05)

**Start here:** `git status -sb`, `git log -5 --oneline`,
[workflow](RE_WORKFLOW.md), [architecture](ARCHITECTURE.md), and
[generated progress](PROGRESS.md). Treat **all dirty work as your own**; do
not discard it because no second agent is expected to be editing this tree.
Commit meaningful advances as `gpt-web: ...`, preferably in several scoped
commits; do not push without explicit authorization.

## Current, verified MAINL working-source checkpoint

The **original Japanese PC-98** targets are pinned in
`config/targets.toml`, provenance `candidate-local-attested`. MAINL is the
ending program. **Do not** substitute translated versions, patched outputs,
TH04 binaries or the packed-game image for the pinned original decoded EXE.

| Working-source property | Current verified value |
| --- | ---: |
| Original Borland CRT member slots | 893 |
| Slots rebuilt from complete source | **319** |
| Original contextual vendor programs left unchanged | **574** |
| Source-compiled original-equal CRT CODE | **104,838 bytes** |
| Decoded original Japanese MAINL EXE size | **67,372 bytes** |
| Ordered DOS MZ relocations | **677** |
| Normal native TASM/TLIB/TLINK verification | **2 independent byte-exact EXE/MAP rounds** |

**Live proof:** `scripts/review_th03_mainl_after317_work.py nec-delay-mbyte`
and `tests.test_mainl_after317_work`, bound to
`.analysis/work/mainl-after317-nec-delay-mbyte-build.json`. The driver
`scripts/build_th03_mainl_after317_work.py` verifies the **full 62→319
source-bound receipt DAG in topological order**, including all inherited
original OBJ/LIB/EXE/MAP vectors and phase-log hashes. This is **not** a
319-provider accepted ledger publication, a complete MAINL source tree, or
proof of byte-identical individual BCC OBJ record serialization.

Recent substantive original-source recoveries: C++ `fstreambase`,
`strstreambase` and `iostream` constructors/destructors, the complete nine-API
`xxv` exception/termination runtime (including original DATA and BSS), ten
near/far Japanese DBCS copy/reverse/case algorithms, NEC PC-98 delay and all
five `mbyte1` conversion APIs. Representative evidence:
[C++ exception boss](MAINL_CXX_EXCEPTION_NATIVE_REVIEW.md),
[`iostream` constructors](MAINL_IOSTREAM_CONSTRUCTORS_NATIVE_REVIEW.md),
[`iostream` destructors](MAINL_IOSTREAM_DESTRUCTORS_NATIVE_REVIEW.md),
[base destructors](MAINL_BASE_DESTRUCTORS_NATIVE_REVIEW.md),
[JIS algorithms](MAINL_JIS_COPY_CASE_NATIVE_REVIEW.md),
[NEC delay and `mbyte1`](MAINL_NEC_DELAY_MBYTE_NATIVE_REVIEW.md).
Older milestone writeups are **historical**; consult the selected original OBJ
and current receipts rather than accepting a previous guess as fact.

### Working source is not formally accepted scope

The [generated progress](PROGRESS.md) and the pinned acceptance manifests
separate decoded function ownership from the packed-file unit ledger.
Current accepted **decoded** source scope, not including the 319-source
working-only CRT expansion:

| Product | Decoded accepted scope |
| --- | --- |
| MAIN | 106 extents / 459 functions / 78,737 CODE bytes |
| OP | 60 extents / 92 procedures / 14,985 bytes (13,221 CODE + 1,764 initialized DATA) |
| MAINL | 211 extents / 288 procedures / 36,946 bytes (34,333 CODE + 2,607 initialized DATA + 6 uninitialized file DATA) |
| ZUN | 77 extents / 8,635 bytes (6,179 CODE + 2,456 DATA) |

MAINL decoded accepted source is **16,695 authored + 20,251 library bytes**,
and its accepted CRT has **28 source providers**. A linked EXE/MAP match
does **not** promote the working 319 members into the accepted ledger;
Factory acceptance and packed-file canonical unit credit remain separate.

### Open technical issues — don't overclaim

- **`xxv`**: all 649 CODE / 296 initialized DATA / 4 BSS bytes, all 24
  CODE/DATA publics (9 CODE + 15 DATA) and one BSS public and 16 relocation sites/targets/frames
  match. The typed `ORG` ordering also yields the original **ordered MZ
  table**. Literal original BCC-vs-TASM **OMF FIXUPP record order differs**.
- **`cnectxmd`**: original 505 CODE / 35 DATA match. Its 51 relocation
  sites/targets match, but near CODE+18 has TARGET frame5 in BCC and CODE
  frame0 in TASM; the literal FIXUPP sequence also differs.
- Older discrepancies in `ctime`, locale, `fclose`, `strftime`, etc. are
  indexed in [MAINL OMF gaps](MAINL_OMF_GAPS.md). These are *reviewed
  historical observations*, not universal claims about today's build.
- Source ownership of the **whole game** remains open, even with a fully
  reproduced decoded MAINL working binary. Never confuse a diagnostic
  emulator test, build receipt, accepted extent and exact source identity.

## Next agent: practical workflow

1. Inspect `git status -sb` and own any dirty files; reread actual target
   records, ABI and disassembly before relying on earlier notes.
2. Keep progress balanced: **larger Bosses** with complete executable body,
   RTTI, jump tables and DATA/BSS, plus full **small leaf** functions.
   Potential remaining selected CRT candidates to investigate, **not yet
   accepted claims**: `sdbctr`, `sdboflow`, `fsbopen`, `insert1`, `insert2`,
   `replace`; continue MAIN/OP/ZUN game-module work where ownership is open.
3. Rebuild only changed/impacted members using native TASM/TLIB/TLINK or
   BCC as appropriate, serialize the Wine writer, and check original selected
   OBJ sections, publics/imports, logical FIXUPPs and the entire linked
   Japanese EXE/MAP. **Do not run a new full cold replay** on an unchanged
   source-bound parent chain.
4. Record what is genuinely original, what differs only in OMF metadata,
   and what is *accepted* by the separate ledger. Commit substantial
   progress in multiple `gpt-web: ...` commits; leave no unexplained dirt.

**Small affected-scope audit (not a cold replay):**

```sh
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after317_work.py nec-delay-mbyte
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after317_work -v
.venv/bin/python scripts/validate_tracking.py
git diff --check
git status -sb
```

The live reviewer validates **all 55 inherited post-62 layers** and their
latest round, so do **not** delete inherited `.analysis/work/after*-round*`
OBJ/LIB/EXE/MAP vectors, build receipts or phase logs just because they look
old. The [storage audit](STORAGE_HANDOFF_2026-11-05.md) lists safe
regenerable scratch and notes which historical branches were retired. The
Wine prefix, Borland tools, pinned targets, runtime images and old-named
`reference.tar` are **not disposable**. Use a scoped dry-run first; the
`clean_generated.py` general preview is **not a dependency oracle**.
