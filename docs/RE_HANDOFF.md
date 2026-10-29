# TH03 handoff

## Current direction and checkpoint

The user's 2026-10-28 instruction is **exact-first reconstruction**. Use direct
local tools and affected native checks. Allocation/null-pointer/input-domain
matrices, large emulator specifications and routine full CI are not per-unit
gates. Reuse an unchanged native cold pair rather than rebuilding every turn.

OP scanner now has complete function ownership at0BEB:0304:417 CODE bytes/
115 instructions/42 native DGROUP WORD fields/no MZ entries. It returns far
without arguments/cleanup. Both direct TC4 and unmodified compiler-S/TASM emit
all417 bytes without the legacy codestring. Their different empty DGROUP member
orders and actual field streams are reviewed independently. Source/header
consumption, both OP MAP tables, full function bytes, nine BIOS group reads and
all direct branch boundaries match. See [input review](OP_INPUT_NATIVE_REVIEW.md).

The legacy byte at04A5 remains unowned. Native compiler ASM has no automatic
trailer. Selected-object links without it have4861 loaded differences; `-P`
does not help. A following-PI WORD alignment annotation control leaves only
00-vs90 at04A5, but still fails ordered relocation equality. It is diagnostic,
not a product fix. No source/OBJ patch, invented padding or whole-TU/product
source acceptance is implied. Original non-acceptance probe records are intact;
this later proof accepts the complete independent function, never the trailer.

CDG drawing retains two complete module extents382/114:3 far Pascal pop6 bodies
493 plus3 separately reviewed ordinary outer EVEN bytes. All19 fields/2 MZ
entries/12 own-CS immediate-word writers match. See [drawing review](OP_CDG_DRAW_NATIVE_REVIEW.md).
CDG loading/text retain1206 CODE/6 procedures/41 fields/27 MZ entries, with real
TC4/TLINK bridges and separate OP addresses. See [shared review](OP_SHARED_NATIVE_REVIEW.md).
Score retains501 CODE/5 procedures and filename DATA11; hi BSS206 adds no file
bytes. Title retains902 CODE/5 procedures; DATA31 is open. Selection retains
3013 CODE/19 procedures; DATA227/BSS23 remain open. Music retains2244 CODE/
14 procedures and DATA1008; BSS1060 adds zero file bytes. Follow the linked
reviews for the original unchecked behavior and ABI details.

All49 previously accepted OP owners and their native source/tool/output/cold
bindings are unchanged. MAINL/ZUN shared helper closures have identical ASTs;
all other proof inputs and complete current native source/staging/output graphs
(938/29 outputs) were checked. Only their shared-module binding changed, with
no audit/witness/time refresh or runtime replay. Receipt:
`.analysis/work/input-native-shared-binding.json`.

Current function evidence: `.analysis/work/input-native-review.json`.
Emitter/layout diagnostics: `.analysis/work/input-layout-diagnostic.json`.
OP accepts50 extents/14061 file-backed bytes. Only selected input/adjacent-PI
emitter and context-link experiments ran; no full native cold replay or ancestor
runtime chain was run. All maintained product sources and native products stay
unchanged. `.analysis/work/input_scope_refresh.py` refreshed the verified OP
region/summary with the existing renderer, preserving every non-OP byte.
Synthetic unaccepted non-OP render branches are discarded. The full generator
still calls ancestor runtime audits; no full generator `--check` is claimed.

Validation:45 focused input/drawing/shared/score/title/selection/current-
acceptance/progress checks PASS, plus tracking and bounded progress verification.
`git diff --check` is clean.

## Verified current source scopes

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 50 extents / 84 procedures / 12,555 CODE + 1,506 DATA bytes | Open |
| MAINL | 97 extents / 102 procedures / 16,138 CODE + 224 DATA bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes22 separately proved inline compiler bytes and3 ordinary outer
ASM EVEN bytes; these layout bytes are not extra procedures. ZUN accepts8,635
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
The scanner acceptance also consumes `.analysis/work/input-nostring.json`,
`input-nostring.obj` and `input-assembly.obj`; preserve these actual proof inputs
and their diagnostic ASM/logs/scripts.
Keep `scripts/lib/zun.py` unchanged unless deliberately updating its frozen MAIN
binding; OP's native builder is also shared by MAINL/ZUN. Preserve actual current
inputs. Obsolete logs and verification history may be deleted.

No native reconstruction process is left running at this checkpoint. Start with Git,
`scripts/preflight.py` and the current review. Remaining OP work can begin with
the unowned input trailer or other unowned producers; selection
DATA227/BSS23 and title DATA31 also remain open. Inspect actual current
OMF/MAP boundaries before choosing a scope. TH04 at `/home/pentester/coding/codex_ida/th04-reconstruction/th04`
is an authorized source reference, not a replacement target or build dependency.

The unchanged-graph reuse guard rejects changed source/verifier inputs. Review
affected native changes rather than refreshing historical runtime receipt hashes.
Generated progress summarizes current scope; historical runtime matrices do
not add source-exact credit. Preserve current receipts and actual native inputs.
