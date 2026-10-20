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

## Historical maintained cold candidate

The two genuine HUD import/call spellings now match the existing lowercase
`@hud_static_story_lives_put$qv` export literally. The earlier uppercase-import
object remains historical isolated evidence, not a link-ready object to reuse.
The source-only candidate is `config/th03_main_score_candidate.toml`; the
accepted manifest, source-present ledger state and 78/371/59,624 totals are
unchanged. No cold result is claimed by installing this candidate.

The retained three-phase native diagnostic is preserved at
`.analysis/gpt-dots-score-retained-diagnostic-v02/run-first-v01/receipt.json`
(SHA256 `cbecdf01d884eb7a67a75c41df94c12c6dc35817d1e686300dbb2c17af9ea8eb`).
Its sole strict failure was eight same-literal-address public display ties.
The independently reviewed read-only supplement
`.analysis/gpt-dots-score-public-ties-review-v01/report.json`
(SHA256 `cd7c65bd8141e1ee7233b8d9b471397928eaeb84183533872fe116b7e218e531`)
passes the exact bounded tie rule while retaining the failed original receipt.
This is retained-link feasibility, not cold or exact acceptance.

The candidate uses the existing serial replay and native Tup build graph, one
additional symbolic ASM object at the actual maintained path, a 454-byte root
extraction and exact-count caller/import/storage-alias edits. Its dedicated
score-only adapter preserves the old score_add semantic owner and 88-byte raw
extent while explicitly validating the new physical carrier. The original
root/include is checked before extraction, and the staged root, score source
and single unchanged score_add include are hash-bound afterward. Generic
candidate additions still cannot replace accepted owners. At that historical checkpoint the default replay did not activate the score
migration or its public-tie treatment.

The conjunctive supplement compares both fresh rounds against both retained
accepted rounds: all 31 game products, all 43 MAP files, prior non-root game
objects using the existing dependency-timestamp comparator, complete MAIN
outside bytes and 1,547 literal relocation pairs, the original six-site new
union, DATA/BSS/STACK, headers and full ordered contribution/public inventories.
Only the two new bands are excluded from outside comparison; score_add remains
outside. The eight enumerated public display ties do not permit arbitrary
sorting, case folding, changed symbol multiplicity or changed addresses.
Historical proof inventories are guarded in place, not copied recursively.

After installation and full CI, the proposed cold command is:

    .venv/bin/python -B scripts/replay_th03_main_serial.py --foreground --run-id UNIQUE_SCORE_ID --candidate-manifest config/th03_main_score_candidate.toml

Two actual independent cold rounds and all configured required gates must pass
before any deliberate promotion/default integration and subsequent fresh
no-candidate regression. Keep assembler logs, including the nine historical
BYTE/EVEN alignment warnings; no warning suppression or alignment compensation
is introduced. Whole-original global relocation interposition remains separate
and unclosed.

The existing input/math DOS probe remains required. Dedicated score/device
traces are supporting Oracles under `config/oracles.toml`, not newly invented
universal acceptance gates. No new behavior proof is claimed for the AL/CX/ES
glyph interface, DF/carry loop (including x640), BCD/story extends, distinct
GRCG effects, writable-CS credit immediate, or overlapping clears. Reset intent,
transitive DS provenance, physical VRAM/GRCG timing and cross-emulator behavior
remain explicit semantic limitations rather than being inferred from raw bytes.


## Candidate cold proof and default-integration checkpoint

Candidate run `gpt-dots-score-candidate-cold-v01` passed both fresh cold rounds
and the configured input/math DOS probe. Its receipt is
`.analysis/th03-main-exact/gpt-dots-score-candidate-cold-v01/receipt.json`,
SHA256 `9bd8e7750ae87a776c73297fa814389a671bfc26b306d15578e55226ef98dcce`.
Supervisor completion is
`.analysis/th03-main-serial/runs/gpt-dots-score-candidate-cold-v01/completion-evidence.json`,
SHA256 `5b253ef6e18a9f18e431c43c1b5f27bf29658769a4847110aee700a14a9bf0c3`.
Independent audit rechecked all four fresh/historical baseline comparisons and
928 object hashes. Game products and game objects are deterministic. Nine
Research objects (if_shift, wide and xfade under 086/286/386) differ in actual
LEDATA banner payload: three ASCII compile-time `__TIME__` digits and their
record checksum. These are not merely dependency metadata. All-object equality
remains false; no banner payload normalization is permitted.

Default preparation now includes the same score owner and genuine extraction,
but omits the candidate-only build.bat scheduling edit: the existing default
adapter keeps build.bat unchanged and uses .tup/options. The score_add logical
owner, source, function, ABI and 88-byte credit stay unchanged; the accepted
build manifest explicitly describes its actual maintained score.asm physical
carrier, score_hud.obj and 454-byte MAP contribution. A dedicated validator
pins the entire default configuration and independently reverses only this
physical transition plus the new score addition to recover the pinned complete
historical configuration. This is not a generic replacement mechanism.

