# Entire original DOS qsort: reconstructed 8086 source and exact MAINL link

The formerly open 756-byte Borland DOS qsort CRT member at index275
is now recovered as a **complete, maintained 8086 assembler source
translation unit**, src/mainl/crt/qsort.asm, using natural
instruction mnemonics, actual original shared BSS symbols, descriptive
control-flow labels and true external arithmetic helper calls. The
source includes qswap.inl, qcore.inl, and qentry.inl, which own
three original contiguous semantic functions. It is a reconstructed
assembly-level implementation, **not a claim to have found the
historical Borland C/C++ source**. No DB opcode arrays, zero/NOP
gaps, arbitrary target bytes, modified original OBJ or post-link
patches are used.

The actual Borland TASM 5.0 output has the following original geometry:

| Source function | Original CODE offset | Full original CODE bytes |
| --- | ---: | ---: |
| private near element swap | 0000 | 46 |
| private near recursive quicksort/partition core | 002E | 666 |
| public far qsort front end | 02C8 | 44 |
| **Entire CODE segment** | | **756, all exact** |

The **entire source-assembled 756-byte CODE segment** is byte-for-byte
equal to the fixed Japanese original qsort.obj, including every branch
encoding and all relative near calls. All **29 literal ordered OMF
FIXUPPs** agree in location, width, frame/target type/index and addend,
not simply in count. The genuine DATA0/BSS6 segments, original
08ff03ff02 GRPDEF, public _qsort at offset712 and original
N_LXMUL@, N_LDIV@ external import order are unchanged. Native
OMF storage/comment wrappers can naturally differ without altering
the original segment ownership or linked product.

The recursive core is reconstructed in understandable algorithm
sections: up to three elements are handled explicitly; the first,
middle and last elements establish the pivot ordering; a partition
walk compares through the original far BSS callback and exchanges
elements with the private near routine; it then places the pivot,
computes partition sizes via the original 16-bit large arithmetic
helpers, recursively sorts the smaller side and tail-loops on the
other. It preserves the original 24-byte stack frame, original far
parameter layout, near Pascal RET 6, near swap RET 8, all seven
indirect far comparator calls, six near swap calls, two recursive
near calls and four native arithmetic helper calls. The BSS holds a
far comparator pointer followed by the element-width WORD.

The independent scoped build_th03_mainl_qsort_work.py compiles this
full original assembly TU twice using native TASM, then reconstructs
the original **893-member MAINL library**, replacing qsort at
original slot275 along with the 16 previously reconstructed source
objects, including the complete 12,622-byte xx and the original
signed/unsigned parser and tokenizer functions. The other **876
complete original member program records** remain unchanged.
Two genuine serialized TLIB/TLINK rounds each reproduce the entire
**67,372-byte decoded Japanese MAINL EXE** and the complete original
MAP byte-for-byte, including all **677 original MZ relocations**.
The combined exact native source CODE extent is **14,870 bytes**
across 17 genuine source library modules.

Before this complete recovery, earlier bounded diagnostic sources
proved only the 46-byte private swap and 42 of44 public-entry bytes,
with a deliberately short stub for the 666-byte core. Those
diagnostics and the original control-flow blueprint remain useful
historical checks, but **their earlier complete_qsort=false
results do not describe the current full native source**. The real
full source now has the complete 666-byte core, no stub, all29 fields
and a verified whole-product link.

The original accepted28-provider CRT library, the frozen211-owner
MAINL source publication, the retained original cold pair and
the canonicality status candidate-local-attested are unchanged.
This is exact natural assembler-source output in a separate working
CRT, **not an automatic formal accepted-ledger promotion**:
source_acceptance=false, added_accepted_bytes=0. No full cold
replay, DIET repack or ancestor runtime chain was performed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_qsort_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_qsort_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_qsort_work

Retain .analysis/work/mainl-qsort-native-{build,review}.json,
two complete qsort-full-roundN-{qsort.obj,newcrt.lib,linked.exe,linked.map}
raw native output vectors, TASM/TLIB/TLINK phase logs and response
files. Both source and report hashes are independently bound to the
original Japanese module and unchanged accepted baseline.
