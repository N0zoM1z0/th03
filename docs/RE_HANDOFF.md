# TH03 — current agent handoff (2026-11-06; after536 baseline refinements)

**Start with this file and actual Git state.** Check `git status -sb`
and `git log -8 --oneline`. Latest source-bound CRT working evidence:
**after533**. Latest independently protected-storage audit:
**after520**. The former 1,494-line handoff is preserved in
[historical archive](RE_HANDOFF_ARCHIVE_PRE_CLEANUP_AFTER520.md).
Latest read-only baseline ownership audit: **after534**; no new native build.
Latest source-startup/native-link evidence: **after535**. Its two native
TASM/TLINK rounds reuse the unchanged after533 CRT libraries.
Latest native composition: **after536**, refining existing `h_padd` PUBLIC
chronology and `ioerror` GROUP ownership; zero new members or CODE credit.

## Current, independently verified Japanese MAINL CRT

| Evidence | Current after536 |
| --- | ---: |
| Original Borland CL.LIB slots | **893** |
| Explicit incremental CRT source members | **889** |
| Earlier baseline source members, now traced | **4** |
| Source-bound union of original compiler-library slots | **893/893** |
| Original-equal maintained-source CODE-segment bytes, union | **209,272** |
| Additional source-generated startup | **625 CODE extent / 144 DATA** |
| Latest native assembly/TLIB/TLINK rounds | **2; whole EXE byte-exact** |
| Native MAP | **80,967 bytes; one alias tie + zero-BSS owner reviewed** |
| Original decoded Japanese MAINL EXE / ordered MZ relocations | **67,372 bytes / 677** |
| Formal Factory canonical packed-file unit acceptance | **0/250** |

Latest native root:
`.analysis/work/mainl-after536-baseline-refinements-build.json`

SHA-256: `c2b2853f4bddda4a73e2e01c8a78fe407c6a32e35b0f41ed8a6217f306de831d`.

Producer/reviewer: `scripts/build_th03_mainl_after536_work.py` and
`scripts/review_th03_mainl_after536_work.py`. The refined TUs are
`src/mainl/crt/h_padd_link.asm` and `ioerror_link.asm`; frozen cold owners stay
unchanged. `h_padd` now matches the original six-export ordered symbol payload
through the pinned compatible emitter. `ioerror` now matches the literal GROUP;
its five-field order and PUBLIC order still differ. All 178 CODE / 91 DATA bytes
remain original-equal, with **zero new source credit**. All 891 other member
programs and all 893 positions stay unchanged; after535's source C0 is reused.
Complete EXE and 677 ordered MZ relocations are exact. The raw MAP differs from
the historical retained MAP only by `F_PADD@`/`PADD@` display order at `0000:3182`
and the zero-sized `ioerror` BSS owner at existing `0E3F:286A`. Every other MAP
byte/address/size/flag is equal. No artifact is rewritten or broadly normalized.
See the [baseline refinement review](MAINL_BASELINE_REFINEMENTS_AFTER536_NATIVE_REVIEW.md).
New raw vectors/logs use **af536f-baseline-refinements-**; sources, recipes and
both responses remain in `probe/af536f`. The first zero-BSS MAP-comparison stop,
its raw vectors/logs, original `probe/af536e` and 21 SHA-inventoried snapshots
remain; earlier four bounded probes remain too. Do not replace the historical
MAP or require it to be raw-equal to this reviewed native MAP.

Unchanged source-startup root:
`.analysis/work/mainl-after535-startup-build.json`

SHA-256: `9a3592185b880d53d344cdd3f0cf0c0b13534d186833e7d739f673edd2e61d6b`.

Producer/reviewer: `scripts/build_th03_mainl_after535_work.py` and
`scripts/review_th03_mainl_after535_work.py`. The maintained supplier-derived
`src/mainl/startup/c0.asm` preserves all 17 segments, 623 initialized CODE bytes,
a 2-byte uninitialized CODE cache, 144 DATA and 128 reserved STACK bytes.
All 58 full relocation fields agree at their sites; original/native FIELD
and PUBLIC order differ and remain explicitly recorded. No original OBJ
identity, formal acceptance or authored-game credit is claimed. Complete EXE/
MAP and 677 ordered MZ relocations match. See the
[startup review](MAINL_LARGE_STARTUP_AFTER535_NATIVE_REVIEW.md).
Successful raw vectors/logs use **af535e-startup-** paths. `probe/af535e`
retains actual consumed source/recipe/response. The first link's module-name
case correction, eleven SHA-inventoried snapshots, original `probe/af535d`,
raw vectors/logs and earlier three probes all remain retained.

Earlier 889-member incremental composition root (retained):
`.analysis/work/mainl-after533-locale-tables-aliases-twelve-build.json`

SHA-256: `45912144bddb0d0910472133f85055d3b16825bc0130affabebdd1b8e115d450`.

