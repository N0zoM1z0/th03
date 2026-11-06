# Breakthrough: full cplx2 original CODE using native TASM NOSMART

Japanese Borland CL.LIB cplx2 (slot 209) has 5,598 CODE bytes,
22 public FAR complex routines, 63 DATA bytes, empty BSS and
six INITDATA bytes. The maintained
[native full-code source](../src/mainl/crt/cplx2_complete_code_native.asm)
now produces **every single original CODE byte** from real 8086/x87
instructions, including both previously unresolved original
intra-segment direct FAR calls. All 22 PUBLIC offsets match
without any alignment shift, all original 47 initialized DATA
bytes agree, and the six INITDATA bytes including the real
CODE+5575 CRT initialization pointer now also match exactly.

**The key technical discovery is TASM 5 SMART/NOSMART.** Seven
prior experiments replacing CALL with various FAR PTR and segment-
qualified forms all emitted four-byte PUSH CS + NEAR CALL at
original CODE+799 and +984. Turbo Assembler's documented
SMART code generation deliberately performs that transformation
for same-segment FAR targets. The natural, scoped source now
places NOSMART immediately before each genuine FAR CALL to
arg(complex) in acos and SMART immediately afterward. TASM
then emits the authentic five-byte 9A direct FAR CALL instruction
and both original symbolic same-segment fixups. This is *not*
post-assembly patching, embedding original opcode arrays or
NOP padding. The remainder of the source is unchanged.

The independent [complete-CODE verifier](../scripts/probe_th03_cplx2_full_code_exact_native.py)
runs two real TASM rounds under the writer lock. It compares all
**5,598/5,598 original CODE bytes**, 22 PUBDEF entrypoints, all
47 initialized DATA bytes and genuine unmaterialized DATA+0..15
semantics, exact 6-byte INITDATA/CRT initializer, four segment
definitions, the exact original BSS-before-DATA GROUPDEF, and **860/860 exact logical OMF fixup sites, targets
(symbolic identity), location types/widths and addends**.
Both native OMF files are checked for nonvolatile stability.

**Still not raw Borland OBJ parity:** 734 original x87 helper
fixups use Borland frame method 4, where TASM emits method 5.
The single original N_SCOPY@ imported near call at CODE+5561
uses target-frame method 5 and TASM emits CODE-frame method 0.
Borland also lists unused original __turboFloat in EXTDEF;
the source now explicitly declares it, bringing TASM to all
24 original imported symbol identities. Their raw record order
can still differ.
The logical symbol/target/addend parity does not silently
override these real raw-record differences. Subsequent [after514 evidence](MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md)
demonstrates two complete original-equal Japanese MAINL
EXE/MAP links and counts cplx2 as one complete working-source
CRT member. Formal Factory/canonical acceptance remains
unestablished and original OBJ packet equality is not claimed.

This is the first complete natural source for all 22 original
functions and initialization logic and directly resolves the
two CODE length gaps without cheating. Next work: test a
source-bound full-library native link, address frame encoding
and EXTDEF chronology if needed, and preserve the original
code/data/INITDATA evidence. No full cold replay was run.
Test: tests.test_cplx2_full_code_exact_native.


## Later full source-link advancement

The after514 native source is maintained at
[src/mainl/crt/cplx2.asm](../src/mainl/crt/cplx2.asm). It
adds the correct original BSS-before-DATA GROUPDEF and unused
__turboFloat EXTDEF, then verifies exact complete MAINL EXE/MAP
through two TASM/TLIB/TLINK rounds. See
[full source-linked review](MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md).
The earlier statements that full source linkage was not yet
established are historical evidence boundaries, superseded by
after514; original raw Borland OMF remains different.
