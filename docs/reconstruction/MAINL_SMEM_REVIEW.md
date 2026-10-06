# Complete MAINL stack-memory candidate review

Two complete frozen stack-library includes own74 body bytes /30instructions
and two trailing NOPs, all76bytes at decoded0000:1EAA..1EF5. SMEM_WGET's
private six-byte assignment prefix is part of the same include; its public
entry is1EC0. The complete previously reviewed628-byte heap/assignment cluster
executes as native context and receives no duplicate progress credit. All704
scoped raw bytes and empty original ordered relocations agree with two cached
products. No maintained MAINL source, stored-file offset or exact credit is added.

```sh
python3 scripts/review_th03_mainl_smem.py --output .analysis/NEW_SMEM_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_smem_review.py -v
```

Final receipt: `.analysis/sol-mainl-smem-review-20261006-final.json`. The guarded
prior heap receipt binds canonical stored/decoded/cached lineage. Eighteen frozen
providers bind both source trees, including the two new includes and the prior
heap/ABI/flags scaffold. Seven previously maintained MAIN-only Tupfile edits are
explicitly checked; MAINL includes and GAME=3 flags remain frozen. Source ASM/INC
comparisons normalize only LF/CRLF. Both cached root OMF objects are valid
TASM5/th03_mainl.asm and equal after dependency-timestamp normalization. MAP
containment scopes both clusters inside _TEXT. The rest of the generated root,
CRT/data/BSS and stored packaging remain unaccepted. Current Ghidra fails
headless usage before database attestation; no new database facts or cold build.

| Include /entry | Decoded offset | Body bytes /instructions | Far cleanup |
| --- | --- | ---: | ---: |
| SMEM_RELEASE | 1EAA | 15 /6 | 2 |
| SMEM_WGET including ASSIGNALL prefix | 1EBA /public1EC0 | 59 /24 | 2 |

The private prefix at1EBA is PUSH CS, CALL MEM_ASSIGN_ALL, JB error2; it falls
through to the public entry. SMEM_WGET's TopSeg-zero branch returns to that
prefix. Its direct errors share the1EEF failure tail, with distinct BX-pop
requirements depending on whether the argument-loading prefix has run. NOPs
at1EB9/1EF5 are macro EVEN results. Every body instruction, interior RETF2,
direct branch and call site is checked. Operand/neighbor/indirect/far edges
and any DOS/ports inside the two new bodies are rejected. DOS appears only
inside the reviewed native assignment context.

## Native execution and comparison scope

Each image has488 scenarios and582 terminal top-level invocations, with692
native entries including context. Across original/two caches,1746 calls return
and2076 native entries execute. Full1MiB outside the declared64K stack is
checked against an independent physical-memory scalar algorithm after every
call. Whole-memory hashes remain per-image because unrelated target/cached
PI encodings and DGROUP0849 differ; scoped state, requests, return values,
native counts and writes agree across images. No new malformed-loop budget
is substituted for a return; the prior heap receipt keeps its separate cycles.

The probe relocates the image to2000, with DGROUP2E3F and stack4000. Heap
fixtures and owned header words follow the prior heap review. Only original
DOS INT21/AH48 and49 at four reviewed context sites are modeled, returning
explicit AX/BX/CF without real allocation/free, ownership or memory unmapping.
All new bodies, MEM_ASSIGN_ALL/MEM_ASSIGN and connected HMEM allocation/free/
unassign functions execute native instructions and real RETFs. Native frame
tracking handles a public get-entry recheck after the private assignment prefix
without inventing a second call frame or duplicate invocation count. Unknown
interrupts, ports, writes, escapes and invalid frames fail; callback exceptions
stop execution and raise outside FFI. No MEM_READ hook is installed.

