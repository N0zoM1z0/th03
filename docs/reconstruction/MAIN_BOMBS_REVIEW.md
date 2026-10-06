# MAIN character-bomb owner review

MAIN_05_TEXT is the next complete TH03 MAIN owner under reconstruction. The
maintained source is src/main/player/bombs.inl, injected into the frozen
th03_main.asm carrier by a bounded, single-hit edit during the owned-extent
cold replay. The edit removes the legacy procedure block before copying the
maintained include, so accepted bytes cannot be inherited from the unowned
scaffold.

## Target boundary review

The immutable MAIN target places this owner at 183C:0001 with size 0x0C29
(3113 bytes). scripts/review_th03_main_bombs.py independently decodes the
entire extent and proves an exact seven-function partition:

| Function | Segment offset | Bytes | Return |
| --- | ---: | ---: | --- |
| chiyuri_bomb | 0001 | 490 | RETF |
| ellen_bomb_update (ellen_185AB) | 01EB | 280 | RETF |
| ellen_bomb_render (ellen_bomb_186C3) | 0303 | 163 | RET |
| ellen_bomb | 03A6 | 580 | RETF |
| kana_bomb | 05EA | 526 | RETF |
| kotohime_bomb | 07F8 | 528 | RETF |
| rikako_bomb | 0A08 | 546 | RETF |

The seven spans total exactly 3113 bytes, with no padding/table hole between
them. The target review records 71 relocation sites wholly contained in the
owner and rejects any relocation that crosses an owner edge.

Ghidra is treated as provisional semantic assistance, not a boundary oracle.
In particular, its automatic body membership under-counts parts of kana_bomb
and rikako_bomb, and it did not initially expose chiyuri_bomb as an automatic
function. The accepted boundary model therefore comes from the raw target
instruction stream, return instructions, contiguous adjacency, and the frozen
symbolic carrier, all checked back against the original MAIN image.

## Source-carrier experiment

An isolated archive of the pinned ReC98 revision was modified only for a
producer experiment: the seven legacy procedure definitions were removed from
th03_main.asm and replaced by one include of the extracted maintained block.
A complete 20-product build succeeded, and main.map retained the exact
MAIN_05_TEXT contribution at 183C:0001, size 0x0C29, module th03_main.asm.

The production replay implements this as a declarative carrier edit with
freeze-before-edit verification. Existing bounded owners sharing
th03_main.asm are hash-checked before any edit. The bomb owner is then checked
again for exactly one maintained include. No PUBLIC aliases are added merely
to satisfy the Oracle; the original module-private symbol visibility is
preserved.

## Current exactness blocker

The symbolic TASM candidate reproduces all 3113 owner bytes exactly and keeps
the same 71 relocation sites, but it does not reproduce the target relocation
ORDER. This is not caused by the maintained include: the frozen pre-carve
scaffold produces the same wrong order.

The target relocation table exposes a strong producer-boundary signal. Within
the owner, relocation entries form five consecutive high-address-to-low-address
groups: Chiyuri, Ellen (all three Ellen procedures together), Kana, Kotohime,
and Rikako. The TASM carrier instead emits the same sites largely in ascending
address order. This is consistent with five character-specific Turbo C++
producers and is now the working hypothesis for the next reconstruction step.
The ordered-relocation gate remains strict; no set/multiset substitution is
accepted.

The retained two-round candidate receipt is
.analysis/th03-main-exact/gptweb-bombs-tasm-blocker-20261007/receipt.json.
Both rounds report raw_equal=true, zero differing bytes, and
ordered_relocations_equal=false for the full owner and for each of its seven
functions. The pre-carve baseline candidate emits the same wrong ordering,
which rules out the new include as the source of this drift.

## Ellen Turbo C++ producer reconstruction

The five-producer hypothesis is no longer based only on the MZ relocation
shape. src/main/player/bomb_ellen.cpp now reconstructs the complete Ellen
producer as natural Turbo C++: the 280-byte update function, 163-byte near
render helper, and 580-byte bomb function. A fresh pinned-ReC98 TC4J compile
produces exactly 1023 CODE bytes and 347 decoded instructions. Every candidate
instruction has the same offset, size, and mnemonic as the corresponding
immutable-target instruction, and the three return boundaries are exactly
279/RETF, 442/RET, and 1022/RETF.

