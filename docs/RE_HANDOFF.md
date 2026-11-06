# TH03 — current agent handoff (2026-11-06; after527)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after527**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after527 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **774** |
| Original-equal maintained-source CODE-segment bytes | **202,930** |
| Original vendor members retained for context | **119** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after527-stream-integer-assign-final-eight-build.json`

SHA-256: `e353d9add7801b06681b4a81df6b50f0d4cf13a66bf1fd019fdf04fb1be425d8`.

Producer: `scripts/build_th03_mainl_after527_work.py`,
mode `stream-integer-assign-final-eight`.
Independent reviewer: `scripts/review_th03_mainl_after527_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: `iostasn2`, `istasn1`, `istasn2`, `isteint`, `istesh`,
`isteuint`, `isteulng`, `isteush`: **428 executable CODE bytes**, all eight
literal ordered FIXUPPs and complete segment packing/alignment match.
Two bounded includes preserve original state-guarded writes and truncation.
Original slots **740–824 now all source-link** in the working CRT library.
See the [eight-member review](MAINL_STREAM_INTEGER_EIGHT_AFTER527_NATIVE_REVIEW.md).
Successful raw files/logs use **af527b-** paths, explicitly bound in the
receipt. The old `probe/after527` long-include crash branch is retained;
keep new include basenames short (the 33-character name crashed TASM32).
The [after526 FP/stream proof](MAINL_STREAMS_FOURTEEN_AFTER526_NATIVE_REVIEW.md)
remains unchanged, including its 12 x87 and 2 near-call frame differences.
The [after525 proof](MAINL_STRING_FIND_TEN_AFTER525_NATIVE_REVIEW.md) closed
original string/regexp slots **384–426** and remains source-bound.

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

**Next live candidates:** `xxas` (slot 155, 143 CODE), `spawnlpe`
(371, 129), `spawnle` (369, 127), `screen` (564, 126), `unhandl`
(135, 122), `ccomputn` (515, 119), `pc98mous` (504, 114), `movetext`
(562, 111), `crtinit` (555, 106), `_setcoll` (188, 106), `FMBBTYPE`
(653, 103) and `MBBTYPE` (580, 103). These come from the actual after527
library. Inspect actual ABI, segment/storage and ordered field questions.
Do not repeat the completed string/regexp or 740–824 stream blocks.

**Extending after527:** validate both parent `source_include_sha256`
entries and eight TU hashes. Its retained-parent review also verifies
all after526 raw FP/near-call frame descriptions; preserve that check.

Choose additional large and small CRT work from the **live**
inherited library membership in after527, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after527_work.py stream-integer-assign-final-eight
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after527 using only **affected source**
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
All new after521–after527 native outputs and scratch are retained; a fresh
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
