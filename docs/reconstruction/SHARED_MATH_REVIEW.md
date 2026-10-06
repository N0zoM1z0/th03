# TH03 vector and horizontal-flip table carriers

The complete MAINL vector160 and shared LUT30 carriers are independently
reviewed. OP links only the LUT; MAINL links both. The frozen vector C++ uses
MOVSX opcode fragments and a `codestring` NOP, so that text is not imported into
product source. A symbolic implementation lives in
`src/shared/math/vector_far.asm`, using real MOVSX/IMUL/SAR/LES, far Pascal
frames and natural `EVEN`. Existing MAIN assembly supplies a candidate precedent
without inherited acceptance. Its maintained MAIN owner and accepted aggregate
remain unchanged. `src/shared/formats/hfliplut.asm` preserves the complete
frozen symbolic generator, with no synthetic lookup table substituted.

| Unit or binding | OP | MAINL |
| --- | --- | --- |
| VECTOR2 /69 | absent |0C7E:0110|
| Separate vector producer /1 | absent |0C7E:0155|
| BETWEEN_PLUS /90 | absent |0C7E:0156|
| LUT generator /30 |0BEB:0CB8|0C7E:0FA4|
| DGROUP |0D7F|0E3F|
| LUT destination /256 |1E70|20D6|
| Sin / Cos overlapping words | unreviewed here |05BA /063A|
| Native IATAN2 /107 context | absent here |0000:175E|
| Atan byte table /256 | unreviewed here |041C|

Complete carrier bytes and original ordered relocation rows match two preceding
text cold images: one vector far-call row, zero LUT rows. All branches, actual
MOVSX table operands, LUT immediate binding and the IATAN2 call are checked
independently. Seventeen frozen providers and the complete frozen link graph
match both prior trees. Canonical packed Ghidra databases are re-attested;
Japanese YUMEZIKU provenance remains candidate-local-attested, independent
pristine-dump attestation unknown.

MAINL has124 decoded positions in189 function bytes plus107 contextual helper
bytes. The helper NOP at0000:1799/IATAN+3B is unreachable: an unconditional JMP
precedes it and no edge targets it. It is separately checked without fabricating
execution. The complete reachable set has123 positions, including all70
positions in the three owned functions and53 in IATAN2. The historical math
note's description of executed internal alignment is corrected by this CFG
observation. The separate vector producer byte is outside both function bodies
and receives no function credit. OP has16 LUT positions.

The native functions and IATAN2 execute without any substituted function,
port/device fixture or read-memory hook. A scalar specification reads actual
before-call coefficient and arctangent bytes, implements signed word coordinate
subtraction, low-byte angles, word absolute values, signed octant selection,
unsigned DIV and low-byte XLAT. Baseline320 sine words/640bytes and256 atan bytes
are independently regenerated from nearest rounding and agree with target and
frozen literals. They remain unowned DATA diagnostics. Cos begins64 words into
Sin, rather than being a separate256-word array.

Vector products are signed32bits, arithmetic-shifted by8 before low-word output.
Cosine is written first, sine second. Both coefficients are loaded before either
store. Equal or partially overlapping far outputs retain this order. Effective
word offsets wrap without segment normalization; a word atFFFF crosses adjacent
linear bytes in the declared Unicorn fixture. Real CPU segment-limit/device
outcomes remain outside this observation. Parameter pointer names in the new
symbolic assembly follow the actual Pascal frame: BETWEEN's ret_y at+8, ret_x
at+0C. There is no invented ABI to arrange output equality.

Every invocation checks complete ordered stores, native IATAN2 argument/return
SS/SP/BP frames, saved BP/SI/DI/DS/FS, incoming IF/DF and all physical1MiB outside
the64KiB stack. Full before/after digests remain per-image observations; only
these digests are excluded from cross-image semantic comparison. Actual stores,
faults, frames, registers and visited positions remain compared.

All256 angles with12 signed lengths, every atan index/octant/quadrant, extreme
word values, coordinate subtraction wrap, angle high-byte rejection, output
physical aliases and end offsets are included. Five calls on one emulator
retain coefficient DATA changed by previous aliased outputs. Later vector and
BETWEEN calls read those changed overlapping Sin/Cos values. LUT generation
checks all256 ascending writes from constructed nonzero initial bytes and all
four IF/DF combinations; it retains incoming DF and restores DI.

INT_MIN absolute value remains8000. Signed comparison can select a zero or small
denominator, producing actual DIV0/overflow stops at the two original DIV BX
sites. No interrupt handler or successful return is modeled. Each trapped
instance is discarded before subsequent calls because Unicorn retains pending
exception state. Nonfaulting out-of-domain quotients still use AL for lookup;
no widened absolute value, clipping or repaired angle is authored.

