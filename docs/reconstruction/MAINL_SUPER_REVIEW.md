# Complete MAINL BFNT and super sprite candidate review

Three disjoint decoded extents own 1542 new bytes: 1533 complete CODE bytes /
742 instructions plus nine producer NOPs. BFNT owns512 at0272..0471, super
owns1008 at237E..276D and DOS_CLOSE owns22 at0A98..0AAD. The BFNT boundary
starts0272, after the preceding CRT return; decoding from0270 would cross it.
Native heap628, stack76, BFNT palette64 and DOS-open26 are794 prior-context
bytes, without duplicate credit. All2336 scoped raw bytes and empty original
ordered relocation lists agree with both cached products. Three decoded
module rows add no maintained source, canonical stored-file offset or exact.

```sh
python3 scripts/review_th03_mainl_super.py --output .analysis/NEW_SUPER_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_super_review.py -v
```

Receipt: `.analysis/sol-mainl-super-review-20261006.json`, SHA-256
`d78e3b9410ed314ded32ab5a9b45f6a4b6609fe5785b70b59460e8b39a7c620b`.
Its547 guarded inputs retain the previous VSYNC receipt's stored/decoded/
cached lineage. Fifty-three consulted frozen providers bind both cached
source trees, including BFNT/super includes and relevant declarations/masks.
ASM/INC normalize only LF/CRLF; seven prior MAIN-only Tupfile substitutions
remain explicit, with no BFNT/super substitution. Both root OMF objects are
valid TASM5/th03_mainl.asm, equal after dependency timestamp normalization.
MAP ownership places every include inside root _TEXT at0272,size10944.
Other root code, DATA/BSS/CRT and physical packaging remain unaccepted.

| Complete body | Decoded offset | Bytes /instructions | Return |
| --- | --- | ---: | --- |
| BFNT_ENTRY_PAT with private invalid/fault tails | 0272; public0286 | 322 /158 | RETF8 |
| BFNT_EXTEND_HEADER_SKIP | 03B4 | 34 /12 | RETF6 |
| BFNT_HEADER_READ | 03D6 | 59 /31 | RETF6 |
| BFNT_HEADER_ANALYSIS | 0412 | 95 /52 | RETF6 |
| SUPER_FREE | 237E | 48 /18 | RETF |
| SUPER_ENTRY_PAT with private error tails | 23AE; public23C2 | 191 /104 | RETF8 |
| SUPER_ENTRY_AT | 246E | 116 /50 | RETF6 |
| SUPER_ENTRY_BFNT | 24E2 | 137 /84 | RETF4 |
| SUPER_CANCEL_PAT | 256C | 79 /32 | RETF2 |
| SUPER_PUT | 25BC | 240 /91 | RETF6 |
| Even-address/even-width draw | 26AC | 35 /18 | near RET |
| Even-address/odd-width draw | 26D0 | 45 /25 | near RET |
| Odd-address/even-width draw | 26FE | 54 /30 | near RET |
| Odd-address/odd-width draw | 2734 | 49 /26 | near RET |
| Mutable near draw dispatcher | 2766 | 8 /3 | tail JMP |
| DOS_CLOSE /file_close alias | 0A98 | 21 /8 | RETF2 |

## Native execution and declared models

Each image has949 terminal scenarios,964 top-level calls and7636 native
entries. Three images total2892 terminal calls and22908 entries. Thirty
separate budget observations execute978 entries; these are checked partial
executions, not claimed returns. Native code includes all scoped procedures,
heap/stack/palette/open context, actual near/far calls and returns, nibble
conversion, pattern masks and self-modifying draw dispatch. After every
terminal call and budget prefix, all1MiB outside the declared64K stack agrees
with an independent physical-memory scalar algorithm. Cross-image comparison
retains state/registers/DF/requests/ports/entry counts and omits per-image
whole-memory hashes because unrelated PI and DGROUP0849 bytes still differ.

MZ relocates to2000, DGROUP2E3F and stack4000. Fixtures initialize BFNT header
085A, Buffer087A, Patnum087C, near character-free pointer087E, PatData1460 and
PatSize1860, heap/stack state and palette141E. Pattern source is synthetic
segment5000, header5100, heap/temp6000..8FFF and flat VRAM A800:0000..FFFF,
including the following physical byte for an offsetFFFF word store. All
16-bit offsets wrap separately from segment-base arithmetic. Original
BFNT ID at051C and byte-mask table084A are target observations, supported by
frozen providers; this is not an accepted generated DATA graph.

DOS21 open3D/read3F/seek42/close3E and heap48/49 replies are explicit models,
including AX/CF, short/stale data, destination and handle. They are not native
DOS or filesystem implementations. The optional near character-free fixture
at2000:8000 contains real RET and declares its pointer/frame. The marker lies
outside the pattern arrays; a fixture at2000:FF40 would overlap those arrays.
Actual character cleanup, files/resources and DOS ABI guarantees remain open.
Only declared service sites and byte OUT7C/7E are allowed. GRCG effects are
not simulated: native stores are compared in flat physical memory, without
claiming hardware plane masking, read/modify/write or display correctness.

