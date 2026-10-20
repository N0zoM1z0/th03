# MAINL heap maintained-source checkpoint

This is a bounded source/staging checkpoint, not default-build integration,
cold proof, exact acceptance, or a complete MAINL reconstruction. The source
additions are src/mainl/memory/heap.inl, scripts/stage_th03_mainl_heap.py,
tests/test_mainl_heap_stage.py, and this document. A bounded progress extension
also updates the existing heap unit and adds diagnostic evidence, adjusts only
the MAINL rendering in scripts/progress.py, adds tests/test_progress_mainl.py,
and regenerates docs/PROGRESS.md and resources/progress.svg. The successor also
adds a narrow retained-source distinction and tests in the MAINL candidate
intake gate, and updates only the affected candidate-index evidence union.
No existing
product source, build file, Oracle, acceptance configuration or historical
receipt changes.

## Source and ownership

The include retains the exact reviewed proposal bytes, SHA-256
3960b8f2ff1821475f86d947b82380957a35ce4c7169a518689e857560774432.
It localizes five master.lib providers at ReC98 revision
b6ba5b0a529edbb31efdf8c0e939263804f8ee47, with Akihiko Koizuka's
attribution preserved. This is disclosed reference-derived symbolic source,
not a claim to have recovered independently authored original source.

The retained source header's provenance.json refers to
.analysis/gpt-dots-mainl-heap-source-v01/provenance.json. That historical
proposal also retains the provider hashes, original source-statement verifier
and staged root. Its twelve static tests compare 338 active statements after
only GAME=3 selection, explicit FAR procedure/RETF and EVEN expansion, and
named Pascal argument offsets. The maintained stager does not require that
private proposal or a reference checkout: it pins the complete source and root
bytes directly.

One ownership cluster covers eight procedures at decoded 0000:210A..237D:
HMEM_LALLOCATE, MEM_ASSIGN_DOS, MEM_ASSIGN, MEM_ASSIGN_ALL, HMEM_ALLOCBYTE,
HMEM_ALLOC, HMEM_FREE and MEM_UNASSIGN. The 628-byte scope comprises 625 body
bytes and three trailing EVEN bytes. The shared ALLOCBYTE entry, invalid-FREE
epilogue, interior alignment and GAME=3 emitted unreachable failure return are
kept. No edge-case behavior is repaired. See [the heap review](MAINL_HEAP_REVIEW.md)
for the detailed ABI, branch, header and modeled-DOS contracts.

The enclosing .386 / USE16 / MODEL LARGE _TEXT context and DS=DGROUP contract
remain required. Far Pascal argument offsets are 6 and 8 after the saved word.
MEMHEAD describes using/nextseg/id words at offsets 0/2/4 within a paragraph,
not a six-byte allocation. Existing root DATA/BSS still owns all eight mem_*
words and Reserve=256. The include allocates no global storage and contains
no copied target-byte arrays, padding calibration or product dependencies.

## Strict staging, not a build

From a checkout with these additions, run:

    python3 -B scripts/stage_th03_mainl_heap.py \
      --frozen-root PATH_TO_PINNED_TH03_MAINL_ASM \
      --output-dir .analysis/NEW_MAINL_HEAP_STAGE
    python3 -B -m unittest discover -s tests -p test_mainl_heap_stage.py -v

The explicit root input must hash to
d0c9d5b9576c9e1300d48a22449fb6acbc35c796e1071e21a2f5cf330d659713.
It is the complete th03_mainl.asm at the revision above. The stager handles
its mixed encoding as bytes, never decodes or normalizes it, and replaces only
these five consecutive includes between palette_white_out.asm and
super_free.asm:

- libs/master.lib/hmem_lallocate.asm
- libs/master.lib/mem_assign_dos.asm
- libs/master.lib/mem_assign.asm
- libs/master.lib/memheap.asm
- libs/master.lib/mem_unassign.asm

The replacement is one include src/mainl/memory/heap.inl. Reversing it must
restore every input byte. Exact source/root pins, unique slots and neighbors,
and source identity are checked before any output is created. Inputs may not
traverse symlinks. Output is restricted to a fresh .analysis/NAME leaf;
existing directories, partial attempts and symlink aliases are never reused
or overwritten.

The output consists only of th03_mainl.asm, the unchanged source include at
its maintained relative path, and staging.json. This is not a standalone
build tree: all other root dependencies must be supplied separately by a
reviewed native plan. No compiler, linker, target emulator, reference Git,
default graph, Oracle or acceptance action is invoked by this script.

The focused tests are portable stdlib tests. Synthetic roots test both newline
styles, non-UTF-8 outside-byte preservation, slot/order/neighbor rejection,
root and source drift, relevant ABI/shared-tail mutations, path restrictions,
symlink rejection, non-overwrite and explicit nonacceptance reporting. Their
synthetic input hash override exists only inside the tests; production has no
pin override option. These checks are staging controls, not native proof.

## Native attempt and retained-only supplement are distinct

The original diagnostic attempt is retained under
.analysis/th03-mainl-heap-native/mainl-heap-feasibility-20261020-v01/.
Its receipt.json remains **failed**, SHA-256
476c40fc05d320075cc0a627aefcbe38eeb489060323f7f66a151110e71f1329.
The planned TASM/TLINK phases produced outputs, then Python validation failed
during dependency import. Neither later validation nor this checkpoint
rewrites that receipt or reports the original run as passing.

