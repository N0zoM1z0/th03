# TH03 — current agent handoff (2026-11-06; after529)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after529**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after529 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Explicit incremental CRT source members | **811** |
| Original-equal maintained-source CODE-segment bytes | **205,748** |
| Baseline/context members retained | **82** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after529-platform-startup-stack-fourteen-build.json`

SHA-256: `8a08bde43984b4031b9260915985866764e9212bdc30848edc84a5c64896073b`.

Producer: `scripts/build_th03_mainl_after529_work.py`,
mode `platform-startup-stack-fourteen`.
Independent reviewer: `scripts/review_th03_mainl_after529_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: `screen`, `ccomputn`, `pc98mous`, `movetext`, `crtinit`,
`conioini`, `cibmcrsr`, `validate`, `cputype`, `ctrlbrk`, `hard`, `alloca`,
`chainint`, `stack`: **1,119 CODE-segment bytes** (1,101 instructions +
18-byte inline diagnostic), **24 DATA / 8 BSS / 16 initialized INITDATA**
bytes. The near CPU startup record also has two uninitialized bytes, checked
as absent rather than invented zeros. LIDATA is materialized for exact
original initialized coverage. All 71 ordered logical fields match; twelve
literal near-call frame differences across three console members are recorded
per round. See the [14-member review](MAINL_PLATFORM_FOURTEEN_AFTER529_NATIVE_REVIEW.md).
Successful vectors/logs use **af529b-** paths and `probe/af529b` scratch.
The old fifteen-member `probe/after529` alias diagnostic and its source/
recipe/profile SHA inventory remain retained. Its `h_padd` EXE matched but
one MAP alias pair differed; that experiment receives no additional credit.
`h_padd.asm` already has complete cold source and remains unchanged.
Counts enumerate explicit incremental member receipts, not all earlier
baseline source owners. Do not treat the 82 context entries as missing code.
Original string/regexp **384–426** and stream **740–824** blocks remain closed.
The after528 23-member proof retains all sixteen loader frame differences.
The after526 proof retains its 12 x87 and 2 near-call differences; the after527
**af527b-** vectors, short includes and old long-include crash branch remain.

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

**Next live candidates:** `_setcoll` (slot 188, 106 CODE / 2 DATA),
`FMBBTYPE` (653, 103), `MBBTYPE` (580, 103), `_setxfrm` (190, 101 / 2),
`FNTHCTYP` (695, 91), `NTHCTYPE` (652, 91), `newf` (92, 85), `fddvt`
(54, 84), `MBISPRN` (595, 83), `ddvt` (53, 83), `fsattch` (705, 82),
`fstrdup` (445, 81) and `rmtmp` (106, 81). These are actual after529 context
entries; check existing source/ownership before selecting one. `h_padd`
(slot 72) and `ioerror` (79) already have cold-source owners, despite appearing
in the incremental context set. Do not duplicate their source or progress.

**Extending after529:** use `parent.SOURCE_PATHS` and
`parent.original_member_programs()` for original profiles. The pinned compiler
CL.LIB is distinct from the inherited 28-source carrier; its hash is verified
through the retained cold receipt and exposed by the independent review.
Validate actual initialized coverage/uninitialized extents, all fourteen TU
hashes and twelve raw console-frame descriptions. This stage adds no includes.
Retain the after528 two include hashes and sixteen loader-frame checks.

Choose additional large and small CRT work from the **live**
inherited library membership in after529, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after529_work.py platform-startup-stack-fourteen
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after529 using only **affected source**
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
All new after521–after529 native outputs and scratch are retained; a fresh
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