Producer: `scripts/build_th03_mainl_after533_work.py`,
mode `locale-tables-aliases-twelve`.
Independent reviewer: `scripts/review_th03_mainl_after533_work.py`.
This stage uses TASM 5.0 and native TLIB/TLINK. The unchanged after532 parent
retains its pinned compatible-emitter attestation and five math PUBLIC payloads.

Latest additions: six DATA owners `clocale`, `clower`, `cupper`, `ctype`,
`syserrls`, `MBCTYPE`, plus four empty module shapes and two alias modules:
**4,382 DATA bytes, 62 literal FAR fields and 73 literal ordered ALIAS records**.
There is **zero new CODE/BSS/INITDATA credit or frame exception**. Character
maps are generated from 8-bit rules; locale/error objects use typed fields,
fixed-capacity strings and symbolic pointers. See the
[12-member review](MAINL_LOCALE_TABLES_ALIAS_12_AFTER533_NATIVE_REVIEW.md).
The stage binds `char_tables.inl` and unchanged `locale_fields.inc`. Corrected
vectors/logs use **af533b-** paths and `probe/af533b`; the old local-name/EQU
collision branch, original `probe/after533`, logs and SHA-inventoried source/
recipe/include snapshots remain retained. The aliases are semantic owners,
not empty functions. Original iostream **696–892 (197 members)** and
string/regexp **384–426** blocks remain source-linked.
After532's five arithmetic helpers/typed storage still bind original PUBLICs,
tool attestation, two FILE includes and seven literal fields. After531 retains
seven stdio gaps; after530 retains its DDVT layout and arithmetic gap; after529
retains original storage and twelve console gaps. After528's sixteen loader
gaps and after526's 12 x87 / 2 near-call gaps remain bound. All historical
failed branches remain. The four context entries already have source files/
older evidence; after534 now traces their actual adoption in both latest
libraries. This adds **zero new members/bytes**. See the
[baseline ownership audit](MAINL_BASELINE_OWNERSHIP_AFTER534_REVIEW.md).
The union is source-bound, not an assertion of literal original OBJ equality:
the earlier `h_padd` PUBLIC and `ioerror` GROUP gaps are refined at after536;
`ioerror` PUBLIC/FIXUPP ordering still differs.

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

**Next work:** prioritize actual product coverage over restoring unlinked
library members. A concrete next native question is whether the source-generated
C0 / complete CRT can replace the same installed `C0L.OBJ` / `CL.LIB` in **OP**.
Read `.analysis/work/op-build.json` and the current OP source adapter first:
the retained cold pair is complete/repeated with 330 source files, and
`TH03OP/obj/th03/op.@l` explicitly uses `c0l.obj` and `cl.lib`. Verify original
library hash/ABI, current OP source bindings and actual selected member/layout
coverage before reusing this library. Only affected TLINK/native work is needed;
do not rerun the whole OP cold graph. Common-source ownership across products
must be proved, not inferred from the names or counted as new authored code.

`ioerror`'s five-field order and startup's 58-field order remain explicit gaps;
the bounded C/alias/two-pass ioerror probes did not close them. Do not repeat
those unchanged attempts or call them literal-exact from EXE equality. The current MAIN
ledger has **106 entries, all marked exact**; that is not proof of the unknown
whole-game denominator, and none should be repeated as a missing ledger unit.
MAINL's startup is now source-generated. Its response still
lists `EMU.LIB` and `MATHL.LIB`, but the current detailed MAP has **no member
names contributed by either**; do not recover those entire unlinked libraries
just to increase counts. All non-CL MAP contributors are the startup and the
existing project objects. Consult actual product source/tracking/native evidence
before claiming a missing bounded unit. Do not overwrite frozen cold sources or replay
the whole graph. The historical h_padd alias diagnostic is retained, with the
same-address tie now explicitly reviewed by after536.
Formal canonical packed-unit acceptance is still 0/250; library source
ownership is not whole-product acceptance. Avoid recounting closed CRT work.

**Extending after536:** invoke its independent reviewer once, then read its
actual retained pair and the unchanged after535 source-startup pair. The
reviewer already validates the full source/receipt DAG, all include/alias/raw
frame profiles and compatible-emitter attestations; do not separately replay
every ancestor. Preserve the two refined objects and explicitly reviewed MAP
when constructing the next library. Starting only from after533 would silently
drop these refinements. All 893 slots now have source owners: old candidate
lists are not missing-source work queues.

## Scoped commands for the next agent

~~~sh
git status -sb
git log -8 --oneline
.venv/bin/python scripts/preflight.py
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after536_work.py
.venv/bin/python scripts/progress.py --check
.venv/bin/python scripts/validate_tracking.py
git diff --check
~~~

Extend from verified after536 using only **affected source**
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
All new after521–after533 native outputs and scratch are retained; a fresh
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
