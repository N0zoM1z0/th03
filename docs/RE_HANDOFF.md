# TH03 — current agent handoff (2026-11-06; after520)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after520**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after520 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **728** |
| Original-equal maintained-source CODE bytes | **194,292** |
| Original vendor members retained for context | **165** |
| Independent TASM/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after520-fstreambase-virtual-setbuf-ios-state-build.json`

SHA-256: `f32c534f42d520f2c07a3acce769857d01ef310c04c00b419b585bf650994d8e`.

Producer: `scripts/build_th03_mainl_after520_work.py`,
mode `fstreambase-virtual-setbuf-ios-state`.
Independent reviewer: `scripts/review_th03_mainl_after520_work.py`.
Focused test: `tests.test_mainl_after520_work`.

Four complete additions since after516: `istedbl` (124 CODE,
double input), `isteflt` (157 CODE, float input),
`fsopen` (105 CODE, fstreambase open) and `fssbuf`
(91 CODE, virtual setbuf). All passed two complete original-equal
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

**Large Boss: isteldbl (slot 765).** The original ten-byte
long-double parser has **1,947 CODE bytes**. Its maintained
[754-byte partial source](../src/mainl/crt/isteldbl_fraction_prefix_partial.asm)
recovers sign, real streambuf refill, EOF, integer/fraction digit loops
and x87 accumulation. **752/754 CODE bytes** equal original;
only CODE+30/+31 remain a genuinely unresolved near jump to
original CODE+0x78F. All 27 original prefix OMF symbolic fields
match; 15 Borland x87 frame-4 differences remain, plus one
TASM relocation for the unresolved jump. **1,193 CODE bytes**
including exponent parsing, normalization and error paths remain.
This **is not a complete source-linked CRT member**.
See [partial parser review](MAINL_ISTELDBL_FRACTION_PREFIX_LARGE_BOSS_NATIVE_REVIEW.md)
and `tests.test_isteldbl_fraction_prefix_partial_native`.

**Other arithmetic Boss: h_ldiv.** Natural source recovers all
174 original CODE bytes and 12 near/FAR quotient/remainder
entrypoints; a complete native EXE equals original. But two
same-address public alias pairs are reversed in the MAP, so
**h_ldiv is uncredited as a complete CRT member**.
Retain [its scoped MAP diagnostic](MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md)
and repair genuine symbolic output ordering, not the MAP bytes.

Choose additional large and small CRT work from the **live**
inherited library membership in after520, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after520_work.py fstreambase-virtual-setbuf-ios-state
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after520_work tests.test_mainl_after520_storage_cleanup tests.test_isteldbl_fraction_prefix_partial_native -v
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after520 using only **affected source**
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
Further after520 dry-run now reports zero eligible files.
The after520 guard **intentionally fails closed** after a new
after521+ stage, and must be independently repinned before
later deletion. The old after439/after388 cleanup guards
remain frozen historical audits; do not bypass them.

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
