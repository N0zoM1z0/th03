# Complete MAINL PFOPEN candidate review

The TH03-specific bounded archive-open include owns 281 decoded CODE bytes /
97 instructions at 0000:2B16..2C2E, followed by one observed producer NOP at
2C2F. Its private near STR_IEQ dependency owns 56 contextual bytes /29
instructions at 2C30..2C67. All 338 bytes match both cached candidates; both
extents have empty MZ relocation sets. These are decoded candidate diagnostics,
with no maintained MAINL source, canonical stored offset or exact acceptance.

```sh
python3 scripts/review_th03_mainl_pfopen.py --output .analysis/NEW_PFOPEN_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_pfopen_review.py -v
```

Receipt: `.analysis/sol-mainl-pfopen-review-20261006.json`. The preceding math
receipt guards the canonical/decoded/cached lineage. Seventeen consulted frozen
providers bind to both cached source trees. Their th03/formats/pfopen.asm is
overlaid with maintained MAIN src/main/formats/pfopen.inl; that bounded include
and its header match both caches. The root th03_mainl.asm includes it and the
frozen library STR_IEQ in the same _TEXT contribution. No accepted MAIN proof
is inherited by MAINL. Only assembler-provider line-ending normalization is
allowed when comparing frozen and cached source.

Both complete root OMF objects have valid TASM 5.0 /th03_mainl.asm identity and
agree after dependency-timestamp normalization. MAP carrier containment is
checked separately. This does not establish ownership or acceptance of the
entire generated root. The adjacent six bytes at 2C68..2C6D are the leading
GRPPP8NC_CLIPOUT return tail from graph_pack_put_8_noclip.asm, before its public
entry at 2C6E. They are excluded from STR_IEQ and from this unit's credit.
Ghidra fails headless-usage before database attestation; no new database
observations are used. No cold compiler run is claimed.

## ABI, state and explicit models

PFOPEN executes its real far RET8, with reverse Pascal request-filename and
archive-filename far pointers on the stack. STR_IEQ executes its actual near
RET8 with header-filename and request-filename far pointers. All branches stay
on instruction boundaries; near calls to far interfaces require the preceding
PUSH CS. Terminal cases check SP/BP/SI/DI/DS and the conditional DF effect.

The heap fixture is a 31-byte PFILE: bf/getc/getx words at 0/2/4; size/read/home/
loc/osize dwords at 6/10/14/18/22; cnt/ch words at 26/28; key byte at 30.
Directory records are 32 bytes: type word, auxiliary byte, thirteen filename
bytes, packed/original size words, offset dword and eight reserved bytes.
DGROUP mem_AllocID0856, pferrno05B2 and pfint21_entries1D06 are checked with
the full 65536-byte before/after DATA image. Full directory/request buffers
and every owned heap byte are checked independently.

Five optimized PUSH-CS/near-call interfaces are explicit request/status models:

| Interface | Decoded entry | Far cleanup | Checked request |
| --- | --- | ---: | --- |
| HMEM_ALLOCBYTE | 0000:21AE | 2 | 31 bytes |
| BOPENR | 0000:05B8 | 4 | archive far pointer |
| BSEEK_ | 0000:067E | 8 | whence 0, offset low/high, buffer handle |
| BCLOSER | 0000:0472 | 2 | buffer handle |
| HMEM_FREE | 0000:22B2 | 2 | allocated segment |

These models execute no real heap, buffered read, seek, free, DOS or assets.
They preserve required callee state and supply specified AX/CF/error results.
STR_IEQ runs natively. There is no modeled filename equality or substituted
successful return from PFOPEN. Callback errors stop the engine and raise
outside FFI. No memory-read hook is used with native far returns.

Each original/cached image has 106 invocations: 104 native returns and two
nonterminal searches stopped at 10000 instructions. Across three images,
318 calls give 312 returns and six budgets. Cases cover both DF states,
allocation segments 0/6000/6100 and both allocation CF values, open handles
0/1/FFFF and independent CF, both known compression types, unknown/end types,
auxiliary values 0/1/255, ignored seek status, ASCII case/prefix/empty strings,
multiple records, malformed field termination and request offset wrap.
Eight controls reject truncation/incorrect returns, operand/neighbor branches,
producer mutation, unknown calls/ports/interrupts, unowned writes including
word-span overrun, stale completion, segment aliases and invalid native frames.

## Preserved archive-open behavior

Only the low byte of a record's type determines the end marker. Directory DI
increments by 32 as a word. On a low-byte-zero marker, PFOPEN sets AX to
PFENOTFOUND (2), but falls through into the normal seek path. Loading the
record's home offset overwrites AX. The code calls seek, sets the getx/key
fields, then rejects the unknown full type with pferrno=5, closes the buffer
and frees the PFILE. Thus type F300 also stops the scan, even when a later
record would match. A matched unknown nonzero type likewise seeks before
the error/close/free path. No repaired error control flow is introduced.

Allocation CF selects failure independently of returned AX. It writes only
pferrno's low byte (3), preserving the prior high byte: BEEF becomes BE03.
CF-clear AX=0 is accepted as segment zero; successful initialization can then
return AX=0, indistinguishable to the caller from failure. BOPENR uses only
AX==0 and ignores CF. Its failure frees the PFILE without close or an explicit
new PFOPEN errno. Seek AX and CF are both ignored. Success does not clear
pferrno. These effects are observed under the declared interface statuses;
the real interfaces' failure guarantees are not established here.

Known types are NONE F388 and LEN9595. The auxiliary byte chooses plain/keyed
getx at 1952/1996 and, when nonzero, stores key. NONE uses getx as getc and
leaves cnt/ch unchanged; LEN selects getc1904 and sets cnt=0/ch=FFFF. Auxiliary
zero leaves the old key byte untouched. Packed/original word sizes are
zero-extended to dwords, home retains all 32 bits, and read/loc become zero.
Prior A5-filled heap bytes make untouched fields observable.

STR_IEQ unconditionally clears DF and folds ASCII lowercase a..z only. It
returns AX=9F00 /ZF clear for equality and AX=0 /ZF set for mismatch, as the
caller requires. There is no thirteen-byte bound on directory filenames.
Thirteen A bytes followed by packed4141/original0041 match a requested sixteen
A bytes and NUL by consuming adjacent size fields. Request offsets FFF8 and
FFFF wrap as words with the same segment. Comparison clears incoming DF;
allocation/open failure and an immediate end marker can retain it.

A constructed full 64K directory with no end marker or match keeps searching,
wrapping DI. Budget stops are observations of that loop, not terminal returns
or real malformed-archive safety. One decoded PFOPEN row adds no authored
MAINL source or accepted-intake credit; the private helper is contextual.
Buffer/heap/interrupt-hook dependencies, generated root DATA/BSS/CRT ownership,
cold localization and canonical DIET packaging/full Oracles remain open.
The complete 505-file intake and requested English commits remain unfinished.
