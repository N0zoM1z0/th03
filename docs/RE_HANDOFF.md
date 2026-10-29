# TH03 handoff

## Current direction and checkpoint

The user's 2026-10-28 instruction is **exact-first reconstruction**. Use direct
local tools and affected native checks. Allocation/null-pointer/input-domain
matrices, large emulator specifications and routine full CI are not per-unit
gates. Reuse an unchanged native cold pair rather than rebuilding every turn.

Score file CODE is now complete across `op_02.cpp`165 and `scoredat.cpp`229:
4 procedures/394 CODE bytes/33 native CODE fields/7 literal MZ relocations.
The prior loader107 remains separate, making5 accepted score procedures/501
CODE total. Initialized DATA11 has a16-bit near filename pointer and one native
WORD fixup, without a MZ entry. `hi` is206 bytes of BSS, adding no file-backed
credit. Keep the BYTE cleared enum, checksum over204 score bytes and backward
encryption of hi offsets203..0 (including checksum). File calls remain unchecked;
rank multiplication wraps16 bits before widening. IRAND42 stays vendor context.
See [score review](OP_SCORE_NATIVE_REVIEW.md).

Title animation now has complete CODE ownership across its actual TC4
`op_main.cpp` producer:5 procedures/902 CODE bytes/97 native fields/53 literal
ordered MZ relocations. Title808 and column94 are separate accepted extents.
The old three-byte column mismatch is historical: today's maintained symbolic
raster source already emits all94 target bytes. No codegen fix is claimed.
Native DGROUP is group1 here; CODE has no OMF group. Preserve genuine near
selection calls, far library calls and the column's compiler-owned BP/SI/DI
saves/Pascal pop2. DATA31 remains unaccepted. See [title review](OP_TITLE_NATIVE_REVIEW.md).

Character selection retains complete CODE ownership across `selhelp.cpp`155
and `seltail.cpp`2858:19 procedures/3013 CODE/287 fields/91 literal relocations.
The107-byte loader,48-byte unlock helper and2858-byte tail are separate extents;
the old2906-byte aggregate adds no duplicate credit. Native callbacks are far
DWORD pointers despite their typedef name. Private DATA227/BSS23 and the next
alignment byte remain unaccepted. See [selection review](OP_SELECTION_NATIVE_REVIEW.md).

Music Room retains CODE2244/14 procedures and DATA1008. Its BSS1060 has reviewed
layout and adds zero file-backed bytes; preserve the10-point array's40-byte
declaration. See [Music Room](OP_MUSIC_MENU_REVIEW.md).

OP retains old34-owner observations from immutable `6cfa85f` under unchanged
native bindings; all42 owners accepted before this turn are unchanged. New score
scopes are checked independently. MAINL/ZUN shared imports and their helper
closure have identical ASTs and all other proof inputs are unchanged; only the
shared-module binding was updated. Their audit, gate witnesses and observation
times were preserved. Receipt: `.analysis/work/score-native-shared-binding.json`.

Current score evidence: `.analysis/work/score-native-review.json`. OP publication
accepts45 extents/11942 file-backed bytes. Native source/tool/staging/output/cold
and packed-target bindings are unchanged. No native build was repeated. The OP
score check did not invoke old score runtime models. Generated progress still
invokes MAINL/ZUN runtime audits indirectly through `status.py`; do not describe
that generator as avoiding all ancestor runtime checks. Validation:34 focused score/title/selection/current-
acceptance/progress checks PASS; tracking and progress regeneration/check PASS.
`git diff --check` is clean.

## Verified current source scopes

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 45 extents / 74 procedures / 10,436 CODE + 1,506 DATA bytes | Open |
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
shared CDG loader593, graph_putsa_fx613 or other unowned substantial producers;
selection DATA227/BSS23 and title DATA31 also remain open. Inspect actual current
OMF/MAP boundaries before choosing a scope. TH04 at `/home/pentester/coding/codex_ida/th04-reconstruction/th04`
is an authorized source reference, not a replacement target or build dependency.

The unchanged-graph reuse guard rejects changed source/verifier inputs. Review
affected native changes rather than refreshing historical runtime receipt hashes.
Generated progress summarizes current scope; historical runtime matrices do
not add source-exact credit. Preserve current receipts and actual native inputs.
