# MAIN score HUD source milestone

2026-10-19: source-present only. One symbolic assembly reconstruction at
`src/main/hud/score.asm` adds six complete functions / 362 body bytes and four
separately classified EVEN producer bytes. Two ledger bands avoid overlap:
D50E..D5B0 (162B) and D608..D6D4 (204B). Accepted score_add D5B0..D608 / 88B
remains its original owner, source, evidence and count; the TU includes it once.
Reviewed MAIN becomes85 extents / 404 functions / 65,598 CODE bytes. Accepted
MAIN stays78 extents / 371 functions / 59,624 bytes. No new exact credit.

## Source and ABI

The unchanged source header records its original research-proposal provenance.
Current source-present status and native-object evidence are recorded in the
ledgers and this review; the historical header is not a current build-status claim.

The source reconstructs complete observed algorithms; original language and TU
partition are not established. D50E is a genuine AL/CX/ES glyph interface with
DF0 and SI/DI preservation. Its carry loop has seven rows for ordinary screen
x; x640 produces eight. D52E renders BCD scores and story extends. D608 adds an
implicit trailing zero and turns GRCG off; D668 suppresses zero and leaves GRCG
on. D6C0 symbolically writes the renderer's MOV AL immediate at loadD56C,
preserving initial80h and byte-wrapping3-minus-credits behavior. No fake ABI,
clipping, padding arrays or replacement data variable is introduced.

D5A2 performs14 overlapping WORD stores, clearing15 bytes at current DS offsets
3E2E..3E3C. Under ordinary DGROUP DS this overlaps background records70/71;
3E2E also equals the glyph CODE offset. Reset intent and transitive DS provenance
remain open. The descriptive background alias is not exclusive storage ownership
or proof of the original operand's provenance. All DATA/BSS allocations remain
external; no overlapping allocation is created.

## Native evidence and preserved failure

Historical v01 omitted the accepted carrier's `.model use16 large _TEXT`.
Its segment-framed BSS OFFSETs resolved to39E4/2CAE/39F4/39E4 instead of
4B64/3E2E/4B74/4B64. A conditional resolver substitution was not valid linker
evidence. Frozen failure: `.analysis/gpt-dots-tail-score-omf-review-v01/frame-audit.json`
and `FRAME_CORRECTION.md` in that directory.

Restoring only the genuine MODEL ambient produced14 DGROUP-framed data fixups
among22 total without changing raw LEDATA. Maintained-layout v03 assembled the
actual `src/main/hud/score.asm` with root-qualified unchanged score_add include:
454 CODE bytes, zero DATA/BSS allocation, a zero-size model-generated _TEXT.
All nonmetadata OMF records equal v02; only THEADR and two dependency COMENT
records differ. No metadata normalization or object patching was used.

Faithful resolution against original accepted MAP group bases and reviewed
symbols matches all454 bytes (362 new body + 88 existing + 4 outer producer).
Six predicted MZ sites preserve original order: D537,D573,D583,D619,D660,D679.
This is isolated object resolution, not a literal linked MZ or cold acceptance.
Nine “Segment alignment not strict enough” warnings remain because EVEN is used
in BYTE PUBLIC CODE. Local output matches the six observed NOP sites, but final
linked placement remains a gate; alignment was not changed to hide warnings.

Maintained receipt: `.analysis/gpt-dots-tail-score-probe-v03/compile-first-v01/receipt.json`
SHA256 de9ae1c8a950e04080a46109fba0fff9c24f81960c7aa98370d283fa265699b6.
Object SHA25631626ed097bea3013f47c7488b2ed1e42e061e6e6369d26cb7fd5fc0290b15fd.
Final audit: `.analysis/gpt-dots-tail-score-omf-review-v03/review.json`
SHA2561e888396c4c62aff01422dc89265fbe9f11f68a45ee4200576beeeb70a004d67;
`maintained-layout.json` SHA2562b76d8a2f4818f31b666e251161a501a976a7de9b66daeedccb3991247d23c0e.
The audit script `review.py` in that directory is retained with these inputs.

## Remaining gates

Full link, grouped near HUD calls, actual ordered relocations, outside payload,
DATA/BSS identity, accepted score_add containing-carrier MAP metadata, all default
products, cold replay and runtime remain open. Source/default exact manifests,
exclusions and historical proofs are unchanged. New source includes accepted
score_add once but must not be linked alongside a second physical owner.
Frozen target audit `.analysis/gpt-dots-tail-score-proposal-v01/audit.json` and
`.analysis/gpt-dots-tail-score-review-v02/ADDENDUM.md` retain boundary/ABI evidence.
That historical audit.py writes its sibling JSON; regenerate only in fresh
copied evidence directories, never overwrite frozen evidence.
