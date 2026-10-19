# MAIN Yumemi charge, shared targeting, and bomb source milestone

2026-10-19: **source-present only; no exact promotion**. Two natural C++
producers cover 11 complete functions and 2,343 original CODE bytes. Retained
native linking reproduces those bytes, individual extent relocation order,
MAP placement, and existing storage, but two strict relocation-order checks
fail. Accepted MAIN remains **78 extents / 371 functions / 59,624 CODE bytes**.
With these source-present additions the tracked scope is 80 extents and 382
functions; this is not a whole-game denominator or a 95% claim.

## Ownership and ABI

Pinned Japanese MAIN.EXE SHA-256:
f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.
Provenance remains candidate-local-attested; independent pristine-dump
attestation is open. Original MZ header size is 0x1860.

| Extent | Load interval, end-exclusive | File start | CODE / functions | MAP producer |
| --- | --- | --- | --- | --- |
| Yumemi bomb | 159FF..15CB9 | 1725F | 698 / 1 | bm_yume, P_COMBO_TEXT, 139D:202F |
| Shared targeting + charge/gauge | 16983..16FF0 | 181E3 | 1,645 / 10 | cs_yume, PELLET_PUT, 139D:2FB3 |

There is one semantic gameplay owner with two disjoint file-backed CODE ledger
extents and two physical producers, following the existing Mima convention.
The two unit rows do not duplicate bytes or claim DATA/BSS ownership.
Both physical segments belong to MAIN_04, public byte-aligned CODE, ACBP 28.
Charge includes the genuine 32-byte value/jump table at 16FA0..16FC0;
2,311 bytes are function bodies. No internal return is split into an extra
function. Existing combo and pellet-renderer suffixes remain separate owners.

Maintained paths:
- src/main/player/chargeshot_yumemi.cpp
- src/main/player/bomb_yumemi.cpp
- src/main/player/yumemi_gameplay.hpp
- src/main/enemy/target_record.hpp

Both ledger extents use the semantic owner's primary charge source, matching
the existing multi-producer replay model. This does not assign the bomb's
physical production to cs_yume. The candidate manifest records both real TUs.

The first 210-byte helper is the shared ELLEN_TARGET_SET selector. Preserve the
two ordinary root calls and accepted Ellen caller. It selects transformed boss
coordinates or the live enemy with smallest unsigned formation index, uses
the complete 48-byte enemy record, and retains the selected marker if output
coordinates fall back. Boss/no-target paths do not overwrite the shared near
enemy pointer. Its pid is a byte in a word Pascal carrier, RETF 2.

Charge state comprises two six-byte state/frame/x/y records. Reset, update,
and renderer retain the declared far Pascal public ABI. Ring rendering is near
Pascal, with full-word sprite offset/radius and byte phase in a word carrier,
RET 6. Gauge type is unsigned16, RET 2. The real sprite-size helper halves
pixel height, so set(32,32) stores height16; bomb GRC clipping uses the
200-line domain and restores bottom199. polar remains far cdecl. The genuine
FAR bullets_add call relaxes to NOP/PUSH CS/near CALL; it is not a near-return
ABI. No target arrays, padding, fake ABI, no-op barriers, or OMF edits are used.

## Native and retained observations

The reviewed v02 change declares left before top at ring-function scope.
Natural TC4 allocation removes three instruction bytes; natural subsequent
table placement removes the remaining producer byte. The result is exactly
1,645 charge CODE bytes and 698 bomb CODE bytes. Charge remains one TU:
native LEDATA is 1,024 + 621 bytes. All 133 charge and 53 bomb symbolic fixups
were independently checked. Both objects allocate zero private DATA/BSS.

The retained run reused these immutable v02 objects, rebuilt the root carrier
once with TASM, and linked once with TLINK. Both native exits were zero;
cleanup and input-preservation checks passed. This was not a cold build, and
the localized maintained source paths have not yet been freshly compiled.

The original diagnostic stopped with KeyError: 'segment' after linking,
because 20 prior function entries inherit the manifest default segment.
Its receipt remains unchanged and diagnostic_complete=false. A separately
reviewed offline verifier derives only those omitted segments from the frozen
manifest, keeps explicit segments unchanged, and preserves the original run.

Supplemental bounded checks pass:
- All 80 extent-local raw bytes and literal MZ relocation lists
- All 382 complete function bodies and the 32-byte switch table
- All expected producer MAP contributions and 30 root CODE rows
- Existing DATA/BSS layout, initialized bytes, shared publics and new aliases
- Complete outside-Yumemi payload equality against the accepted default
- All 30 other retained game products unchanged, not freshly rebuilt or
  credited as new source progress

## Two preserved strict failures

