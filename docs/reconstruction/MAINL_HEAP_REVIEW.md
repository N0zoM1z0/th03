# Complete MAINL heap-manager candidate review

Five complete frozen heap/assignment includes cover eight procedures, 625
body bytes /257instructions and three trailing NOPs: all628bytes at decoded
0000:210A..237D. Shared byte-allocation and invalid-free tails remain inside
this single ownership cluster. Every scoped raw byte and the empty original
ordered MZ relocation set agree with both cached products. No maintained
MAINL source, canonical stored-file offset, source acceptance or exact credit
is added.

```sh
python3 scripts/review_th03_mainl_heap.py --output .analysis/NEW_HEAP_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_heap_review.py -v
```

Receipt: `.analysis/sol-mainl-heap-review-20261006.json`. The guarded preceding
file-library receipt carries stored/decoded/cached target lineage. Sixteen
consulted frozen providers bind both source trees, normalizing LF/CRLF only
for ASM/INC. Heap includes have no maintained MAIN source overlay. Cached
Tupfile.lua retains seven explicitly checked substitutions inside the earlier
maintained MAIN graph; MAINL and the GAME=3 assembler flags remain frozen.
These scaffold edits grant no MAINL acceptance. Both root OMF objects have
valid TASM5 /th03_mainl.asm identity and equal dependency-timestamp-normalized
hashes. MAP containment binds the complete cluster to _TEXT. Neighbors, the
separate CRT farheap contribution and generated DATA/BSS ownership are excluded.
Current Ghidra fails headless usage before database attestation; no new database
observations or fresh cold compiler execution are used.

| Entry | Decoded offset | Body bytes /instructions | Far cleanup |
| --- | --- | ---: | ---: |
| HMEM_LALLOCATE | 210A | 52 /24 | 4 |
| MEM_ASSIGN_DOS | 213E | 33 /15 | 2 |
| MEM_ASSIGN | 2160 | 38 /13 | 4 |
| MEM_ASSIGN_ALL | 2186 | 39 /20 | 0 |
| HMEM_ALLOCBYTE | 21AE | 20 /9 | 2 via shared tail |
| HMEM_ALLOC | 21C2 | 240 /90 | 2 |
| HMEM_FREE | 22B2 | 168 /71 | 2 including shared exits |
| MEM_UNASSIGN | 235A | 35 /15 | 0 |

Trailing NOPs are215F/21AD/237D; `func.inc` aligns function starts/ends with
EVEN. The internal233D NOP remains a body-owned instruction. ALLOCBYTE ends
with a jump21C0->21C9 into the allocation body after its argument-loading
prefix. FREE's two invalid-input branches22C4/22CC enter the allocation return
tail22AC, sharing POP ES/CX/BX and RETF2. Four reviewed PUSH-CS/native CALL sites
link long->alloc, assign-DOS->assign, assign-all->assign and alloc->assign-all.
Every instruction, branch, interior far return and cleanup is checked; other
operand/neighbor/indirect/far edges and unknown ports/DOS sites are rejected.

MEM_UNASSIGN also emits the four-byte XOR AX/AX, STC, RETF failure tail at2379.
Under the pinned GAME=3 conditions, the two GAME==1 live-allocation tests are
absent. No branch in the reviewed include cluster reaches this emitted tail;
it remains classified compiler/source code, not omitted or padding. External
private-entry ownership is not inferred from this bounded CFG observation.

## Native execution and explicit DOS boundary

Each image has814 terminal matrix scenarios,1302 top-level calls and1416
native entries. Across original/two caches,3906 calls return and4248 native
entries execute. Each image additionally has four1000-instruction malformed
cyclic-list budgets; across all three, twelve calls remain nonterminal. Thus
3918 total invocations comprise3906 returns and12 budgets. Budgets are recorded
separately; no synthetic return or full malformed-list termination is claimed.

