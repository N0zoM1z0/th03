# Original high-address qsort: complete 916-byte native DOS source

The separate Borland CRT high-address sorting module (member464,
public __hqsort) is now a **complete maintained 8086 source** in
src/mainl/crt/hqsort.asm with its private hqcore.inl and public
hqentry.inl. It shares the already recovered original private
qswap.inl swap implementation with ordinary qsort. This source
reconstructs the original instruction-level implementation; it is
**not a claim to possess the original historical Borland C file**.

Unlike ordinary qsort, this high-address variant must preserve
actual DOS far-pointer arithmetic and segment carry semantics.
It imports eight real native near arithmetic helpers in original
order: N_PADD@, N_LXMUL@, N_PADA@, N_PCMP@, N_PSBA@, N_PSUB@,
N_PSBP@ and N_LDIV@. Its recursive sorter handles the original
first/middle/last ordering, far comparator callbacks, pivot
placement, forward/reverse partition walks, swap calls and
smaller-side recursive/tail-loop logic with genuine Pascal RET 6.

| Original native function | CODE offset | Reconstructed bytes |
| --- | ---: | ---: |
| private near swap | 0000 | 46 |
| near high-address recursive core | 002E | **826** |
| far public __hqsort | 0368 | 44 |
| **Complete original TU** | | **916** |

All **916 original CODE bytes** of hqsort.obj now exactly match
actual native TASM output, not just the function lengths. All
**52 literal ordered OMF FIXUPPs** agree with the fixed Japanese
original in site, field width, segment-relative/absolute kind,
frame, target, index and addend. The original public entry at
offset872, all eight imported symbols and their actual EXTDEF
order, zero-length DATA, six genuine BSS bytes and literal
08ff03ff02 segment group also agree. The private near swap
remains identical to the original 46-byte body. The core uses
plain typed 8086 assembly instructions, descriptive control
labels and real imported symbols; no target opcode byte arrays,
alignment padding or binary object patches are used.

The independent scoped build compiles the entire high-address
source twice using actual TASM and then rebuilds the original
**893-member MAINL CRT library**, retaining the 17 previously
proved true source objects (including complete normal qsort,
complete xx exception/RTTI, the signed/unsigned parsers and CRT
string functions). hqsort occupies original slot464; the other
**875 library program records** stay exactly original.
Two serial TASM/TLIB/TLINK rounds independently reproduce the
complete **67,372-byte decoded Japanese MAINL EXE**, its entire
original MAP and all **677 original MZ relocations** byte-for-byte.
The simultaneous reconstructed CODE extent across 18 native
source modules is **15,786 bytes**.

Both normal qsort (756 bytes/29 fields) and high-address qsort
(916 bytes/52 fields) are thus fully source-assembled and
whole-product raw-equal, not merely disassembly blueprints.
Their original ABI and source modules remain distinct.

The accepted 28-provider CRT library, published 211-owner
MAINL accepted scope, pinned Japanese target and unchanged
cold pair are not overwritten. The source-only carrier reports
source_acceptance=false and added_accepted_bytes=0: **this is
reconstructed native source, not yet formal ledger promotion**.
No full cold replay, DIET stage or ancestor runtime reconstruction
was performed in order to validate this member.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_hqsort_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_hqsort_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_hqsort_work

Retain .analysis/work/mainl-hqsort-native-{build,review}.json,
two complete hqsort-full-roundN raw OBJ/LIB/EXE/MAP vectors,
actual TASM/TLIB/TLINK phase logs and the source-bound responses.
