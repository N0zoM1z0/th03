# TH03 reconstruction: current agent handoff (2026-11-07)

This is the CURRENT, compact handoff. The full previous after596 chronology
is frozen in [RE_HANDOFF_ARCHIVE_AFTER596.md](RE_HANDOFF_ARCHIVE_AFTER596.md).
Old after554/after565 instructions and the 258-stage after520 storage audit
are historical baselines, not the latest native source-link or deletion roots.
Read AGENTS.md and the relevant source review, not every historical note.

## Immediate next-agent start

- Inspect git status --short --branch and git log; do not reset or discard
  dirty/untracked/ignored work. At this handoff the last confirmed HEAD was
  94ca133a (Yumemi/CPU); the origin/main relationship can change.
- Use .venv/bin/python scripts/preflight.py when starting or changing the
  toolchain. Check scripts/validate_tracking.py and scripts/progress.py --check.
- For current MAIN native evidence, run the READ-ONLY
  scripts/review_th03_main_yumemi_cpu_after596_work.py.
  For MAINL, run the READ-ONLY
  scripts/review_th03_mainl_score_input_pi_after587_work.py.
  Set DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts and use one allowed CPU
  at nice10. These reviewers do not run full cold replay.
- Wine/Borland writers use .analysis/borland-wine-writer.lock. Preserve the
  candidate-local-attested Japanese targets and existing source inputs.

## What is verified now (different notions of exactness)

| Product | Current verified scope | Formal/remaining boundary |
| --- | --- | --- |
| MAIN | after596 source-native 99-object link; 124,642 program bytes and 1,553 ordered MZ relocations exactly original; standard DOS MZ serializer gives the exact 130,882-byte Japanese file | Direct newer TLINK emits a 132,322-byte MZ with a different header. Source-owned ledger is 459/459 functions and 78,737/78,737 *reviewed authored bytes*, not all program/library bytes or vendor tool identity |
| MAINL (ending) | after587 source-native multi-TU link: entire 67,372-byte Japanese decoded EXE and all 677 ordered relocations exact | Current decoded accepted source remains 220/259 extents, 290 procedures, 37,968 bytes = 17,717 authored + 20,251 library. Historical canonical packed-unit Factory credit 0/250; no whole-game acceptance |
| OP | Retained decoded source publication: 60 extents, 92 procedures, 14,985 reviewed bytes | Canonical packed product/source ownership still open |
| ZUN | Retained decoded publication: 77 extents, 89 procedures/entries and 8,635 reviewed CODE+DATA bytes | Canonical packed product/source ownership still open |

Source-backed whole linked images, raw vendor OMF packet identity, original
historical compiler/linker provenance, physical behavior, source ownership
and canonical packed-file acceptance are DIFFERENT claims. Never upgrade a
reviewed function, normal TLINK equality, or a compact MZ serialization to
formal Factory/whole-product ownership acceptance.

## Retained current native roots — do not delete

- MAIN latest full source graph:
  .analysis/work/main-yumemi-cpu-after596-native-build.json
  and scripts/review_th03_main_yumemi_cpu_after596_work.py.
  The parent chain is after595 results/shots/HUD; after594 entry/round loop;
  after593 player core; after592 nine character callback setup; after591
  collision/386 collmap; after589 large fireball/explosion; after588
  bullet/386 GRCG; after572 four enemy producers; after567 nine BOSSes and
  native held-key input; after568 distinct compact DOS MZ serializer.
- MAINL latest full source graph:
  .analysis/work/mainl-score-input-pi-after587-native-build.json
  and scripts/review_th03_mainl_score_input_pi_after587_work.py.
  Parents: after586 SFX/music/file; after585 input modes/PI raster; after584
  original continue menu segment fix; after583 CG-ROM text; after582 CDG
  loader; after580 root story/stage; after578 score/name-entry; after577
  three 386 CDG blitters; after575 Staff Roll/ending; after573 cutscene;
  after570 natural TASM sound, after569 registration DATA EVEN; earlier
  input/vector/root/CRT and normal C0/linker parents.
