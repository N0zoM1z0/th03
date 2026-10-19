# MAIN visual-effects source milestone

2026-10-19: source-present only. Five complete natural C++ functions cover
original load CDBD..D031: 628 target CODE bytes, including the 337-byte renderer.
No exact promotion, full link, runtime or whole-tail closure is claimed.
Accepted MAIN remains 78 extents / 371 functions / 59,624 bytes. Reviewed source
scope becomes 82 extents / 391 functions / 63,672 bytes; the whole-game denominator
remains unknown. Existing score_add 88 bytes receive no new credit.

## Source, state and ABI

`src/main/player/effects.cpp` and `effects.hpp` preserve frozen source-v04 text
byte-for-byte (SHA256 e13e5f8f30fd0922d7999ab3e8f63b1a3d973bd58516c345d47bf1e07e795139
and c2f5f7037369b331a33b2b2678d4a625d58eef98d2ace7f5d6d9d180e5b34ea5).
The local quoted header resolves beside the maintained CPP; no source rewriting
or compatibility-header change is needed. Its introductory uncompiled-proposal
comment is retained historical provenance, not a claim that the later probe
never ran. Maintained-path native reproduction remains unrun.

Candidate physical producer p_eff: PLAYER_M_TEXT / MAIN_01, 096E:36DD,
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

## Three native outcomes and remaining blocker

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

Renderer remains one byte longer: MOV DX, 7C; XOR AX, AX; OUT DX, AX adds 2 bytes
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
Final object-level audit and replayable reader are
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

## Reproduction and next coherent work

Core pinned TC4J command inside a fresh isolated source/include overlay:

    bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M' -nobj/th03/ th03/p_eff.cpp

Stage the maintained CPP text unchanged as th03/p_eff.cpp and its local header
as effects.hpp in the overlay, using the verified compatibility include closure.
The retained v04 launcher/driver/manifest record the exact supervised envelope;
future runs require a fresh pinned plan rather than reusing its completed path.
No extra -G/-a2, fake definitions, source bytes or OMF modifications are needed.
Native outputs and exact length mismatches must be retained, not overwritten.

Next source scope remains the whole C7A5..D6D4 tail, including both background
animation chains, warning/gauge/pause and score HUD. Effects alone does not
remove the CPU translation-unit placement obstruction. Resolve the authentic
renderer hardware contract separately, then genuinely link complete owners,
check original literal relocations/storage/outside preservation, and satisfy
all cold/runtime/ledger gates before any exact promotion.
