# Complete MAINL buffered-file candidate review

Seven frozen buffer-library contributions own 474 decoded function-body bytes
and four observed alignment NOPs, totaling478bytes. The complete DOS_ROPEN /
FONTFILE_OPEN alias body adds26bytes. These eight functions have500body bytes /
162instructions; all504raw bytes and empty original ordered MZ relocation
sets agree with both cached candidates. No maintained MAINL source, canonical
stored offset or exact acceptance is added.

```sh
python3 scripts/review_th03_mainl_buffer.py --output .analysis/NEW_BUFFER_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_buffer_review.py -v
```

Receipt: `.analysis/sol-mainl-buffer-review-20261006.json`. The preceding archive
reader receipt guards canonical/decoded/cached lineage. Nineteen consulted
frozen providers bind to both cached trees, with explicit LF/CRLF comparison
for ASM/INC only and raw header comparison. All eight contributions remain
frozen providers, with no maintained MAIN remap. Both root OMF objects have
valid TASM5/th03_mainl.asm identity and equal dependency-timestamp-normalized
hashes. MAP containment binds the disjoint CODE extents to _TEXT; surrounding
palette and other library contributions are excluded. This does not prove
ownership or acceptance of that entire generated root. Ghidra fails headless
usage before database attestation; no new database facts or cold build are used.

| Function | Decoded entry | Body bytes /instructions | Far cleanup |
| --- | --- | ---: | ---: |
| BCLOSER | 0000:0472 | 24 /11 | 2 |
| BFILL | 0000:048A | 59 /26 | 2 |
| BGETC | 0000:0506 | 48 /17 | 2 |
| BOPENR | 0000:05B8 | 83 /31 | 4 |
| BREAD | 0000:060C | 48 /24 | 8 |
| BSEEK | 0000:063C | 65 /24 | 6 |
| BSEEK_ | 0000:067E | 47 /18 | 8 |
| DOS_ROPEN /FONTFILE_OPEN | 0000:0AAE | 26 /11 | 4 |

Trailing NOPs are at04C5/060B/067D/06AD. All interior returns and direct branches
are checked; calls stay on approved complete entries and require PUSH CS.
Actual far RETs execute with stack cleanup and BP/SI/DI/DS preservation.
Native BFILL/BGETC/DOS_ROPEN caller frames are checked separately. All functions
retain DF under the declared DOS/heap interface behavior; BREAD uses explicit
MOV/INC rather than PFREAD's CLD/STOSB. No product opcode arrays, padding,
artificial ABI or library source acceptance is introduced.

## Native execution and remaining interfaces

The BFILE fixture has handle,left,pos,size words at0/2/4/6 and byte buffer at8.
The declared BFILE structure size is9; BOPENR requests bbufsiz+9 as a word,
while BFILL requests exactly b_siz bytes at offset8. Whole64K buffer/output
regions and each image's whole64K DGROUP are checked after every call, including
aliases. bbufsiz05B0, pferrno05B2, mem_AllocID0856 and file_sharingmode0558 are
explicit data fields. Before/after DATA hashes remain separate across images
because unrelated original0849 differs. Return values, native entries, request
order, stores and all constructed state agree across original/two caches.

HMEM_ALLOCBYTE21AE and HMEM_FREE22B2 remain explicit far-call models, with
verified argument cleanup, return frames and supplied AX/CF. Native INT21
instructions are intercepted only at five reviewed sites, checking AH and
meaningful handle/pointer/size/whence/offset fields. The declared DOS interface
returns AX/CF and, for seek, DX; read fixtures write only specified synthetic
bytes into the verified buffer destination. Real DOS, allocation/deallocation,
file positions, assets, interrupt vectors and handler frames are not executed.
Callbacks stop on errors and raise outside FFI. Native far returns have no
memory-read hook. No read/open/seek function is replaced by a result model.

Each image has1754 matrix scenarios and1776 top-level invocations, all terminal;
across three images,5328 top-level calls. Native helper calls are additional.
Cases cover every source byte, both DF states, allocation segment0/6000/6100,
AX/CF allocation/open combinations, wrapped allocation sizes, handle extremes,
buffer left/position bounds, fill EOF/error/overreported counts, signed read
sizes, output wrap, field aliases, all tested low-byte whence variants, signed
offset bit patterns and seek failures. Ten sequential chains per image cover
open/getc/read/close and relative/base-seek followed by getc/read. Eight controls
reject truncation/returns, operand/neighbor branches, producer mutation, unknown
edges and DOS sites, ports, invalid native/model frames, whole-span unowned
stores, invalid modeled read destinations, stale completion and segment aliases.

