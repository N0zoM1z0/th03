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

The reproducible object-level probe is:

    python3 scripts/probe_th03_main_bomb_ellen_cpp.py --run-id UNIQUE_ID

The retained maintained-source receipt is
.analysis/th03-main-bomb-ellen-cpp/gpt-web-ellen-compat-20261007/receipt.json.
It intentionally records exact_acceptance=false: the 252 pre-link raw-byte
differences are unresolved OMF data/fixup operands and must not be normalized
away as an exact result. The next gate is to reproduce the historical
MAIN_05_TEXT physical producer placement, the private DGROUP placement, and
the final TLINK/MZ relocation order in a full-owner link.

This document intentionally does not claim exact acceptance yet. The candidate
lives in config/th03_main_bombs_candidate.toml so the default accepted aggregate
remains green. Promotion requires the normal two-round aggregate cold replay to
prove raw bytes, ordered relocations, MAP contribution, generated-object
integrity, determinism, and all pre-existing exact owners.
