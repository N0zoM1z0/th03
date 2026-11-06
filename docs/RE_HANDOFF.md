# TH03 — current agent handoff (2026-11-06; after521)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after521**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after521 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **729** |
| Original-equal maintained-source CODE bytes | **196,239** |
| Original vendor members retained for context | **164** |
| Independent TASM/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after521-istream-long-double-parser-build.json`

SHA-256: `80c78e22d99044c9087fc40ccd9094a5f3eb5cc15a9854736e0c1e03281ab33c`.

Producer: `scripts/build_th03_mainl_after521_work.py`,
mode `istream-long-double-parser`.
Independent reviewer: `scripts/review_th03_mainl_after521_work.py`.

Five complete additions since after516: `istedbl` (124 CODE,
double input), `isteflt` (157 CODE, float input),
`fsopen` (105 CODE, fstreambase open) and `fssbuf`
(91 CODE, virtual setbuf), plus the complete `isteldbl`
(1,947 CODE / 14 DATA, long-double parser). All passed two original-equal
MAINL EXE/MAP rounds. Borland frame-method-4 versus TASM
frame-method-5 metadata differences in x87 wrappers remain disclosed.

The earlier large Boss `cplx2` is **complete and source-linked**
since after514: 22/22 FAR public bodies, 5,598 exact CODE bytes,
original DATA and INITDATA and all 860 logical relocation
sites/targets/addends. Scoped TASM NOSMART produced the two
original direct FAR calls. Final EXE/MAP matches; raw Borland
OBJ/FIXUPP framing is not claimed equal. See
[complete cplx2 review](MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md).

## Next-agent implementation priorities

**Completed Boss: isteldbl (slot 765).** The full 1,947 CODE bytes,
14 DATA bytes and all 112 logical OMF fields are now source-linked at
**after521**. This closes the prior 754-byte partial and its unresolved
near jump. Signed exponent parsing, clamped 32-bit exponent arithmetic,
x87 exponentiation by squaring, range/errno handling and stream flags
are maintained in [isteldbl.asm](../src/mainl/crt/isteldbl.asm).
The typed 80-bit scale constant retains Borland's value; ordinary TASM
`1e2466` conversion is 11 ULP lower. All 85 Borland x87 frame-4 versus
TASM frame-5 differences and raw FIXUPP ordering differences are disclosed;
no raw OBJ record identity is claimed. See the
[complete parser review](MAINL_ISTELDBL_FULL_SOURCE_LINK_AFTER521_NATIVE_REVIEW.md).
The old integer/fraction partials and their proofs remain historical.

**Next arithmetic Boss: h_ldiv.** Natural source recovers all
174 original CODE bytes and 12 near/FAR quotient/remainder
entrypoints; a complete native EXE equals original. But two
same-address public alias pairs are reversed in the MAP, so
**h_ldiv is uncredited as a complete CRT member**.
Retain [its scoped MAP diagnostic](MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md)
and repair genuine symbolic output ordering, not the MAP bytes.

Choose additional large and small CRT work from the **live**
inherited library membership in after521, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after521_work.py istream-long-double-parser
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after521 using only **affected source**
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
The after520 guard **now fails closed** because after521 exists.
All new after521 native outputs and scratch are retained; a fresh
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