This result required source-level compiler archaeology rather than byte
patching. In particular, the render helper needs two independent sentinel
tests to reproduce TC4J's second pointer reload; the update function needs one
loop variable reused across both loops to avoid an extra DI save/restore; the
first four-frame phase test is naturally (frame & 3) < 2 while the later
zero-remainder test is the distinct % 4 expression emitted as IDIV; and the
MRS altered-color argument uses the repository's existing _AX register
pseudo-variable idiom to preserve the target's integer-promotion sequence
without inventing a stack local.

The same object independently strengthens the physical-producer model through
its private data. TC4J emits CODE/DATA/BSS segment sizes 1023/0/132. The
132-byte BSS is exactly particle_spawn_count (2), two players by eight
8-byte position/velocity particles (128), and particle_p (2). Their relative
offsets 0/2/130 map directly onto the otherwise anonymous target DGROUP region
25DC, 25DE..265D, and 265E referenced by the Ellen code.

A full-link split-producer experiment now distinguishes the two parts of the
remaining blocker. First, splitting MAIN_05_TEXT into five separate TASM
objects preserves the exact 3113 bytes, the exact 71 relocation sites, and the
five exact MAP contribution boundaries, but TLINK still emits the relocation
entries in ascending address order. Physical object boundaries alone therefore
do not explain the target.

Replacing only the 1023-byte Ellen TASM contribution with the maintained TC4J
producer changes the result decisively. With #pragma codeseg MAIN_05_TEXT,
main.map places the C++ contribution at exactly 183C:01EB..05E9 and keeps the
other four character contributions at their original offsets. The 71
relocation sites remain identical as a multiset, while Ellen's 15 relocation
entries become exactly the target sequence
1446,1320,1286,1107,1014,1009,991,957,917,883,765,719,710,672,586.
The still-TASM Chiyuri/Kana/Kotohime/Rikako groups remain ascending. This
falsifies the earlier weaker idea that a five-object split by itself was
sufficient and directly identifies the TC4J producer/FIXUPP behavior as the
source of the target ordering.

The mixed full link has only 22 byte mismatches inside the Ellen functions.
Every mismatch is the high byte of a DS-relative reference and every candidate
byte is exactly target+0x43. main.map explains the constant delta: the current
monolithic scaffold owns BSS through DGROUP:68DC, so Ellen's 0x84-byte BSS is
appended there, while the immutable target references the same private layout
at DGROUP:25DC. The difference is exactly +0x4300. Thus Ellen's remaining
linked-byte blocker is specifically private-BSS physical placement, not CODE
generation, ABI shape, relocation-site selection, or relocation ordering.

The enhanced candidate mode in scripts/review_th03_main_bombs.py records raw
owner/function equality, mismatch offsets and byte values, relocation-site
multisets, and relocation order separately so these properties cannot be
conflated again. The retained mixed-link diagnostic is
.analysis/th03-main-bombs-split-probe/ellen-cpp-review-v5.json. This result
made the next step unambiguous: recover the remaining TC4J character producers
and historical DATA/BSS producer boundaries rather than manipulating the final
MZ relocation table.

The reproducible object-level Ellen probe is:

    python3 scripts/probe_th03_main_bomb_ellen_cpp.py --run-id UNIQUE_ID

The retained Ellen maintained-source receipt is
.analysis/th03-main-bomb-ellen-cpp/gpt-web-ellen-main05-v2-20261007/receipt.json.
It intentionally records exact_acceptance=false: the pre-link raw-byte
differences are unresolved OMF data/fixup operands and must not be normalized
away as an exact result.

## Chiyuri Turbo C++ producer reconstruction

src/main/player/bomb_chiyuri.cpp reconstructs the complete 490-byte
single-function Chiyuri producer as natural Turbo C++. A fresh pinned-ReC98
TC4J compile emits exactly 490 bytes in MAIN_05_TEXT, no nonempty private BSS,
169 decoded instructions, and the target far-return boundary. Every instruction
offset, size, and mnemonic matches the immutable TH03 target.

