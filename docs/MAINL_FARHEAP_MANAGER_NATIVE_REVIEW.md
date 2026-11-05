# Full original Borland farheap memory manager and literal OMF equality

`src/mainl/crt/farheap.asm` reconstructs the **entire 1,115-byte original
Japanese CL.LIB farheap member 166** as real 8086 source, including allocator
and deallocator implementations, internal search/merge/split helpers, segment
growth, heap state, and the original heap-copy/resize code. This is a full
heap allocator, not a thin leaf. It preserves the original near/far ABI and
all **nine original public symbols**:

| Original `_TEXT` offset | Original public symbol(s) | Scope |
| ---: | --- | --- |
| 0, 2, 4 | `___first`, `___last`, `___rover` | initialized far-heap segment-link state |
| 320 | `_farfree` and `_free` | the original shared free body and two public aliases |
| 627 | `_malloc` | near malloc wrapper |
| 637 | `_farmalloc` | complete far malloc, rover and heap extension |
| 986 | `_realloc` | near realloc wrapper |
| 993 | `_farrealloc` | far realloc with in-place resize, copying and block management |

The single original `_TEXT` CODE segment is **1,115 bytes**. Its three
public 16-bit state words at offsets 0, 2, 4 are explicitly initialized;
the next three state words at **_TEXT+6..11 are genuinely uninitialized**,
and must *not* be emitted as initialized CODE. The natural declarations
`dw ?` preserve those six nonmaterialized sites, original segment length,
loader behavior and the original object record boundaries. Only the
remaining **1,109 CODE bytes** are materialized in the OMF records. There
is a zero-byte `_DATA` segment; the original DGROUP is preserved.

The source keeps default DS memory references when accessing the heap
block header, explicit CS/SS/ES references for global state, and the original
near Borland `__brk` / `__sbrk` imports. TASM requires the actual default
DS memory operand form (`word ptr ds:[offset]`) for numeric heap header
offsets: plain `[offset]` is otherwise interpreted as an immediate value,
causing illegal-instruction errors. The explicit memory declaration
preserves the original **x86 bytes and OMF frame**, without introducing an
unwanted DS segment override or changing the DOS behavior.

## Strongest scoped native proof: literal OMF program identity

Unlike many reconstructed Borland C++ members, this source produces the
**complete original CL.LIB member OMF program records byte-for-byte** in
both independent native TASM/TLIB/TLINK rounds, not just matching CODE.
The complete **49 original relocation fields, their literal FIXUPP order,
frames and targets** agree. All nine public labels, including the *two*
labels at `_TEXT+320`, both imports and the original uninitialized six-byte
state gap also agree.

`scripts/build_th03_mainl_after332_work.py farheap-manager` consumes the
source/receipt-validated **343-member** MAINL CRT chain (including the 13-API
isctype and 11-API stringio additions) and validates both native rounds
without rebuilding the unchanged cold baseline. All **893** CRT library
programs remain in their original order: **344** produced from complete
native source, **549** carried as unchanged contextual original members.
Both rounds reproduce the full decoded original Japanese **67,372-byte EXE
and MAP** including **677 DOS MZ relocations in exact original order**.
Total working-source CRT CODE reaches **114,620 bytes**, an increase of
**1,115**. The complete raw OBJ/LIB/EXE/MAP and writer logs are retained
under `.analysis/work/after332-*`, with driver/source/parent hashes bound in
both receipts. The affected reviewer and regression tests live in
`scripts/review_th03_mainl_after332_work.py` and
`tests/test_mainl_after332_work.py`.

This member is **working-source native source-bound reconstruction**, not
Factory-accepted decoded/packed-file ownership or whole-game exactness.
No full cold replay or target-object patch was used.
