# Complete MAINL archive INT21 hook candidate review

The complete pfint21.asm contribution spans605decoded bytes at0000:2850..2AAC:
549instruction bytes /225instructions across PFSTART, PFEND and the interrupt
handler,50table bytes, five mutable CS state bytes and one alignment NOP.
All605raw bytes and the single original ordered MZ relocation (0000:295D)
agree with both cached candidates. The root's following db0 at2AAD is excluded.
No maintained MAINL source, canonical stored offset or exact credit is added.

```sh
python3 scripts/review_th03_mainl_pfint21.py --output .analysis/NEW_PFINT21_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_pfint21_review.py -v
```

Receipt: `.analysis/sol-mainl-pfint21-review-20261006.json`. The preceding buffer
receipt guards canonical/decoded/cached lineage. Thirty-two consulted frozen
providers bind both cached trees, using explicit ASM/INC line-ending conversion
and raw header comparison. This hook remains frozen source. Its PFOPEN dependency
retains the previously proved maintained MAIN inl overlay; both local files
match cached copies. No MAIN or earlier decoded acceptance is inherited.
Root OMF has valid TASM5/th03_mainl.asm identity and equal dependency-timestamp
normalized hashes. MAP containment binds this bounded include to _TEXT; other
generated root CODE/DATA/BSS remains unowned. Ghidra fails headless usage before
selected database attestation; no new database facts or cold builds are used.

| Contribution | Decoded coordinate | Bytes | Instructions |
| --- | --- | ---: | ---: |
| Saved old vector /reentrancy byte /NOP | 0000:2850 | 6 | 0 |
| PFSTART, far RET4 | 0000:2856 | 188 | 88 |
| PFEND, far RET | 0000:2912 | 56 | 20 |
| Handler initial code | 0000:294A | 56 | 19 |
| Dispatch table, twelve word pairs | 0000:2982 | 48 | 0 |
| Handler request bodies | 0000:29B2 | 198 | 76 |
| IOCTL mask14CF | 0000:2A78 | 2 | 0 |
| Handler exit code /actual IRET | 0000:2A7A | 51 | 22 |

The handler's305 CODE bytes and50data bytes form one355-byte procedure. Tables
are excluded from disassembly, and direct branches must reach CODE instruction
boundaries. The dispatch operand and all twelve target words are checked at
runtime. Saved-vector far jumps may reach only the declared kernel interface.
Mutable CS slots are old vector2850..2853, on_hook2854, and dispatch sentinel
low byte29AE; no fabricated product byte arrays or padding are introduced.

## Connected native scope and explicit interfaces

All prior archive open/name comparison/read/RLE/rewind/seek/close and buffered
open/fill/getc/read/seek/close/DOS-open instructions execute in the same loaded
image as the hook. Their complete1198-byte contextual contributions, including
producer bytes, are checked against both caches with original relocation order.
They add no duplicate unit/function/byte credit. Calls retain real near/far
frames and returns; native indirect PFILE slots are constrained to their proved
entries. Earlier separate receipts retain their original explicit buffer models.
This receipt establishes a new combined observation without rewriting those
earlier observations or upgrading their acceptance.

Remaining interfaces are HMEM_ALLOCBYTE/HMEM_FREE, high-level FILE_ROPEN/
FILE_READ/FILE_CLOSE used during installation, and DOS INT21 requests. The heap
model supplies header/directory/PFILE/BFILE segments and independent CF values,
recording size and current allocation ID. File models record far-pointer/size
requests and inject constructed16-byte archive headers and encoded entry bytes.
Actual allocation, DOS files/assets, high-level file bodies, vector tables,
interrupt timing and kernel handlers are not executed. Failed statuses with
injected data are adversarial interface fixtures, not actual failure guarantees.

The synthetic old DOS boundary validates the original interrupt frame, records
restored registers/live IF, changes declared AX/DX/CF and then executes a one-byte
fixture IRET. The game's handled-request IRET executes from the actual target
body. Interrupt frames are supplied explicitly; actual hardware INT dispatch
and reentry through an installed DOS vector are not simulated. Inner native
DOS calls use their declared boundary directly, while separate on_hook1/FF
cases execute the game's real immediate old-vector jump. Callback errors stop
and raise outside FFI; there is no memory-read hook with native far returns.

Each original/cached image has1302 scenarios and1398 top-level invocations,
all terminal; across three images,4194 calls and2898 contextual native entries.
The matrix includes both DF/CF states, all256IOCTL modes with matched/unmatched
handles, supported/unknown AH paths, signed handle and seek gates, source name
lengths around128, key/entry-size extremes, ignored installation errors,
immediate reentry, failed archive opens and connected ordinary/keyed/LEN streams.
Eight complete seven-call chains per image install, open, read, rewind/seek,
read, close and uninstall through native archive/buffer bodies.

