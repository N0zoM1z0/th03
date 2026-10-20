# MAIN visual-effects source milestone

## Established caller linkage checkpoint (2026-10-20)

Source remains present/boundary-reviewed, not exact. The three spawn declarations
and definitions now use genuine extern-C far-Pascal names bomb_explosion_add,
bomb_center_add and bomb_axis_add, matching the established BOMB_EXPLOSION_ADD,
BOMB_CENTER_ADD and BOMB_AXIS_ADD caller imports. Parameter types, bodies, ordering,
record storage and the other two functions are unchanged. No alias object,
wrapper, OMF rename or caller patch is introduced. The three function ledger IDs,
bounds, owners and states remain unchanged; only their source names/evidence change.

The fresh maintained-path object is
 d37d84309d2cc4d66ef62e67c2685839ac05c74bc1ea90be60d408cb4272d13a.
All five bodies project to 628 original bytes after genuine symbol binding and
three expected same-group linker call lowerings. All 33 fixups, 11 literal ordered
relocation pairs, five exact publics at 0/79/158/245/291, three RETF 6 argument
contracts at BP+10/+8/+6, and renderer ENTER 20 pass. DATA/BSS remain zero.
Actual linker lowering and complete outside preservation are not yet observed.

The terminal receipt is
`.analysis/gpt-dots-effects-established-linkage-probe-v01/compile-first-v01/receipt.json`
(SHA256 28641d7f2e6385bb2dbc1981ea2c15161f23ded46308c06c625c2350ea3a64b3).
The strict result review is
`.analysis/gpt-dots-effects-established-linkage-result-review-v01/report.json`
(SHA256 d87741784281c94f6440bbe0a81e07828040fe8159722e53118031f85c4e0994).
A separate independent audit also passed in durable Factory repository command
`repository-command:c4a835a526e040329b3f4122b23855f8`, against the same
receipt/object pins. Its persisted report is
`.analysis/gpt-dots-effects-established-linkage-independent-v01/report.json`
(SHA256 244da31bdafca45361bbe9c9e9812ef876d5bf8fbb542bdaa35d1c957d84fc41).
All 48 OMF records were reviewed: exactly three PUBDEF name changes, nine dependency
timestamps and one source timestamp differ; other record payloads remain unchanged.
Nothing was normalized or rewritten. Historical failed and positive probes below
remain immutable descriptions of their respective sources.

Current accepted MAIN remains 81 extents / 378 functions / 60,688 bytes. No exact
manifest, status or progress numerator changes. Retained actual link, accepted-owner
preservation, cold/default and runtime gates remain separate obligations.

## Historical source-present milestone

2026-10-19: source-present only. Five complete reconstructed C++ functions cover
original load CDBD..D031: 628 target CODE bytes, including the 337-byte renderer.
No exact promotion, full link, runtime or whole-tail closure is claimed.
Accepted MAIN remains 78 extents / 371 functions / 59,624 bytes. At the initial milestone, reviewed source
scope became 82 extents / 391 functions / 63,672 bytes; the whole-game denominator
remains unknown. Existing score_add 88 bytes receive no new credit.

## Source, state and ABI

`src/main/player/effects.cpp` now contains the reviewed complete symbolic GRCG
word-disable operation (SHA256
f9dc41b9c6508bfa060257d8704dbe3d799907a34d23e6dfa0d7b7eef2c55134).
The other four functions are unchanged from frozen source-v04; `effects.hpp`
is unchanged (SHA256
c2f5f7037369b331a33b2b2678d4a625d58eef98d2ace7f5d6d9d180e5b34ea5).
The old CPP hash e13e5f8f30fd0922d7999ab3e8f63b1a3d973bd58516c345d47bf1e07e795139
remains the historical v04 source identity.

The initial positive native diagnostic staged the complete CPP as `th03/p_eff.cpp`
and the header as root `effects.hpp` in an isolated include overlay. A subsequent
separate native diagnostic compiled the actual `src/main/player/effects.cpp`
path using `#include "src/main/player/effects.hpp"`. This include spelling is
the only source change from the root-staged positive version; reversing it gives
byte-identical full source, and the header is unchanged. Direct-path success is
therefore measured separately rather than inferred from staging. The introductory
uncompiled-proposal comment remains historical text, not current build status.

