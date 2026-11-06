# TH03 — current agent handoff (2026-11-06; after532)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after532**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).

## Current, independently verified Japanese MAINL CRT

| Evidence | Latest after532 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Explicit incremental CRT source members | **877** |
| Original-equal maintained-source CODE-segment bytes | **209,016** |
| Baseline/context members retained | **16** |
| Independent assembly/TLIB/TLINK rounds | **2; complete EXE/MAP byte-exact** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest root:
`.analysis/work/mainl-after532-math-runtime-storage-twenty-one-build.json`

SHA-256: `6c58f141f33277f5903521492056cb45a1473f6fe1445eb73740a3a0bf2f5307`.

Producer: `scripts/build_th03_mainl_after532_work.py`,
mode `math-runtime-storage-twenty-one`.
Independent reviewer: `scripts/review_th03_mainl_after532_work.py`.
Five arithmetic members use the pinned compatible JWasm emitter; sixteen
storage members use TASM 5.0. Native TLIB/TLINK and the older after522 h_ldiv
proof remain unchanged.

Latest additions: `h_lrsh`, `h_lursh`, `h_psbh`, `h_psbp`, `h_spush`,
`files`, `files2` and fourteen scalar/BSS owners: **176 executable CODE /
468 DATA / 8 BSS bytes**. All seven ordered FIXUPPs match literally;
**zero new frame exceptions**. Original ordered PUBLIC payloads match for
all five helpers through the pinned compatible-emitter profile.
See the [21-member review](MAINL_MATH_RUNTIME_21_AFTER532_NATIVE_REVIEW.md).
The typed FILE table owns twenty original 20-byte records and five symbolic
self tokens; descriptor states and runtime defaults retain WORD/DWORD widths.
The stage binds unchanged `stdio_layout.inc` and `stdio_tmp.inc`, plus tool/
profile/attestation-driver hashes. All native vectors, logs and candidate
branches remain retained. Original iostream **696–892 (197 members)** and
string/regexp **384–426** blocks remain source-linked.
The after531 proof retains three includes and seven raw stdio frame gaps;
after530 retains five includes, word-aligned DDVT data and its arithmetic gap.
After529 retains original LIDATA/near-startup storage, twelve console gaps and
the old h_padd alias diagnostic. After528's sixteen loader gaps and after526's
12 x87 / 2 near-call gaps remain bound. All failed historical branches remain.
Counts cover explicit incremental receipts; sixteen context entries include
four existing source owners and are not a list of missing functions.

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

**Next live work:** six DATA/table owners: `clocale` (slot 124, 2,657 bytes),
`clower` (125, 256), `cupper` (126, 256), `ctype` (127, 257), `syserrls`
(318, 699), `MBCTYPE` (585, 257). Recover typed locale/error metadata and
character-class ranges from actual OMF, including all ordered pointer fields.
Six zero-payload/marker owners remain: `delf`, `delfarry`, `nearheap`,
`nheapchk`, `MBCS`, `JSTR`. Inspect their actual alias/metadata records;
zero CODE bytes alone do not prove an empty semantic owner.
The four remaining CODE context entries `h_llsh`, `h_padd`, `ioerror` and
`lseek` already have source files/older evidence. Inspect actual owner receipts
before changing or counting them. Never overwrite frozen cold source inputs.

**Extending after532:** use `parent.SOURCE_PATHS` and
`parent.original_member_programs()`. Verify 21 TUs, two FILE includes,
`parent.assembler_attestation()` and the exact five-helper PUBLIC payloads.
All seven fields are literal-equal; preserve the zero-gap transcript check.
Validate complete DATA/BSS coverage and all 197 iostream members. Retain
after531's three includes/seven stdio gaps, after530's five includes/arithmetic
gap, after529's storage/console checks and after528's loader checks.

Choose additional large and small CRT work from the **live**
inherited library membership in after532, not stale old
candidate lists. Historical `stsetf1`/ios::setf was already
source-linked at after483; do not double-count it.
Recheck original target evidence rather than assuming old
documents or assembly attempts are correct.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after532_work.py math-runtime-storage-twenty-one
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after532 using only **affected source**
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
All new after521–after532 native outputs and scratch are retained; a fresh
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