An independent scalar shares physical memory across CODE, DGROUP, header,
directory, PFILE/BFILE and client buffers. Every byte of the1MiB model outside
the declared64K emulator stack is checked after every call. Stack cleanup,
callee state, native requests and handled/forwarded interrupt registers/flags
are checked separately. Per-image full-memory hashes retain unrelated target/
cached image differences; cross-image comparison uses outputs, events and
constructed state. Stores retain a total count and bounded prefix, rather than
millions of records. Eight controls reject incomplete contributions/returns,
table/state mutation, data/operand/neighbor branches, unknown edges/interrupts/
ports, bad frames/pointers, unowned writes, invalid dispatch, stale completion
and segment aliases. Native IRET preserves supplied flags in its positive
control; wrong far/interrupt cleanup fails.

## Installation and cleanup

PFSTART clears DF before checking the saved old-vector words. A nonzero saved
vector skips allocation, entry loading, decryption and vector installation,
but still copies the supplied archive filename. It does not close an already
open archive merely because the name changes.

First installation calls FILE_ROPEN, allocates16header bytes and reads them,
extracts entries_size at0 and key at6, frees the header, allocates entries_size,
reads encoded entries, then closes the high-level file. All open/read/allocation
results and CF statuses are ignored. Header fields for unknown/count/zero are
not validated. Only the key's low byte drives decryption: plain=cipher XOR key,
then key=(key-plain) modulo256. A size-zero entry request still executes the
LOOP body65536 times over the complete directory segment, because CX starts0.
The two zero-size cases per image check all resulting bytes; no repaired zero
gate or successful empty-directory return is substituted.

It saves the declared old vector, clears pfint21_pf, sets handle=FFFF and
requests installation of2000:294A. Filename copying uses a65535-count NUL scan
followed by word/byte copies, with no128-byte destination capacity check.
Lengths128/129/134 overwrite adjacent file/handle/entries fields and the next
byte. The tested copies remain bounded constructed inputs; no arbitrary invalid
memory or actual DOS pathname safety is proved. Name processing clears DF even
on repeated installation. Missing/short real headers and allocation failures
that yield invalid segments remain outside the declared successful-memory
fixtures; the source's lack of status gates is retained.

PFEND with a zero saved vector returns immediately. Otherwise it restores the
old vector and clears the saved words, then tests pfint21_pf. **When it is zero,
the TH03 directory allocation is not freed.** Directory freeing is nested after
PFCLOSE, so installing without opening an archive, or closing the archive via
the hook before uninstalling, leaves it allocated. With a nonzero PFILE fixture,
native close/free and directory free execute. PFEND does not clear PFILE/handle
fields after that free; no real lifetime or post-free access guarantee follows.
Repeated PFEND then returns through its zero-vector gate.

## Handler dispatch and preserved anomalies

The handler preserves the interrupted general registers/DS/ES through PUSHA
and saves caller flags. It loads DGROUP, increments on_hook, restores original
flags before dispatch, and writes AH into the final table sentinel. Handled
success clears CF in the saved frame; rejection sets CF and AX=1. All other
saved flags and registers return unchanged, except AX and seek's DX. Forwarded
paths restore registers/flags, execute CLI and far-jump to the old DOS boundary.
A nonzero on_hook bypasses the save/dispatch block entirely.

Read-only open accepts only a zero low mode nibble and a **signed-negative**
stored handle. Any8000..FFFF handle permits an archive attempt; nonnegative
handles pass through. The real PFOPEN returns the BFILE handle on success and
stores PFILE/handle state. Failed PFOPEN passes through to old DOS with restored
client registers while retaining its errno/heap/file effects. Directory misses
retain the previously observed seek/error5 path. Only one archive handle is
tracked. Matched close executes native PFCLOSE, resets PFILE/handle and clears
CF. Matched reads execute actual PFREAD, preserving its EOF/counter/RLE and
low-offset-wrap behavior; the handler clears CF even when its native buffer
read encounters a modeled error.

Seek first rejects an incoming negative CX high word. AL==1 selects current
relative movement; the branch for AL<1 is a signed-byte JL, so AL80..FF also
rewinds as a start-relative request. AL02..7F selects original-size minus
logical-position and ignores the supplied offset. That subtraction may wrap
after the initial sign test. PFREWIND's failed underlying seek status is ignored;
the hook then invokes native relative decode and returns logical DX:AX with
CF clear. These are observed source/instruction behaviors, not normalized DOS
seek semantics or proof that the virtual file supports huge offsets.

Write/duplicate/date-time/lock requests reject a matched archive handle and
forward unmatched handles. **ForceDuplicate (AH46) rejects every handle.** Its
branch contains MOV CX,DI instead of a comparison; MOV preserves the ZF=1 left
by the successful dispatch comparison, so JE always selects error. Matched and
unmatched fixtures confirm the same AX1/CF1 result. No corrected CMP is authored.

IOCTL forms a16-bit1 shifted by CL with the386's five-bit count mask and tests
14CF. Matching flagged modes reject; others pass through. All256AL values are
checked, including32-count aliases and shifts beyond bit15. Terminate restores
the old vector, then forwards the original client request. It does not clear
the saved vector or explicitly close/free the archive in this handler path;
unknown AH values use the mutable sentinel to pass through.

One decoded module row adds no authored source, exact or accepted-intake credit.
High-level file/heap bodies, physical DOS/vector/device behavior, complete root
DATA/BSS/CRT ownership, cold localized production and canonical DIET packaging/
full Oracles remain open, alongside the full505-file intake and actual requested
English commits.
