# MAINL natural C++ allocation and exception providers

`new.cpp`, `xalloc.cpp` and `xmsg.cpp` now reproduce the complete native modules
through the scoped optimizing Borland compiler. Six owners add2258 bytes and16
far procedures. MAINL accepts211 extents/288 procedures/36,946 bytes,including
34,333 instruction bytes,2607 initialized DATA bytes and6 bytes of actual
uninitialized file storage. Source presence stays240 extents/47,388 gross bytes;
historical overlapping aggregates are not additional exact credit.

Operator new converts zero to one,tries malloc,and calls the installed far
handler before retrying. A null handler permits a null return. The default
handler throws the static xalloc("Out of memory",0),without rewriting its size
field. Set-new-handler returns the previous pointer. Xalloc initializes its xmsg
base and size,then raises by value. Xmsg deep-copies its owned string. Assignment
checks self-identity,then deletes before allocating the replacement. The original
unchecked allocation and exception-safety behavior is preserved.

The decisive producer is `BCC.EXE`4.5 with large-model8086 `-O1 -xc -Vs -zC_TEXT`,
using the existing pinned TC4 Japanese SDK headers. The compiler,RTM and DPMI
helper are separately pinned in `config/mainl_work/exception_toolchain.toml` and
kept in a private isolated directory without ambient compiler configuration.
The archived Borland [DOS RTL makefile](https://github.com/earthsiege2/borland-cpp-ide/blob/897e9590fc092739e7bec67423062b7d8a34b568/SOURCE/RTL/DOS.MAK)
also selects `-O1` for normal optimized builds. Its relevance was tested against
the maintained sources; it is not evidence of the game's original compiler
installation. The [Borland4.0 guide](https://bitsavers.org/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_4.0_Users_Guide_Oct93.pdf),
[compatible-exception documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_5_Users_Guide_1997.pdf)
and [local inline documentation](https://bitsavers.trailing-edge.com/pdf/borland/borland_C%2B%2B/Borland_C%2B%2B_Version_3.1_Users_Guide_1992.pdf)
explain the flag families. Native output establishes suitability for this scope.

The previous TC4 `-O -r- -Z` profile emitted735/502/935 bytes. BCC4.5 with that
same profile produces identical initialized payloads and retains the gap.
Selecting its optimizer restores754/513/955 bytes,including the unused SI/DI
saves and original helper instruction choices. BCC4.00 was also examined: it
rejects `-xc` and emits a different exception initializer ABI. The earlier
failed receipts remain historical evidence; the obsolete candidate verifier is
superseded by `decoded_mainl_exception_native.py`.

The three CODE-class segments contain1563 instruction bytes and659 bytes of
inline cleanup/type/scope data. The xmsg constructor's167-byte body is followed
by a36-byte cleanup record. These records are classified independently of
instruction decoding. New also contributes DATA24,INIT6 and EXIT6. Only18 DATA
bytes have OMF initializers; the first6 reserve the static xalloc object.
Those6 file bytes come from the two actual target-equal native links. No source
initializer or zero-filled object buffer is invented for them. Summary fields
keep initialized DATA and uninitialized file storage separate; the progress
image's DATA total2613 includes both. No BSS file-byte credit is added.

The reviewer checks complete native payloads,literal ordered fields,segment
packing/group order,all public/external identities,normal-library MAP allocations,
far cdecl bodies and all local branch destinations. It independently resolves
all122 fields,including real far CALL relaxation and cross-segment string calls.
Each complete extent and literal ordered MZ vector matches target and candidate.
Xalloc's descending vector starts543A,53BB; no vector is sorted or rewritten.

Two actual compiler/TLIB/TLINK rounds repeat whole three-OBJ/LIB/EXE/MAP vectors.
The normal893-member library contains28 source providers,including19 validated
reused natural objects and six retained source providers. All871 other current
members and36 project objects stay unchanged. Complete EXE and MAP match the
fixed Japanese decoded target and retained MAP. The old938-output cold pair is
validated and reused; full cold/DIET and ancestor runtime chains are not replayed.
All205 prior accepted owners and their scopes remain intact. Whole-product
source ownership and whole-game denominators remain open.
