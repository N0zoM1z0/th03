# TH03 — current agent handoff (2026-11-06; after525)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after525**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after525 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **752** |
| Original-equal maintained-source CODE-segment bytes | **200,898** |
| Original vendor members retained for context | **141** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after525-string-find-resize-status-ten-build.json`

SHA-256: `5426bee81630d6492e4644cf78ef870b95a8e7d26a4eea7d63e3cfc42bb46981`.

Producer: `scripts/build_th03_mainl_after525_work.py`,
mode `string-find-resize-status-ten`.
Independent reviewer: `scripts/review_th03_mainl_after525_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: `compare1`, `find2`/`find3`/`find4`, `fndfrst`,
`fndfrstn`, `fndlast`, `fndlastn`, `resize`, `status` retain both CODE
segments and all **52 literal ordered FIXUPPs**. **1,236 CODE-segment
bytes = 1,156 executable + 80 control bytes**. Three bounded includes
are source-bound, including new unwind-only and reverse-find bodies.
Original string/regexp slots **384–426 now all source-link**: no vendor
context remains in that 43-member block. This is a working-library scope,
not whole-product acceptance. See the
[complete ten-member review](MAINL_STRING_FIND_TEN_AFTER525_NATIVE_REVIEW.md).
The [after524 eight-member](MAINL_STRING_REGEXP_EIGHT_AFTER524_NATIVE_REVIEW.md)
and [after523 four-member](MAINL_STRING_DUAL_CODE_FOUR_AFTER523_NATIVE_REVIEW.md)
proofs remain intact, including all their include bindings.

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

**Next live candidates:** `ostfloat` (slot 804, 165 CODE / 2 DATA),
`bcd2` (196, 151 CODE), `mnsetflg` (791, 143), `mnrstflg` (789, 143),
`xxas` (155, 143), `mnsfill` (793, 140), `mnsprec` (794, 139), and
`mnsetw` (792, 139). These come from the actual after525 library.
Inspect real segment ordering, x87 fields and public ABI before choosing
an ordinary single-CODE template. Do not repeat the completed string block.

**Extending after525:** validate all three parent `source_include_sha256`
entries and ten TU hashes. Changes to `string_empty_unwind.inl` also affect
retained after524 members; keep their source/recipe bindings intact.

Choose additional large and small CRT work from the **live**
inherited library membership in after525, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after525_work.py string-find-resize-status-ten
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after525 using only **affected source**
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
All new after521–after525 native outputs and scratch are retained; a fresh
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