Diagnostic receipt `.analysis/sol-shared-math-review-20261006.json`, SHA256
`8f0734efcc7a53706066af5e5fce18daca97a3f7cee96b30adf72665269ca938`,543guards.
Each target/two preceding cold images: OP4 returns/1024 byte stores/all16
positions; MAINL7424 calls/7394 returns/30 DIV stops/11820 stores/all123 reachable
positions. Ten behavioral/adversarial controls pass: binding/call/return/producer,
unreachable-NOP-entry, full LUT/flags, real fault/post-trap rejection, word
crossing/alias order, persistent table changes, swapped stores, physical-byte
mutation and native stack alias.

Replay `python3 scripts/review_th03_shared_math.py --output .analysis/NEW_MATH.json`
and `python3 scripts/replay_th03_shared_math.py --run-id NEW_MATH`.
Full product/CRT/global DATA/BSS/declarations/fault handlers, resources, physical
runtime and canonical DIET packing remain open. Earlier CDG drawing keeps its
own explicit LUT fixture; this review does not claim a combined generator and
blitter execution.

Two fresh cold rounds each run4 OP cases/all16positions and468 MAINL cases/
438 returns/30 faults/all123 reachable positions. Original30/160carrier bytes,
ordered relocations and public/MAP coordinates match. The MAINL input changes
only `th03/vector.cpp` to `th03/vector_far.asm` at the original link ordinal;
original CPPvector.obj remains for other products. Thus source presence does
not normalize away a producer change or grant cross-artifact exactness.

Both20product/351game-object vectors are deterministic; all20products equal
the preceding text proof,349otheroriginalgameobjects remain unchanged and one
newvector_far.obj is added. All417 OMF hashes are recorded; nine Research
benchmark differences remain separate. LUT original nondependency OMF records
match. Vector TC86-to-TASM records differ explicitly, including absence of the
old empty DATA/BSS segment records. Its sole byte-aligned SHARED CODE160 segment
has SEGDEF28A000020301; LUT word-aligned CODE30 has481E00020301. Original vector
CPP records remain recorded separately. These are layout/producer observations,
without an original compiler-identity or complete Oracle claim.

Source receipt
`.analysis/th03-shared-math/sol-shared-math-source-20261006-b/receipt.json`, SHA256
`2e8c4c6205510417b8b298b0ed182ecd11b17ad45b5a52682b581ac3f88f31c1`,550guards.
Initial preparation stopped before compiler execution: preceding overlays
converted the ASM wrapper to CRLF while the frozen blob hash uses LF. Explicit
ASM newline comparison was corrected; the failure transcript and original
replay snapshot remain separate. No instruction or byte gate was waived.

OP has25 reviewed units/11622bytes and18 source-present extents/11255bytes.
MAINL has145 rows/16 source-present extents/1892bytes in two sharedCPP/fourASM.
Four existing MAINL function/producer rows are upgraded without new interval
credit. Whole OP6-byte/MAINL21-byte decoded and original whole relocation-order
inequalities remain unchanged; OP/MAINL exact0.

Current interval receipt
`.analysis/sol-current-decoded-coverage-after-shared-math-20261006.json`, SHA256
`563f3089fda8c53ac1f21fd0f9a200f5a65e42e6141d699e5dbc70e48c91f7da`,565guards:
OP100carriers/55262bytes,11622reviewed/43640gaps; MAINL108carriers/58340bytes,
28381reviewed/29959gaps. Both have zero overlap; MAINL's union is unchanged.

Bounded cleanup removes1928unreferenced precompiler-preparation files/21507828
bytes, with all1871 retained private input states unchanged. Receipt
`.analysis/sol-shared-math-temporary-cleanup-20261006.json`, SHA256
`bad213f06dfc5e2a790e194e8b13cdbd180936bc8c6317620428c7242ff74e39`,5guards.
Complete successful proof trees and the first failure/replay snapshot remain.
Historical missing/stale input states are not repaired or rebased.

Full CI passes557tests and all available private headless gates:
`.analysis/sol-shared-math-complete-ci-20261006.log`, SHA256
`7d49397fd6a760fed5270282ceae786642f0c38238b5681ea8821ac88fa4c52a`.
Tracking after CI:234units/2253evidence/280knowledge/120MAIN authored-function
rows. The505-file review/migration goal remains open; exact acceptance is zero
for OP/MAINL within this scope.