Guards check instruction ownership, complete cleanup, PUSH CS calls, real
near/far frames, declared callback and four dispatch targets. Native writes
may touch declared state, precise mutable operands, heap/temp, VRAM and stack;
full memory catches unintended changes within those broad heap/temp spans.
No MEM_READ hook is installed. Eight controls reject truncated bodies, cleanup,
operand/neighbor branches, unknown calls/indirect/far edges, callback/producer
changes, wrong services/ports/widths, whole-span stores, invalid mutable
branches, missing/incorrect frames, stale completion and segment aliases.
Positive controls exercise a native near tail call, callback RET and legal
single-byte self-modification. Mutants provide guard tests, not product source.

## Loading, stack marks and observed ABI

HEADER_READ asks DOS for32 bytes but never validates returned AX when CF0.
It compares five magic bytes using REPE CMPSB without CLD. DF1 walks backwards
and normally rejects the forward header. A failed read with nonzero AX returns
its negation; CF1/AX0 negation clears carry and can proceed to magic comparison.
Short reads may retain the supplied header. EXTEND always CLD, allocates one
stack region, ignores CF-clear read length, parses declared record lengths,
extracts the low nibble for ID10 and releases its mark. A zero extension skips
allocation. SUPER_ENTRY_BFNT ignores EXTEND's carry and uses AX as clear color;
it gates the optional native palette loader by color bit80 and requires the
other color bits to equal3. Open-success paths always execute native close;
a successful load's final carry comes from END-START, not close status.

BFNT_ENTRY_PAT patches its actual DS/handle/dimensions/plane/read/clear/patsize
operands. Read size is16-bit `(Xdots>>3)*Ydots*4`; conversion loops use only
low-byte column/row counts, with zero counting256. Packed nibbles become four
bitplanes. Its two stack requests occur before conversion. Second-request
failure preserves the first allocation; this is a leak of the stack mark.
A read failure or AX unequal CX releases the original packed mark and returns
FFF3. For AX greater than CX with CF0, the comparison leaves carry clear:
FFF3/CF0 can be treated as success by the caller. Error/status matrices verify
both directions, MAXPAT exhaustion and modular END/START counts.

The BFNT epilogue pushes SI then DI but pops SI then DI: it exchanges the
caller's SI/DI on every return path. The probe explicitly checks this behavior.
The outer load wrapper saves/restores its own SI/DI. Conversion before native
ENTRY_AT retains incoming DF; ENTRY_AT's CLD changes later pattern conversion
in the same multi-pattern BFNT call. Neither frozen macros nor anomalous ABI
behavior are localized maintained source or fresh producer acceptance.

## Registration, cancellation and drawing

ENTRY_AT executes CLD even on an invalid unsigned index>=512. Lazy buffer
allocation requests576 paragraphs and clears512 SIZE words; DATA words and
Patnum are retained. Overwrite frees an existing nonzero-size pointer,
ignoring free carry. Sparse insertion sets Patnum to index+1 and permits
zero-size entries and arbitrary segment pointers. ENTRY_PAT allocates five
planes with16-bit byte size, registers through native ENTRY_AT, copies four
planes and computes the transparent mask by comparing each bit to clear
color. Nonzero clear low byte masks the four planes; the high byte is ignored.
Its failed registration frees the newly allocated pattern.

CANCEL checks unsigned index<Patnum but has no independent512 bound; shifted
word indices alias, including8000→slot0. It requires nonzero SIZE, frees DATA
ignoring carry and clears both slot words. Tail reduction scans DATA, not SIZE,
so stale pointers can retain a zero-size tail. FREE first skips everything when
Buffer0, including character cleanup. Otherwise it frees/zeros Buffer, then
repeatedly cancels the last pattern. A zero-size last slot leaves Patnum
unchanged and loops; a later FREE sees Buffer0 and skips that stale count.
Native budget checks retain this exact partial state.

PUT has no index validation, clipping or CLD. X uses logical SHR3, Y*80 and
addresses wrap at16 bits. Origin parity and width parity select four native
helpers; odd origins first subtract one. Actual CODE patches select the near
tail target, height/mask, pair count and signed-byte row addition. Large widths
can wrap that immediate and produce a stride different from80. Eight shifts,
all parity variants, widths1..255 boundary samples, DF0/1, bottom/negative/wrap
coordinates and connected registration/drawing/release run natively. Zero
width or height decrements wrap the byte loop to256; standalone one-zero cases
return, both-zero drawing is recorded as a checked finite budget prefix.
Five passes emit C0/CE/CD/CB/C7 modes and tile values, then mode0, while actual
stores and source progression match the scalar model. Device semantics,
malformed-input safety, complete game callers, cold root/layout/ownership and
canonical DIET packaging/full Oracles remain open with the remaining intake.
