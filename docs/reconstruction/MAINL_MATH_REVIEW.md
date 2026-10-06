# Complete MAINL vector and flip-table candidate review

This historical cached review is supplemented by the later
[shared math review](SHARED_MATH_REVIEW.md): independently bound OP/MAINL LUT,
localized symbolic MAINL vector ASM, and two fresh cold producer/native rounds.
Four existing rows gain source presence without duplicate interval credit.
A CFG audit shows IATAN2+3B is an unreachable alignment NOP; the earlier
description below of executing internal alignment is superseded. Complete
product/exact gates remain open, and original TC86/TASM producer differences
are explicitly retained.

Two complete TUs contain three functions:189 decoded CODE bytes /
70 instructions, plus one observed vector-producer NOP, totaling190bytes.
All raw bytes and the vector's one ordered MZ relocation agree in both caches;
the flip-table contribution has none. The entire native IATAN2 dependency at
0000:175E..17C8 (107bytes /54instructions) also executes, including its internal
alignment instruction. These remain decoded candidate diagnostics, not authored
MAINL source, canonical stored offsets, fresh builds or exact acceptance.

```sh
python3 scripts/review_th03_mainl_math.py --output .analysis/NEW_MATH_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_math_review.py -v
```

Receipt: `.analysis/sol-mainl-math-review-20261006.json`. The previous text
receipt and canonical/decoded/cached lineage are guarded. Seventeen consulted
frozen providers bind to both caches. Vector.cpp still includes frozen
th03/math/vector.cpp; MAIN's separate natural vector assembly is not that
object's producer. The old cached th03/hfliplut.asm root is instead overlaid
with maintained MAIN formats/hfliplut.asm. That body equals the frozen inner
implementation, but the frozen root's include directive is not the actual
cached producer. Both maintained source/header files match cached copies.
Explicit LF/CRLF conversion is confined to assembler-provider comparison.
No MAIN or library exactness is inherited.

Both cached vector and hfliplut OMF objects are valid, carry their expected
TC86/TASM translator and module identities, and agree after dependency-timestamp
normalization. Complete MAP contributions and original relocation order are
separate diagnostics. Ghidra fails headless-usage before DB attestation; no new
DB observations are used. No cold OMF/source-layout reproduction is claimed.

| Function | Decoded coordinate | Bytes / instructions | Far cleanup |
| --- | --- | ---: | ---: |
| VECTOR2 | 0C7E:0110 | 69 /23 | 12 |
| VECTOR2_BETWEEN_PLUS | 0C7E:0156 | 90 /31 | 20 |
| hflip_lut_generate | 0C7E:0FA4 | 30 /16 | 0 |
| Contextual native IATAN2 | 0000:175E | 107 /54 | 4 |

The NOP at0C7E:0155 belongs to the candidate's diagnostic producer partition;
no codestring/padding/opcode arrays are introduced into product source. Complete
branches stay on instruction boundaries. The only call is from BETWEEN to
native IATAN2. All far returns execute. BP/SI/DI/DS and inherited DF survive
terminal cases; scratch registers/ES are not treated as preserved. No x87
instruction or substituted function occurs in this replay.

## Tables and native execution

The scalar sine specification independently regenerates320 signed words,
using nearest rounding of256*sin(angle*pi/128). Both decoded storage and frozen
assembly literals match all640bytes. Sin begins at DGROUP05BA; Cos at063A is
64 words later and overlaps it, requiring320 total words rather than two
independent256-word arrays. All256 byte arctangent coefficients at041C match
the frozen literals and nearest rounding ofatan(index/256)*128/pi. These are
private DATA diagnostics; generated root/data ownership is still open. No
mathematical library source or target arrays are imported into product code.

All arithmetic functions execute natively. A source-level integer specification
checks full65536 DGROUP bytes and a131072-byte far-output fixture, preserving
each image's own initial bytes. Ordered output stores and IATAN2's actual native
far frames are checked. Only constructed output buffers and the emulator are
fixtures; there are no imported-function/device models. Before/after DGROUP
hashes remain separate and are omitted from cross-image normalization because
unrelated target0849 differs. Outputs, stores, angles, frames and faults agree
across original/two caches.

Each image has7407 top-level invocations:7377 returns and30 DIV fault stops.
Across all three:22221 calls /22131 returns /90 faults. Per image:3097 vector
calls,2179 between calls (20faults),2129 direct IATAN2 calls (10faults), and two
full LUT generations. Cases cover all256 angles with twelve signed lengths,
every quotient-table index in both octants/all quadrants, coordinate subtraction
wrap, zero/diagonal/axes, INT_MIN boundaries, byte-angle addition, and output
pointer alias/overlap/end offsets. Both DF states execute. Eight adversarial
controls reject incomplete/wrong returns, branches into operands/neighbors,
producer mutation, unknown calls/ports/interrupts, unowned writes, invalid
native frames, aliases and stale completion; callbacks raise outside FFI.