The source-level details that matter to code generation were checked rather
than guessed. The two byte locals preserve the target stack layout. Integer
promotion is required for the palette intensity but not its pid parameter,
while the center/axis helper pid parameters do require integer promotion. The
distance expression must remain ((frame - 64) * 2) << 4 so TC4J emits the
target ADD AX,AX; SHL AX,4 rather than folding it to SHL AX,5.

The reproducible object-level probe is:

    python3 scripts/probe_th03_main_bomb_chiyuri_cpp.py --run-id UNIQUE_ID

The retained current source receipt is
.analysis/th03-main-bomb-chiyuri-cpp/gpt-web-chiyuri-precommit-a9-20261007/receipt.json.

Chiyuri also passes the full-link physical-code experiment. Replacing the first
TASM character contribution with this TC4J object places it exactly at
183C:0001..01EA, length 0x01EA, with no DATA/BSS contribution. All 490 linked
Chiyuri bytes match the target. The complete bomb owner still has the same 71
relocation sites, and Chiyuri's 13 relocation entries become exactly the target
descending sequence:

    485,378,341,322,302,283,248,143,109,81,76,58,24

With Chiyuri and Ellen both produced by TC4J, the first two character
relocation groups match the target. Chiyuri itself therefore has target-exact
linked bytes, target-exact MAP placement, target-exact relocation sites, and
target-exact relocation order in a full MAIN link. The retained current
full-link diagnostic is
.analysis/th03-main-bombs-chiyuri-link-probe/review.json.

No aggregate exact credit is claimed yet because MAIN_05_TEXT is accepted as
one complete seven-function owner. Ellen still has 22 DS-relative high-byte
mismatches from the +0x4300 private-BSS displacement. Kana is handled below.

## Kana Turbo C++ producer reconstruction

src/main/player/bomb_kana.cpp reconstructs the complete 526-byte Kana
single-function producer as natural Turbo C++. The first direct translation
compiled to 531 bytes even though its first 133 instructions were already
target-shaped. The only structural cause was source lifetime: keeping the two
polar results in function scope prevented TC4J from reusing SI for the later
playfield-left value and forced a BP-relative local. Moving those temporaries
back into the polar conditional makes TC4J reuse SI exactly as the target does.

The resulting object is 526 bytes / 184 instructions with one byte of private
BSS for the rotating angle. Every decoded instruction offset, size and mnemonic
matches the immutable target, including both cdecl polar calls, both SI/DI
explosion-coordinate pairs, and the final RETF.

The full-link experiment places Kana exactly at 183C:05EA..07F7 and keeps the
complete owner's 71 relocation sites unchanged. Kana's complete 14-entry
relocation group now exactly matches the target order:

    1942,1937,1886,1858,1829,1799,1771,1742,1701,1658,1646,1626,1605,1573

Kana's remaining 18 linked-byte mismatches are not code-generation drift.
They are exactly nine 16-bit DS operands referencing the one-byte private
angle. The target uses DGROUP:2674 at all nine sites, while the mixed link
places Kana's byte at DGROUP:6960. The mismatching operand locations are
function-relative 96, 208, 237, 292, 295, 324, 379, 382 and 387. This separates
the solved TC4 producer/relocation question from the still-open physical BSS
ownership graph.

The reproducible object probe is:

    python3 scripts/probe_th03_main_bomb_kana_cpp.py --run-id UNIQUE_ID

The retained current object receipt is
.analysis/th03-main-bomb-kana-cpp/gpt-web-kana-precommit-b1-20261007/receipt.json.
The retained full-link diagnostic is
.analysis/th03-main-bombs-kana-link-probe/review.json.

No aggregate exact credit is claimed yet. Chiyuri, Ellen and Kana now reproduce
the target TC4J relocation behavior; Ellen and Kana still require their
historical private-BSS placement, and Kotohime/Rikako remain to be reconstructed
as TC4J producers.

This document intentionally does not claim exact acceptance yet. The candidate
lives in config/th03_main_bombs_candidate.toml so the default accepted aggregate
remains green. Promotion requires the normal two-round aggregate cold replay to
prove raw bytes, ordered relocations, MAP contribution, generated-object
integrity, determinism, and all pre-existing exact owners.
