# TH03 — current agent handoff (2026-11-06; after531)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after531**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after531 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Explicit incremental CRT source members | **856** |
| Original-equal maintained-source CODE-segment bytes | **208,840** |
| Baseline/context members retained | **37** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after531-file-stream-fallback-twenty-five-build.json`

SHA-256: `5bf827de0862526924dc01689f3204e6405b2eea6fb28b85495935661fb617d0`.

Producer: `scripts/build_th03_mainl_after531_work.py`,
mode `file-stream-fallback-twenty-five`.
Independent reviewer: `scripts/review_th03_mainl_after531_work.py`.
This stage uses TASM 5.0 / native TLIB/TLINK and preserves after522's
pinned compatible-emitter h_ldiv member unchanged.

Latest additions: eighteen DOS/stdio/file wrappers, six remaining stream
members and `cvtfak`: **1,519 executable CODE / 67 DATA / 82 BSS bytes**,
66 ordered logical fields. Twenty members have literal FIXUPP equality;
five have seven explicitly retained near-stdio TARGET/CODE frame gaps.
The diagnostic module retains all three DATA segments and four symbolic near
fallback pointers. See the
[25-member review](MAINL_FILE_STREAM_25_AFTER531_NATIVE_REVIEW.md).
Original iostream slots **696–892 (197 members) now all source-link**, verified
against actual native library membership in both rounds. The stage binds
unchanged `stdio_layout.inc` and `crt_errno.inc`, plus new `stdio_tmp.inc`
for the original WORD temporary number at FILE+16. Original string/regexp
slots **384–426** remain closed. All new native vectors/logs are retained.
The after530 proof still binds five includes, word-aligned DDVT segments
and its one arithmetic-frame gap. Its old byte-alignment draft and **af530b-**
vectors remain. After529 retains two uninitialized near-startup bytes, LIDATA,
twelve console-frame gaps and the old h_padd alias diagnostic. After528's
sixteen loader gaps and after526's 12 x87 / 2 near-call gaps remain bound.
`h_padd.asm` and other old cold-source owners remain unchanged. Counts cover
explicit incremental receipts; the 37 context entries include existing
baseline owners and are not a list of missing functions.

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

**Next live CODE candidates:** `h_lrsh` (slot 69, 32 bytes), `h_lursh`
(70, 33), `h_psbh` (74, 32), `h_psbp` (75, 40) and `h_spush` (76, 39).
These are the five remaining context CODE members without an existing TU.
Preserve register/near/far ABI and review same-address PUBLIC/MAP chronology;
TASM's export hash enumeration previously required a pinned compatible emitter
for h_ldiv. `h_llsh`, `h_padd`, `ioerror` and `lseek` already have source owners;
inspect existing receipts and never overwrite or double-count frozen inputs.
Remaining context DATA work includes `clocale` (2,657 bytes), `syserrls` (699),
`files` (400), lower/upper/ctype/mbctype tables, runtime scalar/BSS owners and
empty marker members. Inspect typed metadata/storage and actual original OMF.

**Extending after531:** use `parent.SOURCE_PATHS` and
`parent.original_member_programs()`. Verify all 25 TU hashes, three include
hashes, full initialized/uninitialized storage across every segment, seven raw
stdio frame descriptions and complete iostream slots 696–892 membership.
The original compiler CL.LIB hash is independently bound from the carrier.
Retain after530's five includes and arithmetic-frame check, after529's storage/
console checks and after528's two includes/sixteen loader-frame checks.

Choose additional large and small CRT work from the **live**
inherited library membership in after531, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after531_work.py file-stream-fallback-twenty-five
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after531 using only **affected source**
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
All new after521–after531 native outputs and scratch are retained; a fresh
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