A separately guarded, retained-output-only validation is at
.analysis/mainl-heap-retained-validation-20261020-v01/.
Its completion.json passes, SHA-256
61e83cf52a067e02cf743856ee029b6835d1fd5787b063b1b005fa807ca83c51;
it explicitly records original_attempt_pass=false, native_invocations=0,
cold=false and exact_acceptance=false. It preserves the original attempt and
historical full guards; it does not rerun the original 235,340-path inventory.

The supplement's structural.json, SHA-256
cb3379b976fd189e5e419c1d0aa6cec8d8e5821f49268b411f28050645680eb3,
records complete raw equality with the retained baseline, literal MAP equality,
ordered-relocation equality and all 628 original scoped heap bytes.
Full EXE equality here means equality with the retained baseline, not equality
with the whole original decoded/stored MAINL target. The root OMF comparison
permits only its declared dependency-provenance difference, not executable
payload normalization or a claim of identical original OMF.

The behavior.json supplement, SHA-256
c9d3ead4db8db4b311e658350c0c33ad28e027de07802508f94048ce0c89c003,
records, separately for target and candidate, 814 terminal matrix scenarios,
1,302 returned top-level calls, 1,416 native entries, and four malformed-cycle
budgets. Those budgets are nonterminal cases, not successful returns.
The existing explicit DOS AH48/AH49 model remains a boundary: real DOS
allocation, lifetime, exhaustion and freed-storage validity are not proved.

## Remaining gates

The default graph remains unchanged. No maintained-path cold pair, original
whole-image identity, physical DATA/BSS ownership, real DOS lifetime,
canonical DIET packaging, complete product closure or configured exact
acceptance is established. The historical candidate-local target provenance
also remains unchanged. A future native/cold experiment needs its own reviewed
plan, authorization, fresh output, strict full preservation and all applicable
gates. Neither this source checkpoint nor a Git commit grants exactness credit.

## Progress schema and exact ledger delta

MAINL has 145 existing reviewed unit extents: 74 function-kind rows, 70
module-candidate rows and one module row. These are not 145 functions and not
the whole program. The SVG previously read only the MAIN authored-function
ledger, so MAINL incorrectly appeared to have no tracked inventory.

Only the existing th03-mainl-decoded-heap-manager row changes: origin unknown
to library, state boundary-reviewed to source-present, source to the maintained
include, five diagnostic evidence IDs appended, and notes updated. Its ID,
kind, decoded address, 628-byte size, comparison size, boundary state and
historical replay command stay unchanged. No rows are duplicated or added to
the MAIN authored-function ledger. Five appended analysis-bundle evidence
rows record source provenance, the failed original attempt, retained structural
and behavior reports, and retained completion. None uses an acceptance Oracle.

Existing MAINL maintained source remains 34 extents / 3,073 bytes. The new
heap owner adds one extent / 628 bytes: 35 of the same 145 tracked unit
extents / 3,701 source-present bytes. The SVG labels the amber source track
separately from the purple reviewed boundary track and labels MAINL acceptance
in unit terms: exact 0/145. Source presence is not byte-exactness.

Only the heap has the new separate 8-procedure / 628-byte retained-only
annotation, gated by the exact scoped unit and both SHA-pinned diagnostic
pass records. It does not relabel the other 34 units as newly verified, and
does not feed either source or exact counts. The OP, MAIN and ZUN row graphics,
MAIN accepted totals and explicit unknown whole-game denominator are preserved.

Regeneration remains the existing python3 scripts/progress.py workflow and
its --check mode. Focused tests reject mixed function/unit denominators,
duplicate unit inflation, source-only acceptance inflation, and unsafely
scoped or altered retained evidence. No new progress schema file, framework,
acceptance policy or generic metrics system is introduced.

## Retained-only source presence versus cold integration

The first portable installation attempt remains failed and preserved at
.analysis/mainl-source-install-20261020-v01/result.json, SHA-256
9812924bc22e8ca60bc30aac612eb22a978c5cbd23686843e1d0bae6f1bfd6b1.
Its 985 unit tests and tracking/progress checks passed, but the MAINL candidate
intake check rejected this retained-only source checkpoint because its prior
source-present branch required cold compiler/runtime/reproducibility evidence
and a replay_ command. The installer rolled back; this is not a successful
installation or full CI result.

Source-present records a genuine maintained source file. It does not, by
itself, mean cold-integrated or accepted. The successor keeps the normal cold
gate unchanged for all integrated sources. One explicitly named retained heap
checkpoint branch instead admits only this exact unit, decoded scope, source
path and source-content SHA, fixed diagnostic-review command, frozen root
identity, five SHA-pinned diagnostic records and original failed receipt.
The branch requires source_accepted=false and exact_accepted=false, rejects
reproducibility-class claims, and cannot admit a replay_ command without the
normal independent cold/runtime/reproducibility checks.

The corresponding candidate index change affects only the th03_mainl.asm
row: its evidence union gains the five existing checkpoint IDs and its failed
list explicitly retains the original native-attempt failure. Carrier sizes,
coverage, raw/relocation results, receipt, frozen identity, unit membership
and source/exact acceptance flags are unchanged. No failed evidence is erased
or reclassified, and no retained observation is called a cold replay.

The gate adds no new ledger state and grants no default-build integration.
MAINL's source-present SVG remains 35/145 tracked unit extents and 3,701 bytes;
its separate retained heap annotation and zero exact acceptance are unchanged.
Focused intake regressions cover altered source bytes, wrong identities,
paths/spans/hashes/statuses, omitted failed evidence, forged acceptance,
reproducibility relabeling and generic cold-gate preservation. The portable
intake --check must pass in the complete shadow before parent installation.
