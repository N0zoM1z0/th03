# Complete MAINL file-library candidate review

Nine complete frozen file-library includes contain eleven procedures, 783 body
bytes /311 instructions and three trailing NOPs: 786 bytes at0000:0786..0A97.
Native DOS_AXDX and DOS_FILESIZE add78body bytes /40instructions and two NOPs,
80bytes at0000:06AE..06FD. Previously reviewed DOS_ROPEN /FONTFILE_OPEN contributes
26contextual bytes /11instructions; it receives no duplicate progress credit.
All892 scoped bytes and their original ordered relocation sets agree with both
cached products. This is decoded candidate analysis, with no maintained MAINL
source, canonical stored-file offsets, source acceptance or exact acceptance.

```sh
python3 scripts/review_th03_mainl_file.py --output .analysis/NEW_FILE_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_file_review.py -v
```

Receipt: `.analysis/sol-mainl-file-review-20261006.json`. The guarded preceding
archive-hook receipt carries canonical stored/decoded/cached lineage. Twenty-two
frozen providers are compared against both cached source trees, normalizing
LF/CRLF only for ASM/INC. These includes have no maintained MAIN source overlay.
Root OMF identity is valid TASM5 /th03_mainl.asm, with equal hashes after
normalizing dependency timestamps. MAP containment establishes the three scoped
extents inside the complete _TEXT carrier; neighboring CRT/library CODE is
excluded. This does not accept generated root CODE/DATA/BSS or the whole product.
Current Ghidra headless usage fails before database attestation, so there are
no new database observations. Cached production is not a new cold build.

| Procedure | Decoded entry | Body bytes /instructions | Far cleanup |
| --- | --- | ---: | ---: |
| FILE_APPEND | 0000:0786 | 84 /34 | 4 |
| FILE_FLUSH | 0000:07DA | 107 /34 | 0 |
| FILE_CLOSE | 0000:0846 | 15 /6 | 0 |
| FILE_CREATE | 0000:0856 | 64 /27 | 4 |
| FILE_EXIST | 0000:0896 | 28 /13 | 4 |
| FILE_READ | 0000:08B2 | 180 /75 | 6 |
| FILE_ROPEN | 0000:0966 | 59 /24 | 4 |
| FILE_SEEK | 0000:09A2 | 52 /20 | 6 |
| FILE_TELL | 0000:09D6 | 14 /5 | 0 |
| FILE_SIZE | 0000:09E4 | 14 /7 | 0 |
| FILE_WRITE | 0000:09F2 | 166 /66 | 6 |
| DOS_AXDX | 0000:06AE | 23 /12 | 6 |
| DOS_FILESIZE | 0000:06C6 | 55 /28 | 2 |
| DOS_ROPEN /FONTFILE_OPEN (prior context) | 0000:0AAE | 26 /11 | 4 |

Trailing NOPs are0845/0855/09A1/06C5/06FD. Body-owned NOPs at0935/0A67 align
internal direct-access paths; call-site NOPs remain instructions. All body
lengths, interior far returns, branches and seven native calls are checked.
Branches cannot enter operands or neighbors; native calls require their exact
site/target and PUSH CS. Original relocation comparisons are scoped diagnostics.

## Execution and explicit boundaries

Each image has2093 constructed scenarios and2121 top-level calls, all terminal.
Across original/two caches this is6363 calls. Six sequential chains per image
cover open/read/tell/seek/read/close, create/write/tell/flush/size/close and
append/write/flush/close under both DF states. Actual file and DOS-wrapper
instructions execute, including every near CALL with PUSH CS and native RETF.
Frames are tracked at each native entry/return; cleanup and BP/SI/DI/DS are
checked, along with inherited DF. No function in the table is replaced with a
result model. Defined AX/DX results, full native-entry counts and ordered DOS
requests agree with an independent physical-memory scalar algorithm.

The probe relocates the image to2000, with DGROUP2E3F and stack4000. Synthetic
filename5000:0100, buffer6000:0100 and client7000:0100 fixtures are configurable.
All1MiB of physical memory outside the declared64K stack segment is checked
after every call. Each image retains its own before/after memory hashes;
cross-image comparison omits those whole-memory hashes because unrelated PI
encodings and DGROUP0849 remain different. Scoped returns/state, events,
native entries, write counts and cursor observations still agree.

