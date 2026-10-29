# TH03 handoff

## Current direction and checkpoint

The user's 2026-10-28 instruction is **exact-first reconstruction**. Use direct
local tools and affected native checks. Allocation/null-pointer/input-domain
matrices, large emulator specifications and routine full CI are not per-unit
gates. Reuse an unchanged native cold pair rather than rebuilding every turn.

Shared CDG/text now have complete OP native CODE ownership:6 procedures/1206
bytes/41 fields/27 literal ordered MZ relocations across the actual `cdg_load.cpp`
593 and `grppsafx.cpp`613 producers. Both have zero private DATA/BSS. The renderer
is a complete226-instruction far Pascal pop10 function; CDG cleanup is8/8/6/6/2.
Four forward same-CS far calls use normal TLINK NOP/PUSH CS/CALL bridges; the
backward bridge is already emitted by TC4. Comparison buffers never patch an
object. Shared MAINL native shape metadata is reused, but every linked address
and raw byte is independently checked in OP. See [shared review](OP_SHARED_NATIVE_REVIEW.md).

Score CODE remains complete:encode165 + codec229 + prior loader107 =5 procedures/
501 CODE. Filename DATA11 contains a16-bit near pointer, without a MZ entry.
`hi` BSS206 adds zero file-backed credit. Preserve BYTE enums, encrypted checksum,
16-bit size arithmetic and unchecked file calls. IRAND42 stays vendor context.
See [score review](OP_SCORE_NATIVE_REVIEW.md).

Title CODE remains complete:5 procedures/902 bytes, separate title808/column94
owners. The old three-byte column mismatch is historical; today's symbolic
source already emits all94 bytes. DATA31 remains open. See [title review](OP_TITLE_NATIVE_REVIEW.md).

Selection retains CODE3013/19 procedures across selhelp155/seltail2858. The
loader107, unlock48 and tail2858 are separate; the old2906 aggregate adds no
credit. Callbacks are far DWORD pointers despite their typedef name. Private
DATA227/BSS23 and following alignment stay open. See [selection review](OP_SELECTION_NATIVE_REVIEW.md).
Music Room retains CODE2244/14 procedures and DATA1008; reviewed BSS1060 adds
zero file bytes. Preserve the10-point array's40-byte declaration. See [Music Room](OP_MUSIC_MENU_REVIEW.md).

OP retains the old34-owner observations from immutable `6cfa85f`; all45 owners
accepted before this turn are unchanged. New shared scopes are independent.
MAINL/ZUN shared imports/helper closure have identical ASTs and all other proof
inputs are unchanged. Their complete current source/staging/native output graphs
(938/29 outputs) were revalidated; only the shared-module binding changed.
Audit, gate witnesses and observation times were preserved. Receipt:
`.analysis/work/shared-native-shared-binding.json`.

Current evidence: `.analysis/work/shared-native-review.json`. OP accepts47 extents/
13148 file-backed bytes. No native rebuild or ancestor runtime replay was run.
The full progress generator still invokes MAINL/ZUN runtime audits through
`status.py`; it was not used this turn. Instead `.analysis/work/shared_scope_refresh.py`
uses the existing renderer for the verified OP region/summary only and retains
all non-OP output literally. Its synthetic unaccepted non-OP render branches
are discarded, never used as acceptance. The native-binding receipt records the
bounded refresh. No full generator `--check` is claimed.

Validation:38 focused shared/score/title/selection/current-acceptance/progress
checks PASS; tracking and OP-only generated-region verification PASS.
`git diff --check` is clean.

## Verified current source scopes

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 47 extents / 80 procedures / 11,642 CODE + 1,506 DATA bytes | Open |
| MAINL | 97 extents / 102 procedures / 16,138 CODE + 224 DATA bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes22 separately proved inline compiler bytes. ZUN accepts8,635
CODE+DATA bytes: authored2,179, original ASM1,390, library5,066. Whole-game
source/function denominators and the completion percentage remain unknown.

OP/MAINL/ZUN source-only cold pairs match complete decoded and canonical DIET
`-B` stored targets, while retaining unowned reference/vendor context. MAIN
repeats100 outputs/98 project objects and all1,553 ordered relocations; CODE
alignment at EC2D (90 vs00) and MZ headers remain open. Its original VS module
is explicit vendor context. Canonical packed-unit source credit stays separate.

## Retained inputs and next work

Preserve fixed Japanese targets/assets (`candidate-local-attested`), the local
Wine prefix, TC4/TASM/JWasm, `.tools/ghidra`, `.tools/jdk`, `.venv`,
`_reference/ReC98` and `ghidra-project/`. Keep one working build per product:
TH03WORK, TH03OP, TH03ML and TH03ZUN. Actual source input:
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.
Keep `scripts/lib/zun.py` unchanged unless deliberately updating its frozen MAIN
binding; OP's native builder is also shared by MAINL/ZUN. Preserve actual current
inputs. Obsolete logs and verification history may be deleted.

No reconstruction job or ongoing goal is left running. Start with Git,
`scripts/preflight.py` and the current review. Remaining OP work can begin with
shared CDG drawing382/noalpha114 or input scanner417; selection DATA227/BSS23
and title DATA31 also remain open. Inspect actual current
OMF/MAP boundaries before choosing a scope. TH04 at `/home/pentester/coding/codex_ida/th04-reconstruction/th04`
is an authorized source reference, not a replacement target or build dependency.

The unchanged-graph reuse guard rejects changed source/verifier inputs. Review
affected native changes rather than refreshing historical runtime receipt hashes.
Generated progress summarizes current scope; historical runtime matrices do
not add source-exact credit. Preserve current receipts and actual native inputs.