- Both independent compiler rounds, consumed scratch source and response
  files, original OMF/EXE/MAP files, logs, JSON receipts, and relevant
  after514/after520 CRT proof chains are live historical evidence.
  Preserve the entire active source-bound DAG, not only last-stage EXEs.

## Historical claims that must not mislead the next agent

- Older docs calling after554/after565 the CURRENT link predate the
  above after587/after596 source stages. The original MAIN full file
  IS now reproducible using the separate standard MZ format stage;
  the direct TLINK compact header is still not a historical match.
- All 22 FAR procedures, 5,598 CODE bytes and 860 logical fixups of
  cplx2 were source-linked in after514. The unchanged pinned
  src/mainl/crt/cplx2.asm header saying "full native link not yet
  established" is STALE; its original OMF frame metadata is still
  different. See docs/MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md.
- The unchanged pinned src/mainl/cutscene.cpp comment that three PI call
  operands "remain open" is STALE: after573 independently recompiles
  all 3,195 CODE bytes and 236 ordered OMF fields, full MAINL exact.
  Avoid editing those SHA-bound historical inputs just to fix a comment.
- The old continue menu's CONTINUE_TEXT pragma is wrong for the original
  CUTSCENE_TEXT object. The corrected alternative after584 links exact;
  negative C++ direct-section control had 696 MZ relocations vs 677.
- A proposed TASM EVEN at the original root joystick two zero-byte
  positions generated 90h rather than the original 00h. This was
  rejected; do not silently replace semantic db 0 source with EVEN.
- A natural C++ call to explosions_hittest in MAIN hitbox compiles as
  direct FAR CALL 9Ah, not original NOP/PUSH CS/near CALL 90h 0Eh E8h.
  Three negative compiler controls are retained under TH03WORK/probe/af590h.
- A later CRT historical baseline after520 reached 728/893 working
  source-linked members and 194,292 original CODE bytes. The older
  isteldbl and h_ldiv notes describe scoped evidence/limitations,
  not a reason to re-credit already completed cplx2 or to claim all
  893 vendor library members were independently source-linked.

## Latest scoped source refresh (after598)

After the frozen after596 MAIN proof, the large Yumemi Extra Attack producer
and Mima Extra Attack producer now share `src/main/player/exatt_entity.hpp`
instead of maintaining two redundant 32-byte record definitions. Two native
TC4/TLINK rounds in the `af598v` overlay preserve all 2,423 CODE bytes,
131 ordered native fixup fields, nine PUBLICs, segment definitions, the
complete original normal MAIN EXE/MAP and 1,553 MZ relocations. See
[review](MAIN_EXATT_ENTITY_SHARED_AFTER598_NATIVE_REVIEW.md) and
`scripts/probe_th03_main_exatt_layout.py`. No additional accepted byte
scope is claimed. Historical after596 receipt source pins remain frozen;
validate new source with the scoped overlay, not by repinning that receipt.

### Rikako state after599

The `af599t` native overlay covers five physically distinct Extra Attack TUs:
Yumemi, Mima, Rikako, shared flight/Reimu prefix and Reimu update. The original
32-byte entity now exposes Rikako's byte +0x17 as a character-specific
`homing_disabled` state without imposing that meaning on other characters.
Both TC4/TLINK rounds reproduce all 4,281 CODE bytes, 250 ordered fields,
24 PUBLICs and unchanged full Japanese MAIN image/relocations. See
[scoped native review](MAIN_RIKAKO_EXATT_HOMING_AFTER599_NATIVE_REVIEW.md).
The `af598v` frozen source refresh remains separately retained. No extra
owned bytes or historical OMF provenance are claimed.

### Character-specific +0x11 after600