DOS INT21 is an explicit model at sixteen reviewed sites. It verifies site/AH,
meaningful handle, pointer, count, mode and signed32-bit offset requests, and
supplies only AX/CF, plus DX for seeks. Buffered/direct read destinations and
write sources must match the current far pointer or caller arguments. Models
inject bounded synthetic read bytes, hash actual write payloads and maintain
a declared scalar cursor. End positions use a supplied `file_size` fixture;
this is not a DOS filesystem, persisted write-size or real-file proof. Unknown
interrupts and ports stop execution. Native writes are restricted to declared
file state and flat buffer/client fixtures. Callback failures stop execution
and raise outside FFI. No MEM_READ hook is installed for real far returns.

Matrices cover both DF values, all256 read bytes and all256 client-byte values
through a permutation of source offsets, inactive/active/negative-looking
handles, AX/CF open combinations, low-byte seek modes and signed32-bit offsets,
logical-position carry/wrap, direct/buffered counts0/1/2/7/8/9/17/8000/FFFF,
short/failed/overreported reads and writes, zero far pointers, segment-end
word access, shared/overlapping buffer clients and five file-field output
aliases. Adversarial fixtures with inconsistent returned counts/payloads,
CF-set injected bytes or error AX0/FFFF are recorded as such; they do not assert
normal DOS guarantees. Forward/backward MOVSW copies read a whole word before
writing it, then wrap only SI/DI; MOVSB handles the odd tail. They do not carry
into a new segment after advancing acrossFFFF.

Eight controls reject truncation/cleanup, operand/neighbor branches, alignment
mutation, unknown native/indirect/far edges, absent PUSH CS, unknown DOS sites
and ports, unowned whole-span stores, false modeled destinations, invalid
native entry/return frames, stale completion and segment aliases. A synthetic
positive nested-call control executes both real RETFs. Runtime mutations retain
untampered analysis metadata to exercise guards independently; they do not
establish source acceptance for synthetic code.

## Opening, existence and native DOS helpers

FILE_ROPEN /APPEND /CREATE reject any existing file_Handle other thanFFFF
without making DOS requests or clearing state. Once attempted, all reset
InReadBuf, BufPtr, Eof, ErrorStat and both BufferPos words, even on failure.
BufferSize, Buffer far pointer and unrelated file_Pointer remain unchanged.
CF-clear handle0/FFFF is accepted. ROPEN uses native DOS_ROPEN, then sets handle
FFFF on CF-set and returns0; otherwise it returns1. Only the low byte of
file_sharingmode is passed. Native DOS_ROPEN returnsFFFE on CF-set, retaining CF.

APPEND passes3D02 to native DOS_AXDX. It has no create-on-missing fallback,
despite the upstream comment. Successful open immediately seeks to end and
stores returned DX:AX regardless of CF, then returns1. CREATE passes3C00 with
CX20 archive attributes. DOS_AXDX returns DX0 on successful DOS CF; failure
sets DXFFFF and negates the DOS AX word. The final SUB preserves failure carry
for nonzero error codes but clears CF when error AX is0. APPEND/CREATE gate on
DX rather than that final carry, so even the adversarial zero-error failure
still returns0. Their stored handle is AX OR DX, alwaysFFFF on DOS failure.

FILE_EXIST is independent of global file_Handle. It calls native DOS_ROPEN,
then closes the returned handle if open succeeded. Its boolean uses the
**final** CF: failed close makes an otherwise successful open return0. It does
not update shared file state. SS-relative argument loads work with SS != DS.

DOS_FILESIZE first queries current position. Initial failure negates AX and
forms DX by carry; ordinary nonzero error returns DXFFFF. Adversarial errorAX0
produces DX0/CF0, contradicting a universal error-sentinel claim. On initial
success it saves the position, seeks end, saves that returned DX:AX even on
failure, restores the original position, and returns the saved end words.
Final CF comes from restore. FILE_SIZE maps any final CF-set to AX=DX, retaining
DX; failed restore can therefore turn a legitimate size into repeated high
words. End-seek failure followed by successful restore returns the error words
as a size. Neither helper flushes buffered pending writes or validates a handle
against the globalFFFF sentinel before DOS. These are native scoped contracts.

