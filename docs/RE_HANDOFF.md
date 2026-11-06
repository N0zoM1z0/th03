# TH03 — current agent handoff (2026-11-06; after528)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after528**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after528 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **797** |
| Original-equal maintained-source CODE-segment bytes | **204,629** |
| Original vendor members retained for context | **96** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after528-exception-report-process-twenty-three-build.json`

SHA-256: `1c657c3fedcded7918174728314bb84daa5de8c19b6967b0d60763ba7f2787e3`.

Producer: `scripts/build_th03_mainl_after528_work.py`,
mode `exception-report-process-twenty-three`.
Independent reviewer: `scripts/review_th03_mainl_after528_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: `xxas`, `xxa`, `unhandl`, `_abort`, `errormsg`, `pureerr`,
`assert` and all sixteen `exec*`/`spawn*` wrappers: **1,699 executable CODE
bytes / 125 DATA bytes / 80 ordered logical fields**. Seven diagnostic/
exception members have literal ordered FIXUPP equality. Each process wrapper
has one disclosed original TARGET vs native CODE near-loader frame difference;
all 16 raw descriptions are retained and independently verified per round.
The stack exception frame saves **SEG DGROUP** at +0Eh, with original SS
count/list slots and FAR/Pascal cleanup intact. See the
[23-member review](MAINL_EXCEPTION_PROCESS_23_AFTER528_NATIVE_REVIEW.md).
Original string/regexp slots **384–426** and stream slots **740–824** remain
fully source-linked. The unchanged after526 proof retains its 12 x87 and
2 near-call frame differences. The after527 eight-member proof and both
short-DOS **af527b-** output rounds remain bound to this parent chain.
Its old `probe/after527` long-include crash branch is also retained;
keep new include basenames short (the 33-character name crashed TASM32).

The earlier large Boss `cplx2` is **complete and source-linked**
since after514: 22/22 FAR public bodies, 5,598 exact CODE bytes,
original DATA and INITDATA and all 860 logical relocation
sites/targets/addends. Scoped TASM NOSMART produced the two
original direct FAR calls. Final EXE/MAP matches; raw Borland
OBJ/FIXUPP framing is not claimed equal. See
[complete cplx2 review](MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md).

## Next-agent implementation priorities

Completed prior bosses remain source-linked: **isteldbl** at after521
(1,947 CODE / 14 DATA, 112 logical fields, 85 disclosed x87 frame-method
differences) and **h_ldiv** at after522 (174 CODE, twelve exports and
original-equal MAP alias chronology through pinned compatible JWasm).
See [full parser proof](MAINL_ISTELDBL_FULL_SOURCE_LINK_AFTER521_NATIVE_REVIEW.md)
and [full divmod proof](MAINL_H_LDIV_FULL_SOURCE_LINK_AFTER522_NATIVE_REVIEW.md).
Do not double-count their historical partial/TASM-only diagnostic sources.

**Next live candidates:** `screen` (slot 564, 126 CODE), `ccomputn`
(515, 119), `pc98mous` (504, 114), `movetext` (562, 111), `crtinit`
(555, 106 CODE / 22 DATA), `_setcoll` (188, 106 / 2), `FMBBTYPE`
(653, 103), `MBBTYPE` (580, 103), `_setxfrm` (190, 101 / 2) and
`h_padd` (72, 96). These come from the actual after528 library's remaining
96 vendor members. Inspect ABI, storage and ordered fields. Do not repeat
the completed process wrappers, string/regexp or 740–824 stream blocks.

**Extending after528:** validate its 23 TU hashes and both existing include
hashes (`crt_errno.inc`, `stdio_layout.inc`), plus all 16 raw loader-frame
descriptions. Its retained-parent review verifies both after527 include hashes
and the earlier after526 FP/near-call descriptions; preserve these checks.

Choose additional large and small CRT work from the **live**
inherited library membership in after528, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after528_work.py exception-report-process-twenty-three
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after528 using only **affected source**
and incremental native TASM/TLIB/TLINK. Do not run
routine whole-product cold replay. Continue all existing
dirty work, preserve historical native proof files, and
commit each substantial change as `gpt-web: xxx`.
Do not push unless explicitly requested.

## Latest protected-storage audit: after520

The latest [storage audit](STORAGE_HANDOFF_CURRENT.md)
traces **258 active source-bound stages and protects
5,760 receipt/log/native-output files**. Both raw
OBJ/LIB/EXE/MAP rounds, all writer logs, original sources,
targets, toolchain, databases and other products' evidence
must remain intact.

The pinned `scripts/cleanup_mainl_after520_handoff.py`
already removed **15 superseded raw files** from the
historical alternative after506 ios-iword build,
saving **1,642,496 allocated bytes (1.57 MiB)**.
That mode's JSON receipt and the actual active after506/
after507 evidence remain. SHA-256 deletion inventory:

`.analysis/work/handoff-after520-retired-20261106.json`

Manifest SHA-256: `ffed6609142ed39414970fb15a35f88b467488792cff0ed61f6b705cc7425392`.
The audited after520-only dry-run reported zero eligible files.
The after520 guard **now fails closed** because after521+ stages exist.
All new after521–after528 native outputs and scratch are retained; a fresh
source-DAG/SHA-256 audit is required before any later deletion.
The old after439/after388 cleanup guards remain frozen historical audits;
do not bypass them.

The separate cache-only cleanup was also applied using
`clean_generated.py --caches-only --apply`; it removed
`scripts/__pycache__`, `scripts/lib/__pycache__`
and `tests/__pycache__`, freeing 10,428 KiB (10.18 MiB)
of allocated space immediately. The cache action log is
`.analysis/work/after520-cache-cleanup-applied.txt`.
**Combined immediate storage reclaimed: about 11.75 MiB.**
This does not delete `.analysis`, and bytecode will
regenerate during subsequent test runs.

Never blanket-run `clean_generated.py --apply` or
`--prune-unreferenced-receipts`; they are not native
proof dependency oracles.

The pinned targets are **candidate-local-attested**, not
independently proved pristine dumps. Byte-exact decoded
EXE/MAP and working-source CRT membership are **not**
raw Borland OBJ identity or Factory whole-product
source acceptance. Formal MAINL canonical packed-unit
acceptance remains **0/250**, and whole-game percent
is not established.

For older decisions, use [handoff history](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md)
and [member recovery index](MAINL_WORKING_CRT_RECOVERY_INDEX.md).
