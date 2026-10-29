# TH03 handoff

## Current direction and checkpoint

The user's 2026-10-28 instruction is **exact-first reconstruction**. Use direct
local tools and affected native checks. Allocation/null-pointer/input-domain
matrices, large emulator specifications and routine full CI are not per-unit
gates. Reuse an unchanged native cold pair rather than rebuilding every turn.

OP sound-mode29/PMD57/polar26/hflip30 now have complete function ownership:
142 CODE bytes/4 procedures/8 native offset WORD fields/empty literal MZ
vectors. Actual OMF/MAP geometry and all source/header dependencies are checked.
The three C/C++ helper wrappers have verified two-hop maintained include chains;
their generic frozen-context inventory label remains unchanged. Sound C/GAME2/O
source without its explicit trailing pragma was compiled twice per body: both
complete raw objects repeat identically and all body bytes/fields equal the
current native function. NOP0067/00A1 remain unowned. See
[helper review](OP_LEAF_NATIVE_REVIEW.md).

Mode returns raw zero-extended MIDI active on FF and preserves FM possible on
that branch. PMD follows INT60's vector and checks ISR+2/+3/+4 for P/M/D;
preserve ES/BX and both far exits. Polar uses signed32 multiply/SAR8 then AX
addition. Hflip generates256 reversed bytes but grants no external BSS credit.

Title DATA31 is separately accepted: opwin.bft/op.m/TL01.PI/TL02.PI at local
offsets0/10/15/23,derived from source calls and the actual consumed macros.
Complete LEDATA matches target/candidate with no DATA fixups/MZ entries; all
CODE local-DATA references enter those literals. Following0A01 remains unowned.
Selection DATA227/BSS23 stays open: filename-pointer/stats/cursor/state
declarations still come from frozen `th03/op/m_select.cpp` outside the maintained
function include. Do not infer storage ownership from accepted function CODE.

PI/PFOPEN retain524 CODE bytes/4 procedures/28 fields/5 MZ entries. PFOPEN is in
the1258-byte `th03_optail.asm` producer at native offset920,with an exact maintained
source copy and dense281-byte coverage. Five PUSH CS/CALL bridges,three decoder
pointers andfour DGROUP words give PFOPEN no MZ entries. Preserve zero-type
fall-through into seek,16-bit sizes,transient ES=CX and original error/register
behavior. See [asset review](OP_ASSET_NATIVE_REVIEW.md).

The retained PFOPEN `.asm` provider is a bounded include in the real tail TU,
not a newly claimed standalone TU. Its legacy include naming is future cleanup
with a deliberate update of the frozen source-copy recipe; no duplicate unused
source or fabricated native object was introduced.

Scanner417/115 instructions/42 near DATA fields remains accepted independently
of its legacy trailing byte at04A5. Direct TC4 and unmodified compiler-S/TASM
emit the complete function without that codestring; the trailer stays unowned.
Selected-object links isolate00-vs90 at04A5 under a diagnostic following-PI WORD
annotation,which also fails relocation order. This is not an accepted fix.
See [input review](OP_INPUT_NATIVE_REVIEW.md).

CDG drawing retains382/114 CODE:3 bodies493 plus3 ordinary outer EVEN bytes,
19 fields/2 MZ entries/12 own-CS operand writers. CDG loading/text retain1206
CODE/6 procedures/41 fields/27 MZ entries. Score retains501 CODE/5 procedures
and DATA11; hi BSS206 adds no file bytes. Title retains902 CODE/5 procedures,
plus DATA31. Selection retains3013 CODE/19 procedures,with DATA227/BSS23
open. Music retains2244 CODE/14 procedures and DATA1008; BSS1060 adds zero file
bytes. Follow the individual reviews for original unchecked behavior and ABI.

All54 prior OP owners and their native source/tool/output/cold bindings are
unchanged. MAINL/ZUN shared helper AST closures and all other proof inputs are
unchanged. Their entire current native source/staging/output graphs(938/29
outputs) were checked; only the shared-module binding changed. Audit/witness/
observation times were preserved,with no runtime replay during this refresh. Receipt:
`.analysis/work/leaf-native-shared-binding.json`.

Current evidence: `.analysis/work/leaf-native-review.json`, `sound-bodies.json`
and `title-storage-review.json`. OP accepts59 extents/14758 file-backed bytes.
Only four scoped TC4 compilations ran; no native linking or cold rebuild ran.
The session preflight's existing status.py invoked MAINL/ZUN audits once; scoped
acceptance/publication/progress did not repeat them. This preflight is already
complete for the current unchanged session/environment.
`.analysis/work/leaf_scope_refresh.py` refreshed
only the verified OP region/summary through the existing renderer,retaining every
non-OP byte. Synthetic unaccepted non-OP branches are discarded. The full progress
generator still invokes ancestor runtimes; no full generator `--check` is claimed.

Validation:55 focused helper/storage/asset/input/drawing/shared/score/title/selection/current-
acceptance/progress checks PASS,tracking and bounded generated-region checks PASS.
`git diff --check` is clean.

## Verified current source scopes

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 59 extents / 92 procedures / 13,221 CODE + 1,537 DATA bytes | Open |
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
The helper acceptance consumes `.analysis/work/sound-bodies.json`, both
`sound-body0.c`/`sound-body1.c` stripped inputs and their four `-roundN.obj`
outputs. Preserve these actual proof inputs and the scoped compiler driver.
Keep `scripts/lib/zun.py` unchanged unless deliberately updating its frozen MAIN
binding; OP's native builder is also shared by MAINL/ZUN. Preserve actual current
inputs. Obsolete logs and verification history may be deleted.

No native reconstruction process is left running at this checkpoint. Start with Git,
`scripts/preflight.py` and the current review. Remaining OP work can begin with
the three unowned input/sound trailers or recover the selection prefix naturally:
DATA227/BSS23 remains open. Inspect actual current
OMF/MAP boundaries before choosing a scope. TH04 at `/home/pentester/coding/codex_ida/th04-reconstruction/th04`
is an authorized source reference, not a replacement target or build dependency.

The unchanged-graph reuse guard rejects changed source/verifier inputs. Review
affected native changes rather than refreshing historical runtime receipt hashes.
Generated progress summarizes current scope; historical runtime matrices do
not add source-exact credit. Preserve current receipts and actual native inputs.