DOS fixtures with count greater than requested bytes, counts inconsistent with
the injected payload, zero handles or unusual CF/AX pairs are adversarial
caller-contract observations. They do not establish real DOS guarantees.
Undefined close/free results are recorded as final registers, not promoted
to public C return-value promises. Earlier PFOPEN/PFREAD receipts retain their
separate buffer models; this scope does not retroactively claim a combined
archive/interrupt-hook execution.

## Opening, filling and buffered bytes

BOPENR sets the allocation ID word to6 and forms allocation size modulo65536.
Allocation CF determines failure independently of AX: CF-set writes only errno
low byte3; CF-clear segment0 is accepted and can initialize low memory while
returning0. bbufsiz65527 requests0bytes; bbufsizFFFF requests8. There is no
overflow or minimum-capacity check. A successful DOS open stores its handle,
sets left=0 and size=bbufsiz, but leaves pos and payload unchanged. Success
retains errno. Failed open frees the allocated segment, then writes errno's
low byte1; prior BEEF becomes BE01/BE03 without replacing the high byte.

DOS_ROPEN reads only the low byte of file_sharingmode, loads the actual filename
far pointer through LDS, executes INT21/AH3D, restores DS, and returns the DOS
handle on CF-clear. On CF-set it returns FFFE (FileNotFound), preserving CF.
BOPENR gates on that CF, not on any handle value; zero and FFFF CF-clear handles
are accepted in the fixtures. DOS_ROPEN and FONTFILE_OPEN name one body, with
one function row and no duplicate byte credit.

BFILL switches DS to the BFILE segment and requests handle read into offset8
for b_siz bytes. CF-set or AX=0 sets left=0 and returns FFFF, leaving pos
unchanged. Any CF-clear nonzero AX is accepted: left=AX-1, pos=1, and the first
buffer byte is returned with AH=0. It does not check AX against request size
or infer how many bytes were actually overwritten. Old buffer bytes remain
outside the explicitly injected payload. DS is restored on both paths.

BGETC trusts a nonzero left: decrement it, load old pos, increment pos, then
read ES:[old-pos+8] and clear AH. The effective offset wraps as a word, so
posFFF8 reads the handle's low byte at offset0 rather than carrying into a
new segment. When left=0, the function invokes real BFILL with the same BFILE
segment and returns its result. No check relates left/pos to size or storage.

## Read, movement and failure chains

BREAD treats the size word as signed: sizes8000..FFFF immediately return0
without invoking BGETC. Size zero does the same. Positive sizes call real
BGETC and stop on FFFF; destination offsets increment as words with the same
segment, and return count is final-minus-initial DI. Unlike PFREAD, it preserves
DF. Output aliases into left/pos change subsequent cached reads. Handle/size
aliases are also exercised through the next real BFILL, changing the requested
handle/length. These are unchecked source behaviors, not safe-buffer guarantees.

BSEEK takes a signed32-bit relative offset, but its in-buffer condition is
high-word==0 and unsigned low-word<=left. That path subtracts offset from left, adds it to pos
modulo65536 and returns0 without DOS. Outside the buffer it requests DOS
whence1 at offset-left, compensating for read-ahead. Signed negative bit
patterns are forwarded with32-bit subtraction; there is no clipping. Success
returns0 and clears left. Failure returnsFFFF **and stores FFFF in left**,
leaving pos unchanged.

BSEEK_ clears left before calling DOS, regardless of eventual failure. It
uses only the low whence byte; low byte1 subtracts old left from the requested
offset, other values forward it unchanged. Thus word0101 selects current
position, while0100 selects start. Both success/failure leave left=0 and pos
unchanged; AX is0/FFFF from CF. Returned DOS position is not stored in BFILE.

The native failure chains make the distinction observable. With left2/pos0
and relative offset3, both request DOS offset1. Failed BSEEK then causes BGETC
to return old byte11 and BREAD to consume three more old bytes, with no DOS
read. Failed BSEEK_ causes BGETC to refill from declared bytes91/92; BREAD
consumes the remaining byte then encounters a fresh EOF read. The old buffer
was never made valid by the failed seek; the FFFF state causes that behavior.

BCLOSER unconditionally submits the stored handle to DOS close and then frees
the BFILE segment. It ignores close status and does not clear metadata. Actual
heap ownership/lifetime is unproved, so no post-free valid-memory claim follows.
Eight decoded rows add no maintained source, exact or accepted-intake credit.
Combined archive/hook execution, generated root DATA/BSS/CRT ownership, cold
localization and canonical DIET packaging/full Oracles remain open, alongside
the full505-file intake and requested English commits.
