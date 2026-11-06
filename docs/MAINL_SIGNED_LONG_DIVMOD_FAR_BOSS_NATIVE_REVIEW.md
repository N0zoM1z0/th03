# Original 32-bit signed ldiv quotient/remainder FAR boss — after512

Japanese Borland CL.LIB member ldivt (index 243) has been fully
recovered as maintained [8086 source](../src/mainl/crt/ldivt.asm).
The complete FAR _ldiv computes both 32-bit quotient and
remainder of two signed long integers. It performs original
16-bit halfword absolute-value operations and sign correction,
a 32-round restoring division loop when necessary, a native
short-divisor fast path, and returns the original eight-byte
quotient/remainder pair through the real near N_SCOPY@ helper
to the caller's FAR result buffer. The 16-bit register,
stack and hidden-result ABI remain original.

All **152 CODE bytes**, single FAR public, lone near N_SCOPY@
import, original DATA-before-BSS GROUP and empty DATA/BSS
match CL.LIB. The single **literal ordered original OMF FIXUPP**
at CODE+138 has the exact original near call width, frame,
target and addend. Original byte comparison caught one source
encoding question: XCHG of SI and DX has two equivalent ModRM
forms, but the original uses 87 F2. Writing the true register
order as xchg si,dx reproduces that byte without a target
opcode array, artificial padding or object rewrite.

After512 validates its unchanged after511 719-source parent,
then performs two real TASM/TLIB/TLINK rounds with all original-
equal decoded Japanese MAINL EXE/MAP outputs. The 67,372-byte
EXE and all 677 ordered MZ relocations are identical, as is
the complete MAP. Both raw OBJ/LIB/EXE/MAP vectors, logs and
source/driver hashes are retained. Working CRT reaches
**720/893** complete original source-linked members,
**187,886 CODE bytes**, with 173 contextual vendor members.
This does not claim full cold replay or formal Factory accepted
source credit.

This is independent of the separately recovered h_ldiv twelve-
public helper, whose two same-address MAP alias ordering gaps
remain unresolved; no h_ldiv member credit is claimed here.

Reviewer: scripts/review_th03_mainl_after512_work.py
(mode signed-32bit-quotient-remainder-far-boss).
Tests: tests.test_mainl_after512_work.
