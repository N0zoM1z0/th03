# Complete MAINL archive-reader candidate review

Five bounded library includes contain eight complete functions, 353 decoded
CODE bytes /126 instructions plus three source/producer bytes, at
0000:18DA..1A3D. All 356 raw bytes and the empty original ordered MZ relocation
set agree with both cached candidates. Internal RLE and plain/keyed readers
execute natively, including actual indirect near calls and far returns.
No maintained MAINL source, canonical stored offset or exact credit is added.

```sh
python3 scripts/review_th03_mainl_pfread.py --output .analysis/NEW_PFREAD_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_pfread_review.py -v
```

Receipt: `.analysis/sol-mainl-pfread-review-20261006.json`. The preceding PFOPEN
receipt guards canonical/decoded/cached lineage. Seventeen consulted frozen
providers bind to both cached trees. Unlike PFOPEN, these five library includes
remain frozen source with no maintained MAIN overlay. Provider comparison uses
explicit LF/CRLF normalization; func.hpp also matches raw in both trees. Root
OMF has valid TASM5/th03_mainl.asm identity and equal dependency-timestamp-normalized
hashes. MAP containment binds the includes to _TEXT. This is scoped cached
producer evidence, not ownership or acceptance of that whole root or library.
Ghidra fails headless-usage before database attestation; no new database facts
or cold compiler observations are used.

| Function | Decoded entry | Body bytes /instructions | Return |
| --- | --- | ---: | --- |
| PFCLOSE | 0000:18DA | 26 /11 | far RET2 |
| PFGETC | 0000:18F4 | 15 /6 | far RET2 |
| PFGETC1 | 0000:1904 | 78 /22 | near RET |
| PFGETX0 | 0000:1952 | 68 /21 | near RET |
| PFGETX1 | 0000:1996 | 13 /5 | near RET |
| PFREAD | 0000:19A4 | 46 /23 | far RET8 |
| PFREWIND | 0000:19D2 | 59 /18 | far RET2 |
| PFSEEK | 0000:1A0E | 48 /20 | far RET6 |

The PFGETC include has 174 body bytes and two trailing/alignment bytes: an
observed NOP at1903 between public/internal entries, and its declared db0 at
19A3. PFREWIND has 59 body bytes plus one observed NOP at1A0D. Complete source
contributions are26/176/46/60/48 bytes. No literal producer arrays or padding
are introduced into product source; the declared zero is diagnostic source
ownership, not an instruction bridging into PFREAD or a new function.

## State, ABI and model boundary

The same 31-byte PFILE layout as PFOPEN is checked. bf/getc/getx are words;
packed size, physical read, home, logical position and original size are
dwords; cnt/ch are words, key is a byte. A5-filled full64K PFILE/output buffers
make untouched fields and alias effects observable. Each image's full64K
DGROUP is checked unchanged, separately preserving unrelated original DATA.
Incoming BP/SI/DI/DS and terminal stack cleanup are checked. ES and scratch
registers are not declared preserved. PFREAD clears DF even for size zero;
the other functions retain it under the declared interface models.

PFILE indirect getc may select actual PFGETC1/PFGETX0/PFGETX1; getx may select
PFGETX0/PFGETX1. Both the exact call-site operand and the runtime segment,
destination, native near return frame and dispatch counts are checked. All
direct branches stay on reviewed instruction boundaries. Optimized far calls
require PUSH CS and the exact modeled return frame.

Four interfaces are explicit models: BGETC0506 (RET2), BCLOSER0472 (RET2),
HMEM_FREE22B2 (RET2), and BSEEK_067E (RET8). They check the ordered buffer/free/
seek requests and supply declared AX/CF values. BGETC changes ES to its buffer
segment; actual PFGETX0's push/pop restores the PFILE segment. Real buffered
file bodies, DOS, heap and assets do not execute. Returned status-word fixtures
outside byte/FFFF are adversarial caller-contract observations, not a claim
that real BGETC produces those values. Close/free/seek statuses are ignored by
their callers; the undefined close/rewind C results are not promoted as an ABI
promise merely because final AX still contains an interface result.