`af600b` recompiled eight complete Extra Attack owners (7,442 original CODE
bytes / 484 ordered fields / 42 PUBLICs) in two real TC4/TLINK rounds while
preserving the full MAIN program/1,553 relocations and normalized MAP. Ellen's
+0x11 is a **signed spin delta**, Kotohime's is the **unsigned extra mode**;
Chiyuri uses the same 32-byte entity but currently does not read that byte.
The shared struct keeps both alternatives in a one-byte union and retains the
Rikako +0x17 overlay. See
[after600 native review](MAIN_EXATT_CHARACTER_BYTE11_AFTER600_NATIVE_REVIEW.md).
The historical after599 handoff's 262 count was a transcription error: the
live proof records 250 (after600 includes 484). No new accepted bytes.

### Chiyuri's natural C++ branch after601

`exatt_update_chiyuri` now uses ordinary C++ `if`/`continue` to
skip an inactive paired beam instead of the old manual register/CODE
label branch. The **entire 978-byte Chiyuri object**, all 55 ordered
native fields, four PUBLICs and full Japanese MAIN link pass both
real Turbo C++/TLINK rounds; see
[review](MAIN_CHIYURI_NATURAL_BRANCH_AFTER601_NATIVE_REVIEW.md) and
`.analysis/work/exatt-layout-af601n/report.json`. Historical evidence
remains immutable; no additional accepted byte claim.

### Natural Chiyuri control flow after601

The full Chiyuri beam renderer and paired projectile update no longer need
handwritten ASM for their state==0 jump or phase taper. Native TC4 produces
all original 978 CODE bytes (and original ordered native fields/segdefs) from
the maintained C++ source in two independently compiled and full-linked
rounds, latest `af601e`. The beam renderer still uses the observed AX return
register interface at its shared phase-label boundary. Read
[after601 native review](MAIN_CHIYURI_NATURAL_CONTROL_AFTER601_NATIVE_REVIEW.md)
for the exact accepted and rejected variants. This changes expression
recoverability, not the amount of previously owned target CODE.

### Ten complete Extra Attack producers after602

The current `af602a` source overlay compiles/links all **ten** complete
physical Extra Attack owners: 8,781 original CODE bytes, 563 ordered fields
and 52 PUBLICs in two fresh native TC4/TLINK rounds. Source now shares one
32-byte entity view for Marisa/Kana as well as the prior Ellen/Kotohime/
Chiyuri/Yumemi/Mima/Rikako and Reimu/flight producers. It includes the
original-equal natural Chiyuri control and beam expression. See
[after602 review](MAIN_EXATT_ALL_TEN_AFTER602_NATIVE_REVIEW.md) and the
SHA-bound ignored report; do not treat a historical after596 source-hash
reviewer as suitable for these later changed sources. No extra accepted bytes.

## Remaining priorities for real reconstruction

Prioritize truly unowned byte/OMF/segment scopes or semantics; do not
count historical original functions again because an extra source-forward
TU recompiled them. Check original 16-bit ABI, x87, source-local packing,
segment naming, literal ordered FIXUPPs and target program bytes.
Verify MAINL project ownership and leftover root alignment evidence;
do not equate administrative publication gaps with source-missing bytes.
Clarify actual whole-file/packed-file provenance and original vendor
OMF frames without inventing target opcode arrays or object patches.
Continue OP/ZUN decoded source questions when material. Do not run full
cold replay unless their source/recipe inputs materially changed.

## Storage and historical references

The after520 CRT retention guard covers 258 source stages and 5,760
native files ONLY in its historical prefix. It is not a deletion
authorization for after521–596, MAIN/MAINL source scratch, tools or
pinned targets. See docs/STORAGE_HANDOFF_CURRENT.md and the latest
audited storage addendum. Native after559/after561 BOSS source proof
workspaces are active; do not blanket-prune the .analysis tree.
The after554 maintenance did not delete new native proofs.

History: docs/RE_HANDOFF_ARCHIVE_AFTER596.md;
docs/RE_HANDOFF_ARCHIVE_AFTER554.md; docs/MAINL_WORKING_CRT_RECOVERY_INDEX.md.
Run only affected review and tracking/progress checks, then git diff --check;
commit substantial changes as gpt-web: xxx. Do not push unless asked.
