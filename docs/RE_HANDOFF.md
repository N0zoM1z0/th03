# TH03 — current agent handoff (2026-11-06; after530)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after530**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after530 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Explicit incremental CRT source members | **831** |
| Original-equal maintained-source CODE-segment bytes | **207,321** |
| Baseline/context members retained | **62** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after530-locale-multibyte-dispatch-twenty-build.json`

SHA-256: `97416af0d48e07559a469928bc2fff5c39c0e909fe087d72132e5096410d7733`.

Producer: `scripts/build_th03_mainl_after530_work.py`,
mode `locale-multibyte-dispatch-twenty`.
Independent reviewer: `scripts/review_th03_mainl_after530_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: five locale owners, five multibyte classifiers, `ddvt`,
`fddvt`, `newf`, `fcorelft`, `fstrdup`, `fstrrchr`, both memicmp and both
stpcpy owners: **1,573 CODE-segment bytes** (1,557 instructions + 16 inline
FAR pointer metadata), **8 DATA bytes**, 67 ordered logical fields. Nineteen
members have literal FIXUPP equality; only `fcorelft`'s near `N_PSBP@` field
at CODE+34 has the disclosed TARGET/CODE frame difference. The DDVT CODE
segments are **word-aligned**. See the
[20-member review](MAINL_LOCALE_MULTIBYTE_TWENTY_AFTER530_NATIVE_REVIEW.md).
Five short includes are hash-bound: locale fields, byte/nth classifiers,
case comparison and copy-end bodies. Successful vectors/logs use **af530b-**
paths and `probe/af530b`; the failed byte-alignment draft, `probe/after530`,
writer logs and SHA-inventoried source/recipe/include snapshots are retained.
The after529 fourteen-member proof retains original LIDATA/initialization
coverage, its two absent near-startup bytes and twelve console frame gaps.
The after528 proof retains sixteen loader frame differences; after526 retains
12 x87 and 2 near-call gaps. Both after527 **af527b-** vectors remain bound.
`h_padd.asm` already has complete cold source and remains unchanged; its old
after529 alias diagnostic receives no new credit. Counts enumerate explicit
incremental receipts, not all earlier baseline owners. The 62 context entries
are not a list of missing functions. Original string/regexp **384–426** and
stream **740–824** blocks remain closed.

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

**Next live candidates:** `fsattch` (slot 705, 82 CODE), `rmtmp`
(106, 81), `stbstb1` (870, 79), `stbalc` (853, 77), `chmod` (200, 77),
`tmpfile` (322, 75 CODE / 4 DATA / 2 BSS), `srchenv` (281, 71 / 1),
`srchpath` (119, 68 / 5 / 80), `fdopen` (218, 67), `fsclose` (718, 66),
`xfclose` (334, 66), `freopen` (230, 64), `sopen` (118, 63), `dosdfree`
(24, 60) and `_access` (182, 59). These come from the actual after530 carrier.
Check existing source/ownership before selecting. `h_llsh`, `h_padd` and
`ioerror` already have cold-source owners; `lseek.asm` also already exists.
Do not overwrite frozen source inputs or count an earlier owner twice.

**Extending after530:** use `parent.SOURCE_PATHS` and
`parent.original_member_programs()` for original profiles. Validate twenty TU
hashes, **all five include hashes** and the one raw arithmetic-frame gap.
Its receipt separately binds original compiler CL.LIB SHA-256; the compiler
library is distinct from the inherited 28-source carrier. Retain after529's
initialized/uninitialized storage profiles and twelve console-frame checks,
plus after528's two includes and sixteen loader-frame checks.

Choose additional large and small CRT work from the **live**
inherited library membership in after530, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after530_work.py locale-multibyte-dispatch-twenty
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after530 using only **affected source**
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
All new after521–after530 native outputs and scratch are retained; a fresh
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