Each original/cached image has1494 top-level calls:1492 returns and two
nonterminal maximum-offset observations, for4482 /4476 /6 across three images.
The matrix covers all256 source bytes, both DF states, plain/keyed/LEN modes,
duplicate/zero/max-length/truncated streams, every byte-valued run character,
physical/logical32-bit boundaries, cached cnt/ch extremes, high-byte statuses,
size-zero reads, output offset wrap and aliases into PFILE fields. Complete
near-entry/dispatch counts, request order and full memory agree. Ordered writes
retain counts, a hash and the first32 records; large loops do not inflate the
receipt with millions of write records. Eight controls reject incomplete/wrong
returns, branches into operands/neighbors, producer mutation, unknown calls/
ports/interrupts, wrong indirect slots, invalid pointers/frames, whole-span
unowned stores, stale completion and segment aliases. Callback failures raise
outside FFI. Native far returns use no memory-read hook.

## Plain/keyed and RLE behavior

PFGETX0 compares physical read against packed size as an unsigned32-bit value.
When the limit is reached, it returns FFFF without a buffer call or counter
change. Otherwise it increments both physical and logical dwords before BGETC,
including low-word carry and logical32-bit wrap. The unsigned packed-size gate
prevents a normal physical counter increment from FFFFFFFF. A failed underlying read does not
undo either increment. Original size is ignored by these readers.

PFGETX1 calls the real PFGETX0 and XORs AL with key only when AH is zero. The
four-bit rotate in general master.lib documentation is commented out in this
frozen Touhou producer and does not execute. Key is reread on each call.

PFGETC1 first uses a nonzero cnt: decrement it, increment logical position,
return ch without reading or touching physical position. Otherwise it reads
a new getx value. A nonzero AH returns immediately without changing ch. A
different byte becomes ch and returns normally. An equal byte causes a second
getx read for the run count. A valid count is stored in cnt and logical position
is reduced by one so the count byte is not counted as output. The saved run
character is then returned. For A,A,255, there are257 output A bytes: the two
literal occurrences plus255 cached repetitions. A zero count still returns
the two literals. Keyed counts undergo the same XOR as ordinary bytes.

A truncated duplicate run still returns its saved character when fetching
the count gives EOF or another nonzero-AH result; it leaves cnt unchanged and
does not subtract the count read's logical increment. If the packed-size gate
caused that EOF, there was no increment to retain. These cases are distinguished
with constructed physical limits and underlying failure statuses.

## Output and relative movement

PFREAD takes reversed Pascal stack words pf,size,output-offset,output-segment.
It repeatedly invokes actual getc, increments AH, and stops only when that
increment becomes zero. Thus any FFxx status stops, but a nonzero high byte
such as01 or12 is accepted and its low byte is written. PFGETC1/PFGETX1/PFSEEK
instead treat every nonzero AH as failure. This difference is retained in
adversarial status fixtures.

STOSB advances only the output offset. Reads starting FFFE/FFFF wrap to zero
with the same segment; the returned count is the word difference of final and
initial DI. No guard enforces the source comment prohibiting offset+size
crossing64K. Output can alias key/read/loc/cnt storage: earlier bytes then
change the state used by subsequent native reads. Both plain/keyed and cached
RLE alias effects are checked against a scalar sharing the same underlying
PFILE/output memory. Overwriting function pointers is not supported as a
valid fixture; unknown destinations are rejected before executing them.

PFSEEK implements unsigned relative movement by decoding bytes. It increments
the high word of its stack argument, uses DI for the low-word loop, and
decrements that high word after each low-word group. Offset zero invokes no
decoder. Offset65536 successfully executes65536 native LEN calls in the full
case; the high stack word reaches zero and the returned DX:AX is the logical
position. Separate EOF cases stop partway and leave the high argument word
in its partially consumed state. No widened or signed negative-offset repair
is introduced. PFSEEK returns the current logical32-bit position and ignores
original size as a direct limit; EOF is supplied by the selected decoder.

A FFFFFFFF offset with an always-successful declared BGETC fixture is stopped
after500 complete native decodes at the next indirect-call boundary. Full
state and ordered requests agree at that boundary; no terminal return value
is fabricated. The function would keep consuming the relative count. This is
a bounded synthetic stream observation, not a real maximum-length file run.

PFREWIND clears cnt/physical/logical, sets ch=FFFF, then requests absolute seek
to all32 home bits with whence0; getc/getx/key/sizes remain unchanged. Failed
seek status does not restore the cleared state. PFCLOSE unconditionally closes
the stored buffer then frees the PFILE segment; it has no NULL or ownership
guard and ignores statuses. There is no real deallocation proof here.

Eight decoded rows add no maintained source, source progress or accepted-intake
credit. Actual buffered file/heap bodies, interrupt hooking and combined
PFOPEN/read/rewind/close execution, generated root DATA/BSS/CRT ownership,
cold localization and canonical DIET packaging/full Oracles remain open.
The full505-file intake and requested English commits remain unfinished.