## Buffered/direct reads and writes

Buffered FILE_READ refills when unsigned BufPtr >= InReadBuf. Before the DOS
read it adds the old InReadBuf word to the32-bit BufferPos. CF-set forces the
returned count to0; count0 sets Eof1, retains old BufPtr and exits. Nonzero
count resets BufPtr0 without clearing Eof. It trusts returned counts, performs
unsigned minimum selection and updates live file fields after copying. A
zero-size call can refill an empty buffer, but copies/consumes no bytes; an
already valid buffer needs no DOS call. A NULL destination0000:0000 discards
bytes but still consumes counts; the direct path does not have this special
case. Output aliases into BufPtr/InReadBuf/EOF/ErrorStat/Handle are executed
against the same physical memory and can change subsequent state/requests.

Direct FILE_READ issues DOS even for size0 and ignores CF completely. It adds
AX to BufferPos, compares AX to the requested count, sets Eof1 on any inequality
and returns AX. Thus failed DOS with errorAX6 can advance position and report
six bytes; short reads and oversized counts set Eof. Successful buffered/direct
reads do not clear a previously set EOF. Real file behavior is not inferred
from these explicit boundary-return fixtures.

Buffered FILE_WRITE computes unsigned remaining capacity modulo65536, advances
BufPtr before copying and follows inherited DF. It flushes only when capacity
is **strictly less** than remaining data. An exactly full final buffer remains
pending; a following size0 returns1 without flushing it. Oversized BufPtr wraps
the computed capacity; no safe-buffer invariant is invented. After a full
flush it requires CF-clear and AX equal to current BufferSize; otherwise it
sets ErrorStat1, retains the pointer/full-buffer state and returns0. Successful
full flush resets BufPtr0 and advances BufferPos. The remainder stays buffered.
Buffered success is AX1, including zero-size calls, despite the upstream
zero-size prohibition comment.

Direct FILE_WRITE also invokes DOS for size0. On CF-set it writes ErrorStat1
and replaces AX with0 before position accounting. CF-clear short writes are
accepted: any nonzero AX advances BufferPos and returns **FFFF**, not1; AX0
returns0. This differs from buffered boolean1. Prior ErrorStat is retained on
successful writes. Source comments are candidate material, not ABI Oracles.

## Flushing, seeking, telling and closing

FILE_FLUSH first loads BX=file_Handle. FFFF returns immediately. Otherwise it
chooses write when unsigned InReadBuf < BufPtr. Write flush requests BufPtr
bytes, advances BufferPos by returned AX only if CF-clear, sets ErrorStat1 on
CF or count mismatch, then clears BufPtr regardless. It leaves InReadBuf and
EOF unchanged. The read route seeks absolute BufferPos+BufPtr only when
InReadBuf is nonzero; it clears both counters before DOS and overwrites
BufferPos with returned DX:AX regardless of CF. If both counters are zero,
flush makes no DOS request. All void final registers remain observations.

FILE_CLOSE calls real FILE_FLUSH, unconditionally submits DOS close with BX,
then sets file_HandleFFFF. Even an already inactiveFFFF handle is submitted;
no buffer free or pointer cleanup occurs. It ignores close status.

FILE_SEEK calls real flush, skips further work only for handleFFFF, then issues
the requested seek with low whence byte and full32-bit offset. Regardless of
that result it queries current position via4201, clears Eof and stores that
query's DX:AX without checking its CF. Flush/write errors and failed seek/query
requests remain in the ordered traces. FILE_TELL returns BufferPos+BufPtr
modulo2^32 without DOS; its local word carry is preserved.

Two decoded module rows cover786file bytes and80new-helper bytes. Prior DOS-open
context is not credited again. Cold localized production, library/root/data/
CRT ownership, physical DOS/files/heap/vector runtime and canonical DIET
packaging/complete Oracles remain open alongside the full505-file intake and
requested English commits. Earlier CDG/PI/cutscene/root/registration/hook
receipts keep their explicit file models; this review does not retroactively
claim their complete combined runtime.