Native assignment/allocator/free bodies and actual RETFs execute. The probe
checks every native caller/return frame and Pascal cleanup. BX/CX/DX/BP/SI/DI/DS
are preserved; ES is also preserved except MEM_UNASSIGN's documented clobber.
Inherited DF and final CF are checked. Defined allocation/assignment diagnostics
and all memory effects agree with an independent scalar segment-list algorithm;
void free/assignment AX registers are not promoted to C return guarantees.

The image is relocated to2000, DGROUP2E3F, stack4000. Declared heap fixtures
occupy5000..8FFF segments; specified additional headers support high-segment
wrap and invalid-free controls. Each header has using,nextseg,id words at0/2/4
within a16-byte management paragraph; its remaining bytes are preserved. All
1MiB outside the declared64K stack is checked after each normal call. The
actual native writer may change only the managed DGROUP fields and complete
owned header words. Cyclic controls compare expected partial memory effects
and the live instruction against the known loop. Whole-memory hashes remain
per-image because unrelated PI bytes and DGROUP0849 differ; scoped results,
requests, native counts, state and write counts agree across images.

Only DOS INT21/AH48 and49 at four reviewed sites are modeled. Allocation
fixtures return explicit AX/BX/CF without supplying a real allocator or lifetime;
free returns AX/CF without unmapping memory. Requests record sizes/segments and
order. Other DOS calls, ports and escaped CODE fail. Callbacks stop execution
and raise outside FFI. No MEM_READ hook is installed with native far returns.
These results do not prove real DOS allocation, ownership, exhaustion or use
of freed storage. Unusual CF-clear zero segments, query success, errorAX0 and
noncanonical header states are explicitly adversarial interface fixtures.

Matrices cover both DF states, byte/paragraph/long rounding boundaries,
capacity subtraction/borrow and end-marker equality, zero/wrapped assignments,
reserve versus largest-block bounds, DOS AX/CF combinations, lazy initialization
failure with stale fields, every3-header combination of using0/1/2, hole split/
just-fit/later-hole/center fallbacks, add carry, header ID preservation, invalid
free values/flags and missing upper bound. Twenty-four release permutations
per DF execute four allocations, every free order, full-capacity reuse and
unassign. Additional sequences reuse holes or combine DOS assignment/allocation/
unassign. The three raw translations receive the same matrix.

Nine controls cover complete lengths/cleanups, the shared branch whitelist,
unreachable-tail/producer mutation, native sites/PUSH CS, unknown indirect/far
edges/DOS/ports, scaffold substitution scope, guarded FFI failures, whole-span
header/data stores, native entry/return frames, shared and nested positive
RETFs, stale completion, segment aliases and ES versus other saved registers.
Runtime mutations retain untampered analysis metadata to exercise guards
independently, without accepting synthetic code as product source.

## Allocation size, lazy setup and ID behavior

HMEM_ALLOCBYTE forms ceil(bytes/16) using ADD15 with its carry through RCR,
then three SHR instructions. The17-bit result prevents FFF1..FFFF byte sizes
from wrapping to0; they request1000 paragraphs. Paragraph allocation accepts
only nonzero size strictly below unsigned OutSeg-EndMark, then adds one header
paragraph. Zero/full-gap failures clear the whole AllocID word, returnAX0/CF1
and preserve other public registers.

Long allocation adds15 modulo2^32, shifts right four bits and rejects any
remaining nonzero high word before entering HMEM_ALLOC. This early failure
returns0/CF1 while **retaining AllocID**. FFFF1 bytes need10000 paragraphs and
follow that path. FFFFFFF1..FFFFFFFF instead wrap the rounding addition to0,
enter real HMEM_ALLOC with0 and fail while **clearing AllocID**. FFFF0 bytes
formFFFF paragraphs but fail the allocator's strict gap gate. There is no
saturating arithmetic or universal ID-clearing contract for the long wrapper.

When TopSeg is0, HMEM_ALLOC calls real MEM_ASSIGN_ALL before checking even a
zero request. It does not branch on the returned carry. Failed DOS setup can
therefore leave TopSeg0 while stale OutSeg/EndMark/TopHeap permit a successful
allocation. The matrix explicitly checks that path; it does not make stale
fields valid DOS ownership. Each eventual allocator success transfers AllocID
to header.id via XCHG, clears it in DGROUP, returns header segment+1 and CF0.
Failure clears it as described. Free does not clear ID or payload/header-id.