Historical root-staged producer p_eff: PLAYER_M_TEXT / MAIN_01, 096E:36DD,
original file E61D, length 0274. Names are semantic proposals, not recovered
original identifiers. Existing caller symbols still need integration bindings.

| Function | Load span | Bytes | ABI; direct target callers |
| --- | --- | ---: | --- |
| player_effect_circle_expand | CDBD..CE0C | 79 | far Pascal, RETF 6; 17 far + 1 relaxed |
| player_effect_circle_shrink | CE0C..CE5B | 79 | far Pascal, RETF 6; 34 far |
| player_effect_quad_shrink | CE5B..CEB2 | 87 | far Pascal, RETF 6; 20 far |
| player_effects_update | CEB2..CEE0 | 46 | far no args, RETF; 1 relaxed |
| player_effects_render | CEE0..D031 | 337 | far no args, RETF; 1 relaxed |

Spawn parameters are signed 16-bit x, y, pid2, left-to-right Pascal word carriers at
BP+10/+8/+6. Record pointer is near. DS:3946..39BE contains 12 records × 10 bytes;
byte cursor 39BE increments before slot selection and wraps at 12. Record fields:
kind +0/u8, age +1/u8, x +2/s16, y +4/s16, radius +6/u8, delta +7/int8_t, angle +8/u8,
unclassified +9/u8. Static width/offset assertions protect the layout. Storage
is extern-only and remains in its existing carrier; physical DATA/BSS ownership
is unproved. Byte 9 is untouched existing storage, not artificial code padding.

Circle spawns use radius 8/+8 and 136/-8; quad uses 162/-10 and a random byte angle.
Active update increments byte age; age > 16 clears kind but still updates wrapped
radius that iteration. Render treats every nonzero noncircle kind as quad.
Signed x < 320 chooses left clipping. Circle y >> 1 floors negative odd coordinates;
quad polar(y, r, sin) / 2 truncates toward zero. Quad angle mutates during rendering,
+8 for even slot index and -8 for odd, with four vertices 64 angle units apart.
GRCG uses RMW/color 13; final disable precedes restoring clip (0, 0, 639, 199).

Accepted playfield conversion remains far Pascal despite local link relaxation;
polar remains far cdecl with caller cleanup of 6 bytes. Reuse maintained playfield/polar/
randring declarations and explicit master graphics compatibility forwarders.
No sprite register ABI is invented. Existing trig storage at DS:0316/0396 is reused.

## Historical three native outcomes

All runs compiled the entire five-function owner once, with zero DATA/BSS,
verified inputs, one CPU, nice 10, a 90-second compile bound, clean owned-process
cleanup and unchanged HEAD/worktree. They are isolated compiler evidence,
not cold-link acceptance. Receipts retained under
`.analysis/gpt-dots-tail-effects-probe-v02/compile-first-v01/receipt.json`,
`.analysis/gpt-dots-tail-effects-probe-v03/compile-first-v01/receipt.json`, and
`.analysis/gpt-dots-tail-effects-probe-v04/compile-first-v01/receipt.json`.

- v02: 637 bytes; 80/80/88/49/340. Consumed prefix increments retain AL values;
  CPU-derived -G uses a longer frame. No exact result.
- v03: 646 bytes; 83/83/91/51/338. Separating prefix increments leaves their
  load/inc/store and adds memory comparisons; removing -G restores ENTER.
- v04: 629 bytes; 79/79/87/46/338. Discarded postfix increments, grounded in
  accepted hitcircle source/native output, restore the first four body sizes.
  Independent object review matches all 291 bytes of those four functions
  after genuine symbolic binding and three same-CS far-call lowerings.
  This does not independently accept those functions or the owner.

