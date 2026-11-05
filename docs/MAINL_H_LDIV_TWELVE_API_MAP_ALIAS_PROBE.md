# Source-complete Borland h_ldiv arithmetic core, MAP alias order unresolved

The original Japanese CL.LIB h_ldiv (slot 67) contains 174 CODE bytes,
no initialized DATA, two original segments and zero OMF FIXUPPs.
Its twelve original public names provide near/far aliases for
signed and unsigned 32-bit quotient and remainder operations:
N_LDIV@ / F_LDIV@ / LDIV@, N_LUDIV@ / F_LUDIV@ / LUDIV@,
N_LMOD@ / F_LMOD@ / LMOD@, and
N_LUMOD@ / F_LUMOD@ / LUMOD@.

Meaningful [8086 source](../src/mainl/crt/h_ldiv.asm) recreates the
actual near-to-far return-stack conversion, the shared 32-bit
restoring-division loop, sign adjustment, modulus selection and
short-divisor fast path. **All 174 original CODE bytes** and every
one of the twelve named public CODE offsets match original CL.LIB.
The segment, group and empty relocation population also match.
No original opcode arrays, padding or object patches are used.

**Important evidence limit: the original full decoded EXE is equal,
but the original full MAP is not yet equal.** A strict after503
native TASM/TLIB/TLINK experiment rebuilt the full MAINL EXE with
all 67,372 bytes and 677 ordered MZ relocations original-equal.
The full MAP has only two reversed same-address alias pairs:
at MAP lines 1321/1322 (LDIV@ vs F_LDIV@, both CODE+3), and
lines 1330/1331 (F_LUMOD@ vs LUMOD@, both CODE+26).
There are no CODE, segment placement or relocation-list gaps.
The original Borland and TASM PUBDEF symbol chronology differs
even though every public symbol and offset match. Four distinct
source-level experiments (label order, PUBLIC order, both, and
individual PUBLIC directives) produced the same native PUBDEF
chronology, so simply swapping declaration lines is not a fix.

This remains an **unfinished exact full-member link**. The
fail-closed after503 trial producer/reviewer and its detailed
native-linked EXE/MAP diagnostic are retained in the ignored
.analysis/work/probe/ area rather than committed as a falsely
successful complete source stage. No full cold replay was run,
and no target MAP, EXE or OBJ bytes were patched.

The independent [scoped source verifier](../scripts/probe_th03_h_ldiv_scoped.py)
compiles h_ldiv twice with real TASM under the writer lock.
It verifies the complete original 174-byte CODE, all twelve
public offsets, segment/GROUP layout, zero FIXUPPs and
nonvolatile OMF stability. Where the preserved local native
link diagnostic exists, it independently confirms exact
EXE, 677 relocations and precisely the two reversed MAP
alias pairs. The targeted test is tests.test_h_ldiv_scoped_native.

**This is a real arithmetic-core source advance but is not
accepted as the next fully source-linked CRT member.**
The latest complete carrier remains after502 at **710/893**,
and h_ldiv contributes zero new complete source-member or
Factory/canonical accepted credit pending source-based
original-equal MAP symbol ordering.
