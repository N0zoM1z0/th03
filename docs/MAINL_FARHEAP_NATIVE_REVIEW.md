# MAINL complete paragraph far heap

`src/mainl/crt/farheap.asm` recovers the complete 1,115-byte runtime member:
1,103 CODE +12 file-backed CS state bytes, with 14 procedures or ABI entries.
This is library source, with no authored game credit. Previous 181 owners and
nested scopes remain unchanged. Whole-product source ownership remains open.

## Actual native production

Two actual TASM assemblies, normal TLIB library builds and TLINK links produce
identical complete raw OBJ/LIB/EXE/MAP vectors. The complete EXE equals the pinned
Japanese decoded target; the complete MAP equals the retained MAP. All 893 member
positions and all 892 other current member payloads remain unchanged. The six
previous CRT source objects and 36 project objects are reused.

The new object's complete initialized payload and all 49 literal ordered native
fields equal the original member. LEDATA/FIXUPP packet boundaries may differ;
absolute field identity/order is checked without sorting. BYTE CODE, WORD empty
DATA, DGROUP membership, all state/API publics and both MAP tables are checked.
Every field resolves independently at the product layout. The complete literal
scoped MZ vector is empty: CS state references are offsets, not segment loads.

All 938 retained cold outputs, sources, recipe and tools remain validated and
unchanged. Only this producer, its normal library replacement and the affected
links were rebuilt. No full cold, DIET or ancestor runtime replay is needed.
The full cold recipe still contains six maintained CRT replacements; this
separate selected recipe adds the seventh source provider. Its actual native
closure is bound by the current publication. Future full recipe integration
must preserve the demonstrated member order and ABI.

## Heap representation and state

Blocks are measured in 16-byte paragraphs. Allocated headers store paragraph
count at offset 0 and preceding physical segment at 2. A zero predecessor marks
a free block. Free nodes keep circular-list previous/next segments at 4/6 and
the preceding physical segment at 8. User pointers have offset 4; free and resize
use the supplied segment and preserve the original ignored-offset behavior.

The first six CS bytes are genuine zero WORDs `___first`, `___last`, `___rover`.
The next six bytes are original uninitialized scratch WORDs: saved DGROUP and
the pending long resize request. They have no LEDATA initializers. Only these
six file bytes use actual repeated fresh linked output in the comparison;
neither invented zeros nor a new source initializer supplies them. The complete
bank owns 12 file DATA bytes, of which six have source initializers.

TASM treats a bracketed equated constant ambiguously. Explicit `DS:` identifies
the node accesses as memory, preserving the original default-DS instructions
without adding segment prefixes. CS and temporary SS accesses retain their
actual overrides. No target-byte arrays, NOP padding or object patches are used.

## Complete callable paths

| Physical body | Bytes | ABI or shared exit |
| --- | ---: | --- |
| Release top / interior block | 99 /113 | Near; interior can fall into unlink |
| Unlink / insert free node | 41 /55 | Near register ABI |
| free / farfree | 41 | One aliased far cdecl body |
| Start / extend heap | 100 /131 | Near register ABI |
| Allocate free tail | 35 | Near register ABI |
| malloc / farmalloc entries | 10 /125 | Shared far-return allocation body |
| Move growing / shrink block | 124 /100 | Near register ABI |
| realloc / farrealloc entries | 7 /122 | Shared far-return resize body |

All 1,103 instruction bytes, local branch destinations, near/far returns and
shared entry/exit boundaries are checked. Aliases add no procedures or bytes.
Allocation rounds byte count plus 19 into paragraphs, scans the rover ring and
takes oversized free blocks from their tail. Free coalesces physical neighbors
and updates the circular free ring. Insertion temporarily addresses the rover
through SS under CLI, restoring SS before the original POPF.

Resize preserves null-segment and zero-size paths, same-size returns, interior
remainder freeing and top-block brk changes. Growth copies the old payload:
12 bytes in the first paragraph, then up to 64 KiB per iteration. It then frees
the old block. Original global CS scratch, 16-bit arithmetic, CLD behavior,
partial-growth failures and state writes before brk are unchanged. No defensive
product fixes or physical DOS behavior claims are introduced.

Actual private inputs in `.analysis/work/`: `mainl-farheap-build.json`,
`mainl-farheap-native.json`, `farheap-source.asm`, `farheap-library.rsp`,
`farheap-link.lnk`, and both `farheap-roundN.obj/.lib/.exe/.map` vectors.
The verifier is `scripts/lib/decoded_mainl_farheap_native.py`.