The historical v04 renderer remains one byte longer: MOV DX, 7C; XOR AX, AX; OUT DX, AX adds 2 bytes
versus the original immediate-port word OUT sequence; two PUSH AX zeros save 1
versus original dword PUSH immediate zero. Native XOR 33 C0 also differs from
original 31 C0. Native additionally clobbers DX; original immediate OUT preserves
its previous value. Hardware behavior, byte identity and caller-visible scratch
state must not be conflated. The normal intrinsic's DX-port convention is
explicit in x86real.h; genuine hardware-source provenance remains unresolved.
No further flag tuning, emitted opcode workaround, padding or assembly patch
was used to conceal this failure.

Target literal relocation order, indices 977..987:
D02B, D00B, CFFA, CFE9, CFD8, CFA5, CF7B, CF3D, CF24, CEF2, CEA8.
Independent review confirms all 33 symbolic fixups and 18 branch destinations.
The native symbolic order predicts this surviving sequence after three genuine
same-CS playfield-call relaxations; it is not a tested linked MZ result.
Existing combo sites interpose before effects and must retain their order.

Target boundary audit is `.analysis/gpt-dots-player-tail-map-v01/audit.json`.
Negative compiler analysis and accepted postfix precedent are retained in
`.analysis/gpt-dots-tail-effects-native-review-v03/REPORT.md` and
`.analysis/gpt-dots-tail-effects-native-review-v03/native.json`.
Historical v04 object-level audit and replayable reader are
`.analysis/gpt-dots-tail-effects-independent-review-v04/report.json` and
`.analysis/gpt-dots-tail-effects-independent-review-v04/audit.py` (report SHA256
3e30419b1106404a8c2b94fdc4ad349f1cff9458cfb4b4bdfc2dfa0b1de7ce7e).
The milestone's compact facts/hashes are
`.analysis/gpt-dots-tail-effects-milestone-v01/observations.json`.
All prior source/probe revisions remain frozen; no accepted manifest, comparator,
exclusion, root carrier or source-default build graph changes accompany this step.

Target observation generators write their output files. Treat recorded generator
commands as historical evidence; reproduce observations only in a fresh scratch
copy, never by rerunning them over a frozen source/proof directory.

## Complete word-disable operation: positive object diagnostic

The new operation writes zero to the named GRCG mode port with the observed
16-bit width. AX is the actual I/O accumulator; DX is untouched locally. It has
no C result, extra call ABI, stack manipulation, dead scratch, padding or emitted
bytes. Surrounding frames, arguments and calls remain compiler-generated. This
is a complete architecture-dependent operation, not an empty optimizer barrier.
The historical source spelling remains unknown; reference wrappers support the
operation's meaning, not TH03 source provenance or inherited exactness.

One root-staged complete-TU native compile produced **628 CODE bytes**, with
spans **79 / 79 / 87 / 46 / 337**, zero DATA/BSS, clean guards and process cleanup.
Independent scratch symbol resolution and three genuine same-group far-call
lowerings match all five complete target bodies, all 18 branches and 33 fixups.
Public ABI, actual fixup frame bases, zero addends and the predicted literal
11 offset/segment pairs pass; every segment carrier is 096E. The site list above
is unchanged. This is not an actual linked-MZ, maintained-path or cold proof.

The final sequence naturally contains XOR AX, AX / immediate-port WORD OUT /
DWORD immediate-zero push / packed 639,199 push / GRC_SETCLIP. The assembler
selects the XOR encoding; no encoding is forced. The earlier two PUSH AX zeros
were 16-bit register pushes, not immediate-zero instructions. The separate
639,199 pair is identical. This result supports the opaque hardware-operation
hypothesis without recovering the original spelling. No shared wrapper changes.

Receipt: `.analysis/gpt-dots-effects-word-disable-probe-v02/compile-first-v01/receipt.json`,
SHA256 `ddd890a30746028edda6e712de3368a2b473c59b92b7f588fd430954ee3f5fbe`.
Object: the same run's `source/obj/th03/p_eff.obj`, SHA256
`82bfc9033ea55776095b42f38c5dcf2c61eb1c94941996c0e12f64a2db02c8db`.
Independent report: `.analysis/gpt-dots-effects-word-disable-independent-v01/report.json`,
SHA256 `d88a576bf00acb3f22946c30b3510f509cd74ff5ce321ac5228c34322362db7d`.
Its `audit.py` and `REVIEW.md` retain complete binding/frame/relocation checks.
Original provenance remains candidate-local-attested. Source metrics and exact
credit are unchanged; actual linkage, outside preservation, cold replay, runtime,
DATA/BSS ownership and whole-tail acceptance remain open.