## Holes, central allocation and release

Search begins at FirstHole when nonzero, walking nextseg words and treating
only using0 as free. A candidate must add total paragraphs without16-bit carry
and fit at or below nextseg. A remainder of0/1 paragraphs consumes the whole
hole; larger remainders create a new free header, retaining its old id/other
bytes. FirstHole updates only when consuming/splitting that first hole; the
next-hole LES loop reads the current using/nextseg pair and finds a later0
flag or clears FirstHole at OutSeg. Unsuccessful search falls back to the
central unused region, subtracting total size from TopHeap with borrow/end
checks, setting using1/nextseg and the transferred ID.

Non-first FREE converts data segment to header via DEC, rejects headers below
TopHeap, and otherwise requires using==1. It does not check an upper bound,
block-list membership or payload lifetime. Inactive using0 returns through the
shared tail with CF1; other non-1 flags returnCF0 from CMP, and a below-heap
header returnsCF1. These are incidental void-return flags, not validation APIs.
A declared header at OutSeg or wrappedFFFF can be released under those rules.

Valid non-first release marks using0, keeps its id and chooses the smaller of
old FirstHole and freed segment. If there was no earlier hole, it returns
immediately. Otherwise it traverses and joins adjacent free headers through
the freed block's successor, adjusting the limit for a tail block. Native
coalescing is tested against all release permutations and the scalar graph.
There is no cycle or corruption check. A cyclic used search list loops without
writes; a cyclic connection list remains nonterminal after marking the requested
header free and updating FirstHole. Expected partial effects are retained.

When a supplied header equals TopHeap, FREE skips the using==1 check, moves
TopHeap to its nextseg and optionally absorbs the following free block. It
then searches for the next FirstHole; the original freed header's using/id
remain unchanged. Top-header fixtures with using0/2/FFFF are accepted by this
path. No generalized idempotent-free or heap-integrity promise is inferred.

## Assignment and removal

MEM_ASSIGN writes TopSeg/EndMark, adds paragraph size modulo65536 into
OutSeg/TopHeap, resets FirstHole and MyOwn, and clears CF. It validates neither
zero top, zero size nor segment-add overflow. MEM_ASSIGN_DOS requests AH48,
uses returned AX/BX for real assignment on CF-clear, sets MyOwn1 and returns
AX0/CF0. DOS failure negates the AX error word; error0 therefore appears as
AX0/CF0 without assignment. Return BX is explicitly preserved by the wrapper.

MEM_ASSIGN_ALL first requestsFFFF paragraphs to obtain the largest block in
BX, ignoring the first AX/CF. It subtracts Reserve only if largest>Reserve;
otherwise it requests the entire largest value, including0. Second-call
success assigns returned AX/BX, sets MyOwn1 and returns the saved DOS segment;
failure preserves old managed fields. Default Reserve is256 paragraphs in
the frozen declaration; real available-memory behavior remains unproved.

TH03 MEM_UNASSIGN does not inspect live heap or stack allocations. If TopSeg0,
it returns1 without DOS. Otherwise ES receives TopSeg, TopSeg is cleared, and
MyOwn controls whether DOS free is requested. Both DOS success and failure
returnAX1; CF from free remains observable. OutSeg/TopHeap/FirstHole/EndMark/
MyOwn/AllocID are retained. Non-owned memory is merely removed from management.
This can report C success with live allocations and a failed DOS free; the
GAME==1 checks cannot be imported into TH03 as an exactness fix.

One decoded module row covers this628-byte cluster. Prior archive, file,
CDG/PI/cutscene and lifecycle receipts retain their explicit heap models;
this review does not retroactively claim their complete combined execution.
The stack-memory/CRT allocators, full root/data/ownership, actual DOS/runtime,
cold localized production and canonical DIET packaging/full Oracles remain
open alongside the full505-file intake and requested English commits.