Matrices cover both DF values, byte-size boundaries0/1/2/15/16/17/FF/100/101/
FFF/1000/1001/FFF0/FFF1/FFFF, EndMark0/1/6000/60FF/6100/6101/FFF0/FFFF,
word-add carry, heap equality/overflow, releases with initialized/uninitialized
TopSeg and arbitrary segment values, DOS status/zero-segment retry fixtures,
reserve/largest-block cases, release/get reuse and native stack/heap collisions.
One128-case subset checks all64 arithmetic-status combinations (CF/PF/AF/ZF/
SF/OF) under both DF states for release; IF is1 and TF0. Real interrupt routing,
trap behavior and physical DOS allocation are outside this fixture proof.

Eight controls reject body/context truncation/cleanup, private-prefix and
producer mutation, operand/neighbor/unknown call/indirect/far edges, DOS/ports
inside owned stack bodies, guarded FFI failures and unowned whole-span stores,
release AX/flag clobbers, invalid native entry/return frames, stale completion
and segment aliases. A positive private-prefix/assignment/entry-recheck control
executes nested native far returns with one get frame. Runtime controls retain
untampered static metadata while injecting synthetic code to test guards;
this does not accept synthetic code as product source.

## Stack allocation and lazy initialization

SMEM_WGET tests TopSeg before reading its argument. Zero TopSeg branches into
the private native MEM_ASSIGN_ALL call. Returned CF-set immediately returns
FFF8 (InsufficientMemory), preserving the existing EndMark and other stale
managed fields. This differs from HMEM_ALLOC's previously reviewed ignored
assignment carry. Successful assignment falls through and rechecks TopSeg;
an adversarial CF-clear zero DOS segment causes another assignment attempt.
The constructed fixture subsequently returns6000, and both native calls and
all metadata effects are checked. No real DOS zero-segment guarantee follows.

The byte word is rounded with ADD15, carry-preserving RCR and three SHR
instructions. FFF1..FFFF require1000 paragraphs, without a16-bit addition
wrap to zero. The function loads the old EndMark into AX, adds rounded size
into BX and rejects carry or unsigned candidate > TopHeap. On success it
stores the candidate as EndMark and returns the old EndMark with CF0.
On failure it returnsFFF8/CF1 without changing EndMark. Mem_AllocID, MyOwn,
FirstHole and heap headers are untouched by ordinary initialized gets.

A zero-size get still compares EndMark with TopHeap: valid equality succeeds
and returns the current EndMark, but a previously corrupted EndMark > TopHeap
fails. Thus the upstream universal current-position comment depends on the
valid-space invariant. EndMark0 can returnAX0/CF0 in the fixture; do not invent
an AX-zero failure sentinel. Exactly meeting TopHeap is allowed. An allocation
of the next byte then fails unless some space is released or native heap free
moves TopHeap upward.

## Release and shared-space sequences

SMEM_RELEASE loads its segment argument through SS and writes EndMark directly.
It preserves all supplied general registers, DS/ES and the tested status flags,
including incoming carry. It does not inspect TopSeg, TopHeap, OutSeg, MyOwn,
header membership or release order; it can move EndMark forward, backward,
to0 orFFFF. It neither clears payload nor frees a DOS block. The release/get
chains execute those arbitrary updates and resulting capacity checks; they
are unchecked contracts, not safe stack-lifetime guarantees.

The collision chain allocates eight native heap paragraphs, consumes512 stack
bytes, and observes a222-paragraph heap request fail against the moved EndMark.
It releases the saved stack mark and frees the original heap block, then a
255-paragraph heap allocation consumes the entire6000..6100 region including
its header. Get0 succeeds at equal EndMark/TopHeap, while Get1 fails. After
native heap free, Get4096 reaches TopHeap exactly; another byte fails. Release
restores the saved mark, and real TH03 unassign runs. Every step checks physical
memory and CF with the same native heap/stack state. A second chain releases
an earlier mark and reuses it, confirming lack of individual-block tracking.

One decoded module row owns only76new bytes; the628native context is not
credited again. Earlier archive/graphics/file/lifecycle receipts retain their
explicit memory models; complete combined game callers, CRT allocators,
physical DOS/lifetime, root/data/BSS ownership, cold localized production and
canonical DIET packaging/full Oracles remain open with the505-file intake and
requested English commits.