## Actual maintained-path diagnostic

The exact maintained-layout proposal compiled once through
`src/main/player/effects.cpp` with the root-qualified header. Its complete
628-byte owner again passes independent scratch binding of all 33 fixups,
three genuine same-group lowerings, all 18 branches, five public identities
and ABIs, zero DATA/BSS and the 11 predicted literal relocation pairs.
The renderer retains ENTER 20 and the complete WORD-disable/clip/return sequence.

Receipt: `.analysis/gpt-dots-effects-maintained-layout-probe-v01/compile-first-v01/receipt.json`,
SHA256 `34c13e8d107970e2294ecc6e2944f9c81cd7c45381f5ad5bafb000e801e315a3`.
Object: the same run's `source/obj/th03/effects.obj`, SHA256
`3a70c9755f4902a8c6d6f1bb033ecf26644966b2cde9553015a4e9ed58a14b7f`.
Independent report: `.analysis/gpt-dots-effects-maintained-layout-independent-v01/report.json`,
SHA256 `0751948434def8cca3b88232f88ab1a6745b3ba07988c009edd183ee3fec2b32`.
Its `audit.py` and `REVIEW.md` record the complete comparison and differences.

LEDATA, FIXUPP, SEGDEF, EXTDEF, PUBDEF, GRPDEF and MODEND records match the
root-staged positive object byte-for-byte. THEADR and ten COMENT differences
are individually classified source/dependency paths or timestamps. Separately,
LNAMES changes the linker-visible zero-length default segment from P_EFF_TEXT
to EFFECTS_TEXT. This is a real name change, not generic metadata: it emits no
bytes here, but later MAP/name placement and group ordering remain unproved.
No blanket record mask or comparator relaxation is used. Actual linkage,
outside preservation, full storage/MAP, default/cold regression and runtime
remain open, and accepted exact counts are unchanged.

## Reproduction and next coherent work

Historical root-staged TC4J command inside a fresh isolated source/include overlay:

    bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M' -nobj/th03/ th03/p_eff.cpp

For this historical command, stage the exact frozen
`.analysis/gpt-dots-effects-word-disable-proposal-v01/effects.cpp` as
`th03/p_eff.cpp` (SHA256
0ce25866d48a1ff1815ec33edcc9cb9b77c0a3bfff2471963a2d236115865ac7), and its
`effects.hpp` as root `effects.hpp` (SHA256
c2f5f7037369b331a33b2b2678d4a625d58eef98d2ace7f5d6d9d180e5b34ea5).
Use the verified compatibility include closure. This is the historical source
with the short quoted include, not the current root-qualified maintained CPP.
The retained word-disable v02 launcher/driver/manifest record the successful
root-staged supervised envelope;
future runs require a fresh pinned plan rather than reusing its completed path.
No extra -G/-a2, fake definitions, source bytes or OMF modifications are needed.
Native outputs and exact length mismatches must be retained, not overwritten.

The later actual maintained-path diagnostic uses the same pinned options and
output directory, replacing the source argument with `src/main/player/effects.cpp`.
Its fresh overlay preserves that repository path and the root-qualified header;
it does not copy the source to `th03/p_eff.cpp`. Use a new pinned plan for any
reproduction and preserve both historical recipes and their receipts.

Next integration scope remains the whole C7A5..D6D4 tail. Both background
chains, warning/gauge/pause, score HUD and effects already have maintained source;
background's complete-body raw mismatches and stack-dependent phase behavior
remain open. Effects alone does not remove the CPU translation-unit placement
obstruction. Genuinely link complete owners, check original literal relocation
order, storage/MAP and outside preservation, and satisfy all cold/runtime/ledger
gates before any exact promotion.