1. **Combined-owner MZ order:** the target enumerates bomb's 20 sites before
   charge's 12. The v01 candidate links cs_yume before bm_yume and enumerates
   charge's 12 before bomb's 20. Internal order inside each extent is correct.
   A separate untested proposal reverses only the natural object insertion
   order to bomb then charge. Existing zero-byte scaffolds already declare
   both segments. No result is claimed for this proposal.

2. **Outside-carrier MZ order:** after excluding exactly the two new extents,
   payload bytes match the accepted default, but the segment relocation at
   load C7F1 moves four positions in the literal list. That gate remains
   failed independently of the proposed object-order change.

Independent OMF observation narrows the second failure without proving its
cause: the relevant PLAYER_M_TEXT LEDATA still starts at segment+3EF, spans
1,003 bytes (load C4C7..C8B2), and has a 390-byte FIXUPP record. The input-reset
far-pointer fixup at C7EF moves from subrecord60/byte303 to subrecord45/byte232
while its EXTDEF index changes167 to176. The shared selector fixup at C5B9
changes from internal group3/segment21 to external ELLEN_TARGET_SET147.
This is not evidence of a record split; the actual TASM enumeration cause is
unproved. Do not infer that renaming, object order, or a fixed byte shift will
solve it.

Both failures remain evidence. Do not sort relocations, patch the target,
rewrite objects, widen exclusions, or weaken the strict comparator. Native
success and raw equality alone do not grant exactness.

## Storage and integration

Carrier-only labels preserve existing storage:
target_formation_marker at DGROUP38E8; yumemi_gauge_frame at4B7E, retaining
neighbor4B7D; yumemi_chargeshots at4B80 for12 bytes; and six original
yumemi_bomb_triangle_angles bytes at078C. All original reservation totals,
initialized angle bytes, legacy labels, and downstream positions remain.

The shared ELLEN_TARGET_SET PUBLIC/equate pair is replaced by one FAR extern,
not duplicated. Both root calls and callback symbols bind to the natural
producer. Existing BOMB_AXIS_ADD and palette helper bodies remain shared.
Historical physical DATA/BSS compiler ownership is not newly established.

Independent detailed order/framing review:
.analysis/gpt-dots-yumemi-gameplay-integration-v01/RETAINED_ORDER_REVIEW.md
SHA-256 5c78dfc9f7f435639b7fc4c43bab04ea14d01eec8340d7436cc53caba69fc0f9.
A separate coherent CPU-state owner is under investigation; no ordering fix
is promised or included in this milestone.

## Retained evidence and reproduction

Native v02 receipt:
.analysis/gpt-dots-yumemi-gameplay-source-v02/probe-v01/compile-first-v01/receipt.json
SHA-256 943b4b9476bc45b7a36deb74752fc253e4c235cd6d729eccf26806187136bce8.

Original retained native receipt:
.analysis/gpt-dots-yumemi-gameplay-integration-v01/relink-proposal-v01/run-first-v01/receipt.json
SHA-256 1845aa19d695bde0471435c8704e5cc65b7d215134a1bda3e99bcae29f764286.

Supplemental offline report:
.analysis/gpt-dots-yumemi-gameplay-integration-v01/postrun-verifier-v01/report.json
SHA-256 716eeecf6a4c4bba8a24c0e7008eb203b7c18950e35b203ccad66571787edd29.

The following read-only diagnostic is bound to the original pre-milestone
HEAD, Git status, and full worktree hashes. It can be recomputed only in that
unchanged worktree or a separately reconstructed matching checkpoint:

    PYTHONPATH="$PWD/.venv/lib/python3.12/site-packages" python3 -B .analysis/gpt-dots-yumemi-gameplay-integration-v01/postrun-verifier-v01/launch_offline.py --verify-existing-output

In that matching context, expected exit is1 because strict_diagnostic_match
is false. After this milestone is installed or committed, the command will
correctly fail guard_originals before recomputation. Inspect the immutable
report instead, or prepare and review a fresh supervisor plan bound to the new
checkpoint. Do not bypass, remove, or weaken any original guard. If retaining
output from a matching checkpoint, use a new path and preserve the old report.

The installed candidate preserves the observed v01 charge-before-bomb order.
A future canonical reproduction command, after reviewed fixes and separate
execution authorization, is:

    python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_yumemi_gameplay_candidate.toml --run-id yumemi-gameplay-cold-review-v01

This is a plan, not a passing run. It must freshly compile localized source,
retain all existing accepted owners, and satisfy complete raw/MAP/ordered-MZ,
outside-scope preservation, cold determinism and configured behavior gates.
Configured input/math probes do not establish Yumemi gameplay or PC-98
device/runtime correctness. Whole-game source/link/product closure, native
Factory acceptance, and the original target provenance question remain open.