The frozen candidate configuration remains historical evidence; supplying it
again to the default aggregate fails duplicate ownership. Original root/include
checks still precede every transformation, and the maintained single include
and reduced root are validated after staging. All score-preservation checks
remain conjunctive in default mode, including the exact eight public ties.

No ledger promotion is made by this checkpoint. The two score rows remain
source-present, six functions remain boundary-reviewed and accepted totals stay
78 extents / 371 functions / 59,624 bytes. Fresh no-candidate regression, its
independent audit and final metadata validation are still required:

    .venv/bin/python -B scripts/replay_th03_main_serial.py --foreground --run-id UNIQUE_SCORE_DEFAULT_ID

The existing configured runtime gate is unchanged. DS/reset intent, device
timing, original global interposition and Factory acceptance remain open under
their previously documented scopes. Preserve all failed and successful proof
trees and source snapshots; later metadata must not rebind historical proof.


The first score.asm comment now says maintained assembly rather than incorrectly
claiming it was never compiled or installed. Every byte after that first line
is unchanged. Historical candidate source SHA remains
`838cad4521b431e4c287173ef6dcc29c2958ef4cafad30643688c1a5cd1e0a8b`;
the default source SHA is `ec13b2fb32376e0b068ab6fbb49183bbfcad4487bdc0e06a7e7b9bc8356ae62e`.
The original normalized OMF gate
`b07127fbb34727ef1558b95c2d5325ee6c7dedb07b58a6ba1fef3a7afe55db73`
remains mandatory in the future default run. No fresh default object identity
is claimed from a source-only comment comparison.


Independent cold audit is retained in Factory command evidence
`repository-command:21802d789e6c406eb03e025ba1bff1bc` and
`repository-command:be0a4b754b3f4dc085066ab472a5bc35`; no separate audit
file is implied. Reproduction uses the documented repository .venv interpreter.


## Bounded default CODE acceptance

Fresh no-candidate run `gpt-dots-score-default-cold-v01` passed both cold rounds.
Receipt `.analysis/th03-main-exact/gpt-dots-score-default-cold-v01/receipt.json`
has SHA256 `40ce4dc50d432dfa4de815a0929b9d522ad0193f924e84fd67c51fec241cd9ff`.
Completion `.analysis/th03-main-serial/runs/gpt-dots-score-default-cold-v01/completion-evidence.json`
has SHA256 `750bd41229bc012f752c2f8ff7e52aec08cdb4f49da7566aaec3d7dee68c527d`.
Independent audit is retained as Factory command
`repository-command:c459c77e7ddc44ea9099991e6bfba588`.
It rechecked all four historical comparisons, 743 source inputs, 12,418 evidence
files, 5,602 historical files, 249 receipt raw records, 86 MAP copies and 928
object hashes, required runtime and schedule receipts. Both genuine score OMFs
retain normalized SHA256
`b07127fbb34727ef1558b95c2d5325ee6c7dedb07b58a6ba1fef3a7afe55db73`
despite the comment-only source transition.

This accepts exactly two score extents / six complete functions / 366 CODE bytes:
362 function bytes plus four natural EVEN producer bytes. Existing score_add88B
retains its source/semantic ownership and credit; only its physical carrier has
moved, explicitly recorded in the default manifest. MAIN totals become 80 exact
extents / 377 functions / 59,990 bytes, comprising 59,063 function bytes and 927
producer bytes across 71 semantic owners. These are reviewed CODE totals, never
a whole-game percentage. Other artifacts and surrounding DATA/BSS receive no
new acceptance.

Default game products/objects are deterministic. The same nine Research paths
(if_shift, wide and xfade under 086/286/386) differ in FOUR ASCII compile-time
`__TIME__` digits in actual LEDATA payload plus record checksum. The preceding
candidate had three changed digits. Neither is metadata-only drift, and neither
is normalized away. All-object equality remains false.

The existing input/math DOS runtime probe passed; no new score-specific device
trace is claimed. DS provenance/reset intent, physical VRAM/GRCG timing, original
global interposition and whole-game closure remain open. Provenance is still
candidate-local-attested; this is not native Factory acceptance. Retain the
historical MODEL-less and literal-public-order failures and the bounded eight-tie
supplement unchanged.

Metadata validation uses retained snapshot A with inherited ledger evidence, then
a new ledger-consistency row referencing A's actual inventory and validation log,
followed by snapshot B validation. Both are under
`.analysis/gpt-dots-score-metadata-promotion-proposal-v01/`.
No snapshot claims to validate later metadata. Source, manifests, scheduling,
runtime and comparison controls remain byte-identical to the successful default
proof. Final installation CI and clean metadata commit remain separate results.

Recorded successful invocation:

    .venv/bin/python -B scripts/replay_th03_main_serial.py --foreground --run-id gpt-dots-score-default-cold-v01

Use a new run ID for reproduction. Unit ledger driver fields use `python3`
within an activated repository .venv because the existing shell-free driver
validator does not parse interpreter flags; the actual evidence command above
is retained literally.