INT0 is accepted only at the two actual DIV BX sites (0000:1791/17A8), with
that opcode present. The engine is stopped there, before an interrupt handler
or output store. This is a native arithmetic-fault observation, not execution
of a real PC-98 interrupt frame or handler. Unicorn1.0.2rc4 retains pending
exception state if the same instance resumes after a stopped DIV trap; a focused
control observed a subsequent INT8. Each post-trap scenario therefore uses a
fresh engine, with separately reset input memory and registers. A successful
return is never fabricated for a trapped call.

## Vector arithmetic and far outputs

Length is sign-extended from a16-bit word. The low angle byte indexes signed
word coefficients; its caller word's high byte is ignored. Signed32-bit products
are arithmetic-shifted by8, yielding floor rounding for negatives; the low16
bits are written to the far outputs. Products in these tested input/table ranges
fit32bits, while final16-bit output can wrap. For example length-1 at a positive
nonzero coefficient yields-1, rather than truncation toward zero.

VECTOR2 receives length, angle, ret_y far pointer and ret_x far pointer in the
native reverse Pascal stack order. It stores cosine to ret_x first, then sine
to ret_y. BETWEEN receives length, ret_y, ret_x, plus-angle, y2,x2,y1,x1. It
subtracts coordinates as words before passing dx/dy to IATAN2 and adds only
the plus-angle low byte modulo256. The length held in SI survives the real
callee. It then stores cosine to ret_x and sine to ret_y. No pointer swap is
inferred from local assembly alias names; declaration, stack fields and actual
store order determine the ABI.

Equal physical pointers leave the sine store's value; adjacent/partially
overlapping pointers overwrite the corresponding little-endian bytes in that
same order. Different segment:offset representations of one physical address
are tested. Both coefficients are loaded before either output store, so outputs
aliasing the sine storage do not change the current call's computed sine.
Such stores still modify that DATA and could affect later calls; the replay
resets the image between these constructed cases and does not claim safe use.
A word store at far offsetFFFF is observed across two adjacent linear bytes
in Unicorn's flat memory. No segment normalization is performed by the function;
real CPU segment-limit/physical-memory behavior is outside this model.

## IATAN2 word extremes

The native library takes word dx/dy, computes word absolute values, and compares
them **as signed words** before choosing an unsigned division. Equality selects
32 directly; the zero vector returns0. Other ordinary cases divide the smaller
absolute value times256 by the larger, read the low quotient byte through XLAT,
and adjust quadrants. All valid table indices/octants and quadrants are checked
against the independently regenerated table; this is the discrete table result,
not a claim of continuous floating-point atan2 equality.

The absolute value of-32768 remains8000. Signed comparison can then select the
larger value as numerator and the smaller as denominator. Actual IATAN2(0,-32768)
tries division by zero. Values1/-1/127/128 against that extreme produce quotient
overflow. These calls stop at INT0 without returning or writing vector outputs.
The coordinate differences in BETWEEN can create this8000 value even from
other endpoints, for example x1=-32768,x2=0.

For y=129,x=-32768, division fits a word but the quotient exceeds the normal
lookup domain; XLAT still uses only AL, and the native result is64. Other
nonfaulting extremes retain that low-byte behavior. The pair x=y=-32768 takes
the equality branch and returns160 after quadrant adjustment. These are direct
source/instruction/scalar observations. No widened absolute value, clipping,
repaired quadrant or exception recovery is authored.

## Complete flip-table generation

The actual generator writes every LUT byte at DGROUP20D6..21D5 in ascending
order, including initial zero and finalFF. ROL AL /RCR DL loops reverse each
byte's eight bits; eight rotations restore AL before the subsequent increment.
After255, AL wraps to0 and the function returns. Every one of the256 writes
and all surrounding DGROUP/output bytes are checked against independent bit
reversal, with a prior A5-filled table and both DF states. The function uses
explicit DI stores and leaves DF unchanged; it restores DI and does not depend
on an incoming string direction. No synthetic LUT is substituted in this scope.
The earlier CDG blitter review keeps its separately declared LUT fixture; this
review does not retroactively claim a combined loader/drawing execution.

Three decoded function rows add no authored MAINL source or exact credit;
IATAN2 remains a contextual library body, not a new product owner. The generated
MAINL root's other CODE/DATA/BSS, libraries/CRT, localized cold producers and
canonical DIET packaging/full Oracles remain open. The complete505-file intake
and actual requested English commits are unfinished.
