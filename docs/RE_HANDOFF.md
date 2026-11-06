# TH03 — current agent handoff (2026-11-06; after522)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after522**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after522 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Complete original CRT source-linked members | **730** |
| Original-equal maintained-source CODE bytes | **196,413** |
| Original vendor members retained for context | **163** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after522-long-divmod-original-public-order-build.json`

SHA-256: `e581b1a20a5eca64b3cf1524f8e8b53fa6327ab1fbfb7d4efd68452b6fdecaca`.

Producer: `scripts/build_th03_mainl_after522_work.py`,
mode `long-divmod-original-public-order`.
Independent reviewer: `scripts/review_th03_mainl_after522_work.py`.
This stage uses pinned JWasm compatible OMF plus original TLIB/TLINK;
original assembler identity is not claimed.

Six complete additions since after516: `istedbl` (124 CODE,
double input), `isteflt` (157 CODE, float input),
`fsopen` (105 CODE, fstreambase open) and `fssbuf`
(91 CODE, virtual setbuf), plus the complete `isteldbl`
(1,947 CODE / 14 DATA, long-double parser) and `h_ldiv` (174 CODE,
twelve near/far division/modulus entries). All passed two original-equal
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

**Completed arithmetic Boss: h_ldiv (slot 67).** All 174 original CODE
bytes and twelve exports now source-link with exact complete EXE/MAP at
**after522**. The source PUBLIC declarations preserve the original ordered
name/offset/type payload. Pinned JWasm emits that chronology; TASM 5's hash
enumeration had reversed two MAP alias ties. No object/MAP patch is used.
The [complete alias-order review](MAINL_H_LDIV_FULL_SOURCE_LINK_AFTER522_NATIVE_REVIEW.md)
records the compatible emitter, original-zero FIXUPPs and two native rounds.
The older [TASM-only diagnostic](MAINL_H_LDIV_TWELVE_API_MAP_ALIAS_PROBE.md)
remains historical and does not describe the after522 result.

**Next live candidates:** largest remaining CRT members are `oprcall2`
(slot 414: 96 + 251 CODE), `copy2` (387: 96 + 237), `ctor2`
(390: 96 + 233), and `oprcall1` (413: 96 + 232). Their original two CODE
segments and shared 96-byte local helpers need explicit ownership/layout,
not a one-segment flattening. Other related stream manipulators
`mnrstflg`, `mnsetflg`, `mnsetw`, `mnsfill`, `mnsprec` remain vendor members.
These candidates were read from the actual inherited library after522.

Choose additional large and small CRT work from the **live**
inherited library membership in after522, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after522_work.py long-divmod-original-public-order
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after522 using only **affected source**
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
All new after521/after522 native outputs and scratch are retained; a fresh
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
